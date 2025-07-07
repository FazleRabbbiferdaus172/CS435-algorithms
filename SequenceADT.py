class Sequence:
    """A Python implementation of the Sequence ADT."""

    #-------------------------- nested _Position class --------------------------
    class _Position:
        """A lightweight, nonpublic class for storing a node's position."""
        __slots__ = '_element', '_prev', '_next'

        def __init__(self, element, prev_node, next_node):
            self._element = element
            self._prev = prev_node
            self._next = next_node

        def element(self):
            """Return the element stored at this Position."""
            return self._element

    #------------------------------- utility methods -------------------------------
    def _validate_position(self, p):
        """Return position's node if valid, or raise error."""
        if not isinstance(p, self._Position):
            raise TypeError('p must be a proper Position type')
        if p._next is None or p._prev is None:
            raise ValueError('p is no longer a valid position')
        return p

    def _make_position(self, node):
        """Return Position instance for given node (or None if sentinel)."""
        if node is self._header or node is self._trailer:
            return None
        return self._Position(node._element, node._prev, node._next)

    #------------------------------- sequence methods -------------------------------
    def __init__(self):
        """Create an empty sequence."""
        self._header = self._Position(None, None, None)
        self._trailer = self._Position(None, self._header, None)
        self._header._next = self._trailer
        self._size = 0

    def __len__(self):
        """Return the number of elements in the sequence."""
        return self._size

    def size(self):
        """Return the number of elements in the sequence."""
        return len(self)

    def isEmpty(self):
        """Return True if the sequence is empty."""
        return self._size == 0

    def first(self):
        """Return the first Position in the sequence (or None if empty)."""
        return self._make_position(self._header._next)

    def last(self):
        """Return the last Position in the sequence (or None if empty)."""
        return self._make_position(self._trailer._prev)

    def isFirst(self, p):
        if p._prev == self._header:
            return True
        else:
            return False
    def isLast(self, p):
        if p._next == self._trailer:
            return True
        else:
            return False

    def before(self, p):
        """Return the Position just before p (or None if p is first)."""
        node = self._validate_position(p)
        return self._make_position(node._prev)

    def after(self, p):
        """Return the Position just after p (or None if p is last)."""
        node = self._validate_position(p)
        return self._make_position(node._next)

    def atRank(self, r):
        """Return the element at rank r."""
        if not 0 <= r < self._size:
            raise IndexError('rank out of range')
        # Search from beginning
        if r < self._size // 2:
            walk = self._header._next
            for _ in range(r):
                walk = walk._next
        # Search from end
        else:
            walk = self._trailer._prev
            for _ in range(self._size - 1 - r):
                walk = walk._prev
        return walk

    def rankOf(self, p):
        """Return the rank of the element at Position p."""
        node = self._validate_position(p)
        rank = 0
        walk = self._header._next
        while walk is not node:
            walk = walk._next
            rank += 1
        return rank

    def insertFirst(self, e):
        """Insert element e at the front of the sequence."""
        return self._insert_between(e, self._header, self._header._next)

    def insertLast(self, e):
        """Insert element e at the back of the sequence."""
        return self._insert_between(e, self._trailer._prev, self._trailer)

    def insertBefore(self, p, e):
        """Insert element e into sequence before Position p."""
        original = self._validate_position(p)
        return self._insert_between(e, original._prev, original)

    def insertAfter(self, p, e):
        """Insert element e into sequence after Position p."""
        original = self._validate_position(p)
        return self._insert_between(e, original, original._next)

    def remove(self, p):
        """Remove and return the element at Position p."""
        original = self._validate_position(p)
        return self._delete_node(original)
        
    def _insert_between(self, e, predecessor, successor):
        """Add element e between two existing nodes and return new Position."""
        newest = self._Position(e, predecessor, successor)
        predecessor._next = newest
        successor._prev = newest
        self._size += 1
        return self._make_position(newest)

    def _delete_node(self, node):
        """Delete nonsentinel node from the list and return its element."""
        predecessor = node._prev
        successor = node._next
        predecessor._next = successor
        successor._prev = predecessor
        self._size -= 1
        element = node._element
        # Deprecate the node
        node._prev = node._next = node._element = None
        return element

    def __iter__(self):
        """Generate a forward iteration of the elements of the sequence."""
        cursor = self.first()
        while cursor is not None:
            yield cursor.element()
            cursor = self.after(cursor)

    def __str__(self):
        """Return a string representation of the sequence."""
        if self.isEmpty():
            return "[]"
        return f"[{', '.join(str(e) for e in self)}]"
