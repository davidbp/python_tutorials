

# IO


## serialization

We can store python objects to disc and load them back from disc.
The `pickle` module allows us to dump and load most python objects. The
key methods to do this are:

- **`pickle.dump(python_object, opened_file)`**: stores `python_object` to disc in the file `opened_file`.
- **`pickle.load(opened_file)`**: returns a Python object stored in `opened_file`.

```python
class A():
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def save(self, path):
        with open(path,'wb') as f:
            pickle.dump(self, f)
    
    @classmethod
    def load(self, path):
        with open(path, 'rb') as f:
            return pickle.load(f)
```

The following code
```python
a = A(1,2)
a.save('a.pkl')
a_rec = A.load('a.pkl')
print(f'a.__dict__={a.__dict__}')
print(f'a_rec.__dict__={a_rec.__dict__}')
assert a_rec.__dict__ == a.__dict__
```
prints
```commandline
a.__dict__={'a': 1, 'b': 2}
a_rec.__dict__={'a': 1, 'b': 2}
```


### Example of pickled class that will not work 

Note that the following code will not work since sqlite cursor objects are not pickable:

```python
import sqlite3

conn = sqlite3.connect('vectors.db')
cursor = conn.cursor()
a_with_sqlite_cursor = A(1, cursor)
a_with_sqlite_cursor.save('a_with_sqlite_cursor.pkl')
```

the previous code prints

```python
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
----> 1 a_with_sqlite_cursor.save('a_with_sqlite_cursor.pkl')

<ipython-input-7-7e6d252e2106> in save(self, path)
      6     def save(self, path):
      7         with open(path,'wb') as f:
----> 8             pickle.dump(self, f)
      9 
     10     @classmethod

TypeError: cannot pickle 'sqlite3.Cursor' object
```



#### Possible workaround (how not to do it)

In this case we can't pickle the class containing an `sqlite3.Cursor` object. 
Instead of saving the object with a `Cursor` we can store a path and then load it.
This means we need to remove inside the `.save` the cursor  and create it inside the `.load`.

```python
class ASQLite():
    def __init__(self, a, db_path):
        self.a = a
        self.db_path = db_path
        self._connect_to_db()

    def _connect_to_db(self):
        self.cursor = sqlite3.connect(self.db_path)

    def save(self, path):
        self.cursor = None
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load(self, path):
        with open(path, 'rb') as f:
            asqlite = pickle.load(f)
        asqlite.connect_to_db()
        return asqlite
```

With this class now we can save and reconstruct since we make sure the `self.cursor` is removed.

```python
a_sqlite = ASQLite(a=1, db_path='database.db')
a_sqlite.save('a_sqlite.pkl')
a_sqlite_rec = ASQLite.load('a_sqlite.pkl')
```


#### Possible workaround (how to do it)

There is a better alternative that does not envolve modifying the `.cursor` inside the `.save`
and `.load` functions but externalizes this work to `__setstate__` and `__getstate__`. The advantage of implementing 
such methods is that even if a user uses `pickle` without calling `.save` and `.load` the code will still work.

```python
class ASQLite():
    def __init__(self, a, db_path):
        self.a = a
        self.db_path = db_path
        self.connect_to_db()

    def __getstate__(self):
        # remove the sql conection
        state = dict(self.__dict__)
        state['cursor'] = None
        print('this is called when pickling')
        return state

    def __setstate__(self, state):
        print('this is called when unpickling')
        self.__dict__ = state
        self.connect_to_db()

    def connect_to_db(self):
        self.cursor = sqlite3.connect(self.db_path)

    def save(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load(self, path):
        with open(path, 'rb') as f:
            asqlite = pickle.load(f)
        return asqlite
```
Now, the following code 
```python
a_sqlite = ASQLite(a=1, db_path='database.db')
a_sqlite.save('a_sqlite.pkl')
a_sqlite_rec = ASQLite.load('a_sqlite.pkl')
print(f'a_sqlite_rec.cursor={a_sqlite_rec.cursor}')
```
prints
```commandline
this is called when pickling
this is called when unpickling
a_sqlite_rec.cursor=<sqlite3.Connection object at 0x7fab287053f0>
```
This tells us that the method `__getstate__` is called when pickling the object and the 
mehtod `__setstate__` is called when unpickling the object. Note that the intance `a_sqlite_rec` has
access to `.cursor` even though the `load` method does not explicitly calls `connect_to_db`.
This happens because `__setstate__` ends up calling `.connect_to_db`.

### Example of pickled class that might not work 

Note that the following code might not work depending on the Python version that you are using,
since compiled regular expressions where not "pickable" in some python versions. 

```python
import re
a_with_regex = A(1, re.compile('\w+'))
a_with_regex.save('a_with_regex.pkl')
a_with_regex_rec = A.load('a_with_regex.pkl')
```


### hdf5