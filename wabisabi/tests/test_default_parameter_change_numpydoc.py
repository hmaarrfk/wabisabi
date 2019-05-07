import pytest
from wabisabi import default_parameter_change
from functools import partial
from pytest import warns


pytest.importorskip('numpydoc')

from numpydoc.docscrape import FunctionDoc  # noqa

__version__ = '0.14'
default_parameter_change = partial(default_parameter_change,
                                   current_library_version=__version__,
                                   library_name='mylib')


def foo_with_docs(bar='hello'):
    """This is a function foo!

    It has some docs, isn't this cool!

    Parameters
    ----------
    bar: str
        This is a parameter.

    """
    return bar


foo_with_docs_15 = default_parameter_change('0.15',
                                            dict(bar='world'))(foo_with_docs)
foo_with_docs_13 = default_parameter_change('0.13',
                                            dict(bar='world'))(foo_with_docs)


def test_foo_docs():
    assert 'Warns' in foo_with_docs_15.__doc__
    docs = FunctionDoc(foo_with_docs_15)
    assert 'Warns' in docs
    assert 'FutureWarning' == docs['Warns'][0].type
    assert "`bar` : `'world'` -> `'hello'`" in '\n'.join(docs['Warns'][0][2])

    assert foo_with_docs_13.__doc__ == foo_with_docs.__doc__

    with warns(FutureWarning, match='In release 0.15 of mylib'):
        assert foo_with_docs_15() == 'world'


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
    docs = FunctionDoc(foo2_with_docs_15)
    assert 'Warns' in docs
    assert 'FutureWarning' == docs['Warns'][0].type
    assert "`bar` : `'bonjour'` -> `'hello'`" in '\n'.join(docs['Warns'][0][2])
    assert "`baz` : `'monde'` -> `'world'`" in '\n'.join(docs['Warns'][0][2])
    assert "`'hello'`\n\n  `baz`" in '\n'.join(docs['Warns'][0][2])
    assert foo2_with_docs_13.__doc__ == foo2_with_docs.__doc__

    with warns(FutureWarning, match='In release 0.15 of mylib'):
        assert foo2_with_docs_15() == 'bonjour monde'
    assert foo2_with_docs_13() == 'hello world'
