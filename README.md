# GraphExec

GraphExec is a tool for executing [litegraph.js](https://github.com/jagenjo/litegraph.js) graphs on a server, with node operations implemented as Python functions.

Slot types can be any Python types, including [NumPy](https://numpy.org/) arrays and custom, opaque classes.

It runs as a REST back-end for litegraph.js with some aftermarket modifications, or as a command-line tool. Generating JavaScript code for client-side _stub nodes_ (with slots, properties and widgets, but no business logic) is also possible, based on user-provided model in YAML format.

For each node, server-side code can return image results (including [Matplotlib](https://matplotlib.org/) figures).

The project is in an alpha development stage; for example, litegraph.js built-in nodes are not implemented, and there is no support for the REST back-end in the upstream library.

![screenshot](doc/screenshot.png?raw=true)

---

## Usage (example currently incomplete)

    cd my_package
    graphexec-generate-js-module -o ../litegraph/src/nodes/my-package-generated.js my_package_node_types.yml
    env PYTHONPATH=. graphexec-server --wwwroot ../litegraph -m my_package_node_types

## Format check

    black --diff **.py

## Type check

    mypy graphexec
