from DataStructures.List import list_node as node

def new_list():
    newlist = {
        "first": None,
        "last": None,
        "size": 0,
    }
    return newlist

def get_element(my_list, pos):
    searchpos = 0
    node = my_list["first"]
    while searchpos < pos:
        node = node["next"]
        searchpos += 1
    return node["info"]

def is_present(my_list, element, cmp_function):
    is_in_array = False
    temp = my_list["first"]
    count = 0
    while not is_in_array and temp is not None:
        if cmp_function(element, temp["info"]) == 0:
            is_in_array = True
        else:
            temp = temp["next"]
            count += 1
    
    if not is_in_array:
        count = -1
    return count

def add_first(my_list, element):
    nodo = node.new_single_node(element)
    nodo["next"] = my_list["first"]
    my_list["first"] = nodo
    
    if my_list["size"] == 0:
        my_list["last"] = nodo
    
    my_list["size"] +=1
    return my_list

def add_last(my_list, element):
    nodo = node.new_single_node(element)
    
    if my_list["size"] == 0:
        my_list["first"] = nodo
    else:
        my_list["last"]["next"] = nodo
        
    my_list["last"] = nodo
    my_list["size"] += 1
    return my_list

def size(my_list):
    return my_list["size"]

def is_empty(my_list):
        return my_list["size"] == 0 #Si la condicion es cierta retorna True

def first_element(my_list):
    if is_empty(my_list):
        raise Exception("IndexError: list index out of range")
    else:
        return my_list["first"]["info"]

def last_element(my_list):
    if is_empty(my_list):
        raise Exception("IndexError: list index out of range")
    else:
        return my_list["last"]["info"]
    
def remove_first(my_list):
    if is_empty(my_list):
        raise Exception("IndexError: list index out of range")
    else:
        valor= my_list["first"]["info"]
        my_list["first"] = my_list["first"]["next"]
        my_list["size"] -= 1
        
        if my_list["size"] == 0:
            my_list["last"] = None
    return valor

def remove_last(my_list):
    if is_empty(my_list):
        raise Exception("IndexError: list index out of range")
    else:
        valor = my_list["last"]["info"]
        if my_list["size"]==1:
            return remove_first(my_list)
        else:
            actual = my_list["first"]
            while actual["next"] != my_list["last"]:
                actual = actual["next"]
            
            actual["next"] = None
            my_list["last"] = actual
            my_list["size"] -= 1
        
    return valor
            
def delete_element(my_list, pos):
    if pos < 0 or pos >= size(my_list):
        raise Exception('IndexError: list index out of range')
    else:
        if pos == 0:
            remove_first(my_list)
        elif pos == size(my_list)-1:
            remove_last(my_list)
        else:
            anterior = my_list["first"]
            for i in range(pos - 1): #se detiene en el anterior a eliminar
                anterior = anterior["next"]
            anterior["next"] = anterior["next"]["next"]
            my_list["size"] -=1
        
    return my_list
    
def insert_element(my_list, element, pos):
    if pos < 0 or pos > size(my_list):
        raise Exception('IndexError: list index out of range')
    else:
        if pos == 0:
            add_first(my_list, element)
        elif pos == my_list["size"]:
            add_last(my_list, element)
        else:
            nodo = node.new_single_node(element)
            anterior = my_list["first"]
            for i in range(pos-1):
                anterior = anterior["next"]
            nodo["next"] = anterior["next"]
            anterior["next"] = nodo
            my_list["size"] += 1
    return my_list

def change_info(my_list, pos, new_info):
    if pos < 0 or pos >= size(my_list):
        raise Exception('IndexError: list index out of range')
    else:
        actual = my_list["first"]
        for i in range(pos):
            actual = actual["next"]
        actual["info"] = new_info
    return my_list
    
def exchange(my_list, pos_1, pos_2):
    if (pos_1 < 0 or pos_1 >= size(my_list)) or \
        (pos_2 < 0 or pos_2 >= size(my_list)):
        raise Exception('IndexError: list index out of range')
    else:
        if pos_1 != pos_2:
            nodo_1, nodo_2 = None, None
            actual = my_list["first"]
            for i in range(pos_2 +1):
                if i == pos_1:
                    nodo_1 = actual 
                if i == pos_2:
                    nodo_2 = actual
                actual = actual["next"]
            
            auxiliar = nodo_1["info"]
            nodo_1["info"] = nodo_2["info"]
            nodo_2["info"] = auxiliar 
    return my_list
            
def sub_list(my_list, pos, num_elements):
    if pos < 0 or pos >= size(my_list) or (pos + num_elements > size(my_list)):
        raise Exception('IndexError: list index out of range')
    else:
        nueva_lista = new_list()
        actual = my_list["first"]
        
        for i in range(pos):
            actual = actual["next"]
            
        for i in range(num_elements):
            add_last(nueva_lista, actual["info"])
            actual = actual["next"]
        
        return nueva_lista

def default_sort_criteria(element_1, element_2):
    is_sorted = False
    if element_1 < element_2:
        is_sorted = True
    return is_sorted

def selection_sort(my_list, sort_crit):
    size_list = size(my_list)
    if size_list <= 1:
        return my_list
    else:
        nodo_base = my_list["first"]
        while nodo_base != None:
            nodo_act = nodo_base["next"]
            nodo_min = nodo_base
            while nodo_act != None:
                if sort_crit(nodo_act["info"], nodo_min["info"]):
                    nodo_min = nodo_act
                nodo_act = nodo_act["next"]
            if nodo_min != nodo_base:
                temp = nodo_base["info"]
                nodo_base["info"] = nodo_min["info"]
                nodo_min["info"] = temp
            nodo_base = nodo_base["next"]
            
    """ Si quitamos las posiciones y no llamamos exchage,
    la complejidad del algoritmo bajaria"""
    return my_list

def insertion_sort(my_list, sort_crit):

    if my_list["size"] <= 1:
        return my_list

    primer_ordenado = my_list["first"]
    nodo_desordenado = primer_ordenado["next"]

    primer_ordenado["next"] = None

    while nodo_desordenado is not None:

        siguiente = nodo_desordenado["next"]

        # meterlo al inicio
        if sort_crit(nodo_desordenado["info"], my_list["first"]["info"]):
            nodo_desordenado["next"] = my_list["first"]
            my_list["first"] = nodo_desordenado

        else:
            actual = my_list["first"]

            while (actual["next"] is not None and
                   not sort_crit(nodo_desordenado["info"], actual["next"]["info"])):
                actual = actual["next"]

            nodo_desordenado["next"] = actual["next"]
            actual["next"] = nodo_desordenado

        nodo_desordenado = siguiente

    # actualizar el last
    ultimo = my_list["first"]
    while ultimo["next"] is not None:
        ultimo = ultimo["next"]

    my_list["last"] = ultimo

    return my_list

def shell_sort(my_list, sort_crit):
    size_list = size(my_list)
    if size_list <= 1:
        return my_list
    else:
        h = 1
        while h < size_list:
            h = 3 * h + 1
        while h > 0:
            for i in range(h, size_list):
                valor = get_element(my_list, i)
                posicion = i
                while posicion >= h and sort_crit(valor, get_element(my_list, posicion - h)):
                    change_info(my_list, posicion, get_element(my_list, posicion - h))
                    posicion -= h
                change_info(my_list, posicion, valor)
            h = h // 3
    return my_list

def merge_sort(my_list, sort_crit):
    if is_empty(my_list) or size(my_list) == 1:
        return my_list
    mitad = size(my_list) // 2
    lista_izq = sub_list(my_list, 0, mitad)
    lista_der = sub_list(my_list, mitad, size(my_list) - mitad)
    izq = merge_sort(lista_izq, sort_crit)
    der = merge_sort(lista_der, sort_crit)
    return merge(izq, der, sort_crit)

def merge(izq, der, sort_crit): # para linked
    nueva = new_list()
    while not is_empty(izq) and not is_empty(der):
        dere = first_element(der)
        izqu = first_element(izq)
        if sort_crit(izqu, dere):
            add_last(nueva, remove_first(izq)) # se pone add_last(nueva, remove_first(izq)) para evitar doble llamado
        else:
            add_last(nueva, remove_first(der))
    while not is_empty(izq):
        add_last(nueva, first_element(izq))
        remove_first(izq)
    while not is_empty(der):
        add_last(nueva, first_element(der))
        remove_first(der)
    return nueva

def quick_sort(my_list, sort_crit):
    if size(my_list) <= 1:
        return my_list
    
    quick_sort_recursive(my_list, my_list["first"], my_list["last"], sort_crit)
    return my_list

def quick_sort_recursive(my_list, low_node, high_node, sort_crit):
    if low_node != None and low_node != high_node and low_node != high_node["next"]:
        pivote = partition(my_list, low_node, high_node, sort_crit)
        
        if pivote != low_node:
            anterior = low_node
            while anterior["next"] != pivote:
                anterior = anterior["next"]
            quick_sort_recursive(my_list, low_node, anterior, sort_crit)
            
        quick_sort_recursive(my_list, pivote["next"], high_node, sort_crit)

def partition(my_list, low_node, high_node, sort_crit):
    if is_empty(my_list):
        return None
    
    pivote = high_node["info"]
    i = low_node
    j = low_node
    
    while j != high_node:
        if sort_crit(j["info"], pivote):
            temp = i["info"]
            i["info"] = j["info"]
            j["info"] = temp
            i = i["next"]
        j = j["next"]
        
    temp = i["info"]
    i["info"] = high_node["info"]
    high_node["info"] = temp
    return i

def default_function(elemen_1, element_2):

   if elemen_1 > element_2:
      return 1
   elif elemen_1 < element_2:
      return -1
   return 0