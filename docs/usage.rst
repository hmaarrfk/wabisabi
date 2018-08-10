=====
Usage
=====

This project is meant to be used by library developers. You are meant to
use ``functools.partial`` as a shortecuct to set things like your friendly
library name, and the current library version.

In something like your project's ``utils`` file, you should include adapted
versions of this code::

    import deprecation_factory
    from functools import partial
    from ..__init__ import __version__  # or the applicable line

    default_parameter_change = partial(default_parameter_change,
                                       current_library_version=__version__,
                                       library_name='mylib')

After this, you can use the decorators to deprecated functions how you please
