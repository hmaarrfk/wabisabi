from wabisabi import default_parameter_change
from functools import partial
import warnings
import inspect
import pytest
from pytest import warns


parametrize = pytest.mark.parametrize
__version__ = '0.14'
versions_above = ['0.14.1', '0.14.post0', '0.15', '1.0']
default_parameter_change = partial(default_parameter_change,
                                   current_library_version=__version__,
                                   library_name='mylib')


def foo(bar='hello'):
    return bar


def test_dummy():
    assert foo() == 'hello'


@parametrize('version_above', versions_above)
def test_deprecating(version_above):
    foo_0_15 = default_parameter_change(version_above, dict(bar='bar'))(foo)
    with warns(FutureWarning,
               match='In release {} of mylib'.format(version_above)) as record:
        assert foo_0_15() == 'bar'

    assert len(record) == 1
    the_warning = record[0]
    assert 'The default value of ``bar``' in str(the_warning.message)
    assert "from ``'bar'`` to ``'hello'``" in str(the_warning.message)


@parametrize('version_above', versions_above)
def test_deprecating_param_provided(version_above):
    foo_0_15 = default_parameter_change(version_above, dict(bar='bar'))(foo)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert foo_0_15(bar='bar23') == 'bar23'

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert foo_0_15('bar23') == 'bar23'


def test_deprecated():
    foo_0_13 = default_parameter_change('0.13', dict(bar='bar'))(foo)

    assert inspect.signature(foo) == inspect.signature(foo_0_13)
    assert foo == foo_0_13
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert foo_0_13() == 'hello'


def foo2(a, b='b', c='c'):
    return a + b + c


foo2_0_15 = default_parameter_change('0.15', dict(b='B', c='C'))(foo2)
foo2_0_13 = default_parameter_change('0.13', dict(b='B', c='C'))(foo2)


def test_deprecating2():
    with warns(FutureWarning, match='In release 0.15 of mylib') as record:
        # Be careful adding code between these two
        expeccted_warning_lineno = inspect.currentframe().f_lineno + 1
        assert foo2_0_15('a') == 'aBC'

    assert len(record) == 1
    the_warning = record[0]
    assert expeccted_warning_lineno == the_warning.lineno
    assert 'The default value of ``b``' in str(the_warning.message)
    assert "from ``'B'`` to ``'b'``" in str(the_warning.message)

    assert 'The default value of ``c``' in str(the_warning.message)
    assert "from ``'C'`` to ``'c'``" in str(the_warning.message)

    with warns(FutureWarning, match='In release 0.15 of mylib') as record:
        assert foo2_0_15('a', b='D') == 'aDC'

    assert len(record) == 1
    the_warning = record[0]

    assert 'The default value of ``b``' not in str(the_warning.message)
    assert "from ``'B'`` to ``'c'``" not in str(the_warning.message)

    assert 'The default value of ``c``' in str(the_warning.message)
    assert "from ``'C'`` to ``'c'``" in str(the_warning.message)

    # Positional argument
    with warns(FutureWarning, match='In release 0.15 of mylib') as record:
        assert foo2_0_15('a', 'D') == 'aDC'

    assert len(record) == 1
    the_warning = record[0]

    assert 'The default value of ``b``' not in str(the_warning.message)
    assert "from ``'B'`` to ``'c'``" not in str(the_warning.message)

    assert 'The default value of ``c``' in str(the_warning.message)
    assert "from ``'C'`` to ``'c'``" in str(the_warning.message)

    with warns(FutureWarning, match='In release 0.15 of mylib') as record:
        assert foo2_0_15('a', c='D') == 'aBD'

    assert len(record) == 1
    the_warning = record[0]

    assert 'The default value of ``b``' in str(the_warning.message)
    assert "from ``'B'`` to ``'b'``" in str(the_warning.message)

    assert 'The default value of ``c``' not in str(the_warning.message)
    assert "from ``'B'`` to ``'c'``" not in str(the_warning.message)


def test_deprecating_param_provided2():
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert foo2_0_15('a', b='X', c='Y') == 'aXY'

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert foo2_0_15('a', 'X', 'Y') == 'aXY'


def test_deprecated2():
    assert inspect.signature(foo2) == inspect.signature(foo2_0_13)
    assert foo2 == foo2_0_13
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert foo2_0_13('a') == 'abc'


def test_foo2_signature():
    sig_15 = inspect.signature(foo2_0_15)
    assert sig_15.parameters['b'].default == 'B'
    assert sig_15.parameters['c'].default == 'C'

    sig_13 = inspect.signature(foo2_0_13)
    assert sig_13.parameters['b'].default == 'b'
    assert sig_13.parameters['c'].default == 'c'


def foo_with_docs(bar='hello', zip='zap'):
    """This is a function foo!

    It has some docs, isn't this cool!

    Parameters
    ----------
    bar: str
        This is a parameter.

    """
    return bar


# Something needs to use the decorator syntax or I might make
# a tool that can't be used the way I want it to.
@default_parameter_change('0.15', dict(bar='world'))
def foo_with_docs_15(bar='hello', zip='zap'):
    """This is a function foo!

    It has some docs, isn't this cool!

    Parameters
    ----------
    bar: str
        This is a parameter.

    """
    return bar


foo_with_docs_13 = default_parameter_change('0.13', dict(bar='world'))(
    foo_with_docs)


def test_foo_docs():
    assert 'Warns' in foo_with_docs_15.__doc__
    assert 'FutureWarning' in foo_with_docs_15.__doc__
    assert "`bar` : `'world'` -> `'hello'`" in foo_with_docs_15.__doc__
    assert "zip" not in foo_with_docs_15.__doc__

    assert foo_with_docs_13.__doc__ == foo_with_docs.__doc__

    with warns(FutureWarning, match='In release 0.15 of mylib'):
        assert foo_with_docs_15() == 'world'
    assert foo_with_docs() == 'hello'


def foo2_with_docs(bar='hello', baz='world'):
    """This is a function foo!

    It has some docs, isn't this cool!

    Parameters
    ----------
    bar: str
        This is a parameter.

    """
    return bar + ' ' + baz


foo2_with_docs_15 = default_parameter_change(
    '0.15', dict(bar='bonjour', baz='monde'))(foo2_with_docs)
foo2_with_docs_13 = default_parameter_change(
    '0.13', dict(bar='bonjour', baz='monde'))(foo2_with_docs)


def test_foo2_docs():
    assert 'Warns' in foo2_with_docs_15.__doc__
    assert 'FutureWarning' in foo2_with_docs_15.__doc__
    assert "`bar` : `'bonjour'` -> `'hello'`" in foo2_with_docs_15.__doc__
    assert "`baz` : `'monde'` -> `'world'`" in foo2_with_docs_15.__doc__
    assert foo2_with_docs_13.__doc__ == foo2_with_docs.__doc__

    with warns(FutureWarning, match='In release 0.15 of mylib'):
        assert foo2_with_docs_15() == 'bonjour monde'
    assert foo2_with_docs_13() == 'hello world'
