from expects import *

import doctest

import intercept as mod
from intercept import intercept, returns, raises, InterceptorError


with description('Interceptor decorator'):

    with context('Doc Tests'):

        with it('runs ok'):
            failed, tested = doctest.testmod(mod)
            expect(failed).to(equal(0))

    with context('Actions'):

        with it('returns works with basic types'):
            a_returns = returns(None)
            expect(a_returns('some exception')).to(equal(None))
            a_returns = returns(43)
            expect(a_returns('some exception')).to(equal(43))
            a_returns = returns('abc')
            expect(a_returns('some exception')).to(equal('abc'))

        with it('raises works with exceptions'):
            a_raises = raises(TypeError)
            expect(lambda: a_raises('some exception')).to(raise_error(TypeError))

        with it('returns works with callables'):
            a_returns = returns(lambda e: 'a_value')
            expect(a_returns('some exception')).to(equal('a_value'))

        with it('raises works with callables'):
            a_raises = raises(lambda e: TypeError)
            expect(lambda: a_raises('some exception')).to(raise_error(TypeError))

    with context('Decorator'):

        with it('fails when an unexpected action is declared'):
            expect(lambda: intercept({
                TypeError: 'bad action'
            })).to(raise_error(InterceptorError))

        with it('bypasses when nothing is passed'):
            an_interceptor = intercept({})

            expect(an_interceptor(
                lambda: _test_raise(TypeError('should not intercept')))
            ).to(raise_error(TypeError, 'should not intercept'))

        with it('bypasses when something not declared happens'):
            an_interceptor = intercept({
                TypeError: returns(None)
            })

            expect(an_interceptor(
                lambda: _test_raise(AttributeError('should not intercept')))
            ).to(raise_error(AttributeError, 'should not intercept'))

        with it('intercepts and returns'):
            an_interceptor = intercept({
                TypeError: returns('intercepted!')
            })

            expect(an_interceptor(
                lambda: _test_raise(TypeError)
            )()).to(equal('intercepted!'))

        with it('intercepts and raises'):
            class InterceptedError(Exception):
                pass

            an_interceptor = intercept({
                TypeError: raises(InterceptedError)
            })

            expect(an_interceptor(
                lambda: _test_raise(TypeError)
            )).to(raise_error(InterceptedError))


def _test_raise(e: Exception):
    raise e
