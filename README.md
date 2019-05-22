# python_tutorials
This repository contains little tutorials showcasing relevant aspects of python 3.

The repository is organized into 5 sections (folders) each folder contains little scripts to test and show how to accomplish different tasks.

- **python_basics**: Contains basic modules to dominate python.
- **python_advanced**: Contains examples from  task-specific libraries such as cython and pyspark.
- **python_environments**: Contains exampes of how to isolate python environments.
- **python_libraries**: Contains examples of relevant python libraries
- **python_tiny_projects**: Contains little projects to showcase the previous folders



##Python Basics

This folder contains subfolders dedicated to different python modules or topics.

- **sys**: Control system-specific parameters and functions
  - sys.argv: Basic way to retrieve arguments to python scripts. First element is the python script name.
  - argparse: How to pass keyword arguments to python scripts.

- **async**: Launch python tasks without beeing blocked by others. Typically very usefull for io bound tasks.
- **concurrent_execution**: Do work in parallel in python
  - multiprocessing: How to use multiple threads in parallel in python.

- **io**: Write to files and read from files
- **strings**: Format, edit, parse and construct strings.
- **os_communication**: Move, create, read, inspect the file system of your operating system inside python.



## Python Advanced

This folder contains subfolders dedicated to special (but general purpose)  python libraries or advanced topics.

- **cython**:  Allows you to compile "python code" (cython code) to C and use it in python applications.
- **pyspark**: Use pyspark to do parallel work in computer clusters.