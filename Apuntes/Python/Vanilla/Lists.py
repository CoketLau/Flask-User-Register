import colorama
MyList = ["Manzana", "Piña", "Plátano", "Papaya", "Guayaba"]

while True:
    Answer = input(colorama.Fore.CYAN + "Choose a fruit: ")
    
    for i in MyList:
        if Answer == i:
                MyList.remove(Answer)
                print(colorama.Fore.YELLOW + f"You ate {Answer}")
                break
    else:
        print(colorama.Fore.RED + colorama.Style.BRIGHT + f"{Answer} is not availeable")