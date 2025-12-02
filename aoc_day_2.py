import time, os, threading, copy, math
from AOC_Loader import AOCLoader

YEAR = 2025
DAY = 2

class Part1:
    def __init__(self, raw_input, eg_input=None):
        self.raw_input = raw_input
        if eg_input == None or len(raw_input) < 1:
            print("No Example Input")
        if raw_input == None or len(raw_input) < 1:
            raise KeyError("Forgor input value")
        self.eg_input = eg_input.split(",")
        self.input = self.raw_input.split(",")
        #self.input = self.eg_input
        self.invalids = []
    
    def solve(self):
        for i in range(len(self.input)):
            a = self.input[i].split("-")
            start_n = int(a[0])
            end_n = int(a[1])
            for id_num in range(start_n, end_n+1):
                num_str = str(id_num)
                mid = len(num_str) // 2
                if num_str[:mid] == num_str[mid:]:
                    self.invalids.append(id_num)
        return sum(self.invalids)
                
    def __str__(self):
        return str(self.__dict__)
    
class Part2:
    def __init__(self, raw_input, eg_input=None):
        self.raw_input = raw_input
        if eg_input == None or len(raw_input) < 1:
            print("No Example Input")
        if raw_input == None or len(raw_input) < 1:
            raise KeyError("Forgor input value")
        self.eg_input = eg_input.split(",")
        self.input = self.raw_input.split(",")
        #self.input = self.eg_input
        self.invalids = set()
        
    # def solve(self):
    #     for i in range(len(self.input)):
    #         a = self.input[i].split("-")
    #         start_n = int(a[0])
    #         end_n = int(a[1])
    #         for id_num in range(start_n, end_n+1):
    #             num_str = str(id_num)
    #             mid = len(num_str) // 2
    #             charter = {j: [num_str[:j+1],len(num_str[:j+1])] for j in range(0, mid)} # for each i:[value, step]
    #             for item, value in charter.items():
    #                 if value[0][0] == '0':
    #                     continue
    #                 stuff = [num_str[k:k + value[1]] for k in range(0, len(num_str), value[1])]
    #                 if len(set(stuff)) == 1 and len(stuff) > 1:
    #                     if not id_num in self.invalids:
    #                         self.invalids.append(id_num)
    #     return sum(self.invalids)

    def solve(self):
        for item in self.input:
            start_n, end_n = map(int, item.split("-"))
            max_len = len(str(end_n))
            for base_len in range(1, (max_len // 2) + 1): # base number length cannot be longer than half of max_len
                # Generate all possible base numbers based on base_len, if base_len is 2 -> base start: 10, base_end -> 99
                base_start = 10 ** (base_len - 1)
                base_end = (10 ** base_len) - 1
                for base_num in range(base_start, base_end + 1):
                    s_base = str(base_num)
                    repetitions = 2 # Base case for number of repetitions
                    candidate_str = s_base * repetitions
                    while len(candidate_str) <= max_len:
                        candidate_int = int(candidate_str)
                        if candidate_int > end_n:
                            break
                        if candidate_int >= start_n:
                            #print("INVALID: ", candidate_int)
                            self.invalids.add(candidate_int)
                        repetitions += 1
                        candidate_str = s_base * repetitions
        return sum(self.invalids)

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
        print("=============================================")
        print(f"{label} | Result: [{result}] | Execution Time: {duration_ms:.4f} ms | ")
        print("=============================================")
        return result