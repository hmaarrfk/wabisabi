# Deprecation Factory

[![pypi](https://img.shields.io/pypi/v/deprecation_factory.svg)](https://pypi.python.org/pypi/deprecation_factory)
[![Travis](https://img.shields.io/travis/hmaarrfk/deprecation_factory.svg)](https://travis-ci.org/hmaarrfk/deprecation_factory)
[![Docs](https://readthedocs.org/projects/deprecation-factory/badge/?version=latest)](https://deprecation-factory.readthedocs.io/en/latest/?badge=latest)


Python3 deprecation factory. Automatically write boilerplate code for many kinds
of deperecations through python decorators.


  * Free software: [BSD license](LICENSE)
  * [Documentation](https://deprecation-factory.readthedocs.io)


## Motivations
Breaking things is important! Breaking other's things is just mean!

The goal of deprecations is to warn other library writers that their code is
about to break so you can keep making agressive changes to your own.

Often when you want to deprecate a feature, you end up following a procedure
similar to

  1. Make the useful modification to your code.
  2. Decide on when the old behaviour should be switched over.
  3. Add warnings INSIDE your function to warn users.
  4. Change the function signature to something non-sensical to detect the
     default behaviour.
  5. Add messages in the documentation.

Finally, when the behaviour is official depreprecated, you need to do all these
changes again.

  6. Remove the warnings.
  7. Remove the documentation messages.
  8. Remove the old behaviour.
  9. Change the function signature back to something useful.

The goal of this library is to allow you to shortcut steps 3-9. You shouldn't
have to revisit the deprecation long after you completed implementing your new
features

This library modifies function signatures and docstrings to make the current
version of the function appear in autocompletions and on the automatically
generated documentation.

The library will point the user to **their** line of code, so that they can
make the appropriate modifications.

It is even safe to leave the deprecators in place after the threshold version
has been reached. The decorator will behave as a no-op and your library will
use the updated version of your code. Deprecations should not have to be
blockers for your development.


## Current deprecators

  * Deprecator for change of default values in `kwargs`. Handles `kwargs`
    passed as positional arguments too!

## Future deprecators

  * Transitionning to keyword only arguments.
  * Swapping the order of positional arguments
  * Making an old `kwarg` a manditory positional `arg`
  * Feature requests are welcome!

## Other directions

  * Input sanitization.

## Development Lead

  * Mark Harfouche

## Contributors

None yet. Why not be the first?


### How to contribute
Ready to contribute? We use the standard github contribution model.
Scikit-Image has a great
[writeup](http://scikit-image.org/docs/dev/contribute.html) on how to setup
your environment. Adapt it for our environment.

##### Cookiecutter

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
