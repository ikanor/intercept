interceptor
===========

Intercept your Python exceptions! As awesome as driving a real Interceptor.

![As awesome as this.](Anakin_jedi_interceptor.jpg)

Usage
-----

You can use `interceptor` to return a value or raise a specific error when the declared exceptions are risen:

```python
@intercept({
   TypeError: returns('intercepted!'),
   AttributeError: raises(Exception('intercepted!'))
})
def f():
    raise TypeError
```

Also, you might also want to use callables if you need to inspect the risen errors:

```python
@intercept({
   TypeError: returns(lambda e: 'intercepted {}'.format(e))
})
def f():
    raise TypeError
```

You can read the docs for further examples.

Compatibility
-------------

Tested with Python 3.5.

