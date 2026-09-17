import time, sys

def tprint(text):
  for character in text:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)
    
quit_statements = ["q", "quit", "exit", "exit game"]

def qinput(prompt):
  u = input(prompt)
  if u in quit_statements:
    sys.exit("User Exited")
  return u

def game():
  score = 0
  shield_points = 0
  sheild_health = 0

  user = input("please input the main charater's name: ")

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

  print(score)
 
  if score == 1:
    shield_points = 2
   
  elif score == 2:
    shield_points = 5
   
  elif score == 3:
    shield_points = 10
   
  else:
    shield_points = 20 
    sheild_health += shield_points


  if user != "admin":
    admin = False
   
if __name__ == "__main__":
  game()


