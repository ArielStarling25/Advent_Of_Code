class SparseGrid:
    def __init__(self, default_val=''):
        self._grid = {}
        self.default_val = default_val
        # Initialize bounds. 
        # We start at -1 so an empty grid returns len() of 0, not 1.
        self.max_x = -1
        self.max_y = -1

    def __len__(self):
        # Returns the "Height" (max y index + 1)
        # Example: If largest y is 9, len is 10.
        return self.max_y + 1

    def __getitem__(self, y):
        return self._RowProxy(self, y)

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            y, x = key
            self._set_cell(x, y, value)
        else:
            raise TypeError("Use grid[y][x] or grid[y, x] = value")

    def _get_cell(self, x, y):
        return self._grid.get((x, y), self.default_val)

    def _set_cell(self, x, y, value):
        if value == self.default_val:
            if (x, y) in self._grid:
                del self._grid[(x, y)]
        else:
            self._grid[(x, y)] = value
            # Update 'max' bounds to track the size of the grid
            self.max_x = max(self.max_x, x)
            self.max_y = max(self.max_y, y)

    class _RowProxy:
        def __init__(self, parent, y):
            self.parent = parent
            self.y = y

        def __getitem__(self, x):
            return self.parent._get_cell(x, self.y)

        def __setitem__(self, x, value):
            self.parent._set_cell(x, self.y, value)

        def __len__(self):
            # Returns the "Width" (max x index + 1)
            # This allows len(grid[0]) to return the global width
            return self.parent.max_x + 1