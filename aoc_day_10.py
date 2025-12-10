import time, os, threading, copy, math, pprint, csv
from AOC_Loader import AOCLoader
from collections import deque
from itertools import combinations
import z3

YEAR = 2025
DAY = 10

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
        self.machines = []
        self.min_counter = 0
        for line in self.input:
            split_item = line.split(" ")
            formatted_item = {
                'indicators': "",
                'btn_list': [],
                'joltages': []
            }
            for item in split_item:
                if item.startswith('['):
                    formatted_item['indicators'] = item.strip("[]")
                elif item.startswith('('):
                    formatted_item['btn_list'].append(list(map(int,item.strip("()").split(','))))
                elif item.startswith('{'):
                    formatted_item['joltages'] = list(map(int, item.strip("{}").split(',')))
                else:
                    print(f"WARN - Invalid operator: {item}")
            self.machines.append(formatted_item)
        #pprint.pprint(self.machines)
    
    def solve(self):
        for item in self.machines:
            self.min_counter += self.min_button_presses(item)
        return self.min_counter

    def min_button_presses(self, machine):
        target_mask = 0
        start_state = 0
        button_masks = []
        for i, char in enumerate(machine['indicators']):
            if char == '#':
                target_mask |= (1 << i)
        if start_state == target_mask:
            return 0
        for btn_indices in machine['btn_list']:
            mask = 0
            for idx in btn_indices:
                mask |= (1 << idx)
            button_masks.append(mask)
        queue = deque([(start_state, 0)])
        visited = {start_state}
        while queue:
            current_state, presses = queue.popleft()
            for btn_mask in button_masks:
                # XOR acts like a toggle # 0 ^ 1 = 1 # 0 ^ 1 = 1
                next_state = current_state ^ btn_mask
                if next_state == target_mask:
                    #print(f"next_state:[{next_state:08b}] | target_mask:[{target_mask:08b}] | Depth:[{presses+1}] | MATCHED")
                    return presses + 1
                #print(f"next_state:[{next_state:08b}],target_mask:[{target_mask:08b}] |  | Depth:[{presses+1}]")
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, presses + 1))
        print("ERROR - combination not possible")
        return -1

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
        self.machines = []
        self.min_counter = 0
        for line in self.input:
            split_item = line.split(" ")
            formatted_item = {
                'indicators': "",
                'btn_list': [],
                'joltages': []
            }
            for item in split_item:
                if item.startswith('['):
                    formatted_item['indicators'] = item.strip("[]")
                elif item.startswith('('):
                    formatted_item['btn_list'].append(list(map(int,item.strip("()").split(','))))
                elif item.startswith('{'):
                    formatted_item['joltages'] = list(map(int, item.strip("{}").split(',')))
                else:
                    print(f"WARN - Invalid operator: {item}")
            self.machines.append(formatted_item)
        #pprint.pprint(self.machines)
        
    def solve(self):
        for item in self.machines:
            #self.min_counter += self.min_button_presses_joltage(item)
            #self.min_counter += self.min_button_presses_joltage_v2(item)
            count = self.min_button_presses_z3(item)
            print(f"COUNT:{count}")
            self.min_counter += count
        return self.min_counter

    def min_button_presses_joltage(self, machine):
        target_mask = 0
        target_joltage = machine['joltages']
        start_state = [0 for _ in range(len(target_joltage))]
        if start_state == target_joltage:
            return 0
        queue = deque([(start_state, 0)])
        visited = []
        visited.append(start_state)
        press_log = set()
        while queue:
            current_state, presses = queue.popleft()
            for btn in machine['btn_list']:
                next_state = copy.deepcopy(current_state)
                for wiring in btn:
                    next_state[wiring] += 1
                if next_state == target_joltage:
                    print(f"next_state:[{next_state}], target_mask:[{target_joltage}] | Depth:[{presses+1}] | MATCHED")
                    return presses + 1
                if presses not in press_log:
                    press_log.add(presses)
                    print(f"LOG - Currently at machine: {machine['joltages']} at Depth: {presses+1}")
                if next_state not in visited:
                    visited.append(next_state)
                    queue.append((next_state, presses + 1))
        print("ERROR - combination not possible")
        return -1

    def min_button_presses_z3(self, machine):
        """
        Uses Z3 Constraint Solver to find the minimum button presses 
        for a system of linear equations.
        """
        
        # Create the Solver instance (Optimize allows us to minimize variables)
        optimizer = z3.Optimize()
        
        # Define Variables
        # Create one integer variable for each button in the list
        # x0 represents how many times we press button 0, etc.
        num_buttons = len(machine['btn_list'])
        press_counts = [z3.Int(f'btn_{i}') for i in range(num_buttons)]
        
        # Add Constraints: Non-negative presses
        # You cannot press a button -1 times.
        for p in press_counts:
            optimizer.add(p >= 0)
            
        # Add Constraints: Joltage Equations
        # For each "counter" (joltage index), the sum of contributions must match target
        target_joltages = machine['joltages']
        num_counters = len(target_joltages)
        
        for i in range(num_counters):
            # Build the sum for the i-th counter
            # expression = (btn0_contribution) + (btn1_contribution) + ...
            expression = 0
            for btn_idx, btn_wiring in enumerate(machine['btn_list']):
                # If the current button (btn_idx) affects the current counter (i), add it
                if i in btn_wiring:
                    expression += press_counts[btn_idx]
            optimizer.add(expression == target_joltages[i])
            
        # 5. Objective: Minimize Total Presses
        # We want the sum of all x variables to be as small as possible
        total_presses = z3.Sum(press_counts)
        optimizer.minimize(total_presses)
        
        # 6. Solve
        status = optimizer.check()
        
        if status == z3.sat:
            # Solution found!
            model = optimizer.model()
            # Evaluate the total_presses based on the model and convert to Python int
            return model.eval(total_presses).as_long()
        else:
            # unsat (Impossible configuration)
            return -1

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