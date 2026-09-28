import time, sys

user = ""
tprintDel = 0.07
DEBUG_SKIP = 0
DEBUG_SECTIONS = [
  "jeffy_scene",
  "ex_scene",
  "family_scene",
  "fight_scene",
  "camp_scene",
  "portal_scene",
  "flash_scene"
]

Jeffy = {
  "true": False, 
  "damage": 5,
  "tier": 0,
  "tiers": ["Jeffy", "Jeffry", "Jeffred", "Geoffry"]
         }
def getJeffy():
  Jeffy["name"] = Jeffy["tiers"][Jeffy["tier"]]
  return (Jeffy["name"])

Tom = {
  "true": False,
  "damage": 10
}
player = {
  "health": 20,
  "damage": 5
         }

def set_debug_mode(username):
  global DEBUG_SKIP, tprintDel
  DEBUG_SKIP = 0
  tprintDel = 0.07

  if not isinstance(username, str):
    return

  name = username.strip().lower()
  if name.startswith("test") and name[4:].isdigit():
    DEBUG_SKIP = int(name[4:])
    tprintDel = 0.01


def skip_section(section_name):
  if DEBUG_SKIP <= 0:
    return False
  if section_name not in DEBUG_SECTIONS:
    return False
  return DEBUG_SECTIONS.index(section_name) < DEBUG_SKIP


def tprint(text, speed=None):
  global tprintDel
  delay = tprintDel if speed is None else speed
  for character in text:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(delay)


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
def statcheck():
  global user
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
  global user, player, Jeffy, Tom, tprintDel
  user = qinput("please input your name: ")
  set_debug_mode(user)
  tprint("Welcome to Project J.A.C.K. GPT. If you want to quit at any time input q\n")
  statcheck()

  if not skip_section("jeffy_scene"):
    tprint(f"Today while you were at work your co-worker, {getJeffy()}, climbed out of a dumpster covered in sludge. He had placed a milk jug on his back, and told you he was a snail. He asks you to throw salt on him and call him a bad boy\nOptions:\n1:Play Along\n2:Play the Banjo in a summer breeze\n3:Report him to HR\n4:Ignore him\n")
    try:
      option = intput("")
      if option == 1:
        tprint(f"{getJeffy()} got scared and ran away.")
        time.sleep(3)
        tprint(" He came back from behind you and ate you\n")
        sys.exit("GAME OVER: You died")
      elif option == 2:
        tprint(f"the music hypnotizes {getJeffy()}, he will now follow you. (+5 to all attack damage)\n")
        Jeffy["true"] = True
        player["damage"] += 5
      elif option == 3:
        tprint(f"You call HR to report him, as you raise your phone to your ear {getJeffy()} sees who you are calling and lunges at you, accidentally snaping your neck in the proccess\n")
        sys.exit("GAME OVER: You died")
      else:
        tprint("Jeffy snarls at you as you walk away")
    except Exception as e:
      print(f"ERROR: {e}")

  if not skip_section("ex_scene"):
    try:
      tprint("Later that day you find your ex upside down in a dumpster passed out. \noptions:\n1: Call 911\n2: Call 988 because your sad\n3: Not your problem\n4: Feed her to jeffy\n")
      option = intput("")
      if option == 1:
        tprint("You call 911 and they arrive in 5 minutes, they take her to the hospital and she of alcohol poisoning\n")
      elif option == 2:
        tprint("You call 988 and they give you a pep talk\n")
      elif option == 3:
        tprint(f"You walk away and {getJeffy()} eats her\n")
      else:
        tprint("Jeffy eats her\n")
        if Jeffy["true"] == True:
          Jeffy["tier"] += 1
          tprint(f"Jeffy is has evolved to a {getJeffy()} (+10 to all attack damage)\n")
          Jeffy["damage"] += 5
    except Exception as e:
      print(f"ERROR: {e}")

  if not skip_section("family_scene"):
    tprint("Your shift has ended and you walk back to the Burger King parking lot. Your parents are gone and when you get closer you find a note laying in they're place, it reads: 'Property of the J.A.C.K.' You go back the the magic carpet and look at your parents side of it and  find a giant bulletin board full of propaganda and stuff, and see they found a superweapon called “JackGPT and they think it is the end of humanity. ")
    tprint("You decide to be heroic and also you miss your family so you go find them, but your magic carpet doesn’t have gas and you don’t feel like spending that much money so you go on foot. You take your trusty cardboard shield(+5 health) and hope to upgrade it along the way\n")
    tprint("after a while, as you pass a shady ally and a homeless tweaker jumps out of a dumpster and attacks you. You have no choice but to fight him\n")
    player["health"] += 5

  if not skip_section("fight_scene"):
    fight("Homeless Tweaker", 5, 10, player["health"], player["damage"])

  if not skip_section("camp_scene"):

    tprint("you search the dumster the tweaker came out of and find a used needle(+10 to attack damage) and a cast iron pan(+10 to health)\n")
    player["health"] += 10
    player["damage"] +=10
    tprint("You have left boring oregon and set off towards mexico on Interstate 69\n")
    tprint("You find the road that lead to the tweaker civilization and you have to get in so you put on the homeless tweaker's clothes.\nWhen you get to the camp, you see a ton of the homeless tweakers making out with female musk-oxes. You try to join the party. You can either:\n1: Go find a male ox name Tom and bribe him to help you on your journey.\n2: Have a fun night with an ox\n3: Go make out with one of the oxes\n")
    try:
      option = intput("")
      if option == 3:
        tprint("You have a nice kiss but nothing comes of it...\n")
        option = intput("")
      if option == 1:
        tprint("You go find tom and give him a fun time, and afterword he comes with you on your journey.(+10 to attack damage)\n")
        player["damage"] += 10
        Tom["true"] = True
      if option == 2:
        tprint("You have a fun night with the ox but it senses you have an std and kicks you, killing you.\n")
        sys.exit("GAME OVER: You died")
    except Exception as e:
      print(f"ERROR: {e}")

  if not skip_section("portal_scene"):
    tprint("you ride Tom to the other side of the camp and find a pocket portal gaurded by a fat homeless dude. You must fight him to reach the portal.\n")
    fight("Fat Homeless Dude", 10, 40, player["health"], player["damage"])
    tprint("You enter the portal and a nauseating stobing effect happens for a few seconds. ")
    time.sleep(3)
  if not skip_section("flash_scene"):
    tprint("You find yourself face to face with the flash, and before you can react he he picks you up and your smelly clothes burn off in the friction of speed as he takes you somewhere.\n")
if __name__ == "__main__":
  game()
