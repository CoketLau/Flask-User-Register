#Índice
Amigos = ["Derek", "Iván", "Aco", "Aarón"]

print(Amigos[2]) #Printea el objeto en índice 2
print(Amigos[0:2]) #Printea del index 0 al 2
print(Amigos[::2]) #Printea de 2 en 2


#MÉTODOS DE LISTAS:
Frutas = ["Manzana", "Pera", "Piña", "Coco"]

Frutas.insert(0, "Plátano") #Se le da un index y un objeto a añadir

Frutas.pop(0) #Se le dá un index y se quita ese objeto, devolviendo el objeto

len(Frutas) #Dale una lista y te devuelve el número de onjetos en ella

Frutas.count("Pera") #Devuelve el número de veces que aparece un valor

#Frutas.clear() #Borra todo lo de la lista

Frutas.sort() #Ordena por orden alfabético

print(Frutas)