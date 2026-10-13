import math
import sys
DEBUG_MODE = False


def innit():
    global score, shield_points, shield_health, full_health, DEBUG_MODE
    score = 0
    shield_points = 0
    shield_health = 0
    full_health = 0
    DEBUG_MODE = False
    difficulty = input("Please select a difficulty level:\n1: Easy\n2: Medium\n3: Hard\n4: Debug\n")
    if difficulty == "1":
        print("You have selected Easy difficulty. You will need to reach 50 HP to complete your quest.")
        full_health = 50
    elif difficulty == "2":
        print("You have selected Medium difficulty. You will need to reach 75 HP to complete your quest.")
        full_health = 75
    elif difficulty == "3":
        print("You have selected Hard difficulty. You will need to reach 100 HP to complete your quest.")
        full_health = 100
    elif difficulty == "4":
        DEBUG_MODE = True
        print("You have selected Debug difficulty. Extra debug prints will show each password score and health change.")
        full_health = 40
    else:
        print("Invalid selection. Defaulting to Easy difficulty. You will need to reach 50 HP to complete your quest.")
        full_health = 50
    print("You are an apprentice security mage forging a powerful shield to defend the realm. Each password you craft adds HP to your shield. Reach " + str(full_health) + " HP to complete your quest.")


def log(password):
    with open("password_log.txt", "a") as file:
        file.write(password + "\n")

def show_menu():
    print("Menu Options:\n1: Enter a password\n2: Learn how to make good passwords\n3: Check shield health\n4: Quit")
    return input("Please select an option:\n")

def check_common_passwords(password):
    with open("common_passwords.txt", "r") as file:
        for line in file:
            if password.strip() == line.strip():
                if DEBUG_MODE:
                    print(f"DEBUG: password='{password}' is a common password")
                return True
    if DEBUG_MODE:
        print(f"DEBUG: password='{password}' is not a common password")
    return False

def do_menu():
    global shield_health
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
        return


def ask_password():
    return input("Please enter a password:\n")
    


def check_character_diversity(password):
    score = 0
    previous_char = None
    for char in password:
        if previous_char is not None and char == previous_char:
            score -= 1
        previous_char = char
    return score

def entropy(password):
    if not password:
        return 0.0
    counts = {}
    for char in password:
        counts[char] = counts.get(char, 0) + 1

    total = len(password)
    entropy_value = 0.0
    for count in counts.values():
        probability = count / total
        entropy_value -= probability * math.log2(probability)
    return entropy_value * total

def score_password(password):
    log(password)

    score = 0
    missing = []

    if len(password) < 8:
        missing.append("too short")
    else:
        score += 1

    if any(char.isupper() for char in password):
        score += 1
    else:
        missing.append("no uppercase letters")

    if any(char.islower() for char in password):
        score += 1
    else:
        missing.append("no lowercase letters")

    if any(char.isdigit() for char in password):
        score += 1
    else:
        missing.append("no numbers")

    if len(password) >= 8 and any(char.isdigit() for char in password):
        score += 1

    if entropy(password) > 75:
        score += 1

    if check_common_passwords(password):
        score -= 2
        missing.append("common password")

    score += check_character_diversity(password) * 0.1

    if DEBUG_MODE:
        print(f"DEBUG: password='{password}', score={score}, entropy={entropy(password):.2f}, diversity={check_character_diversity(password)}")

    for item in missing:
        print(f"Your password is missing: {item}")
    return max(score, 0)


def convert_points_to_health(points):
    health_values = [-5, 2, 5, 10, 20, 30, 45]
    strength_strings = ["extremely weak", "very weak", "weak", "moderate", "strong", "very strong", "extremely strong"]
    clamp_index = max(0, min(int(points), len(health_values) - 1))
    health = health_values[clamp_index]
    label = strength_strings[clamp_index] if clamp_index < len(strength_strings) else "Unknown"
    if DEBUG_MODE:
        print(f"DEBUG: password strength={label}, raw_points={points}, health_gain={health}")
    print(f"This password is {label}\n")
    return health


def game():
    global shield_health, full_health
    while shield_health < full_health:
        do_menu()

    print(f"Shield health: {shield_health}/{full_health}")
    print("Your Phoenix Aegis is complete! The realm is safe.")


if __name__ == "__main__":
    innit()
    game()