names = ["Ana", "Luca", "Emilia", "oscar", "Ulises", "bruno"]

def contar_vocales(lista_nombres)
    contador = 0
    for nombre in nombres:
        if nombre[0].lower in ['a', 'e', 'i', 'o', 'u']:
            contador = contador + 1
    return contador

resultado = contar_vocales(names)
print("Cantidad de nombres que comienzan con vocal es: " + resultado)
