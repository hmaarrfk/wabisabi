"""
Keyword only deprecation
------------------------

This is how the docstrings will appear if you decide to deprecate positional
arguments to keyword.

"""

from deprecation_factory import kwonly_change
import functools


# In your own library's testing module, you should simply use
# functools.partial to set the library version and name.
kwonly_change = functools.partial(kwonly_change,
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


@kwonly_change('0.15')
def foo_new(zap='zip', *, bar='hello', baz='world'):
    """Adds bar and baz

    **The decorator will infer the old order of the paramters.**

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


@kwonly_change('0.15', keep_old_signature=True)
def foo_new_keep_signature(zap='zip', *, bar='hello', baz='world'):
    """Adds bar and baz

    **You can choose to keep the old signature.**

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


@kwonly_change('0.15', previous_arg_order=['zap', 'bar', 'baz'])
def foo_new_swap_arguments(zap='zip', *, baz='world', bar='hello'):
    """Adds bar and baz

    **You can even swap the order of the arguments, though you should
    specify how they were ordered.**

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
