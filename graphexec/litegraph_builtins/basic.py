def const(value: float):
    return dict(value=value)


NODE_TYPES = {
    "basic/const": const,
}
