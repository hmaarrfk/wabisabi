# wabisabi

[![pypi](https://img.shields.io/pypi/v/wabisabi.svg)](https://pypi.python.org/pypi/wabisabi)
[![Travis](https://img.shields.io/travis/hmaarrfk/wabisabi.svg)](https://travis-ci.org/hmaarrfk/wabisabi)
[![Docs](https://readthedocs.org/projects/wabisabi/badge/?version=latest)](https://wabisabi.readthedocs.io/en/latest/?badge=latest)


Python3 wabisabi. Automatically write boilerplate code for many kinds
of deperecations through python decorators.


  * Free software: [BSD license](LICENSE)
  * [Documentation](https://wabisabi.readthedocs.io)


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
  5. Add messages in the documentation (numpydoc compatible)

Finally, when the behaviour is official depreprecated, you need to do all these
changes again.

  6. Remove the warnings.
  7. Remove the documentation messages.
  8. Remove the old behaviour.
  9. Change the function signature back to something useful.

The goal of this library is to allow you to shortcut steps 3-9. You shouldn't
have to revisit the deprecation long after you completed implementing your new
features. You write your code how it is **supposed to look**, this library,
makes ensures your users have enough time to update their code.

This library

  * Modifies function signatures so to ensure correctness for the current
    version. This should help with autocompletions.
  * Adds a warning section to the docstrings. An attempt is made to properly
    indent the docstring.
  * Point the user to **their** line of code, so that they know where
    to make make the appropriate modification.
  * Leaving deprecators in place after the desired threshold results in a noop.
    This means that you can be lazy about ripping them out of code.
    Deprecations should not have to be blockers for your development.
  * If numpydoc > 0.7 is installed, the "Warns" sections are combined into
    a single section allowing you to chain deprecators.

## Installation

While you can depend on this, I strongly recommend you version the files you
need in your project as the API is highly likely to change and break your code.

## Current deprecators

  * Deprecator for change of default values in `kwargs`. Handles `kwargs`
    passed as positional arguments too!
  * Transitionning to keyword only arguments.

## Future deprecators

  * `kwarg` renaming
  * Swapping the order of positional arguments
  * Making an old `kwarg` a manditory positional `arg`
  * Feature requests are welcome!

## Development Lead

  * Mark Harfouche

## Contributors

Could be you!


### How to contribute
Ready to contribute? We use the standard github contribution model.
scikit-image has a great
[writeup](http://scikit-image.org/docs/dev/contribute.html) on how to setup
your environment. Adapt it for our environment.

##### Cookiecutter

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
