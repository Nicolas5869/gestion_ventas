#main.py

import os
import platform
from trabajopractico1 import VentaOnline, VentaLocal, GestionVentas

def limpiar_pantalla():
    '''Limpiar la pantalla según el sistema operativo'''
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def mostrar_menu():
    print("=======MENU DE VENTAS========")
    print("1. Agregar una Venta Online")
    print("2. Agregar una Venta Local")
    print("3. Buscar Venta por ID")
    print("4. Actualizar Venta por ID")
    print("5. Eliminar Venta por ID")
    print("6. Mostrar todas las Ventas")
    print("7. Salir")
    print("==================================")

def agregar_venta(gestion, tipo_venta):
    try:
        fecha = input("Ingrese la fecha de la venta (YYYY-MM-DD): ")
        cliente = input("Ingrese el nombre del cliente: ")
        productos_vendidos = input("Ingrese los productos vendidos (separados por comas): ").split(',')

        if tipo_venta == "1":
            direccion_entrega = input("Ingrese la dirección de entrega del producto: ")
            metodo_pago = input("Ingrese el método de pago: ")
            venta = VentaOnline(fecha, cliente, productos_vendidos, direccion_entrega, metodo_pago)
        elif tipo_venta == "2":
            direccion_tienda = input("Ingrese la dirección de la tienda: ")
            metodo_pago = input("Ingrese el método de pago: ")
            venta = VentaLocal(fecha, cliente, productos_vendidos, direccion_tienda, metodo_pago)
        else:
            print("Tipo de venta no válido")
            return

        gestion.crear_venta(venta)
        input("Presione enter para continuar")

    except ValueError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')

def buscar_venta_por_id(gestion):
    id_venta = input("Ingrese el ID de la venta: ")
    gestion.leer_venta(id_venta)
    input('Presione enter para continuar...')

def actualizar_venta_por_id(gestion):
    id_venta = input("Ingrese el ID de la venta a actualizar: ")
    nuevos_datos = {}
    while True:
        campo = input("Ingrese el campo que desea actualizar (fecha, cliente, productos, direccion_entrega, metodo_pago, direccion_tienda) o 'salir' para terminar: ")
        if campo == 'salir':
            break
        valor = input(f"Ingrese el nuevo valor para {campo}: ")
        if campo == 'productos':
            valor = valor.split(',')
        nuevos_datos[campo] = valor
    gestion.actualizar_venta(id_venta, nuevos_datos)
    input("Presione enter para continuar...")

def eliminar_venta_por_id(gestion):
    id_venta = input("Ingrese el ID de la venta que desea eliminar: ")
    gestion.eliminar_venta(id_venta)
    input("Presione enter para continuar...")

def mostrar_todas_las_ventas(gestion):
    print("LISTADO COMPLETO DE VENTAS")
    for id_venta, venta in gestion.leer_datos().items():
        print(f"ID: {id_venta} - {venta}")
    print("======================================")
    input("Presione enter para continuar...")

def main():
    archivo = "ventas.json"
    gestion = GestionVentas(archivo)

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            agregar_venta(gestion, "1")
        elif opcion == "2":
            agregar_venta(gestion, "2")
        elif opcion == "3":
            buscar_venta_por_id(gestion)
        elif opcion == "4":
            actualizar_venta_por_id(gestion)
        elif opcion == "5":
            eliminar_venta_por_id(gestion)
        elif opcion == "6":
            mostrar_todas_las_ventas(gestion)
        elif opcion == "7":
            print("Salir del menú")
            break
        else:
            print("Opción no válida, seleccione una opción correcta (1 al 7)")

if __name__ == "__main__":
    main()