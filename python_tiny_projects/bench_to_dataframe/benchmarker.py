import re
import inspect
from io import StringIO
from decimal import Decimal, DecimalException

from line_profiler import LineProfiler
import numpy as np
import pandas as pd

def profile_function(my_func, *args, **kwargs):
    lp = LineProfiler()
    output_val = lp(my_func)(*args, **kwargs)
    
    # Redirect stdout so we can grab profile output
    mystdout = StringIO()
    lp.print_stats(stream=mystdout) 
    lprof_lines = mystdout.getvalue().split('\n')

    profile_start = 1 + next(idx for idx, line in enumerate(lprof_lines) if '=====' in line)
    lprof_code_lines = lprof_lines[profile_start:-1]
    source_lines = inspect.getsource(my_func).split('\n')

    if len(source_lines) != len(lprof_code_lines):
        print("WARNING! Mismatch in source length and returned line profiler estimates")
        print('\n'.join(lprof_lines))
        print("---- Code ----")
        print(source)
    else:
        print("\n".join(lprof_lines[:profile_start]))
        print("\n".join(["{0} \t {1}".format(l, s) for l, s in zip(lprof_code_lines, source_lines)]))
    
    return output_val, source_lines, lprof_code_lines

def get_colum_values(lines, source_lines):
    """
    Build a Dataframe containing the line by line metrics of the optimized function
    """
    cols = ['Line #','Hits', 'Time', 'Per Hit', '% Time', 'Line Contents']

    pattern = re.compile(r'\S+')
    
    parsed_lines = []
    for line in lines:
        line_values = []
        line_splitted = pattern.findall(line)
        for value in line_splitted:
            try:
                res = Decimal(value)
                line_values.append(float(res))
            except (ValueError, DecimalException):
                continue
            
        parsed_lines.append(line_values)
    
    result = [p[0:5] for p in parsed_lines[0:-1]]
    df = pd.DataFrame(result, columns=cols[0:-1])
    df = df.replace(np.nan, 0)
    df[cols[-1]] = source_lines[0:-1]
    return df


def profile_as_dataframe(function, *args, **kwargs):
    output_val, source_lines, lprof_code_lines = profile_function(function, *args)
    result_df = get_colum_values(lprof_code_lines, source_lines)
    return result_df

def plot_profile(df_result):
    lines = list(df_result['Line Contents'])
    ax = df_result['% Time'][::-1].plot(kind='barh')
    ax.set_yticklabels(lines[::-1], rotation=0)
    ax.set_title('func_to_test profiling')
