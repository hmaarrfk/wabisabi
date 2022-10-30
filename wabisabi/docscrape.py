import numpydoc
from packaging.version import Version
from numpydoc.docscrape import FunctionDoc as _FunctionDoc
from numpydoc.docscrape import NumpyDocString  # noqa

try:
    if Version(numpydoc.__version__) < Version('0.7'):
        raise ImportError('numpydoc mangling requires numpydoc 0.7.')
except AttributeError:
    raise ImportError('numpydoc mangling requires numpydoc 0.7.')


class FunctionDoc(_FunctionDoc):

    def _str_index(self):
        # This should not be necessary after
        # See https://github.com/numpy/numpydoc/pull/187/files
        idx = self['index']
        out = []
        output_index = False
        default_index = idx.get('default', '')
        if default_index:
            output_index = True
        out += ['.. index:: %s' % default_index]
        for section, references in idx.items():
            if section == 'default':
                continue
            output_index = True
            out += ['   :%s: %s' % (section, ', '.join(references))]
        if output_index:
            return out
        else:
            return ''

    def _str_see_also(self, func_role):
        # See https://github.com/numpy/numpydoc/pull/189
        if not self['See Also']:
            return []
        out = []
        out += self._str_header("See Also")
        last_had_desc = True
        for func, desc, role in self['See Also']:
            if role:
                link = ':%s:`%s`' % (role, func)
            elif func_role:
                link = ':%s:`%s`' % (func_role, func)
            else:
                link = "%s" % func
            if desc or last_had_desc:
                out += ['']
                out += [link]
            else:
                out[-1] += ", %s" % link
            if desc:
                out += self._str_indent([' '.join(desc)])
                last_had_desc = True
            else:
                last_had_desc = False
        out += ['']
        return out

    def __str__(self, func_role=''):
        out = []
        # See https://github.com/numpy/numpydoc/issues/190
        # out += self._str_signature()
        out += self._str_summary()
        out += self._str_extended_summary()
        for param_list in ('Parameters', 'Returns', 'Yields',
                           'Other Parameters', 'Raises', 'Warns'):
            out += self._str_param_list(param_list)
        out += self._str_section('Warnings')
        out += self._str_see_also(func_role)
        for s in ('Notes', 'References', 'Examples'):
            out += self._str_section(s)
        for param_list in ('Attributes', 'Methods'):
            out += self._str_param_list(param_list)
        out += self._str_index()
        return '\n'.join(out)

    def __add__(self, other):
        for section in self.sections:
            if section in ['Signature', 'Summary']:
                # Summary should be
                continue
            elif section == 'index':
                idx = {**other['index']}
                idx.update(self['index'])
                self['index'] = idx
            elif section == 'Extended Summary':
                self['Extended Summary'] += other['Summary']
                self['Extended Summary'] += other['Extended Summary']
            else:
                self[section] += other[section]
        return self


"""

The __str__, _str_index, and __str_see_also methods are slightly modified
versions of the methods that belong to the numpydoc developmenet team.

This copyright applies to those 3 methods listed above.


Copyright (C) 2008 Stefan van der Walt <stefan@mentat.za.net>,
Pauli Virtanen <pav@iki.fi>

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

 1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
 2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

"""
