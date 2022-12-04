import SOUP.Serpent2InputWriter
import SOUP.Serpent2InputParser
# import SOUP.MultipleOutputReader
from SOUP import nuclides

__all__ = [
    "Serpent2InputWriter",
    "Serpent2InputParser",
    "nuclides"
]

__doc__ = """
Usage:
"""

# when changing version also adapt the default string in the input.py file
__version__ = '0.0.1'


class SOUPException(Exception):
    pass
