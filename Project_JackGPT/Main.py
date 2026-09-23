import time, sys

Jeffy = {
  "true": False, 
  "damage": 5
         }
player = {
  "health": 20,
  "damage": 5
         }

def tprint(text):
  for character in text:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.04)
    
quit_statements = ["q", "quit", "exit", "exit game"]

def qinput(prompt):
  tprint(prompt)
  u = input()
  if u in quit_statements:
    sys.exit("User Exited")
  return u

def intput(prompt):
  i = True
  while i:
    u = qinput(prompt)
    try:
      u = int(u)
      i = False
      return u
    except ValueError:
      tprint("Please input a number\n")

def statcheck(user):
  tprint("====================================================================================================\n")
  tprint(f"Name: {user} \nCareer:  D.A.F.D.A.L.U. (Dumpsters Association for DumbAsses Like You)\n")
  tprint(f"Vehicle: Magic carpet\nAdress: Random Burger King Parking lot\nHealth: {player['health']}\nDamage: {player['damage']}\n")

def fight(enemy, enemy_damage, enemy_health, player_health, player_damage):
  tprint(f"You are fighting {enemy}\n")
  tprint(f"{enemy} Health: {enemy_health}\nYour Health: {player_health}\n")
  tprint("Options:\n1:Attack\n2:Defend\n3:Run\n")
  option = intput("")
  if option == 1:
    tprint(f"You attack {enemy} for {player_damage} damage\n")
    enemy_health -= player_damage
    if enemy_health <= 0:
      tprint(f"You have defeated {enemy}\n")
      return True
    else:
      tprint(f"{enemy} attacks you for {enemy_damage} damage\n")
      player_health -= enemy_damage
      if player_health <= 0:
        sys.exit("GAME OVER: You died")
      else:
        return fight(enemy, enemy_damage, enemy_health, player_health, player_damage)  
  elif option == 2:
    tprint(f"You defend against {enemy}'s attack\n")
    player_health -= enemy_damage / 2
    if player_health <= 0:
      sys.exit("GAME OVER: You died")
      return False
    else:
      return fight(enemy, enemy_damage, enemy_health, player_health, player_damage)
  elif option == 3:
    tprint(f"You run away from {enemy}\n")
    return player_health
  else:
    tprint("Invalid option\n")
    return fight(enemy, enemy_damage, enemy_health, player_health, player_damage)

def game():
  user = qinput("please input your name: ")
  tprint("Welcome to Project J.A.C.K. GPT. If you want to quit at any time input q\n")
  statcheck(user)

  tprint("Today while you were at work your co-worker, Jeffy, climbed out of a dumpster covered in sludge. He had placed a milk jug on his back, and told you he was a snail. He asks you to throw salt on him and call him a bad boy\nOptions:\n1:Play Along\n2:Report him to HR\n3:Ignore him\n4:Play the Banjo in a summer breeze\n")
  try:
    option = intput("")
    if option == 1:
      tprint("Jeffy got scared and ran away.")
      time.sleep(3)
      tprint(" He came back from behind you and ate you\n")
      sys.exit("GAME OVER: You died")
    elif option == 2:
      tprint("You call HR to report him, as you raise your phone to your ear jeffy sees who you are calling and lunges at you, accidentally snaping your neck in the proccess\n")
      sys.exit("GAME OVER: You died")
    elif option == 3:
      tprint("Jeffy snarls at you as you walk away")
    else:
      tprint("the music hypnotizes jeffy, he will now follow you. (+5 to all attack damage)\n")
      Jeffy["true"] = True
      player["damage"] += 5
  except Exception as e:
    print(f"ERROR: {e}")
  try:
    tprint("Later that day you find your ex upside down in a dumpster passed out. \noptions:\n1: Call 911\n2: Call 988 because your sad\n3: Not your problem\n4: Feed her to jeffy\n")
    option = intput("")
    if option == 1:
      tprint("You call 911 and they arrive in 5 minutes, they take her to the hospital and she of alcohol poisoning\n")
    elif option == 2:
      tprint("You call 988 and they give you a pep talk\n")
    elif option == 3:
      tprint("You walk away and jeffy eats her\n")
    else:
      tprint("Jeffy eats her\n")
      if Jeffy["true"] == True:
        tprint("Jeffy is has evolved (+10 to all attack damage)\n")
        Jeffy["damage"] += 5
  except Exception as e:
    print(f"ERROR: {e}")
  tprint("Your shift has ended and you walk back to the Burger King parking lot. Your parents are gone and when you get closer you find a note laying in they're place, it reads: 'Property of the J.A.C.K.' You go back the the magic carpet and look at your parents side of it and  find a giant bulletin board full of propaganda and stuff, and see they found a superweapon called “JackGPT and they think it is the end of humanity. ")
  tprint("You decide to be heroic and also you miss your family so you go find them, but your magic carpet doesn’t have gas and you don’t feel like spending that much money so you go on foot. You take your trusty cardboard shield(+5 health) and hope to upgrade it along the way\n")
  tprint("after a while, as you pass a shady ally and a homeless tweaker jumps out of a dumpster and attacks you. You have no choice but to fight him\n")
  player["health"] += 5
  fight("Homeless Tweaker", 5, 10, player["health"], player["damage"])
  tprint("you search the dumster the tweaker came out of and find a used needle(+10 to attack damage) and a cast iron pan(+10 to health)\n")
  player["health"] += 10
  player["damage"] +=10
  tprint("You have left boring oregon and set off towards mexico on Interstate 69")



if __name__ == "__main__":
  while True:
    game()
