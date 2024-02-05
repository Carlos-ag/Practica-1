def enter_valid_input(list, texto):
    
    print(texto)
    number = input()

    while not number.isdigit() or int(number) not in list:
        print("Ingrese un número válido")
        number = input()
    
    return int(number)