from .. import node_type

@node_type.define("basic/const", "Const Number")
def const(value: float):
    return dict(value=value)


NODE_TYPES = [
    const,
]
