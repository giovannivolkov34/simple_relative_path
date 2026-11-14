import os


def relative_path(start, target, sep=os.sep):
    """Return the shortest relative path from *start* to *target*.

    Both arguments are treated as directory paths.  The result is a string
    using *sep* as the path separator.  If the two paths have different
    anchors (drive letters on Windows, or one is absolute and the other is
    relative) the original *target* is returned unchanged, because no
    relative path exists between them.

    The algorithm is a straightforward component-wise comparison after
    normalising both paths with ``os.path.normpath``.  This keeps the
    behaviour predictable and avoids the surprising results that
    ``os.path.relpath`` can produce when one of the paths does not exist.
    """
    start = os.path.normpath(start)
    target = os.path.normpath(target)

    # Different anchors mean no relative path can bridge them.
    if os.path.splitdrive(start)[0] != os.path.splitdrive(target)[0]:
        return target

    start_parts = _split(start)
    target_parts = _split(target)

    # Find the length of the common prefix.
    common = 0
    for a, b in zip(start_parts, target_parts):
        if a != b:
            break
        common += 1

    # If nothing is shared and one side is anchored, there is no relative path.
    if common == 0 and (os.path.isabs(start) != os.path.isabs(target)):
        return target

    up = [".."] * (len(start_parts) - common)
    down = target_parts[common:]
    parts = up + down

    if not parts:
        return "."

    return sep.join(parts)


def _split(path):
    """Split a normalised path into components, ignoring empty ones."""
    if path in ("", "."):
        return []
    return [p for p in path.split(os.sep) if p]
