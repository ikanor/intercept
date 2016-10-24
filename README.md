intercept
===========

Intercept your Python exceptions! As awesome as driving a real interceptor!

![As awesome as this.](Anakin_jedi_interceptor.jpg)

Usage
-----

You can use the `intercept` decorator to return a value or raise a specific error when the declared exceptions are raised:

```python
from intercept import intercept, returns, raises
@intercept({
   TypeError: returns('intercepted!'),
   AttributeError: raises(Exception('intercepted!'))
})
def test(critical: bool):
    if not critical:
        raise TypeError
    else:
        raise AttributeError
```

Also, you might also want to use callables if you need to inspect the raised errors:

```python
from intercept import intercept, returns
@intercept({
   TypeError: returns(lambda e: 'intercepted {}'.format(e))
})
def test():
    raise TypeError('inner exception')
```

The decorator can be instantiated:

```python
from intercept import intercept, returns
interceptor = intercept({
   TypeError: returns('intercepted!')
})
@interceptor
def test():
    raise TypeError
```

so you can reuse it. Bonus: you can name a variable after a spaceship model.

Compatibility
-------------

Tested with Python 3.5.

Installation
------------

You can obtain `intercept` from PyPI:

```bash
pip install intercept
```

