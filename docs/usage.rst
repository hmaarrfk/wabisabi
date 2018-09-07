=====
Usage
=====

This project is meant to be used by library developers. You are meant to
use ``functools.partial`` as a shortecuct to set things like your friendly
library name, and the current library version.

In something like your project's ``utils`` file, you should include adapted
versions of this code::

    from wabisabi import kwonly_change
    from wabisabi import default_parameter_change

    from functools import partial
    from ..__init__ import __version__  # or the applicable line

    default_parameter_change = partial(default_parameter_change,
                                       current_library_version=__version__,
                                       library_name='mylib')
    kwonly_change = partial(kwonly_change,
                            library_name='my super lib',
                            current_library_version=__version__)

After this, you can use the decorators to deprecated functions how you please
