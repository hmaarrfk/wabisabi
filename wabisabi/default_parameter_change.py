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


def default_parameter_change(version, old_kwargs,
                             library_name, current_library_version):
    """Deprecates a default value for a kwarg.

    If the software version is greater or equal to that of ``version``, this
    decorator returns the original function without any modifications.

    If the user doesn't specify a parameter that will change default values,
    it will issue a ``FutureWarning`` pointing to the line of his code,
    in a single warning for all changes in the default parameters.


    It also modifies the ``__signature__`` of the function so that the
    function appears to have the default parameters to whatever the default
    values are in the current version of the function.

    Finally, if a docstring is provided, it appends a warning
    message compatible numpydoc.

    Parameters
    ----------
    version: version-like
        The version in which the parameter will take the new default value.
        If the software version reaches this value, the new default will be
        taken on without warning.

    old_kwargs:
        The list of keyword arguments, with their old default values
        specified, as a dictionary. You should be able to
        copy paste your old keyword arguments and put then in a `dict`.

    library_name : str
        The human readable name for your library.

    current_library_version : version-like
        The current version of your library.

    Examples
    --------
    >>> @default_parameter_change('0.16', doc(this='tim'))
    ... def foo(this='foo', bar='zip'):
    ...     '''Prints your parameter.
    ...
    ...     **This function has a depeprecation decorator set to '0.16'**
    ...
    ...     Parameters
    ...     ----------
    ...     this : str
    ...         This is the string parameter that should be printed
    ...
    ...     '''
    ...     print(bar)
    ...     return this

    """
    def the_decorator(func):
        if Version(current_library_version) >= Version(version):
            return func

        new_signature = inspect.signature(func)
        base_message = ('In release {version} of {module}, the function '
                        '``{funcname}`` '
                        'will have new default parameters. To avoid this '
                        'warning specify the value of all listed arguments.'
                        '\n\n'.format(version=version, module=library_name,
                                      funcname=func.__name__))

        old_parameters = [
            inspect.Parameter(
                key, param.kind,
                default=param.default
                if key not in old_kwargs else old_kwargs[key])
            for key, param in new_signature.parameters.items()]
        func_args = inspect.getfullargspec(func).args
        old_signature = new_signature.replace(parameters=old_parameters)

        @wraps(func)
        def wrapper(*args, **kwargs):
            issue_warning = False
            message = base_message
            for key, old_value in old_kwargs.items():
                # Check if the argument was provided as a
                # positional argument
                if (new_signature.parameters[key].kind is
                        inspect._POSITIONAL_OR_KEYWORD):
                    arg_pos = func_args.index(key)
                    if len(args) > arg_pos:
                        continue

                # check if it was provided as a kwarg
                if key in kwargs:
                    continue
                new_value = new_signature.parameters[key].default
                message = (
                    f'{message}    The default value of ``{key}`` '
                    f'will be changed from ``{repr(old_value)}`` to '
                    f'``{repr(new_value)}``. '
                    '\n'
                )
                kwargs[key] = old_value
                issue_warning = True
            if issue_warning:
                warn(message, FutureWarning, stacklevel=2)

            return func(*args, **kwargs)

        wrapper.__signature__ = old_signature

        # If the wrapper doesn't have a doc string, don't bother adding one.
        if wrapper.__doc__ is None:
            return wrapper

        doc_deprecated_kwargs = ''
        # Iterating through a list is tedius, though it is the only way to
        # ensure things stay in order in python <=3.6
        for param in old_parameters:
            key = param.name
            if key not in old_kwargs:
                continue
            old_value = param.default
            new_value = new_signature.parameters[key].default
            doc_deprecated_kwargs = (
                f'{doc_deprecated_kwargs}    `{key}` : '
                f'`{repr(old_value)}` -> `{repr(new_value)}`'
                '\n\n'
            )
        warnings_string = f"""
Warns
-----
FutureWarning
  In release {version} of {library_name}, this function will take on
  new default value(s) for the following keyword argument(s):

""" + doc_deprecated_kwargs + """

  To avoid this warning in your code, specify the value of all listed
  keyword arguments.

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
