import pandas as pd
import numpy as np
import statistics as stats

import sklearn
from sklearn.base import BaseEstimator, TransformerMixin

def contains_nan(df_col):
    '''
    `contains_nan` checks if a certain column has nans
    '''
    return df_col.isna().any()


def get_dummies_nan(df, return_nancols=False,inplace=False, separator="__"):
    '''
    `get_dummies_nan` creates a new dataframe with binary columns stating wheather variables contain NaNs.
    
    
    
    Examples:
    --------
    
    
    >>> df = pd.DataFrame([[2,"mercedes","middleclass"], 
                           [np.NaN,"mercedes","middleclass"],
                           [3,"Audi",np.NaN]],
                           columns= ["members","vehicles","status"])
    
    >>> df 

           members  vehicles       status
    0      2.0  mercedes  middleclass
    1      NaN  mercedes  middleclass
    2      3.0      Audi          NaN
    
    >>> df_ = get_dummies_nan(df)
    
    >>> df_
    
           members  vehicles       status  members_nan  status_nan
    0      2.0  mercedes  middleclass        False       False
    1      NaN  mercedes  middleclass         True       False
    2      3.0      Audi          NaN        False        True

    >>> df_, nancols = get_dummies_nan(df, return_nancols=True)
    
    >>> nancols
    
    ['members', 'status']

    '''
    def add_nan_columns(df):
        cols_with_nan = []
        for c in df.columns:
            if contains_nan(df[c]):
                cols_with_nan.append(c)
                df[c + separator +"nan"] = df[c].isna().values    
        return df, cols_with_nan


    if inplace:
        df, cols_with_nan = add_nan_columns(df) 
        if return_nancols:
            return cols_with_nan
    else:
        df_copy = df.copy(deep=True)
        df_copy, cols_with_nan = add_nan_columns(df_copy) 
        
        if return_nancols:
            return df_copy, cols_with_nan
        else:
            return df_copy


def _nan_rowfeatures_slowversion(df, reduce_methods=[np.mean, np.std], distances=False, inplace=False):
    
    """
    Slow version of `nan_rowfeatures` easier to understand.
    Generates new features containing for a given row k the "statistic" returned by a reduce
    operation on row k.
    
    t also computes the difference between the most value of the transformed nans per row and the found value.

    Examples:
    ---------
    >>> df = pd.DataFrame([[2,["p","b",None]], 
                   [3,["a","c",None]],
                  [3,["d","w","a"]]],columns= ["first","second"])
                  
    >>> df
    
       first        second
    0      2  [p, b, None]
    1      3  [a, c, None]
    2      3     [d, w, a]
    
    >>> df_ = nan_rowfeatures(df)
    
    >>> df_

        members  vehicles       status  mean_nans  std_nans
    0      2.0  mercedes  middleclass   0.000000  0.000000
    1      NaN  mercedes  middleclass   0.333333  0.471405
    2      3.0      Audi          NaN   0.333333  0.471405

    """
    def create_col(df, reducer):
        colname     = reducer.__name__ + '_rownans'
        df[colname] = df_cars.apply(lambda x: reducer(pd.isna(x)), axis=1)
        if distances:
            mode        = stats.mode(df[colname])[0]  
            df[colname + '_l1_to_mode' ] = np.abs(df[colname] - mode)
            df[colname + '_l2_to_mode']  = (df[colname] - mode)**2
            
    if inplace:
        for reducer in reduce_methods:
            create_col(df, reducer)
    else:
        df_copy = df.copy(deep=True)
        
        for reducer in reduce_methods:
            create_col(df_copy, reducer)
        return df_copy
    
    

def nan_rowfeatures(df, reduce_methods=[np.mean, np.std], distances=False, inplace=False):
    
    """
    `nan_features` generates new features containing for a given row k the "statistic" returned by a reduce
    operation on row k.
    
    It also computes the difference between the most value of the transformed nans per row and the found value.
    
    Examples:
    ---------
    >>> df = pd.DataFrame([[2,["p","b",None]], 
                           [3,["a","c",None]],
                           [3,["d","w","a"]]], 
                          columns= ["first","second"])
                  
    >>> df
    
       first        second
    0      2  [p, b, None]
    1      3  [a, c, None]
    2      3     [d, w, a]
    
    >>> df_ = nan_rowfeatures(df)
    
    >>> df_

       members  vehicles       status  mean_rownans  std_rownans
    0      2.0  mercedes  middleclass      0.000000     0.000000
    1      NaN  mercedes  middleclass      0.333333     0.433013
    2      3.0      Audi          NaN      0.333333     0.433013
    
    >>> df_ = nan_rowfeatures(df, distances=True)

           members  vehicles       status  mean_rownans  mean_rownans_l1_to_mode  \
    0      2.0  mercedes  middleclass      0.000000                 0.333333   
    1      NaN  mercedes  middleclass      0.333333                 0.000000   
    2      3.0      Audi          NaN      0.333333                 0.000000   

       mean_rownans_l2_to_mode  std_rownans  std_rownans_l1_to_mode  \
    0                 0.111111     0.000000                0.372678   
    1                 0.000000     0.372678                0.000000   
    2                 0.000000     0.372678                0.000000   

       std_rownans_l2_to_mode  
    0                0.138889  
    1                0.000000  
    2                0.000000  

    """
    
    def create_col(df, reducer):
        colname                       = reducer.__name__ + '_rownans'
        df[colname]                   = reducer(pd.isna(df), axis=1)
        if distances:
            mode                          = stats.mode(df[colname])[0]  
            df[colname + '_l1_to_mode']   = np.abs(mode - df[colname])
            df[colname + '_l2_to_mode']   = (mode - df[colname])**2
            
    if inplace:
        for reducer in reduce_methods:
            create_col(df, reducer)
    else:
        df_copy = df.copy(deep=True)
        
        for reducer in reduce_methods:
            create_col(df_copy, reducer)

        return df_copy



class _MissingImputer(BaseEstimator, TransformerMixin):
    '''
    `MissingImputer` implements a `fit` and `transform` methods that enable replacing np.NaN values by numerical values.
    This class uses an insane amount of RAM.
    '''
    def __init__(self, treatment="mean"):
        self._allowed_treatments = ["fixed_value", "mean",'median','mode','None',"most_frequent"]     
        assert treatment in self._allowed_treatments or isinstance(treatment,(int,float)),  "the treatment introduced {} is not valid. Please use one in {}".format(treatment, self._allowed_treatments)
        self.treatment = treatment
    
    def fit(self, X, y):
        """
        Learns statistics to impute nans.
        """
        
        if self.treatment == "mean" or self.treatment==None:
            self.treatment_method = sklearn.impute.SimpleImputer(missing_values=np.nan, strategy='mean')
        elif self.treatment == "median":
            self.treatment_method = sklearn.impute.SimpleImputer(missing_values=np.nan, strategy='median')
        elif self.treatment == "most_frequent":
            self.treatment_method = sklearn.impute.SimpleImputer(missing_values=np.nan, strategy='most_frequent')
        elif isinstance(self.treatment, (int,float)):
            self.treatment_method = sklearn.impute.SimpleImputer(missing_values=np.nan,
                                                                 strategy="constant",fill_value=self.treatment)       
        
        if isinstance(X, np.ndarray):   
            self.treatment_method.fit(X)
            
        if isinstance(X, pd.DataFrame):       
            self.treatment_method.fit(X.values)
        
        return self

    def transform(self, X):
        if self.treatment==None:
            return X
        return self.treatment_method.transform(X)



class NaNTransformer():
    def __init__(self, reducer=stats.mode):
        self.reducer = reducer
        self.col_id  = None 
        
    def fit(self, X_col, col_id):
        self.col_id = col_id
        self.learned_value = self.reducer(X_col)[0]
        
    def transform(self, X_col):
        X_col[pd.isna(X_col)] = self.learned_value
        return X_col

def itercols(X):
    
    if isinstance(X, np.ndarray):
        for i in range(X.shape[1]):
            yield i, X[:,i]
            
    if isinstance(X, pd.DataFrame):
        for colname in X:
            yield colname, X[colname]  
        
def get_col(X, col_id):
    
    if isinstance(X, np.ndarray):
        return  X[:,col_id]
            
    if isinstance(X, pd.DataFrame):
        return  X[col_id]  
             
        
class MissingImputer(BaseEstimator, TransformerMixin):
    '''
    `MissingImputer` implements a `fit` and `transform` methods that enable replacing np.NaN values by numerical values.

    This class less RAM han _MissingImputer
    '''
    def __init__(self, treatment=stats.mode):
        self._allowed_treatments = [np.mean, np.median, stats.mode]     
        assert treatment in self._allowed_treatments or isinstance(treatment,(int,float)),  "the treatment introduced {} is not valid. Please use one in {}".format(treatment, self._allowed_treatments)
        self.treatment = treatment
    
    def fit(self, X, y):
        """
        Learns statistics to impute nans.
        """
        
        col_transformers = {}
        
        for col_id, X_col in itercols(X):
            nan_transformer = NaNTransformer(reducer=self.treatment) 
            nan_transformer.fit(X_col, col_id = col_id)
            col_transformers[col_id] = nan_transformer            
                
        self.col_transformers = col_transformers
        return self

    def transform(self, X, inplace = False):
        """
        Method for transforming a dataframe of numpy array X replacing the np.NaN values.
        
        Notice that this method has a for loop over `self.col_transformers` instead of iterating over `itercols(X)`
        the main reason is that after `fit(X,y)` is done, a user might change `X`, introducing new columns that we
        don't want to iterave over (because we don't have a col_transformer for those new columns).

        -  If X is a dataframe users can change the order of the columns and still be able to use the transform method.
        
        -  If X is a numpy array then results will be corrupted because we don't have pointers to columns.
           Notice that if X is a numpy array `col_transformer` uses the indices of the columns found during `.fit(X,y)`.

        """
        
        if inplace:

            if self.treatment==None:
                return None

            #for col_id, X_col in itercols(X):
            #    X_col = self.col_transformers[col_id].transform(X_col)
            for col_id in self.nan_transformers:
                X_col = get_col(X, col_id)
                X_col = self.col_transformers[col_id].transform(X_col)
                
        else:
            X_copy = copy.deepcopy(X)
            
            if self.treatment==None:
                return X_copy
            
            #for col_id, X_col in itercols(X_copy):
            #    X_col = self.col_transformers[col_id].transform(X_col)
            for col_id in self.col_transformers:
                X_col = get_col(X_copy, col_id)
                X_col = self.col_transformers[col_id].transform(X_col)
                
            return X_copy


def onehot_collist_byvalue(collist, values_to_index):
    """
    
    `onehot_collist_byvalue` generates a np.ndarray containing the one hot representation of the input collist
     The returned array stores at position `(i,j)` a 1 if the linked column to integer `j` has a name  found 
     in `collist[i]`.

    ##### Example 
    
    collist         = [["tesla"], ["mercedes", "audi"], ["toyota", "mercedes", "tesla"]]
    values_to_index = {'audi':0, 'mercedes':1, 'tesla':2. 'toyota':3}
    
    The returned array should be:

        [0 0 1 0
         1 1 0 0
         0 1 1 1]
    
    ## INPUTS
    
    values_to_index: dict
    
    Dictionary asigning an index to all the possible values in the different lists o collist.
    
    
    ## OUPTUT
    
    onehot_matrix: np.ndarray
    
    Numpy matrix storing at position `(i,j)` the existance of value `j` in the list `collist[i]`.
    
    """
    
    n_rows = len(collist)
    n_cols = len(values_to_index)
    result = np.zeros((n_rows, n_cols), dtype=np.bool)   
    
    for k,row in enumerate(collist):
        for element in row:
            element_index = values_to_index[str(element)]
            result[k, element_index] = 1
            
    return result
            


def proc_df_collist_byvalue(df: pd.DataFrame, colname: str, inplace=False):
    """
    
    `proc_df_collist` takes a dataframe and a column name as input. If the column of the dataframe
    is made of iterables then it generates new columns. Otherwise it returns an assertion error.
    
    The function generates new columns, as many as different values can be found in the elements of the iterables
    in `df[colname]`. Each new column stores, at position `k`, the presence (or absence) of an item in `df[colname][k]`.

    - Each new column is formated as "colname_X" where X is one of the values found in `pd[colname]`.
    
    - The function returns a new dataframe onehot_df if inplace=False.
    
    - `onehot_df[colname_X][k]` is 1 if and only if `X in pd[colname][k]` (it's zero otherwise).
    
    
    Examples:
    ---------
    >>> df = pd.DataFrame([[2,["p","b",np.nan]], 
                           [3,["a","c",np.nan]],
                           [3,["d","w","a"]]],
                           columns= ["first","second"])
                  
    >>> df
    
       first        second
    0      2   [p, b, nan]
    1      3   [a, c, nan]
    2      3     [d, w, a]

    >>> newcols = proc_df_collist_byorder(df, "second")

    >>> newcols
    
       second_a  second_b  second_c  second_d  second_nan  second_p  second_w
    0     False      True     False     False        True      True     False
    1      True     False      True     False        True     False     False
    2      True     False     False      True       False     False      True

    
    >>> df2 = pd.DataFrame([[2,["p"]], 
                   [3,["a",2,3]],
                   [3,[4]]],columns= ["A","B"])
                   
    >>> df2
    
       A          B
    0  2        [p]
    1  3  [a, 2, 3]
    2  3        [4]

    >>> proc_df_collist_byorder(df2, "B")

      B_0  B_1  B_2
    0   p  NaN  NaN
    1   a  2.0  3.0
    2   4  NaN  NaN

    """
    assert isinstance(colname, str), "type(columname)={} but it should be str".format(type(str))
    assert isinstance(df[colname].iloc[0],(list,set, np.ndarray)), "type(df[colname].iloc[0])={} but it, should be in [list, set, np.ndarray]".format(type(df[colname].iloc[0]))
    
    unique_values = list(set([str(x) for x in itertools.chain(*df[colname].values)]))
    colnames   = [colname + "_" + str(i) for i in unique_values]   
    n_unique_values = len(unique_values)
    colnames.sort()
    unique_values.sort()
    
    unique_values_to_index = {val:i for i,val in enumerate(unique_values)} 
    onehot_array = onehot_collist_byvalue(df[colname], unique_values_to_index)
    
    onehot_df    = pd.DataFrame(onehot_array, columns=[f"{colname}_{c}" for c in unique_values])
    
    return onehot_df 



def proc_df_collist_byvalue(df: pd.DataFrame, colname: str, inplace=False):
    """
    
    `proc_df_collist` takes a dataframe and a column name as input. If the column of the dataframe
    is made of iterables then it generates new columns. Otherwise it returns an assertion error.
    
    The function generates new columns, as many as different values can be found in the elements of the iterables
    in `df[colname]`. Each new column stores, at position `k`, the presence (or absence) of an item in `df[colname][k]`.

    - Each new column is formated as "colname_X" where X is one of the values found in `pd[colname]`.
    
    - The function returns a new dataframe onehot_df if inplace=False.
    
    - `onehot_df[colname_X][k]` is 1 if and only if `X in pd[colname][k]` (it's zero otherwise).
    
    
    Examples:
    ---------
    >>> df = pd.DataFrame([[2,["p","b",np.nan]], 
                           [3,["a","c",np.nan]],
                           [3,["d","w","a"]]],
                           columns= ["first","second"])
                  
    >>> df
    
       first        second
    0      2   [p, b, nan]
    1      3   [a, c, nan]
    2      3     [d, w, a]

    >>> newcols = proc_df_collist_byorder(df, "second")

    >>> newcols
    
       second_a  second_b  second_c  second_d  second_nan  second_p  second_w
    0     False      True     False     False        True      True     False
    1      True     False      True     False        True     False     False
    2      True     False     False      True       False     False      True

    
    >>> df2 = pd.DataFrame([[2,["p"]], 
                   [3,["a",2,3]],
                   [3,[4]]],columns= ["A","B"])
                   
    >>> df2
    
       A          B
    0  2        [p]
    1  3  [a, 2, 3]
    2  3        [4]

    >>> proc_df_collist_byorder(df2, "B")

      B_0  B_1  B_2
    0   p  NaN  NaN
    1   a  2.0  3.0
    2   4  NaN  NaN

    """
    assert isinstance(colname, str), "type(columname)={} but it should be str".format(type(str))
    assert isinstance(df[colname].iloc[0],(list,set, np.ndarray)), "type(df[colname].iloc[0])={} but it, should be in [list, set, np.ndarray]".format(type(df[colname].iloc[0]))
    
    unique_values = list(set([str(x) for x in itertools.chain(*df[colname].values)]))
    colnames   = [colname + "_" + str(i) for i in unique_values]   
    n_unique_values = len(unique_values)
    colnames.sort()
    unique_values.sort()
    
    unique_values_to_index = {val:i for i,val in enumerate(unique_values)} 
    onehot_array = onehot_collist_byvalue(df[colname], unique_values_to_index)
    
    onehot_df    = pd.DataFrame(onehot_array, columns=[f"{colname}_{c}" for c in unique_values])
    
    return onehot_df 


def get_key_value(k):
    return k.split("=")

def proc_df_collist_bykeyvalue(df: pd.DataFrame, colname: str, get_key_value,
                               column_separator="_", inplace=False, treat_nan_func=None):
    """
    
    `proc_df_collist` takes a dataframe and a column name as input. If the column of the dataframe
    is made of iterables then it generates new columns. Otherwise it returns an assertion error.
    
    The function generates new columns, as many as different "keys"  can be found in the elements of the iterables
    in `df[colname]`. In order to found a "key" from an element `proc_df_collist_bykeyvalue` expects a method
    `get_key_value`, that should return a (key,value) pair for a given input. 
    
    
    Each new column stores, the elements of the correspondant variable.
    
    - Each new column is formated as `f"colname{column_separator}X"` where X is one of the variables found
      in `pd[colname]`.
    
    - The function returns a new dataframe `result_df` if inplace=False.
    
    - `result_df[colname{column_separator}X][k]` has a value if and only if `X in pd[colname][k]` (it's zero otherwise).
    
    
    Example of `get_key_value` method
    
    Assume rows of `df[colname]` have the form [`var1=v1`, `var2=v2`]. Then a possible function `get_key_value`
    could be simply `lambda x: x.split("=")` which returns a pair of elements for a given input string.
            
    Examples:
    ---------
    >>> df = pd.DataFrame([[2,["var1=p", "var2=p", np.nan]], 
                           [3,["var2=p", "var1=pc", np.nan]],
                           [3,["var3=pd", "var2=pw", "var1=pa"]]],
                           columns= ["first","second"])
                  
    >>> df

       first                         second
    0      2   [var1=p, var2=p, nan=np.nan]
    1      3  [var2=p, var1=pc, nan=np.nan]
    2      3    [var3=pd, var2=pw, var1=pa]

    >>> colname = "second"
    
    >>> def get_key_value(k):
           return k.split("=")

    >>> proc_df_collist_bykeyvalue(df, colname, get_key_value, column_separator="__")

      second__nan second__var1 second__var2 second__var3
    0      np.nan            p            p            0
    1      np.nan           pc            p            0
    2           0           pa           pw           pd
    
    """
    
    def treat_nan(x):
        result = []
        for x_k in x:
            if isinstance(x_k, str):
                result.append(x_k)
            elif np.isnan(x_k):
                result.append("nan=np.nan")
        return result

    def get_all_keys(df, colname):
        all_keys = set()
        for x in df[colname]:
            all_keys = all_keys.union([get_key_value(x_k)[0] for x_k in x])
        return all_keys   

    def write_row_as_list(row, var_to_pos):
        row_code = [0]*len(var_to_pos)

        for item in row:
            key, value = get_key_value(item)
            row_code[var_to_pos[key]] = value
        return row_code

    if treat_nan_func is None:
        treat_nan = treat_nan
    else:
        treat_nan = treat_nan_func
    
    
    assert isinstance(colname, str), "type(columname)={} but it should be str".format(type(str))
    assert isinstance(df[colname].iloc[0],(list,set, np.ndarray)), "type(df[colname].iloc[0])={} but it, should be in [list, set, np.ndarray]".format(type(df[colname].iloc[0]))

    df[colname] = df[colname].apply(treat_nan)
    all_keys    = list(get_all_keys(df, colname))
    all_keys.sort()
    newcolnames        = [colname + column_separator + name for name in all_keys]
    newcolnames_to_int = {col:i for i,col in  enumerate(newcolnames)}
    var_to_pos         = {col:newcolnames_to_int[fullname] for col,fullname in  zip(all_keys,newcolnames)}
    pos_to_var         = {v: k for k, v in var_to_pos.items()}
    
    result = []
    for row in df[colname]:
        result.append(write_row_as_list(row, var_to_pos))
            
    
    result_df   = pd.DataFrame(result, columns=newcolnames)
    
    return result_df 



def proc_df_collist_byorder(df: pd.DataFrame, colname: str, inplace=False):
    """
    
    `proc_df_collist` takes a dataframe and a column made of lists and generates new columns which write the
    values contained in the original lists in a consecutive order.
    
    For each position in the list it generates a new column. The total number of columns 
    equals the length of the largest list in `df[colname]`. 
    
    - Each new collumn  k is filled with the values of the lists at position k.
    
    - If the value does not exist (because the position does not exist) the position is filled with `NaN`. 
    
    Given `df`  and `colname`, create as many new columns as `n_new_cols =  df[colname].apply(len).max()`
    Write in column `colname_k[j]` the value found `df[colname].iloc[j][k]`. If a position for a given row
    does not exist, write np.nan in the corresponding column.
    
    
    Examples:
    ---------
    >>> df = pd.DataFrame([[2, ["p", "b", np.nan]], 
                           [3, ["a", "c", np.nan]],
                           [3, ["d", "w", "a"]]],
                           columns= ["first","second"])

    >>> df
    
       first        second
    0      2  [p, b, nan]
    1      3  [a, c, nan]
    2      3     [d, w, a]

    >>> newcols = proc_df_collist_byorder(df, "second")

    >>> newcols
    
          second_0 second_1 second_2
    0        p        b     None
    1        a        c     None
    2        d        w        a

    
    >>> df2 = pd.DataFrame([[2,["p"]], 
                   [3,["a",2,3]],
                   [3,[4]]],columns= ["A","B"])
                   
    >>> df2
    
       A          B
    0  2        [p]
    1  3  [a, 2, 3]
    2  3        [4]

    >>> proc_df_collist_byorder(df2, "B")

      B_0  B_1  B_2
    0   p  NaN  NaN
    1   a  2.0  3.0
    2   4  NaN  NaN

    """
    assert isinstance(df, pd.DataFrame), "type(df)={} but it should be pd.DataFrame".format(type(df))
    assert isinstance(colname, str), "type(columname)={} but it should be str".format(type(str))
    assert isinstance(df[colname].iloc[0],(list,set, np.ndarray)), "type(df[colname].iloc[0])={} but it, should be in [list, set, np.ndarray]".format(type(df[colname].iloc[0]))
    
    #n_new_cols = len(df[colname].iloc[0])
    n_new_cols = df[colname].apply(len).max()
    colnames   = [colname + "_" + str(i) for i in range(n_new_cols)]   
    return pd.DataFrame(df[colname].tolist(), columns=colnames)
