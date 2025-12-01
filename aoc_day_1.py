import time, os, threading, copy
from AOC_Loader import AOCLoader

YEAR = 2025
DAY = 1

class Part1:
    def __init__(self, raw_input, eg_input=None):
        self.raw_input = raw_input
        if eg_input == None or len(raw_input) < 1:
            print("No Example Input")
        else:
            self.eg_input = eg_input.split("\n")
        if raw_input == None or len(raw_input) < 1:
            raise KeyError("Forgor input value")
        self.input = self.raw_input.split("\n")
        self.counter = 50
        #self.input = self.eg_input
        self.zero_count = 0
    
    def solve(self):
        for i in range(len(self.input)):
            num = int(self.input[i][1:])
            if self.input[i][0] == 'R':
                self.counter = self.counter + num
            elif self.input[i][0] == 'L':
                self.counter = self.counter - num
            self.counter = self.circular_motion(self.counter)
            if self.counter == 0:
                self.zero_count += 1
            # print(f"Pointing at: {self.counter}")
        print(self.zero_count)

    def circular_motion(self, counter):
        while not (counter <= 99 and counter >= 0):
            if counter > 99 and counter >= 0:
                counter = 0 + (counter - 100)
            elif counter < 0:
                counter = 100 + counter
        return counter

    def __str__(self):
        return str(self.__dict__)
    
class Part2:
    def __init__(self, raw_input, eg_input=None):
        self.raw_input = raw_input
        if eg_input == None or len(raw_input) < 1:
            print("No Example Input")
        else:
            self.eg_input = eg_input.split("\n")
        if raw_input == None or len(raw_input) < 1:
            raise KeyError("Forgor input value")
        self.input = self.raw_input.split("\n")
        self.counter = 50
        self.zero_count = 0
        
    def solve(self):
        for i in range(len(self.input)):
            start_on_0 = False
            num = int(self.input[i][1:])
            if self.counter == 0:
                start_on_0 = True
            if self.input[i][0] == 'R':
                self.counter = self.counter + num
            elif self.input[i][0] == 'L':
                self.counter = self.counter - num
            self.counter = self.circular_motion(self.counter, start_on_0)
            print(f"Pointing at: {self.counter}")
        print("Final Zero Count: [", self.zero_count, "]")

    def circular_motion(self, counter, started_on_0):
        if counter > 99:
            change = int(counter/100)
            self.zero_count += change
            print(f" R at {counter} > 99 | Change: [{change}]")
        elif counter < 0:
            change = int(((-counter)+100)/100)
            if started_on_0 and change > 0:
                change -= 1
            self.zero_count += change
            print(f" L at {counter} < 0 | Change: [{change}]")
        elif counter == 0:
            self.zero_count += 1
            print(f" On top of zero | Change: [1]")
        
        while not (counter <= 99 and counter >= 0):
            if counter > 99 and counter >= 0:
                counter = 0 + (counter - 100)
            elif counter < 0:
                counter = 100 + counter
        return counter

    def __str__(self):
        return str(self.__dict__)

class Runner:
    def __init__(self):
        try:
            self.loader = AOCLoader(year=YEAR, day=DAY)
            self.puzzle_input, self.eg_input = self.loader.load_input()
            print(f"Success! Input starts with: {self.puzzle_input[:20]}...")
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
        print(f"{label} Execution Time: {duration_ms:.4f} ms")
        print("=============================================")
        return result