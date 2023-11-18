from shopping_cart import ShoppingCart

def main():
    cart = ShoppingCart()
    available_items = ['giraffe', 'elephant', 'monkey', 'dinosaur']

    while True:
        print("\nAvailable actions:")
        print("1. Show available items")
        print("2. Add item to cart")
        print("3. Remove item from cart")
        print("4. Show cart items")
        print("5. Save and exit")

        choice = input("Choose an option: ")

        if choice == '1':
            print("Available items:", ", ".join(available_items))
        elif choice == '2':
            item = input("Enter the item to add to your cart: ")
            if item in available_items:
                cart.add_item(item)
            else:
                print("Item not available.")
        elif choice == '3':
            item = input("Enter the item to remove from your cart: ")
            cart.remove_item(item)
        elif choice == '4':
            print("Items in cart:", ", ".join(cart.get_items()))
        elif choice == '5':
            with open('cart_items.txt', 'w') as f:
                f.write('\n'.join(cart.get_items()))
            print("Cart items saved. Exiting program.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()

######
## 연결이 되어있는지 확인 하는 프로그램 추가???? or mater_control.py 에서 시작전?