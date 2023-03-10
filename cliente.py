import psycopg2
import database_config
from deporte import Deporte


class Cliente:
    def __init__(self, nombre, dni, fecha_nacimiento, telefono):
        self.nombre = nombre
        self.dni = dni
        self.fecha_nacimiento = fecha_nacimiento
        self.telefono = telefono
        self.deportes = []

    def __datos_cliente(self):
        return "Nombre: " + self.nombre + " DNI: " + self.dni + " Fecha de nacimiento: " + self.fecha_nacimiento + " Teléfono: " + self.telefono


def conectar_bd():
    try:
        conn = psycopg2.connect(
            host=database_config.host,
            database=database_config.database,
            user=database_config.user,
            password=database_config.password,
            port=database_config.port
        )
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Error de conexión a la base de datos", error)

def comprobar_tablas():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)", ('cliente',))
    existe_cliente = cursor.fetchone()[0]
    cursor.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)", ('deporte',))
    existe_deporte = cursor.fetchone()[0]
    if existe_cliente == False:
        crear_tabla_cliente(conn)
    if existe_deporte == False:
        crear_tabla_deporte(conn)
    desconectar_bd(conn)


def crear_tabla_cliente(conn):
    cursor = conn.cursor()
    sql = "CREATE TABLE cliente (nombre VARCHAR(50), dni VARCHAR(9), fecha_nacimiento VARCHAR(10), telefono VARCHAR(9))"
    cursor.execute(sql)
    conn.commit()
    print("Tabla cliente creada correctamente")


def crear_tabla_deporte(conn):
    cursor = conn.cursor()
    sql = "CREATE TABLE deporte (nombre VARCHAR(50), precio_hora INTEGER)"
    cursor.execute(sql)
    conn.commit()
    print("Tabla deporte creada correctamente")


def desconectar_bd(conn):
    if conn:
        conn.close()
        print("Conexión cerrada")


# Alta de cliente
def alta_cliente():
    conn = conectar_bd()
    nombre = input("Nombre: ")
    dni = input("DNI: ")
    fecha_nacimiento = input("Fecha de nacimiento: ")
    telefono = input("Teléfono: ")
    cliente = Cliente(nombre, dni, fecha_nacimiento, telefono)
    insertar_cliente(conn, cliente)
    desconectar_bd(conn)


def insertar_cliente(conn, cliente):
    cursor = conn.cursor()
    sql = "INSERT INTO cliente(nombre, dni, fecha_nacimiento, telefono) VALUES (%s, %s, %s, %s)"
    datos = (cliente.nombre, cliente.dni, cliente.fecha_nacimiento, cliente.telefono)
    cursor.execute(sql, datos)
    conn.commit()
    print("Cliente insertado correctamente")


# Baja de cliente
def baja_cliente():
    conn = conectar_bd()
    dni = input("Introduce el DNI del cliente: ")
    borrar_cliente(conn, dni)
    desconectar_bd(conn)


def borrar_cliente(conn, dni):
    cursor = conn.cursor()
    sql = "DELETE FROM cliente WHERE dni = %s"
    cursor.execute(sql, (dni,))
    conn.commit()
    print("Cliente borrado correctamente")


# Mostrar datos de un cliente
def mostrar_cliente():
    conn = conectar_bd()
    dni = input("Introduce el DNI del cliente: ")
    cliente = buscar_cliente(conn, dni)
    if cliente:
        print("Nombre: ", cliente.nombre)
        print("DNI: ", cliente.dni)
        print("Fecha de nacimiento: ", cliente.fecha_nacimiento)
        print("Teléfono: ", cliente.telefono)
    else:
        print("Cliente no encontrado")
    desconectar_bd(conn)


def mostrar_clientes():
    conn = conectar_bd()
    clientes = buscar_clientes(conn)
    for cliente in clientes:
        print("Nombre: ", cliente.nombre)
        print("DNI: ", cliente.dni)
        print("Fecha de nacimiento: ", cliente.fecha_nacimiento)
        print("Teléfono: ", cliente.telefono)
    desconectar_bd(conn)


def buscar_cliente(conn, dni):
    cursor = conn.cursor()
    sql = "SELECT nombre, dni, fecha_nacimiento, telefono FROM cliente WHERE dni = %s"
    cursor.execute(sql, (dni,))
    row = cursor.fetchone()
    if row:
        cliente = Cliente(row[0], row[1], row[2], row[3])
        return cliente
    else:
        return None


def buscar_clientes(conn):
    cursor = conn.cursor()
    sql = "SELECT nombre, dni, fecha_nacimiento, telefono FROM cliente"
    cursor.execute(sql)
    rows = cursor.fetchall()
    clientes = []
    for row in rows:
        cliente = Cliente(row[0], row[1], row[2], row[3])
        clientes.append(cliente)
    return clientes


def matricular_cliente():
    conn = conectar_bd()
    dni = input("Introduce el DNI del cliente: ")
    cliente = buscar_cliente(conn, dni)
    if cliente:
        deporte = buscar_deporte(conn)
        if deporte:
            insertar_matricula(conn, cliente, deporte)
        else:
            print("Deporte no encontrado")
    else:
        print("Cliente no encontrado")
    desconectar_bd(conn)


def buscar_deporte(conn):
    cursor = conn.cursor()
    nombre = input("Introduce el nombre del deporte: ")
    sql = "SELECT nombre, precio_hora FROM deporte WHERE nombre = %s"
    cursor.execute(sql, (nombre,))
    row = cursor.fetchone()
    if row:
        deporte = Deporte(row[0], row[1])
        return deporte
    else:
        return None


def insertar_matricula(conn, cliente, deporte):
    crear_tabla_matricula(conn)
    cursor = conn.cursor()
    sql = "INSERT INTO matricula(dni, nombre) VALUES (%s, %s)"
    datos = (cliente.dni, deporte.nombre)
    cursor.execute(sql, datos)
    conn.commit()
    print("Matrícula insertada correctamente")

#Crear tabla matricula N:M con horario solo si no existe
def crear_tabla_matricula(conn):
    cursor = conn.cursor()
    sql = "CREATE TABLE matricula (dni VARCHAR(9), nombre VARCHAR(50), horario VARCHAR(10))"
    cursor.execute(sql)
    conn.commit()
    print("Tabla matricula creada correctamente")


# Desmatricular cliente
def desmatricular_cliente():
    conn = conectar_bd()
    dni = input("Introduce el DNI del cliente: ")
    borrar_matricula(conn, dni)
    desconectar_bd(conn)


def borrar_matricula(conn, dni):
    cursor = conn.cursor()
    sql = "DELETE FROM matricula WHERE dni = %s"
    cursor.execute(sql, (dni,))
    conn.commit()
    print("Matrícula borrada correctamente")


# Mostrar deportes de un cliente
def mostrar_deportes_cliente():
    conn = conectar_bd()
    dni = input("Introduce el DNI del cliente: ")
    cliente = buscar_cliente(conn, dni)
    if cliente:
        deportes = buscar_deportes_cliente(conn, dni)
        for deporte in deportes:
            print("Nombre: ", deporte.nombre)
            print("Precio: ", deporte.precio_hora)
    else:
        print("Cliente no encontrado")
    desconectar_bd(conn)


def buscar_deportes_cliente(conn, dni):
    cursor = conn.cursor()
    sql = "SELECT nombre, precio_hora FROM deporte WHERE nombre IN (SELECT nombre FROM matricula WHERE dni = %s)"
    cursor.execute(sql, (dni,))
    rows = cursor.fetchall()
    deportes = []
    for row in rows:
        deporte = Deporte(row[0], row[1])
        deportes.append(deporte)
    return deportes


# Insertar deportes y su precio de una lista
def insertar_deportes():
    conn = conectar_bd()
    deportes = [("Fútbol", 10), ("Baloncesto", 8), ("Tenis", 12), ("Padel", 10), ("Patinaje", 6)]
    for deporte in deportes:
        insertar_deporte(conn, deporte)
    desconectar_bd(conn)

def insertar_deporte(conn, deporte):
    cursor = conn.cursor()
    sql = "INSERT INTO deporte(nombre, precio_hora) VALUES (%s, %s)"
    datos = (deporte[0], deporte[1])
    cursor.execute(sql, datos)
    conn.commit()
    print("Deporte insertado correctamente")

