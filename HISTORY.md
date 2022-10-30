# History

## 0.3.0 (2022.10.30)

* Use packaging instead of distutils for version comaprison. Note that this
  might cause certain versions to fail. Notably, ``'0.1.dev3'`` is now older
  than ``'0.1'``.
* Require Python 3.8.
* New explicit dependency on ``packaging``.

## 0.2.4 (2018.08.13)
* Apparently numpydoc 0.6 didn't have a `__version__` attribute....


## 0.2.3 (2018.08.13)

* Check for numpydoc 0.7
* Fix a typo in the docstring message

## 0.2.2 (2018.08.12)

* API change. change_default_parameter now takes a dictionary for the
  old_kwargs so that parameter names don't conflict

## 0.2.1 (2018.08.12)

* Merge with other numpydocs so that documentation in Sphinx doesn't crash

## 0.2.0 (2018.08.11)

* Provide a deprecator for changing the number  of keyword only arguments.

## 0.1.1 (2018.08.09)

* Deprecated arguments appear in order for Python 3.5 as well.

## 0.1.0 (2018.08.09)

* New deprecator for changing the default value of `kwards`. Handles arguments
  passed as positional argumnets too.

## 0.0.1 (2018-07-29)

* First release on PyPi
