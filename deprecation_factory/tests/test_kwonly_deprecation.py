from deprecation_factory import kwonly_change
from functools import partial
from pytest import warns, raises
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
    with warns(FutureWarning, match='Whoa!'):
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
    with warns(FutureWarning, match='Whoa!'):
        assert foo_medium(1, 1, 1) == 2

    with warns(FutureWarning, match='Whoa!'):
        assert foo_medium(1, 1, 1, 1) == 1

    with warns(FutureWarning, match='Whoa!'):
        assert foo_medium(1, 1, 1, d=1) == 1

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert foo_medium(1, d=2, c=2) == 8


@kwonly_change('0.15', previous_nargs=3)
def foo_hard(a, b=2, *, c=6, d=2):
    return a * b * c * d


def test_foo_hard():
    with raises(TypeError, match=r'.* missing 1 required positional argument'):
        foo_hard()
    with warns(FutureWarning, match='Whoa!'):
        assert foo_hard(1, 1, 1, d=1) == 1

    with raises(TypeError, match=r'.* takes 3 positional arguments'):
        foo_hard(1, 1, 1, 1)
