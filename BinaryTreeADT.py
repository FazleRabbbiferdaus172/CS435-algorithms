from collections import deque

class BinaryTree:


    #-------------------------- nested _Position class --------------------------
    class _Position:
        """A nonpublic class for storing a node's position."""
        __slots__ = '_element', '_parent', '_left', '_right'

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

        def element(self):
            return self._element

    #-------------------------- public accessor methods --------------------------
    def __init__(self):
        """Create an initially empty tree with a single sentinel root."""
        self._root = self._Position(None)
        self._size = 0 # Number of internal nodes

    def __len__(self):
        """Return the total number of elements (internal nodes) in the tree."""
        return self._size
    
    def size(self):
        """Return the total number of elements (internal nodes) in the tree."""
        return len(self)

    def isEmpty(self):
        """Return True if the tree has no elements."""
        return len(self) == 0

    def root(self):
        """Return the Position of the tree's root."""
        return self._make_position(self._root)

    def parent(self, p):
        """Return the Position of p's parent (or None if p is root)."""
        node = self._validate(p)
        return self._make_position(node._parent)

    def element(self, p):
        """Return the element stored at Position p, raising an error if external."""
        if self.isExternal(p):
            raise TypeError("External nodes do not contain elements.")
        return p._element

    def leftChild(self, p):
        """Return the Position of p's left child."""
        node = self._validate(p)
        return self._make_position(node._left)

    def rightChild(self, p):
        """Return the Position of p's right child."""
        node = self._validate(p)
        return self._make_position(node._right)

    def sibling(self, p):
        """Return the Position of p's sibling (or None if no sibling)."""
        parent = self.parent(p)
        if parent is None:
            return None
        if p == self.leftChild(parent):
            return self.rightChild(parent)
        else:
            return self.leftChild(parent)

    def children(self, p):
        """Generate an iteration of Positions of p's children."""
        if self.leftChild(p) is not None:
            yield self.leftChild(p)
        if self.rightChild(p) is not None:
            yield self.rightChild(p)
            
    def isInternal(self, p):
        """Return True if Position p has at least one child."""
        return self.leftChild(p) is not None

    def isExternal(self, p):
        """Return True if Position p does not have any children."""
        return not self.isInternal(p)

    def positions(self):
        """Generate an iteration of the tree's positions (internal and external)."""
        if self.size() > 0: # only traverse if there are internal nodes
            fringe = deque([self.root()])
            while fringe:
                p = fringe.popleft()
                yield p
                for c in self.children(p):
                    if c is not None:
                        fringe.append(c)

    def elements(self):
        """Generate an iteration of elements from internal nodes only."""
        for p in self.positions():
            if self.isInternal(p):
                yield p.element()

    #-------------------------- non-public utility methods --------------------------
    def _validate(self, p):
        """Return position's node if valid, or raise error."""
        if not isinstance(p, self._Position):
            raise TypeError('p must be a proper Position type')
        if p._parent is p:  # Convention for deprecated nodes
            raise ValueError('p is no longer a valid position')
        return p

    def _make_position(self, node):
        """Return Position instance for given node (or None if None)."""
        return node if node is not None else None

    def _expand_external(self, p, e):
        """
        Helper to expand an external node p, storing element e and creating two new
        sentinel children. Returns the position p, which is now internal.
        """
        node = self._validate(p)
        if self.isInternal(p):
            raise ValueError('Position p is not external')
        
        node._element = e
        node._left = self._Position(None, parent=node)
        node._right = self._Position(None, parent=node)
        self._size += 1
        return p

    #-------------------------- public update methods --------------------------
    def add_root(self, e):
        """Add a root to an empty tree, returning the root's position."""
        if not self.isEmpty():
            raise ValueError('Tree is not empty')
        return self._expand_external(self.root(), e)

    def insertLeft(self, p, e):
        """Insert element e as the left child of internal node p."""
        node = self._validate(p)
        if self.isExternal(node):
            raise ValueError('Cannot insert child for an external node')
        
        left_child = self.leftChild(node)
        if self.isInternal(left_child):
            raise ValueError('Left child already exists')
        
        return self._expand_external(left_child, e)

    def insertRight(self, p, e):
        """Insert element e as the right child of internal node p."""
        node = self._validate(p)
        if self.isExternal(node):
            raise ValueError('Cannot insert child for an external node')

        right_child = self.rightChild(node)
        if self.isInternal(right_child):
            raise ValueError('Right child already exists')
            
        return self._expand_external(right_child, e)

    def remove(self, p):
        """
        Remove the internal node at Position p, making it external.
        Raises ValueError if p's children are not both external.
        Returns the element that was stored at p.
        """
        node = self._validate(p)
        if self.isExternal(p):
            raise ValueError('p is not an internal node')
        
        if self.isInternal(self.leftChild(p)) or self.isInternal(self.rightChild(p)):
            raise ValueError('p has internal children and cannot be removed')
        
        element = node._element
        node._element = None
        node._left = None
        node._right = None
        self._size -= 1
        return element
        
    def replaceElement(self, p, e):
        """Replace the element at internal position p with e."""
        node = self._validate(p)
        if self.isExternal(node):
            raise TypeError("Cannot replace element in an external node.")
        old_element = node._element
        node._element = e
        return old_element
        
    def swapElements(self, p, q):
        """Swap the elements at internal positions p and q."""
        node_p = self._validate(p)
        node_q = self._validate(q)
        if self.isExternal(node_p) or self.isExternal(node_q):
            raise TypeError("Cannot swap elements in an external node.")
        node_p._element, node_q._element = node_q._element, node_p._element

