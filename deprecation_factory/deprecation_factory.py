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

    old_kwargs:
        The keyword arguments with their old default values.

    """
    def the_decorator(func):
        if Version(current_library_version) >= version:
            return func

        new_signature = inspect.signature(func)
        funcname = func.__name__
        base_message = ('In release {version} of {module}, the function '
                        '``{funcname}`` '
                        'will have new default parameters. To avoid this '
                        'warning specify the value of all listed arguments.'
                        '\n\n'.format(version=version, module=library_name,
                                      funcname=funcname))

        old_parameters = [
            inspect.Parameter(
                key, new_signature.parameters[key].kind,
                default=new_signature.parameters[key].default
                if key not in old_kwargs else old_kwargs[key])
            for key in new_signature.parameters]

        old_signature = new_signature.replace(parameters=old_parameters)

        @wraps(func)
        def wrapper(*args, **kwargs):
            issue_warning = False
            message = base_message
            for key, old_value in old_kwargs.items():
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
        for key, old_value in old_kwargs.items():
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
           funcname=funcname) + doc_deprecated_kwargs + """

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
