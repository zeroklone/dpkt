# Python 3 migration notes for dpkt

This markdown file mainly introduce how to migrate `dpkt` from Python 2 to Python 3 in order to provide support for both the two main versions. Also this doc will also provide some suggestions for future hackers who aim to contribute both Python 2 and 3 compatible code to `dpkt`.

## How to migrate Python 2 code to Python 3

**_`2to3` initial conversion_**

Use `2to3` to get an initial result which is compatible for Python 3. `2to3` can automatically solve the following migration issues.

* Python 2 has two integer types `int` and `long`. These have been unified in Python 3, so there is now only one type, `int`. Here is an example.

 _Python 2_
 ``` python
 tmp = ~crc & 0xffffffffL
 ```
_Python 2 & 3_
 ``` python
tmp = ~crc & 0xffffffff
 ```

* The Python 2 `print` statement is in Python 3 a function.

 _Python 2_
 ``` python
 print '%s : time = %f kstones = %f' % (function.__name__, time, kstones)
 ```

 _Python 2 & 3_
 ``` python
 print('%s : time = %f kstones = %f' % (function.__name__, time, kstones))
 ```

* In Python 3 the syntax to catch exceptions have changed.

 _Python 2_
 ``` python
 except struct.error, e:
 ```

 _Python 2 & 3_
 ``` python
 except struct.error as e:
 ```

**_`import` and `dict` related syntax._**

The `import` and `dict` are both changed in Python 3. Note that the `2to3` automatic update cannot provide compatible code for both Python 2 and 3. Thus we should update the code based on different cases. Here are examples.

_Python 2_
``` python
from StringIO import StringIO
```

_Python 2 & 3_
``` python
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
```

_**Metaclass related issues**_

Based on http://python-3-patterns-idioms-test.readthedocs.org/en/latest/Metaprogramming.html.

The equivalent of:

``` python
class C: pass
```

is:

``` python
C = type('C', (), {})
```

Thus the metaclass syntax in `dpkt.py` module can be modified, which is both Python 2 and 3 compatible, as follows.

``` python
class Packet(_MetaPacket("Temp", (object,), {}))
```

**_Import related_**

> Python 3 changes the syntax for imports from within a package, requiring you to use the relative import syntax, saying `from . import mymodule` instead of the just `import mymodule`.

**_`next` method of the iterator_**

In Python 2 iterators have a `.next()` method you use to get the next value from the iterator. For instance,

``` python
>>> i = iter(range(5))
>>> i.next()
0
>>> i.next()
1
```

This special method has in Python 3 been renamed to `.__next__()` to be consistent with the naming of special attributes elswhere in Python. However, we should generally not call it directly, but instead use the builtin is `next()` function. This function is also available from Python 2.6. Here is an example.

``` python
for _ in range(cnt):
    try:
        ts, pkt = next(iter(self))
```

**_`chr` and `ord` built-in function_**

For `ord(c)`, given a string of length one, it'll return an integer representing the Unicode code point of the character when the argument is a unicode object, or the value of the byte when the argument is an 8-bit string. While for `chr(i)`, it'll return a string of one character whose ASCII code is the integer i.

In Python 2, both of the two function's usage is straight forward. For example, we have the following code snippet.

``` python
l = buf.split(chr(IAC))
```

However, in Python 3, please note that most time in `dpkt` we'll deal with data with the type of `bytes`. Thus it is improper if the `buf` is of the type of `bytes` while the `chr()` function returns `str`. In order to solve this problem, we update the code as follows to provide support for both Python 2 and 3.

``` python
if sys.version_info < (3,):
    l = buf.split(chr(IAC))
else:
    l = buf.split(struct.pack("B", IAC))
```

Similarly, for `ord` function, we could have the snippet as follows,

``` python
o = ord(w[0])
```

where `w` is a string and `o` is an integer. Yet in Python 3, every element of `bytes` array is an integer, thus it is no need for the calling of `ord` any more. 

Due to the expandability consideration, we add a `compatible` module in the project, and it'll provide some functions that are both compatible for Python 2 and 3. Currently there is only one function, namely, `ord`. Please see the implementation below.

``` python
if sys.version_info < (3,):
    def compatible_ord(char):
        return ord(char)
else:
    def compatible_ord(char):
        return char
```

Using the `compatible` module, the contributor only need to modify the client code as follows.

``` python
o = compatible.compatible_ord(w[0])
```




## How to contribute both Python 2 and 3 compatible code

If you want to contribute new code to `dpkt`, it is essential to write both Python 2 and 3 compatible code. After `dpkt 2.0`, we'll both provide Python 2.6+ and 3.x support. Also the auto build system `travis` will build on both 2 and 3 for every PR and commit.

Well, my suggestions for writing both Python 2 and 3 compatible code are as follows.

1. Read the `How to migrate Python 2 code to Python 3` section of this documentation and get familar with the key issues while migration the project to Python 3.
2. Setup both 2 and 3 environments on your local machine.
3. Follow the rules below to contribute new code. http://python-future.org/compatible_idioms.html
