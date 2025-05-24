from book_renting.item import Item

def test_item_name() -> None:
    item = Item("a", "b", "c", 16)
    assert len(item.name) > 0