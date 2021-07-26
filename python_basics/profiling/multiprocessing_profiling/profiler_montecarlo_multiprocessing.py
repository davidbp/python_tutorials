from line_profiler import LineProfiler

import montecarlo

lp = LineProfiler()
lp_wrapper = lp(montecarlo.main)
lp_wrapper()
lp.print_stats()

