"""
Provides a function decorator that allows managing exceptions with custom
actions.
"""


def intercept(actions: dict={}):
    """
    Decorates a function and handles any exceptions that may rise.

    Args:
        actions: A dictionary ``<exception type>: <action>``. Available actions\
            are :class:`raises` and :class:`returns`.

    Returns:
        Any value declared using a :class:`returns` action.

    Raises:
        AnyException: if AnyException is declared together with a
            :class:`raises` action.
        InterceptorError: if the decorator is called with something different
            from a :class:`returns` or :class:`raises` action.

    Interceptors can be declared inline to return a value or raise an exception
    when the declared exception is risen:

    >>> @intercept({
    ...    TypeError: returns('intercepted!')
    ... })
    ... def fails(foo):
    ...     if foo:
    ...         raise TypeError('inner exception')
    ...     return 'ok'
    >>> fails(False)
    'ok'
    >>> fails(True)
    'intercepted!'

    >>> @intercept({
    ...    TypeError: raises(Exception('intercepted!'))
    ... })
    ... def fail():
    ...     raise TypeError('inner exception')
    >>> fail()
    Traceback (most recent call last):
    ...
    Exception: intercepted!

    But they can also be declared and then used later on:

    >>> intercept0r = intercept({
    ...    TypeError: returns('intercepted!')
    ... })
    >>> @intercept0r
    ... def fail():
    ...     raise TypeError('raising error')
    >>> fail()
    'intercepted!'

    You can declare also an action that captures the risen exception by passing
    a callable to the action. This is useful to create a custom error message:

    >>> @intercept({
    ...    TypeError: returns(lambda e: 'intercepted {}'.format(e))
    ... })
    ... def fail():
    ...     raise TypeError('inner exception')
    >>> fail()
    'intercepted inner exception'

    Or to convert captured exceptions into custom errors:

    >>> class CustomError(Exception):
    ...     pass
    >>> @intercept({
    ...    TypeError: raises(lambda e: CustomError(e))
    ... })
    ... def fail():
    ...     raise TypeError('inner exception')
    >>> fail()
    Traceback (most recent call last):
    ...
    intercept.CustomError: inner exception
    """

    for action in actions.values():
        if type(action) is not returns and type(action) is not raises:
            raise InterceptorError('Actions must be declared as `returns` or `raises`')

    def decorated(f):
        def wrapped(*args, **kargs):
            try:
                return f(*args, **kargs)
            except Exception as e:
                if e.__class__ in actions:
                    return actions[e.__class__](e)
                else:
                    raise

        return wrapped

    return decorated


class returns:
    """
    Return action for the :class:`intercept` decorator.
    """

    def __init__(self, expression):
        self.expression = expression

    def __call__(self, e: Exception):
        if callable(self.expression):
            return self.expression(e)
        else:
            return self.expression


class raises:
    """
    Raise action for the :class:`intercept` decorator.
    """

    def __init__(self, expression):
        self.expression = expression

    def __call__(self, e: Exception):
        if callable(self.expression):
            raise self.expression(e)
        else:
            raise self.expression


class InterceptorError(Exception):
    """
    Interceptor specific error.
    """
    pass
