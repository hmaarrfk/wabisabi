from deprecation_factory import default_parameter_change
from functools import partial
import warnings

from pytest import warns

__version__ = '0.14'
default_parameter_change = partial(default_parameter_change,
                                   current_library_version=__version__,
                                   library_name='mylib')


def foo(bar='hello'):
    return bar


def test_dummy():
    assert foo() == 'hello'


def test_deprecating():
    foo_0_15 = default_parameter_change('0.15', bar='bar')(foo)
    with warns(FutureWarning, match='In release 0.15 of mylib') as record:
        assert foo_0_15() == 'bar'


    assert len(record) == 1
    the_warning = record[0]
    assert 'The default value of ``bar``' in str(the_warning.message)
    assert "from ``'bar'`` to ``'hello'``" in str(the_warning.message)


def test_deprecating_param_provided():
    foo_0_15 = default_parameter_change('0.15', bar='bar')(foo)

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert foo_0_15(bar='bar23') == 'bar23'


def test_deprecated():
    foo_0_13 = default_parameter_change('0.13', bar='bar')(foo)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert foo_0_13() == 'hello'


def foo2(a, b='b', c='c'):
    return a + b + c


def test_deprecating2():
    foo2_0_15 = default_parameter_change('0.15', b='B', c='C')(foo2)
    with warns(FutureWarning, match='In release 0.15 of mylib') as record:
        assert foo2_0_15('a') == 'aBC'


    assert len(record) == 1
    the_warning = record[0]
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

    with warns(FutureWarning, match='In release 0.15 of mylib') as record:
        assert foo2_0_15('a', c='D') == 'aBD'

    assert len(record) == 1
    the_warning = record[0]

    assert 'The default value of ``b``' in str(the_warning.message)
    assert "from ``'B'`` to ``'b'``" in str(the_warning.message)

    assert 'The default value of ``c``' not in str(the_warning.message)
    assert "from ``'B'`` to ``'c'``" not in str(the_warning.message)

def test_deprecating_param_provided2():
    foo2_0_15 = default_parameter_change('0.15', b='B', c='C')(foo2)

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert foo2_0_15('a', b='X', c='Y') == 'aXY'


def test_deprecated2():
    foo2_0_13 = default_parameter_change('0.13', b='B', c='C')(foo2)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert foo2_0_13('a') == 'abc'
