import os

while True:
    User = input("Username: ")

    if len(User) > 12:
        print("Username can't have more than 12 characters")

        print("Press a key to repete: ")
        os.system("Pause > nul")
        os.system("cls")

    elif User.find(" ") != -1:
        print("Username can't contain spaces, try again")

        print("Press a key to repete: ")
        os.system("Pause > nul")
        os.system("cls")
    
    elif User.isalpha() != True:
        print("Username can't contain digits, try again")

        print("Press a key to repete: ")
        os.system("Pause > nul")
        os.system("cls")
    
    else:
        print("Succesfully logged in!")
        break