import json
from datetime import datetime

class Venta: # Clase principal con atributos fecha, cliente, productos vendidos
    def __init__(self, fecha, cliente, productos_vendidos):
        self.fecha = self.validar_fecha(fecha)
        self.cliente = cliente
        self.productos_vendidos = productos_vendidos

    def validar_fecha(self, fecha):
        try:
            return datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("La fecha tiene que estar en formato YYYY-MM-DD. Ejemplo 2024-08-01")

    def to_dict(self):
        return {
            "fecha": self.fecha.strftime("%Y-%m-%d"),
            "cliente": self.cliente,
            "productos": self.productos_vendidos
        }

    def __str__(self):
        return f"Venta a {self.cliente} el {self.fecha}"

class VentaOnline(Venta): #Clase derivada de una venta on-line
    def __init__(self, fecha, cliente, productos_vendidos, direccion_entrega, metodo_pago):
        super().__init__(fecha, cliente, productos_vendidos)
        self.direccion_entrega = direccion_entrega
        self.metodo_pago = metodo_pago

    def to_dict(self):
        data = super().to_dict()
        data["direccion_entrega"] = self.direccion_entrega
        data["metodo_pago"] = self.metodo_pago
        return data

    def __str__(self):
        return f"Venta Online a {self.cliente} el {self.fecha}, enviado a {self.direccion_entrega}"

class VentaLocal(Venta): #Clase derivada de venta en un local propio
    def __init__(self, fecha, cliente, productos_vendidos, direccion_tienda, metodo_pago):
        super().__init__(fecha, cliente, productos_vendidos)
        self.direccion_tienda = direccion_tienda
        self.metodo_pago = metodo_pago

    def to_dict(self):
        data = super().to_dict()
        data["direccion_tienda"] = self.direccion_tienda
        data["metodo_pago"] = self.metodo_pago
        return data

    def __str__(self):
        return f"Venta Local a {self.cliente} el {self.fecha}, en la tienda de la calle {self.direccion_tienda}"

class GestionVentas:
    def __init__(self, archivo):
        self.archivo = archivo

    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except Exception as error:
            raise Exception(f'Error al leer el archivo: {error}')

    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4)
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
        except Exception as error:
            print(f'Error inesperado: {error}')

    def crear_venta(self, venta): #Operación CRUD
        try:
            datos = self.leer_datos()
            id_venta = len(datos) + 1
            datos[str(id_venta)] = venta.to_dict()
            self.guardar_datos(datos)
            print('Venta guardada exitosamente')
        except Exception as error:
            print(f'Error inesperado {error}')

    def leer_venta(self, id_venta): #Operación CRUD
        try:
            datos = self.leer_datos()
            if str(id_venta) in datos:
                venta_data = datos[str(id_venta)]
                if 'direccion_entrega' in venta_data:
                    venta = VentaOnline(**venta_data)
                else:
                    venta = VentaLocal(**venta_data)
                print(f'Venta encontrada: {venta}')
                return venta
            else:
                print('Venta no encontrada.')
                return None
        except Exception as e:
            print(f'Error al leer la venta: {e}')
            return None

    def actualizar_venta(self, id_venta, nuevos_datos): #Operación CRUD
        try:
            datos = self.leer_datos()
            if str(id_venta) in datos:
                datos[str(id_venta)].update(nuevos_datos)
                self.guardar_datos(datos)
                print(f'Venta actualizada correctamente para el ID: {id_venta}')
            else:
                print(f"El ID de venta {id_venta} no existe")
        except Exception as e:
            print(f"Error al actualizar la venta: {e}")

    def eliminar_venta(self, id_venta): #Operación CRUD
        try:
            datos = self.leer_datos()
            if str(id_venta) in datos:
                del datos[str(id_venta)]
                self.guardar_datos(datos)
                print(f'La venta con ID {id_venta} ha sido eliminada correctamente')
            else:
                print(f"El ID de venta {id_venta} no existe para eliminar")
        except Exception as e:
            print(f"Error al eliminar la venta: {e}")