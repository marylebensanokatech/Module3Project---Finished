# Store our ice cream shop's menu items
flavors = [
    "vanilla", "caramel", "mint",
    "chocolate chip", "strawberry swirl", "cookie dough"  # Added three new flavors
]
toppings = ["sprinkles", "nuts", "cherry"]
prices = {
    "scoop": 2.50,
    "topping": 0.50,
    "cake_cone": 0.00,    # Cake cone is free (base option)
    "sugar_cone": 0.75,   # Sugar cone costs extra
    "waffle_cone": 1.50   # Waffle cone costs the most
}

class IceCream:
    """Base class for ice cream orders"""
    def __init__(self, scoops, flavors, toppings, cone_type):
        self.scoops = scoops
        self.flavors = flavors
        self.toppings = toppings
        self.cone_type = cone_type
    
    def calculate_cost(self):
        """Calculate the base cost of the ice cream"""
        scoop_cost = self.scoops * prices["scoop"]
        topping_cost = len(self.toppings) * prices["topping"]
        cone_cost = prices[f"{self.cone_type}_cone"]
        subtotal = scoop_cost + topping_cost + cone_cost
        
        # Apply 10% discount for orders over $10
        if subtotal > 10:
            return subtotal * 0.9
        return subtotal

class Sundae(IceCream):
    """Special sundae combinations that inherit from IceCream"""
    SPECIAL_COMBINATIONS = {
        "banana_split": {
            "scoops": 3,
            "flavors": ["vanilla", "chocolate chip", "strawberry swirl"],
            "toppings": ["nuts", "cherry"],
            "cone_type": "cake",
            "description": "Classic banana split with three flavors and traditional toppings"
        },
        "triple_chocolate": {
            "scoops": 3,
            "flavors": ["chocolate chip"] * 3,
            "toppings": ["sprinkles"],
            "cone_type": "waffle",
            "description": "Triple scoop of chocolate chip in a waffle cone"
        }
    }
    
    def __init__(self, sundae_type):
        """Initialize a special sundae combination"""
        if sundae_type not in self.SPECIAL_COMBINATIONS:
            raise ValueError("Invalid sundae type")
        
        combo = self.SPECIAL_COMBINATIONS[sundae_type]
        super().__init__(
            combo["scoops"],
            combo["flavors"],
            combo["toppings"],
            combo["cone_type"]
        )
        self.sundae_type = sundae_type
        self.description = combo["description"]

def display_menu():
    """Shows available flavors, toppings, and cone options to the customer"""
    print("\n=== Welcome to the Ice Cream Shop! ===")
    print("\nAvailable Flavors:")
    for flavor in flavors:
        print(f"- {flavor}")
    
    print("\nAvailable Toppings:")
    for topping in toppings:
        print(f"- {topping}")
    
    print("\nCone Options:")
    print(f"- Cake Cone (Free)")
    print(f"- Sugar Cone (${prices['sugar_cone']:.2f} extra)")
    print(f"- Waffle Cone (${prices['waffle_cone']:.2f} extra)")
    
    print("\nPrices:")
    print(f"Scoops: ${prices['scoop']:.2f} each")
    print(f"Toppings: ${prices['topping']:.2f} each")
    print("\n10% discount on orders over $10!")

def search_flavor():
    """Allows customers to search for their favorite flavor"""
    search_term = input("\nEnter a flavor to search for: ").lower()
    matching_flavors = [f for f in flavors if search_term in f]
    
    if matching_flavors:
        print("\nMatching flavors found:")
        for flavor in matching_flavors:
            print(f"- {flavor}")
    else:
        print("\nNo matching flavors found. Try another search!")

def get_cone_type():
    """Gets the customer's cone preference"""
    while True:
        print("\nChoose your cone type:")
        print("1. Cake Cone")
        print("2. Sugar Cone")
        print("3. Waffle Cone")
        
        try:
            choice = int(input("Enter the number of your choice: "))
            if choice == 1:
                return "cake"
            elif choice == 2:
                return "sugar"
            elif choice == 3:
                return "waffle"
            print("Please choose 1, 2, or 3.")
        except ValueError:
            print("Please enter a number.")

def get_flavors():
    """Gets ice cream flavor choices from the customer"""
    chosen_flavors = []
    while True:
        try:
            num_scoops = int(input("\nHow many scoops would you like? (1-3): "))
            if 1 <= num_scoops <= 3:
                break
            print("Please choose between 1 and 3 scoops.")
        except ValueError:
            print("Please enter a number.")
    
    print("\nFor each scoop, enter the flavor you'd like:")
    for i in range(num_scoops):
        while True:
            flavor = input(f"Scoop {i+1}: ").lower()
            if flavor in flavors:
                chosen_flavors.append(flavor)
                break
            print("Sorry, that flavor isn't available.")
    
    return num_scoops, chosen_flavors

def get_toppings():
    """Gets topping choices from the customer"""
    chosen_toppings = []
    while True:
        topping = input("\nEnter a topping (or 'done' if finished): ").lower()
        if topping == 'done':
            break
        if topping in toppings:
            chosen_toppings.append(topping)
            print(f"Added {topping}!")
        else:
            print("Sorry, that topping isn't available.")
    
    return chosen_toppings

def print_receipt(ice_cream):
    """Prints a nice receipt for the customer"""
    print("\n=== Your Ice Cream Order ===")
    
    # Print sundae name and description if it's a sundae
    if isinstance(ice_cream, Sundae):
        print(f"Special Sundae: {ice_cream.sundae_type.replace('_', ' ').title()}")
        print(f"Description: {ice_cream.description}")
    
    # Print scoops and flavors
    for i in range(ice_cream.scoops):
        print(f"Scoop {i+1}: {ice_cream.flavors[i].title()}")
    
    # Print cone type
    print(f"\nCone: {ice_cream.cone_type.title()} Cone")
    
    # Print toppings
    if ice_cream.toppings:
        print("\nToppings:")
        for topping in ice_cream.toppings:
            print(f"- {topping.title()}")
    
    # Calculate and display total
    total = ice_cream.calculate_cost()
    print(f"\nSubtotal: ${total:.2f}")
    if total < ice_cream.calculate_cost() * 1.1:  # Check if discount was applied
        print("10% discount applied!")
    
    # Save order to file
    with open("daily_orders.txt", "a") as file:
        file.write(f"\nOrder: {ice_cream.scoops} scoops - ${total:.2f}")

def main():
    """Runs our ice cream shop program"""
    while True:
        display_menu()
        print("\nWhat would you like to do?")
        print("1. Place a regular order")
        print("2. Order a special sundae")
        print("3. Search for a flavor")
        print("4. Exit")
        
        try:
            choice = int(input("Enter your choice (1-4): "))
            
            if choice == 1:
                num_scoops, chosen_flavors = get_flavors()
                chosen_toppings = get_toppings()
                cone_type = get_cone_type()
                ice_cream = IceCream(num_scoops, chosen_flavors, chosen_toppings, cone_type)
                print_receipt(ice_cream)
            
            elif choice == 2:
                print("\nAvailable Sundaes:")
                for sundae_type in Sundae.SPECIAL_COMBINATIONS:
                    print(f"- {sundae_type.replace('_', ' ').title()}")
                
                while True:
                    choice = input("\nEnter sundae name (or 'back' to return): ").lower()
                    if choice == 'back':
                        break
                    try:
                        sundae = Sundae(choice.replace(' ', '_'))
                        print_receipt(sundae)
                        break
                    except ValueError:
                        print("Invalid sundae type. Please try again.")
            
            elif choice == 3:
                search_flavor()
            
            elif choice == 4:
                print("\nThank you for visiting our ice cream shop!")
                break
            
            else:
                print("Please choose a valid option (1-4)")
        
        except ValueError:
            print("Please enter a number.")

if __name__ == "__main__":
    main()
