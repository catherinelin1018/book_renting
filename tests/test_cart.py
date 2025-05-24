import pytest
from book_renting.cart import Cart
from book_renting.item import Item

@pytest.fixture
def cart():
    database = "./tests/test_database.json"
    cart = Cart(database)
    cart.empty_cart()
    return cart

def test_empty_cart(cart):
    item = Item("a", "b", "c", 16)
    cart.add_item_to_cart(item)
    cart.empty_cart()
    assert len(cart.get_all_items()["Items"].items()) == 0

def test_search_item(cart): ### check this
    item = Item("The Door in the Forest", "Roderick Townley", "Fantasy", 9)
    cart.add_item_to_cart(item)
    items_list = cart.search_items("the door in the forest")
    assert items_list[0].name == "The Door in the Forest"

def test_get_all_items(cart):
    item1 = Item("Emma", "Jane Austen", "Romance", 16)
    item2 = Item("A Forgery of Fate", "Elizabeth Lim", "Fantasy", 12)
    cart.add_item_to_cart(item1)
    cart.add_item_to_cart(item2)
    retrieved_items = cart.get_all_items()
    names_to_compare = [item1.name, item2.name]
    results = [item_data["name"] for item_id, item_data in retrieved_items["Items"].items()]
    assert names_to_compare == results

def test_get_total_item_count(cart):
    item1 = Item("The Door in the Forest", "Roderick Townley", "Fantasy", 9)
    item2 = Item("A Constant Love", "Tracie Peterson", "Historical Romance", 18)
    cart.add_item_to_cart(item1)
    cart.add_item_to_cart(item2, user_age=22)
    assert cart.get_total_items_count() == 2