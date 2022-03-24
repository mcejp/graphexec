import numpy

from .. import node_type


# TODO: how to deal with types here? especially the outputs

@node_type.define("numpy/add", "Add")
@node_type.input("a", "numpy.ndarray,number")
@node_type.input("b", "numpy.ndarray,number")
@node_type.output("result", "numpy.ndarray")
def add(a, b):
    return dict(result=numpy.add(a, b))


@node_type.define("numpy/div", "Divide")
@node_type.input("a", "numpy.ndarray,number")
@node_type.input("b", "numpy.ndarray,number")
@node_type.output("result", "numpy.ndarray")
def div(a, b):
    return dict(result=numpy.divide(a, b))


@node_type.define("numpy/mul", "Multiply")
@node_type.input("a", "numpy.ndarray,number")
@node_type.input("b", "numpy.ndarray,number")
@node_type.output("result", "numpy.ndarray")
def mul(a, b):
    return dict(result=numpy.multiply(a, b))


NODE_TYPES = [
    add,
    div,
    mul,
]
