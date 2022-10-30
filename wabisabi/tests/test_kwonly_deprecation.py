from wabisabi import kwonly_change
from functools import partial
from pytest import warns, raises
import inspect
import warnings

__version__ = '0.14'
kwonly_change = partial(kwonly_change,
                        current_library_version=__version__,
                        library_name='mylib')


@kwonly_change('0.15')
def foo_easy(*, a=6):
    return a


def test_too_easy():
    assert foo_easy() == 6
    with warns(FutureWarning, match='In version 0.15'):
        assert foo_easy(3) == 3
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert foo_easy(a=7) == 7


@kwonly_change('0.15')
def foo_medium(a, b=2, *, c=6, d=2):
    return a * b * c * d


def test_foo_medium():
    with raises(TypeError, match=r'.* missing 1 required positional argument'):
        foo_medium()
    assert foo_medium(0) == 0
    with warns(FutureWarning, match='In version 0.15'):
        assert foo_medium(1, 1, 1) == 2

    with warns(FutureWarning, match='In version 0.15'):
        assert foo_medium(1, 1, 1, 1) == 1

    with warns(FutureWarning, match='In version 0.15'):
        assert foo_medium(1, 1, 1, d=1) == 1

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert foo_medium(1, d=2, c=2) == 8

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert foo_medium(1, c=2) == 8

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert foo_medium(1, 1, c=2) == 4

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert foo_medium(1, 1, d=1) == 6


def foo_hard_new(a, b=2, *, c=6, d=2):
    return a * b * c * d


def foo_hard_old(a, b=2, d=2, *, c=6):
    return a * b * c * d


foo_hard_no_sig_change = kwonly_change('0.15',
                                       previous_arg_order=['a', 'b', 'd'])(
                                           foo_hard_new)

foo_hard_sig_change = kwonly_change('0.15',
                                    previous_arg_order=['a', 'b', 'd'],
                                    keep_old_signature=True)(foo_hard_new)


def test_foo_hard():
    with raises(TypeError, match=r'.* missing 1 required positional argument'):
        foo_hard_no_sig_change()

    # Specifying d both as position and keyword only
    with raises(SyntaxError, match='In version 0.15'):
        assert foo_hard_no_sig_change(1, 1, 1, d=1) == 1

    with raises(TypeError, match=r'.* takes 3 positional arguments'):
        foo_hard_no_sig_change(1, 1, 1, 1)

    assert foo_hard_new(a=1, b=2, c=3, d=4) == \
        foo_hard_no_sig_change(a=1, b=2, c=3, d=4)


def test_foo_signature_change():
    assert inspect.signature(foo_hard_sig_change) == \
        inspect.signature(foo_hard_old)
    assert foo_hard_new(a=1, b=2, c=3, d=4) == \
        foo_hard_sig_change(a=1, b=2, c=3, d=4)


def foo_easy_already_deprecated(*, a=6):
    return a


def test_raises():
    from wabisabi import kwonly_change

    # Without a current_library_version
    with raises(ValueError):
        kwonly_change('15', library_name='mylib')(foo_easy_already_deprecated)

    # Without a library_name
    with raises(ValueError):
        kwonly_change('15', current_library_version='0.1')(
            foo_easy_already_deprecated)


def test_already_deprecated():
    foo_easy_should_not_change = kwonly_change('0.1')(
        foo_easy_already_deprecated)
    assert foo_easy_should_not_change == foo_easy_already_deprecated


@kwonly_change('0.15')
def foo_docs(a='a', *, b='b'):
    """This is foo

    Parameters
    ----------
    a: str
        This is a.

    b: str
        This is b

    """
    return a + b


def test_doc():
    assert "Warns" in foo_docs.__doc__
    assert "`b`" in foo_docs.__doc__
