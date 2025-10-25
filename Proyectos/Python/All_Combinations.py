import keyboard
import time
import threading
from itertools import product

PARAR = False
Cycle_Count = 0
KEYS_PER_COMBINATION = 3

InputsPosibles = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z',

    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',

    'space', 'left', 'right', 'up', 'down',

    'comma', 'period', 'slash', 'semicolon', 'backslash', 'equal' ]

def main():
    global Cycle_Count, PARAR
    combinaciones = product(InputsPosibles, repeat=KEYS_PER_COMBINATION)

    TOTAL_COMBINACIONES = len(InputsPosibles) ** KEYS_PER_COMBINATION
    print(f"{TOTAL_COMBINACIONES}")

    for combo in combinaciones:
        if PARAR:break
        The_comb = ""

        Cycle_Count += 1
        The_comb = " + ".join(combo)
        


        for Key in combo:
            keyboard.press(Key)
        
        time.sleep(0.1)

        for Key in combo:
            keyboard.release(Key)
        

        print(The_comb)


def stopFunc():
    global PARAR
    keyboard.wait("o")
    PARAR = True



threading.Thread(target=main, daemon=True).start()
threading.Thread(target=stopFunc, daemon=True).start()