__author__ = """Mark Harfouche"""
__email__ = 'mark.harfouche@gmail.com'
from .default_parameter_change import default_parameter_change
from .kwonly_change import kwonly_change
from .kwarg_name_change import kwarg_name_change

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
