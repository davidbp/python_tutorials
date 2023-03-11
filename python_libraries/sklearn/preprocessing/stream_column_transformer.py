from sklearn.compose import ColumnTransformer
from sklearn.base import TransformerMixin, BaseEstimator, clone
from sklearn.utils.metaestimators import _BaseComposition


class StreamColumnTransformer(ColumnTransformer, TransformerMixin, _BaseComposition):

    _required_parameters = ["transformers"]

    def __init__(
        self,
        transformers,
        *,
        remainder="drop",
        sparse_threshold=0.3,
        n_jobs=None,
        transformer_weights=None,
        verbose=False,
        verbose_feature_names_out=True,
    ):
        self.transformers = transformers
        self.remainder = remainder
        self.sparse_threshold = sparse_threshold
        self.n_jobs = n_jobs
        self.transformer_weights = transformer_weights
        self.verbose = verbose
        self.verbose_feature_names_out = verbose_feature_names_out
        
    def partial_fit(self, X, y=None):
        for _, transformer, col in self.transformers:
            transformer.partial_fit(X[col], y)


