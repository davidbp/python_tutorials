### Cythonising a single python script



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

Another possible way  to compile the function in `fib_cy.pyx`  is using a setup script. The file  `compile_fib.py` contains the basics to compile the the fib function.


 We can compile the function with the following command:

```
python3 compile_fib.py build_ext --inplace 
```

You should see an output similar to this:
```
running build_ext
building 'fib_cy' extension
creating build
creating build/temp.linux-x86_64-3.6
gcc -pthread -B /home/david/anaconda/envs/py3/compiler_compat -Wl,--sysroot=/ -Wsign-compare -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -I/home/david/anaconda/envs/py3/include/python3.6m -c fib_cy.c -o build/temp.linux-x86_64-3.6/fib_cy.o
gcc -pthread -shared -B /home/david/anaconda/envs/py3/compiler_compat -L/home/david/anaconda/envs/py3/lib -Wl,-rpath=/home/david/anaconda/envs/py3/lib -Wl,--no-as-needed -Wl,--sysroot=/ build/temp.linux-x86_64-3.6/fib_cy.o -o /home/david/Documents/git_stuff/python_tutorials/python_advanced/cython/01_compile_cython/fib_cy.cpython-36m-x86_64-linux-gnu.so
```

Now the extension module  `fib_cy.cpython-36m-x86_64-linux-gnu.so` is created in the same folder  and it should be moved into `cython_code` before executing `test_fib.py`.





### Speed difference

After compiling we can call `test_fib.py`  

We can see a 20X improvement in speed

```
total time fib.fib method is 6.0518574714660645 seconds
total time fib_cy.fib method is 0.3160085678100586 seconds
```

