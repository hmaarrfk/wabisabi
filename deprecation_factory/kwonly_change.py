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

POSITIONAL_OR_KEYWORD = inspect.Parameter.POSITIONAL_OR_KEYWORD


def kwonly_change(version,
                  library_name, current_library_version,
                  previous_nargs=None, keep_old_signature=False):

    def the_decorator(func):
        if Version(current_library_version) >= version:
            return func
        new_signature = inspect.signature(func)

        new_arg_names = [name for name in new_signature.parameters]

        if previous_nargs is None:
            old_nargs = len(new_signature.parameters)
        else:
            old_nargs = previous_nargs

        # These arguments are still required as argument only keywords
        func_args = inspect.getfullargspec(func).args
        new_nargs = len(func_args)

        old_parameters = []
        for key, param in new_signature.parameters.items():
            index = new_arg_names.index(key)
            if key in func_args:
                kind = param.kind
            elif index >= old_nargs:
                kind = param.kind
            else:
                kind = POSITIONAL_OR_KEYWORD
            old_parameters.append(
                inspect.Parameter(key, kind, default=param.default))

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
                new_kwargs = {key: value
                              for key, value in zip(new_arg_names[new_nargs:],
                                                    args[new_nargs:])}
                args = args[:new_nargs]
                kwargs.update(new_kwargs)

                warn("Whoa!", FutureWarning, stacklevel=2)
            return func(*args, **kwargs)

        if keep_old_signature:
            wrapper.__signature__ = old_signature
        return wrapper
    return the_decorator
