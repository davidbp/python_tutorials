from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
from collections import namedtuple

class GeneralScaler(BaseEstimator, TransformerMixin):
    '''
    Scaling class with different options for scaling the data.
    - "StandardScaler": Standardize features by removing the mean and scaling to unit variance
    - "MinMaxScaler":   Transform features by scaling each feature to a given range (0,1) as default.
    - "MaxAbsScaler":   Scale each feature by its maximum absolute value.
    - "Normalizer":     Normalize samples individually to unit norm (l2 norm)
    -  None:            No scaling

    The boolean option `clip` allows clipping values that are outside a range specified by `clip_range`.
    If no `clip_range` is provided the min and max values are found during training.

    Clipping is meant to avoid issues with models predicting insane quantities (or maybe allways the same value)
    in the event that a feature dominates the predictions (for example if it saturates neurons).

    '''
    def __init__(self, scaler_str="StandardScaler", clip=True,  clip_range=None):

        self._allowed_scalers = ['StandardScaler', "MinMaxScaler", "MaxAbsScaler",'Normalizer',None]     
        assert scaler_str in self._allowed_scalers,\
             f"the scaler introduced {scaler_str} is not valid. Please use one in {self._allowed_scalers}"
       
        self.scaler_str = scaler_str 
        self.ClipRange = namedtuple('ClipRange', 'mins maxs')

        if clip is True and clip_range is not None:

            assert isinstance(clip_range, list), "clip_range should be a list with two np.ndarray arrays."
            
            assert len(clip_range[0])==len(clip_range[1]),"len(clip_range[0])={len(clip_range[0])}\
                should be equal to len(clip_range[1])={len(clip_range[1])}"
            
            assert isinstance(clip_range[0], np.ndarray),"type(clip_range[0])={type(clip_range[0])} \
                                                          should be a np.ndarray"
            assert isinstance(clip_range[1], np.ndarray),"type(clip_range[1])={type(clip_range[1])} \
                                                          should be a np.ndarray"

            assert np.all(clip_range[0] < clip_range[1]), f"Indices {list(np.where(clip_range[0]  > clip_range[1])[0])} have higher min than max"

            clip_range = self.ClipRange(mins=clip_range[0], maxs=clip_range[1])

        #import pdb; pdb.set_trace()
        self.clip_range = clip_range
        self.clip = clip


    def fit(self, X, y=None):
        """
        Learns statistics (if needed) to properly scale the data
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
        #if self.scaler_str != "None":
        #    self.scaler.fit(X)
        
        if self.clip is True and self.clip_range is None:
            self.clip_range = self.ClipRange(mins=np.nanmin(X, axis=0), maxs=np.nanmax(X, axis=0))
             

    def clip_X(self, X):

        assert self.clip_range is not None, "clip_range has not been fitted or provided by the user"

        n_cols = X.shape[1]

        for col_id in range(n_cols):
            X[:, col_id] = np.clip(X[:, col_id], self.clip_range.mins[col_id], self.clip_range.maxs[col_id])

        return X


    def transform(self, X):

        if self.scaler_str==None:
            X_aux = X
        else:
            X_aux = self.scaler.transform(X)
        
        if self.clip:
            X_aux = self.clip_X(X_aux)

        return X_aux

