import sys

def innit():
    global score, shield_points, shield_health, full_health
    score = 0
    shield_points = 0
    shield_health = 0
    full_health = 0
    difficulty = input("Please select a difficulty level:\n1: Easy\n2: Medium\n3: Hard\n")
    if difficulty == "1":
        print("You have selected Easy difficulty. You will need to reach 50 HP to complete your quest.")
        full_health = 50
    elif difficulty == "2":
        print("You have selected Medium difficulty. You will need to reach 75 HP to complete your quest.")
        full_health = 75
    elif difficulty == "3":
        print("You have selected Hard difficulty. You will need to reach 100 HP to complete your quest.")
        full_health = 100
    print("You are an apprentice security mage forging a powerful shield to defend the realm. Each password you craft adds HP to your shield. Reach " + str(full_health) + " HP to complete your quest.")


def show_menu():
    print("Menu Options:\n1: Enter a password\n2: Learn how to make good passwords\n3: Check shield health\n4: Quit")
    return input("Please select an option:\n")

def do_menu():
    choice = show_menu()
    if choice == "1":
        pas = ask_password()
        score = score_password(pas)
        shield_points = convert_points_to_health(score)
        shield_health += shield_points
    elif choice == "2":
        print("To create a strong password, follow these tips:\n- Use at least 8 characters\n- Include a mix of uppercase and lowercase letters\n- Include numbers\n")
    elif choice == "3":
        print(f"Shield health: {shield_health}/{full_health}")
    else:
        sys.exit("Exiting the program. Goodbye!")

def ask_password():
    return input("Please enter a password:\n")

def score_password(password):
    score = 0
    missing = ["too short", "no uppercase letters", "no lowercase letters", "no numbers"]

    if len(password) >= 8:
        score += 1
        missing.remove("too short")
    if any(char.isupper() for char in password):
        score += 1
        missing.remove("no uppercase letters")
    if any(char.islower() for char in password):
        score += 1
        missing.remove("no lowercase letters")
    if any(char.isdigit() for char in password):
        score += 1
        missing.remove("no numbers")
        if len(password) >= 8:
            score += 1
    for item in missing:
        print(f"Your password is missing: {item}")
    return score

def convert_points_to_health(points):
    health_values = [2, 5, 10, 20]
    strength_strings = ["Weak", "Moderate", "Strong", "Very Strong"]
    health = health_values[points - 1] if 1 <= points <= len(health_values) else 0
    print(f"This password is {strength_strings[points - 1] if 1 <= points <= len(strength_strings) else 'Unknown'}\n")
    return health

def game():
    global shield_health, full_health
    while shield_health < full_health:
        choice = show_menu()
        if choice == "1":
            pas = ask_password()
            score = score_password(pas)
            shield_points = convert_points_to_health(score)
            shield_health += shield_points
        elif choice == "2":
            print("To create a strong password, follow these tips:\n- Use at least 8 characters\n- Include a mix of uppercase and lowercase letters\n- Include numbers\n")
        elif choice == "3":
            print(f"Shield health: {shield_health}/{full_health}")
        else:
            sys.exit("Exiting the program. Goodbye!")
        
        score = 0  
        
    print(f"Shield health: {shield_health}/{full_health}")
    print("Your Phoenix Aegis is complete! The realm is safe.")

if __name__ == "__main__":
    innit()
    game()