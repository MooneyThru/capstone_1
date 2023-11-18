def choose_item():

    items = ['giraffe', 'elephant', 'monkey', 'dinosaur']
    print("How can I help you~!\n")
    print("we've got three items ; giraffe, elephant, monkey, dinosaur\n")
    while True:
        choice = input("Choose an animal from the list (giraffe, elephant, monkey, dinosaur): ")
        if choice.lower() in items:
            print(f"You have chosen: {choice}")
            return choice

        else:
            print("Invalid choice. Please choose from the list.")