"""Example of how to use the deprecaction factory in your own library.

As a developer, you should inspect the source of this file.

Look at the doc page to see how your users would see your documetnation.

I assume that this package has a version number '0.14'
"""

from deprecation_factory import default_parameter_change
import functools


# In your own library's testing module, you should simply use
# functools.partial to set the library version and name.
default_parameter_change = functools.partial(default_parameter_change,
                                             library_name='my super lib',
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


@default_parameter_change('0.16', this='tim')
def foo_deprecated(this='that'):
    """Prints your parameter.

    **This function has a depeprecation decorator set to '0.16'**

    Parameters
    ----------
    this : str
        This is the string parameter that should be printed

    """
    print(this)


@default_parameter_change('0.13', this='tim')
def foo_deprecated_13(this='that'):
    """Prints your parameter

    **This function has a deprecation decorator set to '0.13'.**

    Parameters
    ----------
    this : str
        This is the string parameter that should be printed.

    """
    print(this)


if __name__ == '__main__':
    foo_deprecated()
