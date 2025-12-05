import time, os, threading, copy, math, pprint
from AOC_Loader import AOCLoader

YEAR = 2025
DAY = 5

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
        self.fresh_ingredients = 0

        self.fresh_ingr_ranges = [item for item in self.input if "-" in item]
        self.ingr_id_list = [item for item in self.input if "-" not in item]
        self.ingr_id_list.remove('')
    
    def solve(self):
        self.combine_ranges()
        for item in self.ingr_id_list:
            for id_range in self.fresh_ingr_ranges:
                start, end = map(int, id_range.split("-"))
                if int(item) >= start and int(item) <= end:
                    self.fresh_ingredients += 1
        return self.fresh_ingredients

    def combine_ranges(self):
        parsed_ranges = []
        merged = []
        for item in self.fresh_ingr_ranges:
            start, end = map(int, item.split("-"))
            parsed_ranges.append([start, end])
        parsed_ranges.sort(key=lambda x: x[0])
        for current_start, current_end in parsed_ranges:
            if not merged:
                merged.append([current_start, current_end])
            else:
                last_start, last_end = merged[-1]
                if current_start <= last_end:
                    merged[-1][1] = max(last_end, current_end) # update the end of the last range to be the maximum of the two ends
                else:
                    merged.append([current_start, current_end]) # if new range starts after the last one ends. Add it as a new entry
        self.fresh_ingr_ranges = [f"{m[0]}-{m[1]}" for m in merged]

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
        self.fresh_ingredients = 0

        self.fresh_ingr_ranges = [item for item in self.input if "-" in item]
        self.ingr_id_list = [item for item in self.input if "-" not in item]
        self.ingr_id_list.remove('')
        
    def solve(self):
        self.combine_ranges()
        for id_range in self.fresh_ingr_ranges:
            start, end = map(int, id_range.split("-"))
            self.fresh_ingredients += ((end+1)-start)
        return self.fresh_ingredients

    def combine_ranges(self):
        parsed_ranges = []
        merged = []
        for item in self.fresh_ingr_ranges:
            start, end = map(int, item.split("-"))
            parsed_ranges.append([start, end])
        parsed_ranges.sort(key=lambda x: x[0])
        for current_start, current_end in parsed_ranges:
            if not merged:
                merged.append([current_start, current_end])
            else:
                last_start, last_end = merged[-1]
                if current_start <= last_end:
                    merged[-1][1] = max(last_end, current_end) # update the end of the last range to be the maximum of the two ends
                else:
                    merged.append([current_start, current_end]) # if new range starts after the last one ends. Add it as a new entry
        self.fresh_ingr_ranges = [f"{m[0]}-{m[1]}" for m in merged]

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

        self.part1 = self._run_and_time("Part 1", Part1, copy.deepcopy(self.puzzle_input), copy.deepcopy(self.eg_input))
        self.part2 = self._run_and_time("Part 2", Part2, copy.deepcopy(self.puzzle_input), copy.deepcopy(self.eg_input))

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
        return result