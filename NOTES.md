Q: How to pass out-of-band results (e.g. visual previews)?

A1: Pass extra argument to function to use as a callback mechanism
- Drawback: introducing procedurality into something purely functional

A2: Return a custom class wrapping real result + out-of-band data
- Drawback: not very elegant, pollutes "business" logic

A3: Have separate function to produce out-of-band results from real results
- Advantage: separation of computation and presentation logic
- Drawback: out-of-band result might need more inputs than what survives to this point


Q: Input and parameter type/range checking?
A: Can use https://typeguard.readthedocs.io/en/latest/api.html#typeguard.check_type
