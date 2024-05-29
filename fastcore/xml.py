# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/11_xml.ipynb.

# %% auto 0
__all__ = ['voids', 'XT', 'xt', 'to_xml', 'highlight', 'showtags', 'Html', 'Head', 'Title', 'Meta', 'Link', 'Style', 'Body',
           'Pre', 'Code', 'Div', 'Span', 'P', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'Strong', 'Em', 'B', 'I', 'U', 'S',
           'Strike', 'Sub', 'Sup', 'Hr', 'Br', 'Img', 'A', 'Nav', 'Ul', 'Ol', 'Li', 'Dl', 'Dt', 'Dd', 'Table', 'Thead',
           'Tbody', 'Tfoot', 'Tr', 'Th', 'Td', 'Caption', 'Col', 'Colgroup', 'Form', 'Input', 'Textarea', 'Button',
           'Select', 'Option', 'Label', 'Fieldset', 'Legend', 'Details', 'Summary', 'Main', 'Header', 'Footer',
           'Section', 'Article', 'Aside', 'Figure', 'Figcaption', 'Mark', 'Small', 'Iframe', 'Object', 'Embed', 'Param',
           'Video', 'Audio', 'Source', 'Canvas', 'Svg', 'Math', 'Script', 'Noscript', 'Template', 'Slot']

# %% ../nbs/11_xml.ipynb 2
from .utils import *

from dataclasses import dataclass, asdict
import types
from functools import partial
from html import escape

# %% ../nbs/11_xml.ipynb 4
def _attrmap(o):
    o = dict(htmlClass='class', cls='class', klass='class', fr='for', htmlFor='for').get(o, o)
    return o.lstrip('_').replace('_', '-')

# %% ../nbs/11_xml.ipynb 5
class XT(list):
    def __init__(self, tag, cs, attrs): super().__init__([tag, cs, attrs])
    @property
    def tag(self): return self[0]
    @property
    def children(self): return self[1]
    @property
    def attrs(self): return self[2]

# %% ../nbs/11_xml.ipynb 6
def xt(tag:str, *c, **kw):
    "Create an XML tag structure `[tag,children,attrs]` for `toxml()`"
    if len(c)==1 and isinstance(c[0], types.GeneratorType): c = tuple(c[0])
    kw = {_attrmap(k):(v if isinstance(v,bool) else str(v)) for k,v in kw.items() if v is not None}
    return XT(tag.lower(),c,kw)

# %% ../nbs/11_xml.ipynb 7
_g = globals()
_all_ = ['Html', 'Head', 'Title', 'Meta', 'Link', 'Style', 'Body', 'Pre', 'Code',
    'Div', 'Span', 'P', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'Strong', 'Em', 'B',
    'I', 'U', 'S', 'Strike', 'Sub', 'Sup', 'Hr', 'Br', 'Img', 'A', 'Link', 'Nav',
    'Ul', 'Ol', 'Li', 'Dl', 'Dt', 'Dd', 'Table', 'Thead', 'Tbody', 'Tfoot', 'Tr',
    'Th', 'Td', 'Caption', 'Col', 'Colgroup', 'Form', 'Input', 'Textarea',
    'Button', 'Select', 'Option', 'Label', 'Fieldset', 'Legend', 'Details',
    'Summary', 'Main', 'Header', 'Footer', 'Section', 'Article', 'Aside', 'Figure',
    'Figcaption', 'Mark', 'Small', 'Iframe', 'Object', 'Embed', 'Param', 'Video',
    'Audio', 'Source', 'Canvas', 'Svg', 'Math', 'Script', 'Noscript', 'Template', 'Slot']

for o in _all_: _g[o] = partial(xt, o.lower())

# %% ../nbs/11_xml.ipynb 12
voids = set('area base br col command embed hr img input keygen link meta param source track wbr !doctype'.split())

# %% ../nbs/11_xml.ipynb 13
def _to_attr(k,v):
    if v==True: return str(k)
    if v==False: return ''
    return f'{k}="{escape(str(v), quote=False)}"'

# %% ../nbs/11_xml.ipynb 14
def to_xml(elm, lvl=0):
    "Convert `xt` element tree into an XML string"
    if isinstance(elm, tuple): return '\n'.join(to_xml(o) for o in elm)
    if hasattr(elm, '__xt__'): elm = elm.__xt__()
    sp = ' ' * lvl
    if not isinstance(elm, list):
        if isinstance(elm, str): elm = escape(elm)
        return f'{elm}\n'

    tag,cs,attrs = elm
    stag = tag
    if attrs:
        sattrs = (_to_attr(k,v) for k,v in attrs.items())
        stag += ' ' + ' '.join(sattrs)
    
    cltag = '' if tag in voids else f'</{tag}>'
    if not cs: return f'{sp}<{stag}>{cltag}\n'
    res = f'{sp}<{stag}>\n'
    res += ''.join(to_xml(c, lvl=lvl+2) for c in cs)
    if tag not in voids: res += f'{sp}{cltag}\n'
    return res

# %% ../nbs/11_xml.ipynb 16
def highlight(s, lang='xml'):
    "Markdown to syntax-highlight `s` in language `lang`"
    return f'```{lang}\n{to_xml(s)}\n```'

# %% ../nbs/11_xml.ipynb 17
def showtags(s):
    return f"""<code><pre>
{escape(to_xml(s))}
</code></pre>"""

XT._repr_markdown_ = highlight
