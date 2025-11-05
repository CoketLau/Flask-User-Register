def characters():
    import string

    characters = string.printable + "ñ" + "Ñ"
    characters = list(characters)

    return characters

def Key(chars:list):
    if not chars:
        print("WE NEED CHARACTER LIST WITH .characters()")
        return
    import random

    Key = chars.copy()
    random.shuffle(Key)

    return Key

def Encript(Msg:str, key, chars:list):
    Cypher_text = ""

    for letter in Msg:
        index = chars.index(letter)
        Cypher_text += key[index]
    
    return Cypher_text


def Decript(Msg:str, key, chars:list):
    Translated_text = ""

    for letter in Msg:
        index = key.index(letter)
        Translated_text += chars[index]

    return Translated_text