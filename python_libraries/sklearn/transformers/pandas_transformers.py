import sklearn
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
from collections import namedtuple

class PandasGeneralScaler(BaseEstimator, TransformerMixin):
    '''
    Scaling class with different options for scaling the data.
    - "StandardScaler": Standardize features by removing the mean and scaling to unit variance
    - "MinMaxScaler":   Transform features by scaling each feature to a given range (0,1) as default.
    - "MaxAbsScaler":   Scale each feature by its maximum absolute value.
    - "Normalizer":     Normalize samples individually to unit norm (l2 norm)
    - None:             No scaling

    The boolean option `clip` allows clipping values that are outside a range specified by `clip_range`.
    If no `clip_range` is provided the min and max values are found during training.

    Clipping can be used to avoid issues with models predicting insane quantities (or maybe allways the same value)
    in the event that a feature dominates the predictions (for example if a feature value saturates neurons in a neural net).
    '''

    def __init__(self, scaler_str="StandardScaler", clip=True,  clip_range=None):

        self._allowed_scalers = ['StandardScaler', "MinMaxScaler", "MaxAbsScaler", 'Normalizer', None]     
        assert scaler_str in self._allowed_scalers,\
             f"the scaler introduced {scaler_str} is not valid. Please use one in {self._allowed_scalers}"
       
        self.scaler_str = scaler_str 
        self.ClipRange = namedtuple('ClipRange', 'min_vals max_vals')

        if clip is True and clip_range is not None:

            assert isinstance(clip_range, list), "clip_range should be a list with two np.ndarray arrays."
            
            assert len(clip_range[0])==len(clip_range[1]),"len(clip_range[0])={len(clip_range[0])}\
                should be equal to len(clip_range[1])={len(clip_range[1])}"
            
            assert isinstance(clip_range[0], np.ndarray),"type(clip_range[0])={type(clip_range[0])} \
                                                          should be a np.ndarray"

            assert isinstance(clip_range[1], np.ndarray),"type(clip_range[1])={type(clip_range[1])} \
                                                          should be a np.ndarray"

            assert np.all(clip_range[0] < clip_range[1]), f"Indices {list(np.where(clip_range[0]  > clip_range[1])[0])} have higher min than max"

            clip_range = self.ClipRange(min_vals=clip_range[0], max_vals=clip_range[1])

        self.clip_range = clip_range
        self.clip = clip


    def fit(self, X, y=None):
        """
        Learns statistics (if needed) to properly scale the data.
        
        If `X` is a `pd.DataFrame` the method stores the columns and the dtypes of the columns.

        """
        if self.scaler_str == "StandardScaler":
            self.scaler = sklearn.preprocessing.StandardScaler()
        elif self.scaler_str == "MinMaxScaler":
            self.scaler = sklearn.preprocessing.MinMaxScaler()
        elif self.scaler_str == "MaxAbsScaler":
            self.scaler = sklearn.preprocessing.MaxAbsScaler()
        elif self.scaler_str == "Normalizer":
            self.scaler = sklearn.preprocessing.Normalizer()
        elif self.scaler_str == None:
            self.scaler = None
        
        if self.clip is True and self.clip_range is None:
            self.clip_range = self.ClipRange(min_vals=np.nanmin(X, axis=0), max_vals=np.nanmax(X, axis=0))
            
        if isinstance(X, pd.DataFrame):
            self.feature_names  = list(X.columns)
            self.feature_dtypes = dict(X.dtypes)


    def clip_X(self, X):
        """
        Clips the values of an input np.ndarray or pd.DataFrame object.
        """
        assert self.clip_range is not None, "clip_range has not been fitted or provided by the user"

        if isinstance(X, pd.DataFrame):
            cols = X.columns
            for col in cols:
                X[col] = np.clip(X[col], self.clip_range.min_vals[col], self.clip_range.max_vals[col])

        elif isinstance(X, np.ndarray)
            n_cols = X.shape[1]
            for col_id in range(n_cols):
                X[:, col_id] = np.clip(X[:, col_id], self.clip_range.min_vals[col_id], self.clip_range.max_vals[col_id])

        return X


    def transform(self, X, cast_to_ndarray=False):
        """
        Transforms a np.ndarray or pd.DataFrame object with the learned scaler during `.fit`.

        if `cast_to_ndarray==True` then the output of the transform is a numpy array always.
        
        If `cast_to_ndarray==False` then the output of the transform is the same type as the input.
        Which means: If the input is a np.ndarray the output is a np.ndarray, 
                     If the input is a pd.DataFrame the output is a pd.DataFrame
              
        """

        if cast_to_ndarray:
            X_aux = np.array(self.transform(X))
        else:

            if isinstance(X, pd.DataFrame):

                # Create a dataframe containing the scaled data with the proper colum names
                X_aux = pd.DataFrame(self.transform(X), columns=self.feature_names)

                # Add the correct type at each of the columns of the transformed data
                for feature, feature_type in self.feature_dtypes.items():
                    X_aux[feature] = X_aux[feature].astype(feature_type)
            
            else:
                X_aux = self.transform(X)

        return X_aux
