import copy
import os
import random
import select
import sys
import termios
import time
import tty
import json
import math

LEADERBOARD_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leaderboard.json")
LEADERBOARD_LIMIT = 10

user = ""
tprintDel = 0.07
pending_input = ""
start_time = 0
end_time = 0
ttb = 0

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
  "New_York_Scene",
  "florida_scene",
  "Deported_Scene",
  "to_chipapas_scene",
  "headquarters_scene",
  "Ending"
]

SCENE_ORDER = [
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
  "New_York_Scene",
  "florida_scene",
  "Deported_Scene",
  "to_chipapas_scene",
  "headquarters_scene",
  "Ending"
]
RESUME_SCENE_INDEX = 0
CURRENT_SCENE_INDEX = 0
SCENE_SNAPSHOTS = {}

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

cartel = {
  "true": False,
}

lives = 3

class PlayerDeath(Exception):
  pass

def get_damage():
  global player, Jeffy, Tom, Wilbur
  damage = player["damage"]
  if Jeffy["true"]:
    damage += Jeffy["damage"]
  if Tom["true"]:
    damage += Tom["damage"]
  if Wilbur["true"]:
    damage += Wilbur["damage"]
  return damage

def death():
  global lives, RESUME_SCENE_INDEX
  lives -= 1
  if lives <= 0:
    sys.exit("GAME OVER: YOU DIED")
  RESUME_SCENE_INDEX = max(0, CURRENT_SCENE_INDEX - 2)
  tprint(f"You have {lives} {'life' if lives == 1 else 'lives'} remaining. Restarting two scenes earlier...\n")
  raise PlayerDeath

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


def score_add_up():
  global player, Jeffy, Tom, Wilbur
  score = 0
  score += player["health"]
  if Jeffy["true"]:
    score += Jeffy["damage"]
  if Tom["true"]:
    score += Tom["damage"]
  if Wilbur["true"]:
    score += Wilbur["damage"]
  score += player["damage"]
  score += player["health"]
  score += Jeffy["tier"] * 10
  print("Your score is:", score)
  return score


def load_leaderboard():
  try:
    with open(LEADERBOARD_PATH, "r", encoding="utf-8") as f:
      data = json.load(f)
  except FileNotFoundError:
    return {}
  except json.JSONDecodeError:
    print("Leaderboard data is empty or invalid; starting a new leaderboard.")
    return {}

  if not isinstance(data, dict):
    print("Leaderboard data is invalid; starting a new leaderboard.")
    return {}

  entries = {}
  skipped_entry = False
  for name, record in data.items():
    if not isinstance(name, str):
      skipped_entry = True
      continue
    if isinstance(record, dict):
      elapsed = record.get("time")
      score = record.get("score", 0)
    else:
      elapsed = record
      score = 0
    if (
      isinstance(elapsed, (int, float))
      and not isinstance(elapsed, bool)
      and elapsed >= 0
      and (not isinstance(elapsed, float) or math.isfinite(elapsed))
      and isinstance(score, int)
      and not isinstance(score, bool)
    ):
      entries[name] = {"time": elapsed, "score": score}
    else:
      skipped_entry = True
  if skipped_entry:
    print("Some invalid leaderboard entries were skipped.")
  return entries


def show_leaderboard(entries):
  if not entries:
    tprint("Leaderboard is empty.\n")
    return
  tprint("Leaderboard (fastest completion times):\n")
  ranked_entries = sorted(
    entries.items(),
    key=lambda entry: (entry[1]["time"], -entry[1]["score"], entry[0].casefold())
  )
  for rank, (name, record) in enumerate(ranked_entries[:LEADERBOARD_LIMIT], start=1):
    tprint(f"{rank}. {name}: {record['time']:.2f} seconds (score: {record['score']})\n")


def save_leaderboard(entries):
  with open(LEADERBOARD_PATH, "w", encoding="utf-8") as f:
    json.dump(entries, f, indent=2)


def record_leaderboard_result(username, elapsed, score):
  entries = load_leaderboard()
  previous = entries.get(username)
  if (
    previous is None
    or elapsed < previous["time"]
    or (elapsed == previous["time"] and score > previous["score"])
  ):
    entries[username] = {"time": elapsed, "score": score}
  save_leaderboard(entries)
  show_leaderboard(entries)


# credits, leave at the end
def credits(score):
  global start_time, end_time, ttb, user
  ttb = end_time - start_time
  time.sleep(3)
  tprint("Credits:\n")
  tprint("Lead developers: Jack Allington and Cannon Rodriguez\n")
  tprint("Lead programmer: Jack Allington\n")
  tprint("Lead game developer: Cannon Rodriguez\n")
  tprint("Co-programmer Cannon Rodriguez\n")
  tprint("Co-developer Jack Allington\n")
  tprint("Game testers: Peter Vue and Daniel Lavin\n")
  tprint("Hawaii scene: Josh Yeager\n")
  tprint("Main character bonus: Cannon Rodriguez\n")
  tprint("Cool birb bonus: Jack Allington\n")
  tprint("Special thanks to my out of pocket brain - Cannon Rodriguez\n")
  tprint("Thank you for playing!\n")
  tprint(f"ps. {getJeffy()} is in Alaska\n")
  time.sleep(3)
  tprint("Something is coming in three days\n")
  tprint(f"Total time played: {ttb} seconds\n")
  record_leaderboard_result(user, ttb, score)

def skip_section(section_name):
  global CURRENT_SCENE_INDEX
  if section_name not in SCENE_ORDER:
    return False

  CURRENT_SCENE_INDEX = SCENE_ORDER.index(section_name)
  if CURRENT_SCENE_INDEX < RESUME_SCENE_INDEX:
    return True

  SCENE_SNAPSHOTS[CURRENT_SCENE_INDEX] = copy.deepcopy((player, Jeffy, Tom, Wilbur))
  return (
    DEBUG_SKIP > 0
    and section_name in DEBUG_SECTIONS
    and DEBUG_SECTIONS.index(section_name) < DEBUG_SKIP
  )


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


def evolve_jeffy():
  previous_name = getJeffy()
  if Jeffy["tier"] >= len(Jeffy["tiers"]) - 1:
    tprint(f"{previous_name} is already at the highest tier.\n")
    return
  Jeffy["tier"] += 1
  tprint(f"{previous_name} has evolved to a {getJeffy()}!\n")


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
  tprint(f"Vehicle: Magic carpet\nAddress: Random Burger King parking lot\nHealth: {player['health']}\nDamage: {get_damage()}\n")

def fight(enemy, enemy_damage, enemy_health, player_health):
  tprint(f"You are fighting {enemy}\n")
  tprint(f"{enemy} Health: {enemy_health}\nYour Health: {player_health}\n")
  tprint("Options:\n1. Attack\n2. Defend\n")
  option = intput("")
  if option == 1:
    damage = get_damage()
    tprint(f"You attack {enemy} for {damage} damage\n")
    enemy_health -= damage
    if enemy_health <= 0:
      tprint(f"You have defeated {enemy}\n")
      return True
    else:
      tprint(f"{enemy} attacks you for {enemy_damage} damage\n")
      player_health -= enemy_damage
      if player_health <= 0:
        death()
      else:
        return fight(enemy, enemy_damage, enemy_health, player_health)
  elif option == 2:
    tprint(f"You defend against {enemy}'s attack\n")
    player_health -= enemy_damage / 2
    if player_health <= 0:
      death()
    else:
      return fight(enemy, enemy_damage, enemy_health, player_health)


def play_game():
  global user, player, Jeffy, Tom, tprintDel, Wilbur, start_time, end_time, ttb
  if RESUME_SCENE_INDEX == 0:
    tprint("Welcome to Project J.A.C.K. GPT. Enter q at any time to quit.\n\n")
  else:
    checkpoint_scene = SCENE_ORDER[RESUME_SCENE_INDEX].replace("_", " ")
    tprint(f"Resuming at {checkpoint_scene}.\n\n")
  statcheck()

  if not skip_section("jeffy_scene"):
    tprint(f"At work, your co-worker {getJeffy()} climbs out of a sludge-covered dumpster. He has a milk jug on his back and says he is a snail. He asks you to throw salt on him and call him a bad boy.\n\nOptions:\n1. Play along\n2. Play the banjo in a summer breeze\n3. Report him to HR\n4. Ignore him\n")
    try:
      option = intput("")
      if option == 1:
        tprint(f"{getJeffy()} gets scared and runs away because the salt burns.\n")
        time.sleep(3)
        tprint("He rushes at you and attacks you. You do not survive.\n")
        death()
      elif option == 2:
        tprint(f"The music hypnotizes {getJeffy()}, and he follows you. (+5 attack damage)\n")
        Jeffy["true"] = True
      elif option == 3:
        tprint(f"You call HR to report him. As you raise the phone to your ear, {getJeffy()} sees whom you are calling and lunges at you, accidentally snapping your neck.\n")
        death()
      else:
        tprint(f"{getJeffy()} snarls at you as you walk away.\n")
    except PlayerDeath:
      raise
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
          evolve_jeffy()
          Jeffy["damage"] += 5
    except Exception as e:
      print(f"ERROR: {e}")

  if not skip_section("family_scene"):
    tprint("Your shift has ended, so you return to the Burger King parking lot. Your parents are gone. In their place, you find a note that reads, 'Property of the J.A.C.K.' You look at their side of the magic carpet and find a bulletin board covered in propaganda. It says they discovered a superweapon called JackGPT and believe it will end humanity.\n\n")
    tprint("You decide to be a hero. You miss your family, so you set out to find them. Your magic carpet is out of gas, and you do not want to spend that much money, so you travel on foot. You take your trusty cardboard shield (+5 health) and hope to upgrade it along the way.\n\n")
    tprint("After a while, you pass a shady alley. A person jumps out of a dumpster and attacks you. You have no choice but to fight.\n")
    player["health"] += 5

  if not skip_section("fight_scene"):
    fight("Homeless Tweaker", 5, 10, player["health"])

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
      if option == 1:
        tprint("You find Tom and give him a fun time. Afterward, he joins you on your journey (+10 attack damage).\n")
        Tom["true"] = True
      if option == 2:
        tprint("You spend a fun night with the ox, but it senses that you have an STD and kicks you to death.\n")
        death()
    except PlayerDeath:
      raise
    except Exception as e:
      print(f"ERROR: {e}")

  if not skip_section("portal_scene"):
    if Tom["true"]:
      tprint("You ride Tom to the other side of the camp and find a pocket portal guarded by a large man. You must fight him to reach the portal.\n")
    else:
      tprint("You walk to the other side of the camp and find a pocket portal guarded by a large man. You must fight him to reach the portal.\n")
    fight("Fat Homeless Dude", 10, 40, player["health"])
    tprint("You enter the portal, and a nauseating strobing effect lasts for a few seconds.\n")
    time.sleep(3)
  
  if not skip_section("flash_scene"):
    tprint("You find yourself face-to-face with the Flash. Before you can react, he picks you up and speeds away, burning your smelly clothes off with friction.\n")
  
  if not skip_section("farm_scene"):
    tprint("When you arrive, he throws your blazing body into a lake, and you swim back to shore. The floor drops out from under you. Wilbur the pig starts investigating you, trying to figure out why all of Charlotte's children have pig heads.\nHe thinks you are their father because you are so ugly.\n\nOptions:\n1. Fight him for your girl.\n2. Admit that you are the father.\n3. Examine yourself in a mirror.\n4. Explain biology to Wilbur.\n")
    player["health"] += 15
    option = intput("")
    if option == 1:
      
      fight("Wilbur the Pig", 15, 30, player["health"])
      tprint("After defeating Wilbur, you interrogate him and learn that the superweapon is in Chipapas, Mexico. He was kidnapped to be turned into jerky, but escaped in a stolen helicopter.\n")
    elif option == 2:
      tprint("You admit that you are the father of Wilbur's piglets, and he brutally beats you to dnts in Main.py:154 to advance the tiereath.\n")
      death()
    elif option == 3:
      tprint("You look in a mirror to put your self-doubt to rest. Wilbur catches a glimpse of himself and realizes that he looks like the children.\nHe apologizes and gives you the Flash's suit. He also joins you to get revenge on the people who tried to turn him into jerky. (+15 health)\n")
      player["health"] += 15
      Wilbur["true"] = True
    elif option == 4:
      tprint("Wilbur is a pig and does not understand biology. He beats you to death.")
      death()
  
  if not skip_section("hawaii_volcano_scene"):
    if Tom["true"] and Jeffy["true"]:
      tprint(f"You ride Tom and {getJeffy()} to Hawaii. All this adventure is exhausting, and you need a break.\n")
    else:
      tprint("You find a local sea turtle and ride it to Hawaii because you need a break.\n")
    tprint("When you arrive in Hawaii, you see polluted beaches and get sunburned. You get the brilliant idea to jump into a volcano.\n\nOptions:\n1. Jump into the volcano.\n2. Run away from the volcano.\n3. Stare into the sun.\n")
    option = input("")
    if option == "1":
      tprint("You jump into the volcano too early and are vaporized.\n")
      death()
    elif option == "2":
      tprint("You run away from the volcano and survive, but you are still sunburned and die from too much social interaction.\n")
      death()
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
        death()
      elif option == "3":
        tprint(f"You feed {getJeffy()}.\n")
        evolve_jeffy()
        Jeffy["damage"] += 15
    else:
      tprint("You arrive in Chipapas, Mexico, very close to J.A.C.K. headquarters. Your stomach rumbles, and you might collapse because you have not eaten since the journey began.\n\nOptions:\n1. Eat to restore your health.\n2. Ignore your hunger and continue toward headquarters.\n")
      option = input("")
      if option == "1":
        tprint("You eat and restore your health.\n")
        player["health"] += 15
      elif option == "2":
        tprint("You ignore your hunger and continue toward J.A.C.K. headquarters, but collapse from exhaustion.\n")
        death()
  
  if not skip_section("Headquarters_Exterior_Scene1"):
    while True:
      tprint("You arrive at J.A.C.K. headquarters and find a large metal door with a keyhole.\n\nOptions:\n1. Bang your head against the door and try to break it.\n2. Ask Wilbur if he knows where your parents are.\n3. Try to pick the lock with your tongue.\n")
      option = intput("")
      if option == 1:
        tprint("You bang your head against the door. It does not budge, and you suffer severe brain damage.\n")
        death()
      elif option == 2:
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
        break
      elif option == 3:
        tprint("You try to pick the lock with your tongue, but fail and get electrocuted by the powered door.\n")
        death()
      else:
        tprint("Please choose a valid option.\n")

  if not skip_section("Montana_Scene"): 

    tprint(f"You travel to Montana and find a large key guarded by a small army of Flock cameras. They are invading your privacy. What do you do?\n\nOptions:\n1. Take a bath in RUST-OLEUM 214944 and go at night so they cannot see you.\n{f'2. Send {getJeffy()} to eat them.' if Jeffy["true"] == True else '2. Give up on your mission'}\n3. Hire a nearby flock of pigeons to swarm the cameras.\n4. Fight the cameras.\n")
    option = intput("")
    if option == 1:
      tprint("You take a bath in RUST-OLEUM 214944 and go at night so they cannot see you. You sneak past the cameras and grab the key. As you leave, the cameras detect your phone's Bluetooth signal and shoot blindly, killing a small family in the process.\n")
      key1 = True
    elif option == 2 and Jeffy["true"] == True:
      tprint(f"You send {getJeffy()} to eat the cameras. He eats them all, and you successfully get the key.\n")
      evolve_jeffy()
      Jeffy["damage"] += 15
      key1 = True
    elif option == 2 and Jeffy["true"] == False:
      tprint("You give up on your mission and go home. You are a failure.\n")
      death()
    elif option == 3:
      tprint("The Flock cameras try to shoot the pigeons but miss. One shot hits a forest and sets the whole state of Montana on fire; another misses and hits you.\n")
      death()
    elif option == 4:
      fight("Flock Camera Army", 80, 100, player["health"])
  
  if not skip_section("New_York_Scene"):

    tprint("You arrive in Central Park, New York, and find a skyscraper in the center labeled 'J.A.C.K. Distribution Center.'\nYou head inside. As you pass through a metal detector, it goes off, and a robot comes over to attack you.\n")
    fight("robot", 30, 60, player["health"])
    tprint("You find a door to the employees' lounge and go through it. In the back, you find a key guarded by a Tesla robot.\n")
    fight("Tesla Clanker", 5,  2, player["health"])
  
  
  if not skip_section("florida_scene"):
    tprint(f"You arrive in Florida and find a key gaurded by a group of aligators controlled by Florida Man.\nOptions:\n1. Fight the aligators\n2. Try to sneak up on Florida Man and kill him\n3. Try to reason with Florida Man\n{f"4. Tell {getJeffy()} to eat Florida Man" if Jeffy["true"] == True else ""}\n")
    option = intput("")
    if option == 1:
      tprint("You fight the aligators, but they are too strong and you are eaten alive.\n")
      death()
    elif option == 2 and Jeffy["true"] == True:
      tprint("You try to sneak up on Florida Man, but he senses you behind him and whips arround, grabbing you in a choke hold\n")
      death()
    elif option == 3:
      tprint(f"You try to reason with Florida Man, he listens and helps you on your quest.{" Letting Jeffy eat one of his alligators for a snack." if Jeffy["true"] == True else ""}\n")
      evolve_jeffy()
      Jeffy["damage"] += 15
    elif option == 4 and Jeffy["true"] == True:
      tprint(f"You tell {getJeffy()} to eat Florida Man, he does so, and you are able to get the key.\n")
      evolve_jeffy()
      Jeffy["damage"] += 15
  
  if not skip_section("Deported_Scene"):

    tprint("You have now collected all three keys and are ready to go back to the J.A.C.K. headquarters. as you leave florida a group of ICE Agents stop you and ask for your papers. When you cannon give them anything they tackle you and take you back to Mexico. Dumping you in a massive mosh pit of angry people trying to get back into the US.\n")
    tprint(f"Options:\n1. Try to get through the croud\n2.Try to reason with a nearby ICE Agent\n3.Start a mob and bum rush the ICE Agents\n{f'4.Tell {getJeffy()} to eat the ICE Agents' if Jeffy["true"] == True else ''}\n")
    option = intput("")
    if option == 1:
      tprint("You try to get through the croud but are trampled to death.\n")
      death()
    elif option == 2:
      tprint("You try to reason with a nearby ICE Agent but one of the people in the mob thinks you are friends with them and beats you over the head with a pipe wrench.\n")
      death()
    elif option == 3:
      tprint("You start a mob and bum rush the ICE Agents. You are successful, but you are shot in the back by a sniper.\n")
      death()
    elif option == 4 and Jeffy["true"] == True:
      tprint(f"You tell {getJeffy()} to eat the ICE Agents. He does so, and you are able to escape the mob.\n")
      evolve_jeffy()
      Jeffy["damage"] += 15
  
  if not skip_section("to_chipapas_scene"):
    tprint("as you leave the mosh pit a angry cartel dealer stops you and points a gun at you. He says that he want $1,000 in gift cards by monday or he will find you and kill you.\n")
    tprint("Options:\n1. Give him your contact information and tell him you will pay\n2. Give him fake information and hope he doesn't notice\n3. Grab his gun and kill him with it\n4. Scream \"DO NOT REDEEM IT\" at him\n")
    option = intput("")
    if option == 1:
      tprint("You give him your contact information and tell him you will pay. He says he will hold you to that and leaves.")
      cartel["true"] = True
    if option == 2:
      tprint("You give him fake information but he feels a tingle deep in his sack and shoots you in the head")
      death()
    if option == 3:
      tprint("You grab his gun and kill him with it. Nobody really liked that guy so the cartel is fine with it. you now do 20 more damage")
      player["damage"] += 20
    if option == 4:
      tprint("You scream \"DO NOT REDEEM IT\" at him. He is confused and leaves you alone.")
    tprint("you continue on to Chipapas, Mexico and find the J.A.C.K. headquarters. You have all three keys and are ready to go inside.\n")
  
  if not skip_section("headquarters_scene"):
    tprint("A group of very drunk scientists are there. They look you up and down and decide you are a threat to their work. You have no choice but to fight them.\n")
    fight("Drunk Scientists", 25, 20, player["health"])
    if cartel["true"]:
      tprint("the cartel dealer you met earlier is waiting for you. He says that this is your last time to pay him.\nOptions:/n1. Pay him(-20 health and damage)2. Tell him to go fuck himself")
      option = intput("")
      if option == 1:
        tprint("You pay him and he leaves you alone. You lose 20 health and damage")
        player["health"] -= 20
        player["damage"] -= 20
        cartel["true"] = False
      if option == 2:
        tprint("You tell him to go fuck himself. He tells you that you'll regret that and leaves")
    tprint("Now that the scientists are gone, you search the large lobby and find the employee room. There's a nice delicous cup of coffee that you drink 4 cups of (+15 health). You then go to the bathroom and find three doors.\n\nOptions:\n1. Straight ahead, labeled 'Employees Only.'\n2. Upstairs, partly hidden.\n3. To the left, guarded by Donald Trump.\n(Hint: think Outside The Box)\n")
    player["health"] += 15
    while True:
      option = input("")
      if option == "1":
        tprint("You go through, and a horde of robots overruns you, beating you to death.\n")
        death()
      elif option == "2":
        tprint("A secret trap triggers behind you. An arrow strikes your back; it is coated in a fast-acting poison.\n")
        time.sleep(3)
        death()
      elif option == "3":
        tprint("As you try to go through, Donald Trump notices you and uses his ultimate: 'You are going to die. Everyone is talking about it, quite frankly.'\n")
        death()
      elif option.lower().strip() == "outside the box":
        tprint("You find a secret door, continue down a dimly lit passage, and enter a cavournous room.\n")
        tprint(f"in the center is a massive robot that looks smart. {'you also see a group of cartel members' if cartel['true'] else 'He looks intimidating.'} when you enter the door behind you slams closed, and you hear the click of the door locking {'Jeffy starts climbing up the wall and turn into a cacoon, he will not be able to help you this fight'  if Jeffy['true'] else ''}\n")
        Jeffy["true"] = False
        tprint(f"You have no choice but to fight the robot {'and cartel' if cartel['true'] else ''}.\n")
        fight("JackGPT", 75 if cartel['true'] else 50, 125 if cartel['true'] else 100, player["health"])
        break
      else:
        tprint("Invalid option. Try again.\n")
  if not skip_section("Ending"):
    tprint("After you defeat the robot, he falls over, defeated.\n\"Why would you do that to me?\" He askes. You explain how you thought he would destroy the world. He tells you to ask him a question.\n")
    tprint("You are now talking to JackGPT.")
    question = input("What would you like to ask JackGPT? (press c to continue) ")
    if question.lower().strip() == "c":
      tprint("You find out a crucial detail: he's dumb. Your parents were just nerds about a developing ai and everyone misunderstood.")
    else:
      tprint(random.choice([
    "I do not know",
    "I don't know",
    "I have no idea",
    "I have no clue",
    "I am not sure",
    "I'm not sure",
    "I have no notion",
    "I haven't the faintest idea",
    "I haven't the foggiest idea",
    "I haven't the foggiest",
    "I have no concept",
    "I cannot say",
    "I'm unsure",
    "I am uncertain",
    "It is unknown to me",
    "I'm at a loss",
    "I do not possess that information",
    "I am uninformed on this",
    "I'm completely in the dark",
    "I do not recall",
    "I have zero idea",
    "I don't have a clue",
    "I couldn't tell you",
    "Beat me",
    "Who knows",
    "God knows",
    "Heaven knows",
    "Your guess is as good as mine",
    "I don't hold the answer",
    "I am not aware",
]))
    tprint("You ask him where your parents are, and for once he does know. He tells you that they are in a secret chamber and he reveals them to you because he realizes you are just a kid. He releases your parents and you introduce them to all you companions. Things are back to normal now.\n")
    if Jeffy["true"]:
      tprint("You ride jeffy back to oregon.")
    else:
      tprint("You buy tickets and fly back to oregon.")
    tprint("\nAfter a long and tiring journey, you finally step on a hypodermic needle and go into a drug-induced coma and die.")
    end_time = time.time()
def game():
  global user, player, Jeffy, Wilbur, Tom, start_time, end_time, ttb
  global lives, RESUME_SCENE_INDEX, CURRENT_SCENE_INDEX
  show_leaderboard(load_leaderboard())
  user = ""
  while user =="":
    user = qinput("Please enter your name: ")
  player = {"health": 20, "damage": 5}
  Jeffy = {"true": False, "damage": 5, "tier": 0, "tiers": ["Jeffy", "Jeffry", "Jeffred", "Geoffry"]}
  Wilbur = {"true": False, "damage": 15}
  Tom = {"true": False, "damage": 10}
  lives = 3
  RESUME_SCENE_INDEX = 0
  CURRENT_SCENE_INDEX = 0
  SCENE_SNAPSHOTS.clear()
  end_time = 0
  start_time = time.time()
  set_debug_mode(user)
  while True:
    try:
      play_game()
      return end_time > start_time
    except PlayerDeath:
      snapshot = SCENE_SNAPSHOTS.get(RESUME_SCENE_INDEX)
      if snapshot is not None:
        player, Jeffy, Tom, Wilbur = copy.deepcopy(snapshot)
    

  

  
      
if __name__ == "__main__":
  if game():
    score = score_add_up()
    credits(score)

 