import json
import os
from dataclasses import dataclass, field

@dataclass
class Fstream:
    name: str
    path: str
    extension: str
    data_file: str = field(init=False)

    @classmethod
    def load_json_files(cls, path) -> dict:
        """
        Read json files from a directory.
        Args:
            path: str : the path for the json file to read.
        Returns:
            dict: A hash map with the json structure.
        """
        with open(path, "rb") as f:
            cls.data_file = json.load(f)
        
        return cls.data_file
    
    @staticmethod
    def print_json_structure(data_file):
        for id, item in data_file["Items"].items():
            print(id, item)

if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)  
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir)) 
    path = os.path.join(parent_dir, "database.json") 
    print(Fstream.load_json_files(path))