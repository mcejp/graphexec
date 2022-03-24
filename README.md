# GraphExec

GraphExec is a tool for executing [litegraph.js](https://github.com/jagenjo/litegraph.js) graphs on a server, with node operations implemented as Python functions.

Slot types can be any Python types, including [NumPy](https://numpy.org/) arrays and custom, opaque classes.

It runs as a REST back-end for litegraph.js with some aftermarket modifications, or as a command-line tool. Generating JavaScript code for client-side _stub nodes_ (with slots, properties and widgets, but no business logic) is also possible, based on decorators added to the node implementation.

For each node, server-side code can return image results (including [Matplotlib](https://matplotlib.org/) figures).

The project is in an alpha development stage; for example, litegraph.js built-in nodes are not implemented, and there is no support for the REST back-end in the upstream library.

![screenshot](doc/screenshot.png?raw=true)

---

## Usage

With my_node_types.py:

```python
from graphexec import node_type

from .my_implementation import _perlin_noise

@node_type.define("my_package/perlin_noise", "Perlin noise")
@node_type.input("width", "number")
@node_type.input("height", "number")
@node_type.output("map", "numpy.ndarray")
def perlin_noise(width, height):
    return dict(map=_perlin_noise(int(width), int(height)))

NODE_TYPES = [
    perlin_noise,
]
```

    graphexec-generate-js-module -o ../litegraph/src/nodes/my-package-generated.js my_node_types
    env PYTHONPATH=. graphexec-server --wwwroot ../litegraph -m my_node_types

## Format check

    black --diff **.py

## Type check

    mypy graphexec
