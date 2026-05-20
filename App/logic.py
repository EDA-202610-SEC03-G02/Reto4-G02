import time 
from DataStructures import map as mp

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    analyzer = {}
    capacity = 1000000 # revisar el numero
    analyzer["vertices_map"] = mp.new_map(capacity) #HECHO
    analyzer["mmsi_records_map"] = mp.new_map(capacity)
    analyzer["edge_info_map"] = mp.new_map(capacity)
    analyzer["g_distance"] = gr.new_graph() # revisar parametro
    analyzer["total_records"] = 0
    analyzer["total_vessels"] = 0

    return analyzer


# Funciones para la carga de datos
def new_cluster(dest_cluster):
    cluster = {
        "id": dest_cluster,

        "lat_sum": 0.0,
        "lon_sum": 0.0,
        "sog_sum": 0.0,
        "length_sum": 0.0,
        "width_sum": 0.0,
        "draft_sum": 0.0,

        "records_count": 0,

        "mmsi_list": al.new_list(),
        "vessel_names": al.new_list(),
        "vessel_types": al.new_list(),
        "cargo_types": al.new_list(),
        "speed_categories": al.new_list(),

        "records": al.new_list(),

        "lat": None,
        "lon": None,
        "avg_sog": None,
        "avg_length": None,
        "avg_width": None,
        "avg_draft": None
    }

    return cluster

def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    
    star_time = get_time()
    computer_file = data_dir + filename
    file = open(computer_file, encoding="utf-8")
    input_file = csv.DictReader(file)
    
    for record in input_file:
        cluster_id = record["DEST_CLUSTER"].lower().strip()
        if mp.get(catalog["vertices_map"], cluster_id) is None:
            new_info = new_cluster(cluster_id)
            mp.put(catalog["vertices_map"], cluster_id, new_info)
        else:
            cluster = mp.get(catalog["vertices_map"], cluster_id)
        cluster["lat_sum"] += float(record["lat"])
        cluster["lon_sum"] += float(record["lon"])
        cluster["sog_sum"] += float(record["sog"])
        cluster["length_sum"] += float(record["length"])
        cluster["width_sum"] += float(record["width"])
        cluster["draft_sum"] += float(record["draft"])
        cluster["records_count"] += 1
        #APPENDS EN LAS LISTAS
        al.add_last(cluster["records"], record)
        #PROMEDIOS
        
        
        
# Funciones de consulta sobre el catálogo


def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
