__author__ = """Mark Harfouche"""
__email__ = 'mark.harfouche@gmail.com'
from .deprecation_factory import default_parameter_change

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
