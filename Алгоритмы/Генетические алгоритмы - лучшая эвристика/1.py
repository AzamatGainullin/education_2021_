def tag(name, *content, cls=None, **attrs):
    if cls is not None:
        attrs['class'] = cls
    if attrs:
        attr_str = ''.join(' %s="%s"' % (attr, value) for attr, value
                            in sorted (attrs.items()))
    else:
        attr_str = ''
    if content:
        return '\n'.join('<%s%s>%s</%s>' % (name, attr_str, c, name) for c
                        in content)
    else:
        return '<%s%s />' % (name, attr_str)

# print(tag('p', 'hello', id=33))


from inspect import signature
sig = signature(tag)


# for name, param in sig.parameters.items():
#     print(param.kind, ':', name, '=', param.default)

from dis import dis
dis(tag)
