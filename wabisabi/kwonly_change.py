"""
As this library is still in early development, the API might change.
I suggest you vendor this so that you don't create conflicts if other
libraries decide to use an older, incompatible version

If you are shipping python source code, then I've included the license
at the bottom of this file to make your life easier.
"""

from warnings import warn
from .update_keyword_only import update_keyword_only


def kwonly_change(version, previous_arg_order=None, keep_old_signature=False,
                  library_name=None, current_library_version=None):
    warn("The function kwonly_change has changed to update_keyword_only",
         FutureWarning, stacklevel=2)

    return update_keyword_only(
        until_version=version,
        previous_arg_order=previous_arg_order,
        keep_old_signature=keep_old_signature,
        library_name=library_name,
        current_library_version=current_library_version)
