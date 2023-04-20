
StreamOneHotEncoder(_BaseEncoder):

    def __init__(
        self,
        *,
        drop=None,
        sparse_output=True,
        dtype=np.float64,
        min_frequency=None,
        max_categories=None,
        feature_name_combiner="concat",
    ):
        self.sparse_output = sparse_output
        self.dtype = dtype
        self.min_frequency = min_frequency
        self.max_categories = max_categories
        self.feature_name_combiner = feature_name_combiner

    def partial_fit(self, X, y=None):
        """
        Fit OneHotEncoder to X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The data to determine the categories of each feature.

        y : None
            Ignored. This parameter exists only for compatibility with
            :class:`~sklearn.pipeline.Pipeline`.

        Returns
        -------
        self
            Fitted encoder.
        """
        self._validate_params()

        if self.sparse != "deprecated":
            warnings.warn(
                "`sparse` was renamed to `sparse_output` in version 1.2 and "
                "will be removed in 1.4. `sparse_output` is ignored unless you "
                "leave `sparse` to its default value.",
                FutureWarning,
            )
            self.sparse_output = self.sparse

        self._check_infrequent_enabled()

        fit_results = self._fit(
            X,
            handle_unknown=self.handle_unknown,
            force_all_finite="allow-nan",
            return_counts=self._infrequent_enabled,
        )
        if self._infrequent_enabled:
            self._fit_infrequent_category_mapping(
                fit_results["n_samples"], fit_results["category_counts"]
            )
        self._set_drop_idx()
        self._n_features_outs = self._compute_n_features_outs()
        return self

    def transform(self, X):
        """
        Transform X using one-hot encoding.

        If there are infrequent categories for a feature, the infrequent
        categories will be grouped into a single category.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The data to encode.

        Returns
        -------
        X_out : {ndarray, sparse matrix} of shape \
                (n_samples, n_encoded_features)
            Transformed input. If `sparse_output=True`, a sparse matrix will 
be
            returned.
        """
        check_is_fitted(self)
        # validation of X happens in _check_X called by _transform
        warn_on_unknown = self.drop is not None and self.handle_unknown in {
            "ignore",
            "infrequent_if_exist",
        }
        X_int, X_mask = self._transform(
            X,
            handle_unknown=self.handle_unknown,
            force_all_finite="allow-nan",
            warn_on_unknown=warn_on_unknown,
        )
        self._map_infrequent_categories(X_int, X_mask)

        n_samples, n_features = X_int.shape

        if self._drop_idx_after_grouping is not None:
            to_drop = self._drop_idx_after_grouping.copy()
            # We remove all the dropped categories from mask, and decrement 
all
            # categories that occur after them to avoid an empty column.
            keep_cells = X_int != to_drop
            for i, cats in enumerate(self.categories_):
                # drop='if_binary' but feature isn't binary
                if to_drop[i] is None:
                    # set to cardinality to not drop from X_int
                    to_drop[i] = len(cats)

            to_drop = to_drop.reshape(1, -1)
            X_int[X_int > to_drop] -= 1
            X_mask &= keep_cells

        mask = X_mask.ravel()
        feature_indices = np.cumsum([0] + self._n_features_outs)
        indices = (X_int + feature_indices[:-1]).ravel()[mask]

        indptr = np.empty(n_samples + 1, dtype=int)
        indptr[0] = 0
        np.sum(X_mask, axis=1, out=indptr[1:], dtype=indptr.dtype)
        np.cumsum(indptr[1:], out=indptr[1:])
        data = np.ones(indptr[-1])

        out = sparse.csr_matrix(
            (data, indices, indptr),
            shape=(n_samples, feature_indices[-1]),
            dtype=self.dtype,
        )
        if not self.sparse_output:
            return out.toarray()
        else:
            return out

    def inverse_transform(self, X):
        """
        Convert the data back to the original representation.

        When unknown categories are encountered (all zeros in the
        one-hot encoding), ``None`` is used to represent this category. If 
the
        feature with the unknown category has a dropped category, the 
dropped
        category will be its inverse.

        For a given input feature, if there is an infrequent category,
        'infrequent_sklearn' will be used to represent the infrequent 
category.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape \
                (n_samples, n_encoded_features)
            The transformed data.

        Returns
        -------
        X_tr : ndarray of shape (n_samples, n_features)
            Inverse transformed array.
        """
        check_is_fitted(self)
        X = check_array(X, accept_sparse="csr")

        n_samples, _ = X.shape
        n_features = len(self.categories_)

        n_features_out = np.sum(self._n_features_outs)

        # validate shape of passed X
        msg = (
            "Shape of the passed X data is not correct. Expected {0} 
columns, got {1}."
        )
        if X.shape[1] != n_features_out:
            raise ValueError(msg.format(n_features_out, X.shape[1]))

        transformed_features = [
            self._compute_transformed_categories(i, remove_dropped=False)
            for i, _ in enumerate(self.categories_)
        ]

        # create resulting array of appropriate dtype
        dt = np.result_type(*[cat.dtype for cat in transformed_features])
        X_tr = np.empty((n_samples, n_features), dtype=dt)

        j = 0
        found_unknown = {}

        if self._infrequent_enabled:
            infrequent_indices = self._infrequent_indices
        else:
            infrequent_indices = [None] * n_features

        for i in range(n_features):
            cats_wo_dropped = self._remove_dropped_categories(
                transformed_features[i], i
            )
            n_categories = cats_wo_dropped.shape[0]

            # Only happens if there was a column with a unique
            # category. In this case we just fill the column with this
            # unique category value.
            if n_categories == 0:
                X_tr[:, i] = 
self.categories_[i][self._drop_idx_after_grouping[i]]
                j += n_categories
                continue
            sub = X[:, j : j + n_categories]
            # for sparse X argmax returns 2D matrix, ensure 1D array
            labels = np.asarray(sub.argmax(axis=1)).flatten()
            X_tr[:, i] = cats_wo_dropped[labels]

            if self.handle_unknown == "ignore" or (
                self.handle_unknown == "infrequent_if_exist"
                and infrequent_indices[i] is None
            ):
                unknown = np.asarray(sub.sum(axis=1) == 0).flatten()
                # ignored unknown categories: we have a row of all zero
                if unknown.any():
                    # if categories were dropped then unknown categories 
will
                    # be mapped to the dropped category
                    if (
                        self._drop_idx_after_grouping is None
                        or self._drop_idx_after_grouping[i] is None
                    ):
                        found_unknown[i] = unknown
                    else:
                        X_tr[unknown, i] = self.categories_[i][
                            self._drop_idx_after_grouping[i]
                        ]
            else:
                dropped = np.asarray(sub.sum(axis=1) == 0).flatten()
                if dropped.any():
                    if self._drop_idx_after_grouping is None:
                        all_zero_samples = np.flatnonzero(dropped)
                        raise ValueError(
                            f"Samples {all_zero_samples} can not be inverted 
"
                            "when drop=None and handle_unknown='error' "
                            "because they contain all zeros"
                        )
                    # we can safely assume that all of the nulls in each 
column
                    # are the dropped value
                    drop_idx = self._drop_idx_after_grouping[i]
                    X_tr[dropped, i] = transformed_features[i][drop_idx]

            j += n_categories

        # if ignored are found: potentially need to upcast result to
        # insert None values
        if found_unknown:
            if X_tr.dtype != object:
                X_tr = X_tr.astype(object)

            for idx, mask in found_unknown.items():
                X_tr[mask, idx] = None

        return X_tr

    def get_feature_names_out(self, input_features=None):
        """Get output feature names for transformation.

        Parameters
        ----------
        input_features : array-like of str or None, default=None
            Input features.

            - If `input_features` is `None`, then `feature_names_in_` is
              used as feature names in. If `feature_names_in_` is not 
defined,
              then the following input feature names are generated:
              `["x0", "x1", ..., "x(n_features_in_ - 1)"]`.
            - If `input_features` is an array-like, then `input_features` 
must
              match `feature_names_in_` if `feature_names_in_` is defined.

        Returns
        -------
        feature_names_out : ndarray of str objects
            Transformed feature names.
        """
        check_is_fitted(self)
        input_features = _check_feature_names_in(self, input_features)
        cats = [
            self._compute_transformed_categories(i)
            for i, _ in enumerate(self.categories_)
        ]

        name_combiner = self._check_get_feature_name_combiner()
        feature_names = []
        for i in range(len(cats)):
            names = [name_combiner(input_features[i], t) for t in cats[i]]
            feature_names.extend(names)

        return np.array(feature_names, dtype=object)

    def _check_get_feature_name_combiner(self):
        if self.feature_name_combiner == "concat":
            return lambda feature, category: feature + "_" + str(category)
        else:  # callable
            dry_run_combiner = self.feature_name_combiner("feature", 
"category")
            if not isinstance(dry_run_combiner, str):
                raise TypeError(
                    "When `feature_name_combiner` is a callable, it should 
return a "
                    f"Python string. Got {type(dry_run_combiner)} instead."
                )
            return self.feature_name_combiner

