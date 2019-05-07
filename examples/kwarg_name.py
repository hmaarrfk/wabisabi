"""
Keyword only deprecation
------------------------

This is how the docstrings will appear if you decide to deprecate positional
arguments to keyword.

"""

from wabisabi import kwonly_change
import functools


# In your own library's testing module, you should simply use
# functools.partial to set the library version and name.
kwarg_name_change = functools.partial(kwarg_name_change,
                                      library_name='my super lib',
                                      current_library_version='0.14')


def foo_old(zap='zip', bar='hello', baz='world'):
    """Adds bar and baz

    Parameters
    ----------
    bar: str
        a string

    baz: str
        an other python object.

    zap: str
        zaps everything to dust

    Returns
    -------
    result: str
        the sum of the zapping.

    """
    return zap + bar + baz


@kwarg_name_change('0.15', {'bar': 'foo'})
def foo_new(zap='zip', foo='hello', baz='world'):
    """Adds bar and baz

    **The decorator will infer the old order of the paramters.**

    Parameters
    ----------
    foo: str
        a string

    baz: str
        an other python object.

    zap: str
        zaps everything to dust

    Returns
    -------
    result: str
        the sum of the zapping.

    """
    return zap + foo + baz


@kwarg_name_change('0.15', {'baz': 'foo', 'bar': 'wap'})
def foo_new_swap_arguments(zap='zip', *, foo='world', wap='hello'):
    """Adds bar and baz

    **You can even swap the order of the arguments, though you should
    specify how they were ordered.**

    Parameters
    ----------
    foo: str
        a string

    wap: str
        an other python object.

    zap: str
        zaps everything to dust

    Returns
    -------
    result: str
        the sum of the zapping.

    """
    return zap + foo + wap
