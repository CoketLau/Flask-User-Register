#Son lo mismo casi que las listas los [:] funcionan igual
Nombre = input("Nombre: ")
Número = input("Número: ")

print(len(Nombre)) #Printea el número de caracteres del string

print(Nombre.find("a")) #Printea index de la primera ocurrencia de un caracter que le demos
print(Nombre.rfind("a")) #Reverse Find printea la última ocurrencia de un caracter

print(Nombre.replace("o", "u")) #Cambia un caracter con otro

#Nombre.capitalize()) --Hace la primera letra mayúscula

print(Nombre.count("a")) #Cuenta el número de veces que aparece un caracter 

print(Número.isdigit()) #Da true si un string solo contiene números