

## Install virtualenv

To install virtualenv:
```
pip install virtualenv
```

##Create a new environment

The **`virtualenv`**  command can be used to create a new environment.

To create an environment with name `name_environment`  do:

```
virtualenv name_environment
```

This command will create a folder `name_environment` in the directory in which it is called.

### Create a new environment with  a specific python version

The **`virtualenv`**  command can be used to create a new environment with a specific python version found in `python_path`:

```
virtualenv -p  python_path name_environment
```

For example:

```
virtualenv -p  /usr/bin/python2.6 name_environment
```



## Use a particular environment

The **`source`** command can be used to  activate a previously created environment

```
source name_environment/bin/activate
```

## Install package

The **`pip install package_name`**  command can be used naturally to install packages inside the running environment

## Go out of an environment

The **`deactivate`** command leaves the current working environment





## Example

Now we will create a folder  `virtualenv_Environments` in which we will create a new project environment `env1`:

```bash
mkdir virtualenv_Environments
cd virtualenv_Environments
virtualenv env1
```

After executing the previous commands we can see a folder  `env1` in  `virtualenv_Environments/env1`.

To activate the environment we need to `source` the `activate` inside `env1/bin`:

```
source env1/bin/activate
```

Now the commandline should have `(env1)` at the start of the terminal to indicate that we are inside the activated environment.

```
(env1) virtualenv_Environments$ 
```

Once inside the new environment we can see that there are no packages installed:

```
pip list
```

```bash
Package    Version
---------- -------
pip        20.2.1
setuptools 49.2.1
wheel      0.34.2
```

Now the pip version we are using inside the environment is located in `env1/bin/`

```
which pip
```

```
python_tutorials/python_environments/manage_virtualenv/virtualenv_Environments/env1/bin/pip
```

Now the python version we are using inside the environment is located in `env1/bin/`

```
which python
```

```
python_tutorials/python_environments/manage_virtualenv/virtualenv_Environments/env1/bin/python
```

Now let us install the `pandas`  package:

```
pip install pandas
```

Since pandas depends on other packages they will be installed.

Now we can see

```
pip list
```

```
Package         Version
--------------- -------
numpy           1.18.5
pandas          0.25.3
pip             20.2.1
python-dateutil 2.8.1
pytz            2020.1
setuptools      49.2.1
six             1.15.0
wheel           0.34.2
```

Imagine that this is all that we will need in `env1` to do a particular project. Then we can do:

```
pip freeze --local > env1/requirements.txt
```

Now we can manually inspect the file `env1/requirements.txt `

```
cat env1/requirements.txt
```

```
numpy==1.18.5
pandas==0.25.3
python-dateutil==2.8.1
pytz==2020.1
six==1.15.0
```

Let us assume we want now `env2` that uses a different python version.

```
virtualenv -p  /usr/bin/python2.6 env2
```



