import requests
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class AOCLoader:
    def __init__(self, year: int, day: int, session_cookie: str = None):
        self.year = year
        self.day = day
        self.session_cookie = session_cookie or os.getenv('AOC_SESSION')
        if not self.session_cookie:
            raise ValueError("No session cookie found. Please provide it as an argument or set 'AOC_SESSION' in your .env file.")
        self.input_data = None
        self.eg_data = None
        self.cache_dir = Path(f"./aoc_inputs/{year}")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / f"day_{day}.txt"
        self.eg_file = self.cache_dir / f"day_{day}_eg.txt"

    def load_input(self) -> str:
        """
        Loads input from the local cache if it exists; otherwise fetches from the server.
        Stores the result in self.input_data and returns it.
        """
        if self.cache_file.exists():
            print(f"Reading input for Day {self.day} from cache...")
            with open(self.cache_file, 'r') as f:
                self.input_data = f.read().strip()
        else:
            print(f"Fetching input for Day {self.day} from server...")
            self._fetch_from_server()

        if self.eg_file.exists():
            print(f"Reading example for Day {self.day} from cache...")
            with open(self.eg_file, 'r') as f:
                self.eg_data = f.read().strip()
        else:
            print(f"Example Data not available...")
        return self.input_data, self.eg_data

    def _fetch_from_server(self):
        url = f"https://adventofcode.com/{self.year}/day/{self.day}/input"
        # HEADERS ARE CRITICAL: 
        # 1. Cookie: To identify who you are.
        headers = {
            "Cookie": f"session={self.session_cookie}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            self.input_data = response.text.strip()
            # Save to cache immediately
            with open(self.cache_file, 'w') as f:
                f.write(self.input_data)
            print("Input fetched and cached successfully.")
        else:
            raise ValueError(f"Failed to fetch input. Status Code: {response.status_code}. Check your session cookie.")