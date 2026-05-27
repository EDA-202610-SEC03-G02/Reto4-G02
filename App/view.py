import sys
import App.logic as logic
from tabulate import tabulate
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as lp
from DataStructures.Graph import diagraph as gr

def new_logic():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función de la lógica donde se crean las estructuras de datos
    control = logic.new_logic()
    return control

def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")

def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    numero_data = input("Ingrese el número de datos a cargar entre 20, 40, 60, 80, 100: ")
    while numero_data not in ["20", "40", "60", "80", "100"]:
        print("Número de datos no válido")
        numero_data = input("Ingrese el número de datos a cargar entre 20, 40, 60, 80, 100: ")
        
    input_file = f"ais_maritime_traffic_{numero_data}pct.csv"
    datos = logic.load_data(control, input_file)
    
    print(f"\nTiempo de carga: {datos['tiempo']} ms")
    print(f"Total de embarcaciones: {datos['total_vessels']}")
    print(f"Total de registros: {datos['total_records']}")
    print(f"Total de vértices: {datos['total_vertices']}")
    print(f"Total de arcos: {datos['total_arcos']}")
    
    print("\nPrimeros 5 vértices:")
    primeros_5 = []
    
    for i in range(len(datos["primeros_5"])):
        vertice = datos["primeros_5"][i]
        vertice_info = print_vertice(vertice)
        primeros_5.append(vertice_info)
    print(tabulate(primeros_5, headers="keys", tablefmt="fancy_grid"))
    
    print("\nÚltimos 5 vértices:")
    ultimos_5 = []
    
    for i in range(len(datos["ultimos_5"])):
        vertice = datos["ultimos_5"][i]
        vertice_info = print_vertice(vertice)
        ultimos_5.append(vertice_info)
    print(tabulate(ultimos_5, headers="keys", tablefmt="fancy_grid"))
    
    print("\nDatos cargados exitosamente\n")
    
def print_vertice(vertice):

    mmsi_str = ""
    size_mmsi = al.size(vertice["mmsi_list"])
    if size_mmsi >= 3:
        limite_a_mostrar = 3
    else:
        limite_a_mostrar = size_mmsi
        
    for i in range(limite_a_mostrar):  
        mmsi_str += str(al.get_element(vertice["mmsi_list"], i))
        if i < limite_a_mostrar:
            mmsi_str += ", "
    if size_mmsi > 3:
        mmsi_str+= ", ..."
    return {
        "ID vertice": vertice["id"],
        "Latitud": vertice["lat"],
        "Longitud": vertice["lon"],
        "Embarcaciones asociadas": mmsi_str,
        "Registros asociados": vertice["records_count"],
        "Velocidad promedio": vertice["avg_sog"]
    }
       
def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    pass


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass

# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 1:
            print_req_1(control)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 6:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
