class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        if item not in self.items:
            self.items.append(item)
            print(f"{item} added to cart.")
        else:
            print(f"{item} is already in the cart.")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"{item} removed from cart.")
        else:
            print(f"{item} is not in the cart.")

    def get_items(self):
        return self.items
