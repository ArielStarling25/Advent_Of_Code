import time, os, threading, copy, math, pprint, csv
from collections import deque
from AOC_Loader import AOCLoader

YEAR = 2025
DAY = 7

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
        self.split_count = 0

        for i in range(0, len(self.input)):
            self.input[i] = [self.input[i][j] for j in range(0, len(self.input[i]))]
    
    def solve(self):
        start_x = 0
        for i in range(len(self.input[0])):
            if self.input[0][i] == 'S':
                start_x = i
                break
        self.draw_beam(start_x, 1)
        #pprint.pprint(self.input)
        return self.split_count

    def draw_beam(self, curr_x, curr_y):
        if curr_y >= len(self.input) or (curr_x < 0 and curr_x >= len(self.input[0])):
            return
        if self.input[curr_y][curr_x] == '.':
            self.input[curr_y][curr_x] = '|'
            self.draw_beam(curr_x, curr_y+1)
        elif self.input[curr_y][curr_x] == '^':
            self.draw_beam(curr_x-1, curr_y)
            self.draw_beam(curr_x+1, curr_y)
            self.split_count += 1
        else:
            return

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
        #self.input = self.eg_input
        self.variants = set()
        self.memo = {}
        for i in range(0, len(self.input)):
            self.input[i] = [self.input[i][j] for j in range(0, len(self.input[i]))]

    def solve(self):
        self.input = [row for row in self.input if any(cell != '.' for cell in row)]
        start_x = 0
        for i in range(len(self.input[0])):
            if self.input[0][i] == 'S':
                start_x = i
                break
        # self.variants = self.get_variants(start_x, 1)
        # return len(self.variants)
        return self.count_variants(start_x, 1)
    
    # DFS method again but with memoisation, caching all instances of paths per coordinate
    def get_variants(self, x, y):
        if y >= len(self.input) or x < 0 or x >= len(self.input[0]):
            return {""}
        cell = (x, y)
        if cell in self.memo:
            return self.memo[cell]
        cell = self.input[y][x]
        paths = set()
        if cell == '.' or cell == '|':
            paths = self.get_variants(x, y+1)
        elif cell == '^':
            left_suffixes = self.get_variants(x-1, y)
            for suffix in left_suffixes:
                paths.add("<" + suffix)
            right_suffixes = self.get_variants(x+1, y)
            for suffix in right_suffixes:
                paths.add(">" + suffix)
        self.memo[cell] = paths
        return paths
    
    def count_variants(self, x, y):
        if y >= len(self.input) or x < 0 or x >= len(self.input[0]):
            return 1
        cell = (x, y)
        if cell in self.memo:
            return self.memo[cell]
        char_value = self.input[y][x]
        total_paths = 0
        if char_value == '.' or char_value == '|':
            total_paths = self.count_variants(x, y+1)
        elif char_value == '^':
            left_count = self.count_variants(x-1, y)
            right_count = self.count_variants(x+1, y)
            total_paths = left_count + right_count
        self.memo[cell] = total_paths
        return total_paths
    
    # def solve(self):
    #     start_x = 0
    #     self.input = [row for row in self.input if any(cell != '.' for cell in row)]
    #     for i in range(len(self.input[0])):
    #         if self.input[0][i] == 'S':
    #             start_x = i
    #             break
    #     queue = deque([(start_x, 1, "")])
    #     visited_states = set()
    #     while queue:
    #         curr_x, curr_y, dir_collection = queue.popleft()
    #         if curr_y >= len(self.input) or (curr_x < 0 or curr_x >= len(self.input[0])):
    #             self.variants.add(dir_collection)
    #             continue
    #         state = (curr_x, curr_y, dir_collection)
    #         if state in visited_states:
    #             continue
    #         visited_states.add(state)
    #         cell = self.input[curr_y][curr_x]
    #         if cell == '.' or cell == '|':
    #             queue.append((curr_x, curr_y + 1, dir_collection))
    #         elif cell == '^':
    #             queue.append((curr_x-1, curr_y, dir_collection+"<"))
    #             queue.append((curr_x+1, curr_y, dir_collection+">"))
    #     return len(self.variants)

    def draw_beam(self, curr_x, curr_y, dir_collection):
        if curr_y >= len(self.input) or (curr_x < 0 and curr_x >= len(self.input[0])):
            self.variants.add(dir_collection)
            print(f"Adding:[{dir_collection}]")
            return
        if self.input[curr_y][curr_x] == '.' or self.input[curr_y][curr_x] == '|':
            self.input[curr_y][curr_x] = '|'
            self.draw_beam(curr_x, curr_y+1, dir_collection)
        elif self.input[curr_y][curr_x] == '^':
            self.draw_beam(curr_x-1, curr_y, dir_collection+"<")
            self.draw_beam(curr_x+1, curr_y, dir_collection+">")
        else:
            return

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