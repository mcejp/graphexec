# GraphExec

GraphExec is a tool for executing [litegraph.js](https://github.com/jagenjo/litegraph.js) graphs on a server, with node operations implemented as Python functions

## Usage

    cd my_package
    env PYTHONPATH=. graphexec-server --wwwroot ../litegraph -m my_package_node_types

## Format check

    black --diff **.py

## Type check

    mypy graphexec
