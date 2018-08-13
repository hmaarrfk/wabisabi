"""
Argument default value
----------------------

One important advantage of using these decorators is that they ensure that the
docstrings are correct. This module has as hypothetical version number of
``0.14``. Click on the source links to see what the source looks like for each
of these functions.

Look at the doc page to see how your users would see your documetnation.

"""

from deprecation_factory import default_parameter_change
import functools


# In your own library's testing module, you should simply use
# functools.partial to set the library version and name.
default_parameter_change = functools.partial(
    default_parameter_change, library_name='my super lib',
    current_library_version='0.14')


def foo(this='that'):
    """Prints your parameter.

    **This function has no deprecation decorator.**

    Parameters
    ----------
    this : str
        This is the string parameter that should be printed

    """
    print(this)


@default_parameter_change('0.16', dict(this='tim'))
def foo_deprecated(two=2, this='that', one=1):
    """Prints your parameter.

    **This function has a depeprecation decorator set to '0.16'**

    Parameters
    ----------
    this : str
        This is the string parameter that should be printed

    """
    print(this)


@default_parameter_change('0.13', dict(this='tim'))
def foo_deprecated_13(this='that'):
    """Prints your parameter

    **This function has a deprecation decorator set to '0.13'.**

    Parameters
    ----------
    this : str
        This is the string parameter that should be printed.

    """
    print(this)


@default_parameter_change('0.16', dict(bar='bonjour', baz='monde'))
def foo_two_params_deprecating(bar='hello', baz='world'):
    """Joins two strings with a space between them.

    **This function has a deprecation decorator set to '0.16'.**

    Parameters
    ----------
    bar : str
        The first word to join.

    baz : str
        The second word to join.

    """
    return bar + ' ' + baz


def foo_two_params(bar='hello', baz='world'):
    """Joins two strings with a space between them.

    **This function has a no deprecation decorator.**

    Parameters
    ----------
    bar : str
        The first word to join.

    baz : str
        The second word to join.

    """
    return bar + ' ' + baz


@default_parameter_change('0.17', dict(baz='monde'))
@default_parameter_change('0.16', dict(bar='bonjour'))
def foo_two_params_redux(bar='hello', baz='world'):
    """Joins two strings with a space between them.

    **This function has a no deprecation decorator.**

    Parameters
    ----------
    bar : str
        The first word to join.

    baz : str
        The second word to join.

    """
    return bar + ' ' + baz


if __name__ == '__main__':
    foo_deprecated()
