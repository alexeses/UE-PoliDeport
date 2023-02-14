import cliente


def main_menu():
    print("Bienvenido al sistema de gestión de Polideportivo")
    print("Selecciona una opción:")
    print("1. Dar de alta un cliente con sus datos personales")
    print("2. Dar de baja un cliente")
    print("3. Mostrar los datos personales de un cliente o todos")
    print("4. Matricular un cliente en un deporte")
    print("5. Desmatricular un cliente de un deporte")
    print("6. Mostrar los deportes de un cliente")
    print("7. Salir")
    opcion = int(input("Opción: "))
    return opcion


if __name__ == "__main__":
    opcion = 0

    while opcion != 7:
        opcion = main_menu()
        cliente.comprobar_tablas()
        if opcion == 1:
            print("Dar de alta un cliente con sus datos personales")
            cliente.insertar_deportes()
            cliente.alta_cliente()
        elif opcion == 2:
            print("Dar de baja un cliente")
            cliente.baja_cliente()
        elif opcion == 3:
            # Mostrar los datos personales de un cliente o todos
            print("Mostrar los datos personales de un cliente o todos")
            opcion_ver = input("¿Deseas ver todos los clientes o solo uno? (T/S): ").upper()
            if opcion_ver == "T":
                # Muestra todos los clientes
                cliente.mostrar_clientes()
            elif opcion_ver == "S":
                # Muestra solo un cliente
                cliente.mostrar_cliente()
            else:
                print("Opción inválida. Por favor, selecciona T o S.")
        elif opcion == 4:
            # Matricular un cliente en un deporte
            print("Matricular un cliente en un deporte")
            cliente.matricular_cliente()
        elif opcion == 5:
            # Desmatricular un cliente de un deporte
            print("Desmatricular un cliente de un deporte")
            cliente.desmatricular_cliente()
        elif opcion == 6:
            # Mostrar los deportes de un cliente
            print("Mostrar los deportes de un cliente")
            cliente.mostrar_deportes_cliente()
        elif opcion == 7:
            print("Gracias por usar el sistema de gestión de Polideportivo.")
            cliente.desconectar_bd()
        else:
            print("Opción inválida. Por favor, selecciona una opción válida.")