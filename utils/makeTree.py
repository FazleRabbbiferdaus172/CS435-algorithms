from ..TreeADT import Tree

def makeTree(tree_dict: dict) -> Tree:
    parent_ref_dict = dict()

    tree = Tree()

    for k,v in tree_dict.items():
        if tree.root() == None:
            parent_ref_dict[k] = tree.add_root(k)
        for j in v:
            parent_ref_dict[j] = tree.add_child(parent_ref_dict[k], j)

    return tree

