import sys
score = 0
shield_points = 0
shield_health = 0

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

while shield_health < full_health:
    choice = input("Menu Options:\n1: Enter a password\n2: Learn how to make good passwords\n3: Check shield health\n4: Quit\n")
    if choice == "1":
        pas = input("Please enter a password:\n")
        score = 0  

        missing = ["too short", "no uppercase letters", "no lowercase letters", "no numbers"]

        if len(pas) >= 8:
            score += 1
            missing.remove("too short")
        if any(char.isupper() for char in pas):
            score += 1
            missing.remove("no uppercase letters")
        if any(char.islower() for char in pas):
            score += 1
            missing.remove("no lowercase letters")
        if any(char.isdigit() for char in pas):
            score += 1
            missing.remove("no numbers")
            if len(pas) >= 8:
                score += 1
        for item in missing:
            print(f"Your password is missing: {item}")
        if score == 1:
            shield_points = 2
            print("This password is very weak, try again")

        elif score == 2:
            shield_points = 5
            print("This password is not strong, try again")
        elif score == 3:
            shield_points = 10
            print("this password is decent, but keep trying to make it better!")

        else:
            shield_points = 20 
            print("This password is very strong, great job!")

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