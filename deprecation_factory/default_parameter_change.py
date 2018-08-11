"""
As this library is still in early development, the API might change.
I suggest you vendor this so that you don't create conflicts if other
libraries decide to use an older, incompatible version

If you are shipping python source code, then I've included the license
as part of this header to make your life easier.

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

from distutils.version import LooseVersion as Version
from functools import wraps
import inspect
import re
import textwrap

from warnings import warn


def default_parameter_change(version,
                             library_name, current_library_version,
                             **old_kwargs):
    """Deprecates a default value for a kwarg.

    If the software version is greater or equal to that of ``version``, this
    decorator returns the original function without any modifications.

    It will warn the user, pointing to the line of his code, in a single
    warning for all changes in the default parameters.

    This decorator does the following:
        - Adds a human readable message whenever the function is invoked
          without specifying the deprecated keyword argument.
        - It modifies the ``__signature__`` of the function so that signature
          reflects the default parameters.
        - Modifies the docstring so as to include a warning about the
          deprecation information compatible numpydoc.

    Parameters
    ----------
    version: version-like
        The version in which the parameter will take the new default value.
        If the software version reaches this value, the new default will be
        taken on without warning.

    library_name : str
        The human readable name for your library.

    current_library_version : version-like
        The current version of your library.

    old_kwargs:
        The keyword arguments with their old default values.

    """
    def the_decorator(func):
        if Version(current_library_version) >= version:
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
                if (new_signature.parameters[key].kind is
                        inspect._POSITIONAL_OR_KEYWORD):
                    arg_pos = func_args.index(key)
                    if len(args) > arg_pos:
                        continue

                if key in kwargs:
                    continue
                new_value = new_signature.parameters[key].default
                message = (message +
                           '    The default value of ``{argname}`` '
                           'will be changed from ``{old_value}`` to '
                           '``{new_value}``. '
                           '\n'.format(argname=key,
                                       old_value=repr(old_value),
                                       new_value=repr(new_value)))
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
        for param in old_parameters:
            key = param.name
            old_value = param.default

            new_value = new_signature.parameters[key].default
            doc_deprecated_kwargs = (
                doc_deprecated_kwargs +
                '    `{argname}` : `{old_value}` -> `{new_value}`'
                '\n\n'.format(argname=key,
                              old_value=old_value.__repr__(),
                              new_value=new_value.__repr__()))
        warnings_string = """
Warns
-----
FutureWarning
    In release {version} of {module}, this function will take on
    new values for the following keyword arguments:

""".format(version=version, module=library_name,
           funcname=func.__name__) + doc_deprecated_kwargs + """

   To avoid this warning in your code, specify the value of all listed
   keyword arguments.

"""

        parameters_line = re.search('.*Parameters$', wrapper.__doc__,
                                    flags=re.MULTILINE)
        if parameters_line is not None:
            indentation_amount = parameters_line.group().find('P')
            warnings_string = textwrap.indent(
                warnings_string, ' ' * indentation_amount)
        wrapper.__doc__ = wrapper.__doc__ + warnings_string

        return wrapper
    return the_decorator
