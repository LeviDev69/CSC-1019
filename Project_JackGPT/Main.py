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

def game():
  user = qinput("please input your name: ")
  tprint("Welcome to Project J.A.C.K. GPT If you want to quit at any time input q\n")
  tprint("====================================================================================================\n")
  tprint(f"Name: {user} \nCareer:  D.A.F.D.A.L.U.B (Dumpsters Association for Dumb Adults Like the Uttlery Broke)\n")
  tprint("Vehicle: Magic carpet\nAdress: Random Burger King Parking lot\n")

  tprint("Today while you were at work your co-worker, Jeffy, Climbed out of a dumpster covered in sludge. He had placed a milk jug on his back, and told you he was a snail. He asks you to throw salt on him and call him a bad boy\nOptions:\n1:Play Along\n2:Report him to HR\n3:Ignore him\n4:Play the Banjo in a summer breeze\n")
  try:
    option = int(qinput(""))
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
  except Exception as e:
    print(f"ERROR: {e}")


if __name__ == "__main__":
  game()

