def draw(tree):
    """Prints a text-based representation of the tree (rotated 90 degrees)."""
    lvl = dict()
    def _draw(tree, p, depth):
        """Recursively draws the subtree rooted at p."""
        if tree.isExternal(p):
            return
        if depth not in lvl:
            lvl[depth] = [p]
        else:
            lvl[depth].append(p)
        _draw(tree, tree.rightChild(p), depth + 1)
        print('   ' * depth + str(tree.element(p)))
        _draw(tree, tree.leftChild(p), depth + 1)

    print("--- Tree ---")
    if not tree.isEmpty():
        _draw(tree, tree.root(), 0)
    else:
        print("Tree is empty.")
    print("------------")