## Cythonizing a single python script

From bash we can use the function `cythonize` to compile a `.pyx` function.

First let us look at the folder `./cython_code` which should contain

```
fib_cy.pyx
python_command_to_compile.txt
```

Now, in order to compile the function `fib_cy.pyx` we can use the `cythonize` command as follows:

 `cythonize --inplace --annotate ./cython_code/fib_cy.pyx`

This  compiles the `fib_cy.pyx` into a module. Now if we inspect the `./cython_code` folder we will see:

```
fib_cy.pyx
python_command_to_compile.txt
fib_cy.cpython-36m-x86_64-linux-gnu.so
fib_cy.html
fuc_cy.c
```



- `fib_cy.cpython-36m-x86_64-linux-gnu.so` is the compiled script that we can now import directly from within python.
- `fib_cy.html` is an annotation file (which is created because we used the option `--annotate`). This file contains hints on which lines of code we can optimize more in the `fib_cy.pyx` file.
- `fib_cy.c` is the translation to `c` of our cython file `fib_cy.pyx`.







## Compiling from a setup file `compile_fib.py`

The cython code neede to generate a cythonized version of `fib.py` is found in the folder `./cython_code`.

Inside the folder there are the rollowing files:

```
compile_fib.py  fib.pyx  __init__.py  python_command_to_compile.txt
```


- `fib.pyx` is a cython function that mimics `../fib.py'.

- `compile_fib.py` is a python function that continas the code to make a cython extension module.

- `__init__.py` is a python file in order to make the folder a Python module which gives us access to the function inside fib.pyx.

- `python_command_to_compile.txt` contains the code needed to call  `compile_fib.py`.


## Copiling a cython file

In order to compile the function in `fib_cy.pyx` we have created `compile_fib.py`.


Then we can compile the function with the following command:

```
python3 compile_fib.py build_ext --inplace
```

This should be executed inside the `./cython_code`.

You should see an output similar to this:
```
running build_ext
building 'fib_cy' extension
creating build
creating build/temp.linux-x86_64-3.6
gcc -pthread -B /home/david/anaconda/envs/py3/compiler_compat -Wl,--sysroot=/ -Wsign-compare -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -I/home/david/anaconda/envs/py3/include/python3.6m -c fib_cy.c -o build/temp.linux-x86_64-3.6/fib_cy.o
gcc -pthread -shared -B /home/david/anaconda/envs/py3/compiler_compat -L/home/david/anaconda/envs/py3/lib -Wl,-rpath=/home/david/anaconda/envs/py3/lib -Wl,--no-as-needed -Wl,--sysroot=/ build/temp.linux-x86_64-3.6/fib_cy.o -o /home/david/Documents/git_stuff/python_tutorials/python_advanced/cython/01_compile_cython/fib_cy.cpython-36m-x86_64-linux-gnu.so
```

inside the folder ``

Moreover, `fib_cy.cpython-36m-x86_64-linux-gnu.so` is created.
