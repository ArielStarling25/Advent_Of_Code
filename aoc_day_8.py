import time, os, threading, copy, math, pprint, csv
from AOC_Loader import AOCLoader

YEAR = 2024
DAY = 1

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
    
    def solve(self):
        pass

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
        
    def solve(self):
        pass

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