import os
import select
import sys
import termios
import time
import tty

user = ""
tprintDel = 0.07
pending_input = ""
DEBUG_SKIP = 0
DEBUG_SECTIONS = [
  "jeffy_scene",
  "ex_scene",
  "family_scene",
  "fight_scene",
  "camp_scene",
  "portal_scene",
  "flash_scene",
  "farm_scene",
  "hawaii_volcano_scene", 
  "chiapapas_scene_1",
  "Headquarters_Exterior_Scene1",
  "Montana_Scene",
  "headquarters_scene1"
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
Wilbur = {
  "true": False,
  "damage": 15
}
  
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
    if DEBUG_SKIP > 0 and not Jeffy["true"]:
      Jeffy["true"] = True
      Key1 = True
      Key2 = True
      Key3 = True
      player["damage"] = 999
      player["health"] = 999

def skip_section(section_name):
  if DEBUG_SKIP <= 0:
    return False
  if section_name not in DEBUG_SECTIONS:
    return False
  return DEBUG_SECTIONS.index(section_name) < DEBUG_SKIP


def tprint(text, speed=None):
  global pending_input, tprintDel
  delay = tprintDel if speed is None else speed
  if not sys.stdin.isatty():
    for character in text:
      sys.stdout.write(character)
      sys.stdout.flush()
      time.sleep(delay)
    return

  input_fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(input_fd)
  try:
    tty.setcbreak(input_fd)
    for index, character in enumerate(text):
      sys.stdout.write(character)
      sys.stdout.flush()
      ready, _, _ = select.select([input_fd], [], [], delay)
      if ready:
        key = os.read(input_fd, 1)
        if key in (b"\n", b"\r"):
          sys.stdout.write(text[index + 1:])
          sys.stdout.flush()
          break
        pending_input += key.decode(errors="replace")
  finally:
    termios.tcsetattr(input_fd, termios.TCSADRAIN, old_settings)


quit_statements = ["q", "quit", "exit", "exit game"]

def qinput(prompt):
  global pending_input
  tprint(prompt)
  u = pending_input + input()
  pending_input = ""
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
      tprint("Please enter a number.\n")
def statcheck():
  global user
  tprint("====================================================================================================\n")
  tprint(f"Name: {user}\nCareer: D.A.F.D.A.L.U. (Dumpsters Association for Dumbasses Like You)\n")
  tprint(f"Vehicle: Magic carpet\nAddress: Random Burger King parking lot\nHealth: {player['health']}\nDamage: {player['damage']}\n")

def fight(enemy, enemy_damage, enemy_health, player_health, player_damage):
  tprint(f"You are fighting {enemy}\n")
  tprint(f"{enemy} Health: {enemy_health}\nYour Health: {player_health}\n")
  tprint("Options:\n1. Attack\n2. Defend\n3. Run\n")
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
  user = qinput("Please enter your name: ")
  set_debug_mode(user)
  tprint("Welcome to Project J.A.C.K. GPT. Enter q at any time to quit.\n\n")
  statcheck()

  if not skip_section("jeffy_scene"):
    tprint(f"At work, your co-worker {getJeffy()} climbs out of a sludge-covered dumpster. He has a milk jug on his back and says he is a snail. He asks you to throw salt on him and call him a bad boy.\n\nOptions:\n1. Play along\n2. Play the banjo in a summer breeze\n3. Report him to HR\n4. Ignore him\n")
    try:
      option = intput("")
      if option == 1:
        tprint(f"{getJeffy()} gets scared and runs away.\n")
        time.sleep(3)
        tprint("He comes back from behind you and eats you.\n")
        sys.exit("GAME OVER: You died")
      elif option == 2:
        tprint(f"The music hypnotizes {getJeffy()}, and he follows you. (+5 attack damage)\n")
        Jeffy["true"] = True
        player["damage"] += 5
      elif option == 3:
        tprint(f"You call HR to report him. As you raise the phone to your ear, {getJeffy()} sees whom you are calling and lunges at you, accidentally snapping your neck.\n")
        sys.exit("GAME OVER: You died")
      else:
        tprint(f"{getJeffy()} snarls at you as you walk away.\n")
    except Exception as e:
      print(f"ERROR: {e}")

  if not skip_section("ex_scene"):
    try:
      tprint(f"Later that day, you find your ex passed out upside down in a dumpster.\n\nOptions:\n1. Call 911\n2. Call 988 because you're sad\n3. Leave her alone\n4. Feed her to {getJeffy()}\n")
      option = intput("")
      if option == 1:
        tprint("You call 911. The responders arrive in five minutes and take her to the hospital because she has alcohol poisoning.\n")
      elif option == 2:
        tprint("You call 988, and they give you a pep talk.\n")
      elif option == 3:
        tprint(f"You walk away, and {getJeffy()} eats her.\n")
      else:
        tprint(f"{getJeffy()} eats her.\n")
        if Jeffy["true"] == True:
          Jeffy["tier"] += 1
          tprint(f"{getJeffy()} has evolved (+10 attack damage).\n")
          Jeffy["damage"] += 5
    except Exception as e:
      print(f"ERROR: {e}")

  if not skip_section("family_scene"):
    tprint("Your shift has ended, so you return to the Burger King parking lot. Your parents are gone. In their place, you find a note that reads, 'Property of the J.A.C.K.' You look at their side of the magic carpet and find a bulletin board covered in propaganda. It says they discovered a superweapon called JackGPT and believe it will end humanity.\n\n")
    tprint("You decide to be a hero. You miss your family, so you set out to find them. Your magic carpet is out of gas, and you do not want to spend that much money, so you travel on foot. You take your trusty cardboard shield (+5 health) and hope to upgrade it along the way.\n\n")
    tprint("After a while, you pass a shady alley. A person jumps out of a dumpster and attacks you. You have no choice but to fight.\n")
    player["health"] += 5

  if not skip_section("fight_scene"):
    fight("Homeless Tweaker", 5, 10, player["health"], player["damage"])

  if not skip_section("camp_scene"):

    tprint("You search the dumpster the attacker climbed out of and find a used needle (+10 damage) and a cast-iron pan (+10 health).\n")
    player["health"] += 10
    player["damage"] += 10
    tprint("You leave boring Oregon and set off toward Mexico on Interstate 69.\n")
    tprint("You find a road leading to a camp and put on the attacker's clothes to sneak inside. When you arrive, you see the campers making out with female musk oxen. You try to join the party.\n\nOptions:\n1. Find a male ox named Tom and bribe him to help you on your journey.\n2. Spend a fun night with an ox.\n3. Make out with one of the oxen.\n")
    try:
      option = intput("")
      if option == 3:
        tprint("You share a nice kiss, but nothing comes of it...\n")
        option = intput("")
      if option == 1:
        tprint("You find Tom and give him a fun time. Afterward, he joins you on your journey (+10 attack damage).\n")
        player["damage"] += 10
        Tom["true"] = True
      if option == 2:
        tprint("You spend a fun night with the ox, but it senses that you have an STD and kicks you to death.\n")
        sys.exit("GAME OVER: You died")
    except Exception as e:
      print(f"ERROR: {e}")

  if not skip_section("portal_scene"):
    tprint("You ride Tom to the other side of the camp and find a pocket portal guarded by a large man. You must fight him to reach the portal.\n")
    fight("Fat Homeless Dude", 10, 40, player["health"], player["damage"])
    tprint("You enter the portal, and a nauseating strobing effect lasts for a few seconds.\n")
    time.sleep(3)
  if not skip_section("flash_scene"):
    tprint("You find yourself face-to-face with the Flash. Before you can react, he picks you up and speeds away, burning your smelly clothes off with friction.\n")
  if not skip_section("farm_scene"):
    tprint("When you arrive, he throws your blazing body into a lake, and you swim back to shore. The floor drops out from under you. Wilbur the pig starts investigating you, trying to figure out why all of Charlotte's children have pig heads.\nHe thinks you are their father because you are so ugly.\n\nOptions:\n1. Fight him for your girl.\n2. Admit that you are the father.\n3. Examine yourself in a mirror.\n4. Explain biology to Wilbur.\n")
    player["health"] += 15
    option = intput("")
    if option == 1:
      
      fight("Wilbur the Pig", 15, 30, player["health"], player["damage"])
      tprint("After defeating Wilbur, you interrogate him and learn that the superweapon is in Chipapas, Mexico. He was kidnapped to be turned into jerky, but escaped in a stolen helicopter.\n")
    elif option == 2:
      tprint("You admit that you are the father of Wilbur's piglets, and he brutally beats you to death.\n")
      sys.exit("GAME OVER: You died")
    elif option == 3:
      tprint("You look in a mirror to put your self-doubt to rest. Wilbur catches a glimpse of himself and realizes that he looks like the children.\nHe apologizes and gives you the Flash's suit. He also joins you to get revenge on the people who tried to turn him into jerky. (+15 health)\n")
      player["health"] += 15
      Wilbur["true"] = True
    elif option == 4:
      tprint("Wilbur is a pig and does not understand biology. He beats you to death.")
      sys.exit("GAME OVER: You died")
  if not skip_section("hawaii_volcano_scene"):
    if Tom["true"] and Jeffy["true"]:
      tprint(f"You ride Tom and {getJeffy()} to Hawaii. All this adventure is exhausting, and you need a break.\n")
    else:
      tprint("You find a local sea turtle and ride it to Hawaii because you need a break.\n")
    tprint("When you arrive in Hawaii, you see polluted beaches and get sunburned. You get the brilliant idea to jump into a volcano.\n\nOptions:\n1. Jump into the volcano.\n2. Run away from the volcano.\n3. Stare into the sun.\n")
    option = input("")
    if option == "1":
      tprint("You jump into the volcano too early and are vaporized.\n")
      sys.exit("GAME OVER: You died")
    elif option == "2":
      tprint("You run away from the volcano and survive, but you are still sunburned and die from too much social interaction.\n")
      sys.exit("GAME OVER: You died")
    elif option == "3":
      tprint("You stare into the sun, go blind, and stumble into the volcano at the perfect moment. It blasts you and your companions into Chipapas, Mexico, a short taxi ride from J.A.C.K. headquarters.\n")
  if not skip_section("chiapapas_scene_1"):
    if Jeffy["true"]:
      tprint(f"\nYou arrive in Chipapas, Mexico, very close to J.A.C.K. headquarters. {getJeffy()} tugs on his leash, trying to lead you toward the market. He seems hungry, but your parents are just ahead at headquarters.\n\nOptions:\n1. Ignore {getJeffy()}'s hunger and continue.\n2. Make {getJeffy()} go hungry while you eat.\n3. Take {getJeffy()} to the market and feed him.\n")
      option = input("")
      if option == "1":
        tprint(f"You ignore {getJeffy()}'s hunger and continue toward J.A.C.K. headquarters.\n")
      elif option == "2":
        tprint(f"You make {getJeffy()} go hungry while you eat. He gets furious, kills you, and calls it rage bait.\n")
        sys.exit("GAME OVER: You died")
      elif option == "3":
        tprint(f"You feed {getJeffy()}, and he evolves!\n")
        Jeffy["tier"] += 1
        player["damage"] += 15
        tprint(f"{getJeffy()} has evolved to the next tier!\n")
    else:
      tprint("You arrive in Chipapas, Mexico, very close to J.A.C.K. headquarters. Your stomach rumbles, and you might collapse because you have not eaten since the journey began.\n\nOptions:\n1. Eat to restore your health.\n2. Ignore your hunger and continue toward headquarters.\n")
      option = input("")
      if option == "1":
        tprint("You eat and restore your health.\n")
        player["health"] += 15
      elif option == "2":
        tprint("You ignore your hunger and continue toward J.A.C.K. headquarters, but collapse from exhaustion.\n")
        sys.exit("GAME OVER: You died")
  if not skip_section("Headquarters_Exterior_Scene1"):
    tprint("You arrive at J.A.C.K. headquarters and find a large metal door with a keyhole.\n\nOptions:\n1. Bang your head against the door and try to break it.\n2. Ask Wilbur if he knows where your parents are.\n3. Try to pick the lock with your tongue.\n")
    option = input("")
    if option == "1":
      tprint("You bang your head against the door. It does not budge, and you suffer severe brain damage.\n")
      sys.exit("!)!(*!&#(*&!)6")
    elif option == "2":
      tprint("You ask Wilbur if he knows where your parents are.\n")
      if Wilbur["true"] == True:
        tprint("Wilbur tells you that there is one in Montana, New York, and Florida.\n")
      else:
        tprint("Wilbur is not with you, so it takes two minutes to find him.\n")
        tprint("Searching for Wilbur...\n")
        for remaining_seconds in range(120, -1, -1):
          minutes, seconds = divmod(remaining_seconds, 60)
          print(f"\rTime remaining: {minutes}:{seconds:02}", end="", flush=True)
          if remaining_seconds:
            time.sleep(1)
        print()
        tprint("Wilbur tells you that there is one in Montana, New York, and Florida.\n")
    elif option == "3":
      tprint("You try to pick the lock with your tongue, but fail and get electrocuted by the powered door.\n")
      sys.exit("GAME OVER: You died")

  if not skip_section("Montana_Scene"):    
    tprint(f"You travel to Montana and find a large key guarded by a small army of Flock cameras. They are invading your privacy. What do you do?\n\nOptions:\n1. Take a bath in RUST-OLEUM 214944 and go at night so they cannot see you.\n2. Send {getJeffy()} to eat them.\n3. Hire a nearby flock of pigeons to swarm the cameras.\n4. Fight the cameras.\n")
    option = intput("")
    if option == "1":
      tprint("You take a bath in RUST-OLEUM 214944 and go at night so they cannot see you. You sneak past the cameras and grab the key. As you leave, the cameras detect your phone's Bluetooth signal and shoot blindly, killing a small family in the process.\n")
      key1 = True
    elif option == "2":
      tprint(f"You send {getJeffy()} to eat the cameras. He eats them all, and you successfully get the key.\n")
      tprint(f"{getJeffy()} has evolved!\n")
      Jeffy["tier"] += 1
      player["damage"] += 15
      key1 = True
      tprint(f"{getJeffy()} has evolved to the next tier!\n")
    elif option == "3":
      tprint("The Flock cameras try to shoot the pigeons but miss. One shot hits a forest and sets the whole state of Oregon on fire; another misses and hits you.\n")
      sys.exit("GAME OVER: You died")
    elif option == "4":
      fight("Flock Camera Army", 80, 100, player["health"], player["damage"])
  if not skip_section("New York"):
    tprint("You arrive in Central Park, New York, and find a skyscraper in the center labeled 'J.A.C.K. Distribution Center.'\nYou head inside. As you pass through a metal detector, it goes off, and a robot comes over to attack you.\n")
    fight("robot", 30, 60, player["health"], player["damage"])
    tprint("You find a door to the employees' lounge and go through it. In the back, you find a key guarded by a Tesla robot.\n")
    fight("Tesla Clanker", 5,  2, player["health"], player["damage"])
  
  # For after we do the keys
  if not skip_section("headquarters_scene1"):
    tprint("A group of very drunk scientists are there. They look you up and down and decide you are a threat to their work. You have no choice but to fight them.\n")
    fight("Drunk Scientists", 25, 20, player["health"], player["damage"])
    tprint("Now that the scientists are gone, you search the large lobby and find the employee room. There's a nice delicous cup of coffee that you drink 4 cups of (+15 health). You then go to the bathroom and find three doors.\n\nOptions:\n1. Straight ahead, labeled 'Employees Only.'\n2. Upstairs, partly hidden.\n3. To the left, guarded by Donald Trump.\n(Hint: think Outside The Box)\n")
    player["health"] += 15
    option = input("")
    if option == "1":
      tprint("You go through, and a horde of robots overruns you, beating you to death.\n")
      sys.exit("GAME OVER: You died")
    elif option == "2":
      tprint("A secret trap triggers behind you. An arrow strikes your back; it is coated in a fast-acting poison.\n")
      time.sleep(3)
      sys.exit("GAME OVER: You died")
    elif option == "3":
      tprint("As you try to go through, Donald Trump notices you and uses his ultimate: 'You are going to die. Everyone is talking about it, quite frankly.'\n")
      sys.exit("GAME OVER: You died")
    elif option =="Outside The Box":
      tprint("You find a secret door, continue down a dimly lit passage, and enter a room.\n") # Add more here after the keys.
      
if __name__ == "__main__":
  game()