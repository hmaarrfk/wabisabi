"""
As this library is still in early development, the API might change.
I suggest you vendor this so that you don't create conflicts if other
libraries decide to use an older, incompatible version

If you are shipping python source code, then I've included the license
at the bottom of this file to make your life easier.
"""

from packaging.version import Version
from functools import wraps
import inspect
from warnings import warn
from .merge_docstrings import merge_docstrings

POSITIONAL_OR_KEYWORD = inspect.Parameter.POSITIONAL_OR_KEYWORD


# Keep the order of params as is,
# `previous_arg_order` and `keep_old_signature`
# should be optional positional args.
def kwonly_change(version, previous_arg_order=None, keep_old_signature=False,
                  library_name=None, current_library_version=None):
    """Returns a decorator that enforces a smaller number of positional arguments.

    If the current library version is smaller than version in which the new
    signature takes effect, this deprecator will:

    Issue a warnign pointing to the user's code if they call a function with
    too many positional arguments.

    If you want to move the new keyword only arguments after the keyword
    only seperator, you should specify a list with the previous order of
    arguments as the parameter ``previous_arg_order``. If this parameter is
    not specified, it is assumed that the previous function signature allowed
    all parameters to be specified as either positional or keyword arguments.

    Parameters
    ----------
    version: version-like
        Version in which the new function signature takes full effect.

    previous_arg_order: list of strings or ``None``
        If the function previously had keyword only arguments, you should use
        this to specify the names of previous positional arguments. If set
        to none, it is assumed that the previous version of the function
        would accept all parameters as positional or keyword arguments.
        Specifying this also allows you to re-order the new keyword only.
        To re-iterate, you cannot swap the order of positional arguments with
        this deprecator.

    keep_old_signature: bool
        If set to true, the signature will reflect the previous signature of
        the function. This is not recommended since showing new users the
        keyword-only version of the signature will not cause them to write
        wrong code. If they follow the new signature, their code will be
        correct and they will avoid the ``FutureWarning``.

    library_name: str
        Friendly library name to include in warning messages

    current_library_version: version-like
        The current version of the shipped library (typically your module's
        ``__version__``).

    Examples
    --------

    >>> from wabisabi import kwonly_change
    >>> import functools
    >>>
    >>> kwonly_change = functools.partial(kwonly_change,
    ...                                   library_name='my super lib',
    ...                                   current_library_version='0.14')
    >>> @kwonly_change('0.15')
    ... def foo_new(zap='zip', *, bar='hello', baz='world'):
    ...     return zap + bar + baz

    """
    if current_library_version is None:
        raise ValueError('Must provide a version for your library.')

    if library_name is None:
        raise ValueError('You must provide a user friendly name for your '
                         'library.')

    def the_decorator(func):
        if Version(current_library_version) >= Version(version):
            return func
        new_signature = inspect.signature(func)

        new_arg_names = [name for name in new_signature.parameters]

        if previous_arg_order is None:
            old_nargs = len(new_signature.parameters)
            old_arg_names = new_arg_names[:old_nargs]
        else:
            old_nargs = len(previous_arg_order)
            old_arg_names = previous_arg_order
        # These arguments are still required as argument only keywords
        func_args = inspect.getfullargspec(func).args
        new_nargs = len(func_args)

        old_parameters = []
        all_params = {**new_signature.parameters}
        for key in old_arg_names:
            param = all_params.pop(key)
            if key in func_args:
                kind = param.kind
            else:
                kind = POSITIONAL_OR_KEYWORD

            old_parameters.append(
                inspect.Parameter(key, kind=kind,
                                  default=param.default,
                                  annotation=param.annotation))
        for key, param in all_params.items():
            old_parameters.append(
                inspect.Parameter(key, kind=param.kind,
                                  default=param.default,
                                  annotation=param.annotation))

        old_signature = new_signature.replace(parameters=old_parameters)

        @wraps(func)
        def wrapper(*args, **kwargs):

            if len(args) > old_nargs:
                # The warning should be issued here too!
                raise TypeError('{name}() takes {old_nargs} positional '
                                'arguments but {len_args} were given'
                                ''.format(name=func.__name__,
                                          old_nargs=old_nargs,
                                          len_args=len(args)))

            if len(args) > new_nargs:
                for key, value in zip(old_arg_names[new_nargs:len(args)],
                                      args[new_nargs:]):
                    if key in kwargs:
                        calling_function = inspect.stack()[1]

                        s = SyntaxError(
                            "In version {version} of {library_name}, the "
                            "argument ('{key}') has "
                            "will become a keyword only argument. You "
                            "specified it as both a positional argument and "
                            "a keyword argument."
                            "".format(version=version,
                                      library_name=library_name,
                                      key=key))
                        s.lineno = calling_function.lineno
                        s.filename = calling_function.filename
                        # Even the normal syntax errors suck at telling you
                        # the position of your error whe a statement spans
                        # multiple lines
                        # s.offset =  # is it worth it to find where?
                        raise s
                    kwargs[key] = value

                warn("In version {version} of {library_name}, the "
                     "argument(s): '{old_pos_args}' will become keyword-only "
                     "argument(s). To suppress this warning, specify all "
                     "listed argument(s) with keywords."
                     "".format(
                         version=version, library_name=library_name,
                         old_pos_args=old_arg_names[new_nargs:len(args)]),
                     FutureWarning, stacklevel=2)

                args = args[:new_nargs]

            return func(*args, **kwargs)

        if keep_old_signature:
            wrapper.__signature__ = old_signature

        # only add a docstring if they had one already
        if wrapper.__doc__ is None:
            return wrapper

        args = ', '.join(old_arg_names[new_nargs:])
        warnings_string = f"""
Warns
-----
FutureWarning
  In release {version} of {library_name}, the argument(s):

    `{args}`

  will become keyword-only arguments. To avoid this warning,
  provide all the above arguments as keyword arguments.

"""
        wrapper.__doc__ = merge_docstrings(wrapper, warnings_string)
        return wrapper
    return the_decorator


"""
BSD 3-Clause License

Copyright (c) 2018, Mark Harfouche
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
