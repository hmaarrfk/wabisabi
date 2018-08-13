import re
import textwrap


def merge_docstrings(func, additional_doc):
    try:
        from .docscrape import FunctionDoc, NumpyDocString

        func_docs = FunctionDoc(func)
        additional_doc = NumpyDocString(additional_doc)
        final_docs = func_docs + additional_doc

        return str(final_docs)
    except ImportError:
        return func.__doc__ + guess_indentation(func.__doc__,
                                                additional_doc)


def guess_indentation(function_doc, additional_doc):
    # Not use anymomre, but this was the little logic I used to guess the
    # indentation amount. I think using numpydoc's str function is better.
    parameters_line = re.search('.*Parameters$', function_doc,
                                flags=re.MULTILINE)
    if parameters_line is not None:
        indentation_amount = parameters_line.group().find('P')
        additional_doc = textwrap.indent(
            additional_doc, ' ' * indentation_amount)
    return additional_doc
