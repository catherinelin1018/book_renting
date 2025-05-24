import json
from typing import Optional
from dataclasses import dataclass, field
from book_renting.item import Item
from book_renting.random_number_utils import RandomUtils
from book_renting.file_io import Fstream

@dataclass
class Cart:
    database_path: str
    isEmpty: bool = True
    isActive: bool = False
    id: str = field(init=False, default_factory=RandomUtils.generate_random_id)

    def read_file(self) -> dict:
        """
        Read json file from database

        Returns:
            dict: get items from database
        """
        return Fstream.load_json_files(self.database_path)

    def get_all_items(self, verbose=0) -> dict:
        """
        Reads and returns a hash map with all the available items

        Args:
            if verbose is set to 1, it will print all the items..

        Returns:
            dict: a hash map with all the items in the database.
        """
        data_file = self.read_file()
        print(data_file)

        if len(data_file.items()) > 0:
            self.isEmpty = False
            self.isActive = True

        try:
            if verbose == 1:
                Fstream.print_json_structure(data_file)
                return data_file
            else:
                return data_file

        except:
            raise ValueError("The value for the verbose as to be 0 or 1")
        
    def search_items(self, query: str) -> list[Item]:
        """
        
        """
        data = self.read_file()
        matching_items = []
        for item_id, item_data in data["Items"].items():
            item = Item(name=item_data["name"], author=item_data["author"], type=item_data["type"], _age_rating=["age_rating"], id=item_id)
            if query.lower() in item.search_string.lower():
                matching_items.append(item)
        
        if len(matching_items) == 0:
            print("The book is not found")
        else:
            for item in matching_items:
                print(f"Found: {item.name} wrote by {item.author} fall under {item.type}, and the age-rating is {item._age_rating}+")

        return matching_items
    
    def get_total_items_count(self) -> int:
        """
        The total number of books in your cart

        Returns:
            int: Total books in your cart
        """
        data = self.get_all_items()
        return len(data["Items"].items())
    
    def add_item_to_cart(self, item:Item, user_age: Optional[int] = None):
        """
        Add an item to the cart and updates the database.json file.

        Args:
            item(Item): The item to add to the cart.
        """
        data = self.read_file()

        new_item = {
            "name": item.name,
            "author": item.author,
            "type": item.type,
            "age_rating": item._age_rating
        }
        if new_item["age_rating"] == 18:
            if user_age == None:
                try:
                    user_age = int(input("Please provide your age - Example: 22\n :"))
                except:
                    raise ValueError("You need to provide your age")
            if user_age >= 18:
                data["Items"][item.id] = new_item
                with open(self.database_path, "w") as f:
                    json.dump(data, f, indent=4)
            else:
                return "Sorry you cannot rent his book yet."
        else:
            data["Items"][item.id] = new_item

            with open(self.database_path, "w") as f:
                json.dump(data, f, indent=4)

        self.isEmpty = False
        self.isActive = True

        print(f"Added {item.name} to the cart.")

    def remove_items_from_cart_by_query(self, query: str):
        """
        Removes all the instances of an item from the cart based on a query.

        Args:
            query(str): The search query to find the item to remove.
        """
        data = self.read_file()
        items_to_remove = []

        for item_id, item_data in data["Items"].items():
            if query.lower() in item_data["name"].lower() or query.lower() in item_data["author"].lower() or query.lower() in item_data["type"].lower() or int(query) in item_data["age_rating"]:
                items_to_remove.append(item_id)

        if not items_to_remove:
            print(f"No items found matching '{query}'")

        for item_id in items_to_remove:
            item_name = data["Items"][item_id]["name"]
            del data["Items"][item_id]
            print(f"Removed {item_name} from the cart.")

        with open(self.database_path, "w") as f:
            json.dump(data, f, indent=4)

        if not data["Items"]:
            self.isEmpty = True
            self.isActive = False

    def remove_items_from_cart_by_selection(self):
        """
        Removes the selected item by index.
        """
        data = self.read_file()
        items = []
        i = 1
        for item_id, item_data in data["Items"].items():
            items.append(item_id)
            print(f"{i}: {item_data}")
            i += 1
        try:
            user_choice = int(input("Select the item to delete by number example: 0 \n:")) - 1
        except:
            raise ValueError("You must selecta valid number!")
        
        if user_choice > len(items):
            print("Item not found!")
            return
        
        item_to_delete = items[user_choice]
        item_name = data["Items"][item_to_delete]["name"]
        del data["Items"][item_to_delete]
        print(f"Removed {item_name} from the cart.")

        with open(self.database_path, "w") as f:
            json.dump(data, f, indent=4)

        if not data["Items"]:
            self.isEmpty = True
            self.isActive = False

    def empty_cart(self):
        """
        Clear all the items in the cart.
        """
        data = self.get_all_items()
        if len(data["Items"].items()) > 0:
            data = {"Items": {}}

            with open(self.database_path, "w") as f:
                json.dump(data, f, indent=4)

            if not data["Items"]:
                self.isEmpty = True
                self.isActive = False
            print("The cart is empty")
        else:
            print("The cart is already empty")