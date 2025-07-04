from collections import deque

class Tree:
    """
    A Tree implementation where only internal nodes store elements
    and external (leaf) nodes act as sentinel placeholders.
    """

    #-------------------------- nested _Position class --------------------------
    class _Position:
        """A lightweight, nonpublic class for storing a node's position."""
        __slots__ = '_element', '_parent', '_children'

        def __init__(self, element, parent=None):
            self._element = element
            self._parent = parent
            self._children = []
    
        def element(self):
            return self._element
 
    #------------------------------- utility methods -------------------------------
    def _validate(self, p):
        """Return position's node if valid, or raise error."""
        if not isinstance(p, self._Position):
            raise TypeError('p must be a proper Position type')
        if p._parent is p:
            raise ValueError('p is no longer a valid position')
        return p

    def _make_position(self, node):
        """Return Position instance for given node (or None if None)."""
        return node if node is not None else None

    #-------------------------- public accessor methods --------------------------
    def __init__(self):
        """Create an initially empty tree."""
        self._root = None
        self._size = 0  # Tracks the number of internal nodes with elements

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
        """Return the Position of the tree's root (or None if empty)."""
        return self._make_position(self._root)

    def parent(self, p):
        """Return the Position of p's parent (or None if p is root)."""
        node = self._validate(p)
        return self._make_position(node._parent)

    def children(self, p):
        """Generate an iteration of Positions of p's children."""
        node = self._validate(p)
        for child_node in node._children:
            yield self._make_position(child_node)

    def isRoot(self, p):
        """Return True if Position p is the root of the tree."""
        return self.root() == p

    def isInternal(self, p):
        """Return True if Position p has at least one child."""
        return len(self._validate(p)._children) > 0

    def isExternal(self, p):
        """Return True if Position p does not have any children."""
        return len(self._validate(p)._children) == 0
        
    def element(self, p):
        """Return the element stored at Position p, raising an error if external."""
        node = self._validate(p)
        if self.isExternal(p):
            raise TypeError("External nodes do not contain elements.")
        return node._element

    def positions(self):
        """Generate an iteration of all node positions (internal and external)."""
        if not self.isEmpty():
            fringe = deque([self.root()])
            while fringe:
                p = fringe.popleft()
                yield p
                for c in self.children(p):
                    fringe.append(c)

    def elements(self):
        """Generate an iteration of elements from internal nodes only."""
        for p in self.positions():
            if self.isInternal(p):
                yield p.element()

    def __iter__(self):
        """Generate an iteration of the tree's elements."""
        yield from self.elements()

    #-------------------------- public update methods --------------------------
    def replaceElement(self, p, e):
        """Replace the element at internal Position p with e."""
        node = self._validate(p)
        if self.isExternal(p):
            raise TypeError("Cannot replace element in an external node.")
        old_element = node._element
        node._element = e
        return old_element

    def add_root(self, e):
        return self._add_root(e=e)

    def add_child(self, p, e):
        n = None
        for c in self.children(p):
            if self.isExternal(c):
                n = c
                break
        if n == None:
            n = self._add_child_sentinel(p)
        self._expand_external(n ,e)

        return n
        
        
    #---------- non-public update methods to build the tree ----------
    def _add_root(self, e):
        """
        Create a root for an empty tree. The new root is made internal
        by automatically creating a sentinel child for it.
        """
        if self._root is not None:
            raise ValueError('Root exists')
        
        self._size = 1
        self._root = self._Position(e)
        self._root._children.append(self._Position(None, parent=self._root))
        
        return self._make_position(self._root)

    def _expand_external(self, p, e):
        """
        Expand an external node p, storing element e and adding a new
        sentinel child. Returns the position of the new sentinel child.
        """
        node = self._validate(p)
        if self.isInternal(p):
            raise ValueError('Position p is not external')
        
        node._element = e
        self._size += 1
        
        new_sentinel = self._Position(None, parent=node)
        node._children.append(new_sentinel)
        return self._make_position(new_sentinel)

    def _add_child_sentinel(self, p):
        """Adds a new external (sentinel) node as a child of internal node p."""
        node = self._validate(p)
        if self.isExternal(p):
            raise ValueError('Cannot add child to an external node')
        new_sentinel = self._Position(None, parent=node)
        node._children.append(new_sentinel)
        return self._make_position(new_sentinel)