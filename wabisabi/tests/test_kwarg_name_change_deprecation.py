from wabisabi import kwarg_name_change
from functools import partial
from pytest import warns, raises
import warnings

__version__ = '0.14'
kwarg_name_change = partial(kwarg_name_change,
                            current_library_version=__version__,
                            library_name='mylib')


@kwarg_name_change('0.15', {'b': 'a'})
def foo_easy(*, a=6):
    return a


def test_too_easy():
    assert foo_easy() == 6
    with warns(FutureWarning, match='In version 0.15'):
        assert foo_easy(b=3) == 3
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert foo_easy(a=7) == 7


def test_too_easy_doubly_specified():
    with warns(FutureWarning, match='In version 0.15'):
        with raises(TypeError,
                    match="'b' and 'a' refer to the same parameter."):
            foo_easy(b=1, a=6)

        with raises(TypeError,
                    match="'b' and 'a' refer to the same parameter."):
            foo_easy(a=6, b=1)


@kwarg_name_change('0.15', {'baz': 'b', 'dare': 'd'})
def foo_medium(a, b=2, *, c=6, d=2):
    return a * b * c * d


def test_foo_medium():
    with raises(TypeError, match=r'missing 1 required positional argument'):
        foo_medium()
    assert foo_medium(0) == 0
    with warnings.catch_warnings():
        # renamed kwargs can still be specified as positional arguments
        warnings.simplefilter("error")
        assert foo_medium(1, 1, c=1) == 2

    # Old kwargs give warnings
    with warns(FutureWarning, match='In version 0.15'):
        assert foo_medium(1, baz=1, c=1, dare=1) == 1
    with warns(FutureWarning, match='In version 0.15'):
        assert foo_medium(1, b=1, c=1, dare=1) == 1
    with warns(FutureWarning, match='In version 0.15'):
        assert foo_medium(1, baz=1, c=1, d=1) == 1

    with warnings.catch_warnings():
        # renamed kwargs can still be specified as positional arguments
        warnings.simplefilter("error")
        assert foo_medium(1, b=1, c=1, d=1) == 1

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


def foo_easy_already_deprecated(*, a=6):
    return a


def test_raises():
    from wabisabi import kwarg_name_change

    # Without a current_library_version
    with raises(ValueError):
        kwarg_name_change('15', library_name='m')(foo_easy_already_deprecated)

    # Without a library_name
    with raises(ValueError):
        kwarg_name_change('15', current_library_version='0.1')(
            foo_easy_already_deprecated)


def test_already_deprecated():
    foo_easy_should_not_change = kwarg_name_change('0.1', {'bar': 'a'})(
        foo_easy_already_deprecated)
    assert foo_easy_should_not_change == foo_easy_already_deprecated


@kwarg_name_change('0.15', {'bar': 'b'})
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
    assert "'b' refers to the old keyword argument 'bar'" in foo_docs.__doc__
