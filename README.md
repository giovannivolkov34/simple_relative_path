# simple_relative_path

Compute the shortest relative path from one directory to another.

```python
from simple_relative_path import relative_path

relative_path("/a/b", "/a/c")
# '../c'

relative_path("/a/b", "/a/b")
# '.'

relative_path("/a", "b")
# 'b'  (no relative path exists between an absolute and a relative path)
```

## Why this exists

`os.path.relpath` is convenient, but it can produce surprising results when the
inputs do not exist on disk, and its behaviour with mixed absolute and relative
paths is easy to misread.  This library makes one clear decision: if the two
paths have different anchors (different drive letters, or one absolute and one
relative), it returns the target unchanged.  That is the only sensible answer
because no relative path can bridge those roots.

For paths that share an anchor, the result is the shortest sequence of `..`
components followed by the target's remaining components.  Trailing separators,
`.` components, and `..` components are normalised first, so the comparison is
component-wise and deterministic.

## Awkward edge

When the start and target are the same directory, the result is `'.'`, not an
empty string.  That matches the convention used by shells and most path
libraries, and it keeps the return type a non-empty string for every valid
input.
