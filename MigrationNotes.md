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

## How to contribute both Python 2 and 3 compatible code
