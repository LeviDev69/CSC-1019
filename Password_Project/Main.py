import time, sys

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

def innit():
  user = qinput("please input your name: ")
  tprint("Welcome to Project J.A.C.K. GPT If you want to quit at any time input q\n")
  tprint("====================================================================================================\n")
  tprint(f"Name: {user} \nCareer:  D.A.F.D.A.L.U.B (Dumpsters Association for Dumb Adults Like the Uttlery Broke)\n")
  tprint("Vehicle: Magic carpet\nAdress: Random Burger King Parking lot\n")

def game():
  score = 0
  shield_points = 0
  sheild_health = 0


  pas = input("please enter a password:\n")
  score = 0  
  if len(pas) >= 8:
     score += 1
  if any(char.isupper() for char in pas):
     score += 1
  if any(char.islower() for char in pas):
     score += 1
  if any(char.isdigit() for char in pas):
     score += 1
 
  if score == 1:
    shield_points = 2
   
  elif score == 2:
    shield_points = 5
   
  elif score == 3:
    shield_points = 10
   
  else:
    shield_points = 20 
    sheild_health += shield_points


  tprint("Today while you were at work your co-worker, Jeffy, Climbed out of a dumpster covered in sludge. He had placed a milk jug on his back, and told you he was a snail. He asks you to throw salt on him and call him a bad boy\nOptions:\n1:Play Along\n2:Report him to HR\n3:Ignore him\n4:Play the Banjo in a summer breeze\n")
  try:
    option = int(qinput(""))
    if option == 1:
      tprint("Jeffy got scared and ran away.")
      time.sleep(3)
      tprint(" He came back from behind you and ate you\n")
      sys.exit("GAME OVER: You died")
  except Exception as e:
    print(f"ERROR: {e}")


if __name__ == "__main__":
  innit()
  game()

