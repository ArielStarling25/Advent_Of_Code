import time, os, threading, copy, math, pprint, csv
from AOC_Loader import AOCLoader
from collections import deque
from Sparse_Grid import SparseGrid

YEAR = 2025
DAY = 9

class Part1:
    def __init__(self, raw_input, eg_input=""):
        self.raw_input = raw_input
        if eg_input == None or len(raw_input) < 1:
            print("No Example Input")
        if raw_input == None or len(raw_input) < 1:
            raise KeyError("Forgor input value")
        self.eg_input = eg_input.split("\n")
        self.input = self.raw_input.split("\n")
        #self.input = self.eg_input
        self.coordinates_dict = {}
        self.coordinates = []
        self.coordinates_set = set()
        self.range_x = 0
        self.range_y = 0
        for item in self.input:
            x, y = map(int, item.split(","))
            if x > self.range_x:
                self.range_x = x
            if y > self.range_y:
                self.range_y = y
            self.coordinates_dict[(x,y)] = []
            self.coordinates.append([x,y,0])
            self.coordinates_set.add((x,y))
        #pprint.pprint(self.coordinates)
    
    def solve(self):
        for i in range(len(self.coordinates)):
            for j in range(len(self.coordinates)):
                x1, y1, _ = self.coordinates[i]
                x2, y2, _ = self.coordinates[j]
                area = (abs(y2-y1)+1)*(abs(x2-x1)+1)
                if area > self.coordinates[i][2]:
                    self.coordinates[i][2] = area
        self.coordinates.sort(key=lambda x: x[2], reverse=True)
        # pprint.pprint(self.coordinates)
        return self.coordinates[0][2]

    def __str__(self):
        return str(self.__dict__)
    
class Part2:
    def __init__(self, raw_input, eg_input=""):
        self.raw_input = raw_input
        if eg_input == None or len(raw_input) < 1:
            print("No Example Input")
        if raw_input == None or len(raw_input) < 1:
            raise KeyError("Forgor input value")
        self.eg_input = eg_input.split("\n")
        self.input = self.raw_input.split("\n")
        self.input = self.eg_input
        self.coordinates = {}
        self.coordinate_sizes = []
        self.grid = SparseGrid(default_val='.')
        self.range_x = 0
        self.range_y = 0
        for item in self.input:
            x, y = map(int, item.split(","))
            if x > self.range_x:
                self.range_x = x
            if y > self.range_y:
                self.range_y = y
            self.coordinates[(x,y)] = []
            self.coordinate_sizes.append([x,y,0])

        # print(self.coordinates)
        # print(self.range_x, self.range_y)
        print("INFO - INITIALIZING...")
        self.grid[self.range_y + 1][self.range_x + 2] = 'o'
        # for i in range(self.range_y + 2):
        #     self.grid.append(['.' for j in range(self.range_x + 3)])
        for key, value in self.coordinates.items():
            self.grid[key[1]][key[0]] = '#'
        #self.print_grid(self.grid)
        
    def solve(self):
        root = next(iter(self.coordinates))
        print("INFO - TRAVERSING TO FIND LOOP...")
        adj_list, guh = self.traverse_seen_directions(copy.deepcopy(self.coordinates), root[0], root[1], True)
        #pprint.pprint(adj_list, sort_dicts=False)
        print("INFO - DRAWING MAP OUTLINE...")
        outline_grid = self.draw_on_grid_list(self.grid, adj_list)
        self.print_grid(outline_grid)
        print("INFO - FILLING MAP OUTLINE...")
        #filled_grid = self.fill_grid_inside(outline_grid, adj_list)
        filled_grid = self.fill_poly_grid(outline_grid)
        self.print_grid(filled_grid)
        print("INFO - COUNTING 'X' in MARKED AREA...")
        count = self.find_largest_area(filled_grid)
        return count

    def find_largest_area(self, filled_grid):
        for i in range(len(self.coordinate_sizes)):
            for j in range(len(self.coordinate_sizes)):
                x1, y1, _ = self.coordinate_sizes[i]
                x2, y2, _ = self.coordinate_sizes[j]
                if x1 == x2 and y1 == y2:
                    continue
                area = self.count_within_area(filled_grid, x1, y1, x2, y2)
                if area > self.coordinate_sizes[i][2]:
                    self.coordinate_sizes[i][2] = area
        self.coordinate_sizes.sort(key=lambda x: x[2], reverse=True)
        return self.coordinate_sizes[0][2]
    
    def count_within_area(self, filled_grid, x1, y1, x2, y2):
        count = 0
        start_x, end_x = sorted((x1, x2))
        start_y, end_y = sorted((y1, y2))
        for y in range(start_y, end_y+1):
            for x in range(start_x, end_x+1):
                if 0 <= y < len(filled_grid) and 0 <= x < len(filled_grid[0]):
                    if filled_grid[y][x] in ['X','#']:
                        count += 1  
                    if filled_grid[y][x] in ['.', 'o']:
                        return 0
        #self.print_grid(self.draw_debug_area(copy.deepcopy(filled_grid), x1, y1, x2, y2))
        return count

    def traverse_seen_directions(self, adj_list, x, y, initial):
        considered_coords = []
        looped = False
        if next(iter(adj_list)) == (x,y) and not initial:
            return adj_list, True
        for key, value in adj_list.items():
            if len(value) > 0 and not next(iter(adj_list)) == (key[0],key[1]):
                continue
            if key[0] == x and key[1] == y:
                continue
            if key[0] == x or key[1] == y:        # same column or same row
                considered_coords.append((key[0], key[1]))
        for coords in considered_coords:
            adj_list_copy = copy.deepcopy(adj_list)
            adj_list_copy[(x,y)].append((coords[0], coords[1]))
            adj_list, looped = self.traverse_seen_directions(adj_list_copy, coords[0], coords[1], False)
            if looped and all(len(value) > 0 for key, value in adj_list.items()):
                break 
        return adj_list, looped    

    def draw_debug_area(self, grid, x1, y1, x2, y2):
        # 1. Normalize coordinates (Start -> End)
        # This guarantees the loop works regardless of which corner comes first
        start_x, end_x = sorted((x1, x2))
        start_y, end_y = sorted((y1, y2))
        rows = len(grid)
        cols = len(grid[0])
        # 2. Iterate through the defined rectangle
        for y in range(start_y, end_y + 1):
            for x in range(start_x, end_x + 1):
                # 3. Safety Check: Only draw if within valid grid bounds
                if 0 <= y < rows and 0 <= x < cols:
                    grid[y][x] = 'O'
        grid[y2][x2] = "@"
        grid[y1][x1] = "@" 
        return grid         

    def draw_on_grid_list(self, grid_data, connections):
        # Helper to safely mark the grid
        def mark(x, y):
            if 0 <= y < len(grid_data) and 0 <= x < len(grid_data[0]):
                if grid_data[y][x] != '#':
                    grid_data[y][x] = 'X'

        # Iterate through each start node and its list of end nodes
        for start, targets in connections.items():
            start_x, start_y = start
            
            for target in targets:
                end_x, end_y = target
            
                # 1. Handle Vertical Lines (x is constant)
                if start_x == end_x:
                    step = 1 if end_y > start_y else -1
                    # Range excludes start/end points to preserve anchors
                    for y in range(start_y + step, end_y, step):
                        mark(start_x, y)
                        
                # 2. Handle Horizontal Lines (y is constant)
                elif start_y == end_y:
                    step = 1 if end_x > start_x else -1
                    # Range excludes start/end points
                    for x in range(start_x + step, end_x, step):
                        mark(x, start_y)
        return grid_data
    
    def fill_poly_grid(self, grid, adjacency_list=None):
        pass
        return grid
    
    def fill_grid_inside(self, grid_data, connections):
        # 1. Identify all 'Vertical Walls'
        # We need to know which path pixels act as vertical barriers.
        # A robust rule is: A pixel is a "wall" if it connects to the pixel BELOW it (South).
        vert_walls = set()
        path_pixels = set()

        for start, targets in connections.items():
            start_x, start_y = start
            path_pixels.add(start)
            for target in targets:
                end_x, end_y = target
                path_pixels.add(target)
                # Handle Vertical Lines
                if start_x == end_x:
                    y_min, y_max = sorted((start_y, end_y))
                    # Add all pixels in this segment to path_pixels
                    for y in range(y_min, y_max + 1):
                        path_pixels.add((start_x, y))
                    # Mark pixels that connect South as walls
                    # (We exclude the very bottom pixel of the segment for the Even-Odd rule)
                    for y in range(y_min, y_max):
                        vert_walls.add((start_x, y))
                # Handle Horizontal Lines
                elif start_y == end_y:
                    x_min, x_max = sorted((start_x, end_x))
                    for x in range(x_min, x_max + 1):
                        path_pixels.add((x, start_y))
        # 2. Scan and Fill
        rows = len(grid_data)
        cols = len(grid_data[0])
        for y in range(rows):
            inside = False
            for x in range(cols):
                # If we hit a vertical wall, toggle the 'inside' state
                if (x, y) in vert_walls:
                    inside = not inside
                # If we are inside, not on the path, and not a node
                if inside and (x, y) not in path_pixels:
                    if grid_data[y][x] == '.': # Only fill empty spots
                        grid_data[y][x] = 'X'
        return grid_data

    def print_grid(self, grid):
        print("--------")
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                print(grid[y][x], end="")
            print("")

    def __str__(self):
        return str(self.__dict__)

class Runner:
    def __init__(self):
        try:
            self.loader = AOCLoader(year=YEAR, day=DAY)
            self.puzzle_input, self.eg_input = self.loader.load_input()
            print(f"Successfully read data!")
        except ValueError as e:
            print(e)

        self.part1, time_1 = self._run_and_time("Part 1", Part1, copy.deepcopy(self.puzzle_input), copy.deepcopy(self.eg_input))
        self.part2, time_2 = self._run_and_time("Part 2", Part2, copy.deepcopy(self.puzzle_input), copy.deepcopy(self.eg_input))

        os.makedirs("aoc_outputs", exist_ok=True)

        data_to_write = [
            ['part', 'answer', 'time_taken'],
            [1, self.part1, time_1],
            [2, self.part2, time_2]
        ]

        with open(os.path.join("aoc_outputs", f"day_{DAY}_output.csv"), 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(data_to_write)

    def _run_and_time(self, label, func, *args):
        runnable = func(*args)
        start_time = time.perf_counter()
        result = runnable.solve()
        end_time = time.perf_counter()
        duration_ms = (end_time - start_time) * 1000
        if '67' in f"{duration_ms:.4f}":
            print("6767676767676767676767676767676767676767676767")
            print(f"{label} | Result: [{result}] | Execution Time: {duration_ms:.4f} ms | ")
            print("6767676767676767676767676767676767676767676767")
        elif '69' in f"{duration_ms:.4f}":
            print("6969696969696969696969696969696969696969696969")
            print(f"{label} | Result: [{result}] | Execution Time: {duration_ms:.4f} ms | ")
            print("6969696969696969696969696969696969696969696969")
        else:
            print("=============================================")
            print(f"{label} | Result: [{result}] | Execution Time: {duration_ms:.4f} ms | ")
            print("=============================================")
        return result, f"{duration_ms:.4f}" 