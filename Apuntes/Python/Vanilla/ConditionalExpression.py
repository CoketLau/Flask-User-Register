#Ahorra los else-if statements, haciendo el código más corto

num = 4

print("Number is larger than 5" if num > 5 else "Number is NOT than 5")

#Tambien se pueden poner en variables:

Temperatura = 30
HaceCalor = True if Temperatura >= 30 else False

print(f"¿Hace calor?: {'Si' if HaceCalor else 'No'}")