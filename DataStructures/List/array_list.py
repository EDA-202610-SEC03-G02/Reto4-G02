import random as random

def new_list():
    newlist = {
        'elements': [],
        'size': 0,
    }
    return newlist

def get_element(my_list, pos):
    if not 0 <= pos < size(my_list):
        raise Exception("IndexError: list index out of range")
    return my_list["elements"][pos]

def is_present(my_list, element, cmp_function):
    
    size = my_list["size"]
    if size > 0:
        keyexist = False
        for keypos in range(0, size):
            info = my_list["elements"][keypos]
            if cmp_function(element, info) == 0:
                keyexist = True
                break
        if keyexist:
            return keypos
    return -1

def add_first(my_list, element):
    my_list["elements"].insert(0, element)
    my_list["size"] += 1
    return my_list

def add_last(my_list, element):
    my_list["elements"].append(element)
    my_list["size"] += 1
    return my_list

def size(my_list):
    return my_list["size"]

def first_element(my_list):
    if is_empty(my_list):
        raise Exception("IndexError: list index out of range")
    return my_list["elements"][0]

def is_empty(my_list):
    
    return my_list["size"] == 0


def last_element(my_list):
    if is_empty(my_list):
        raise Exception("IndexError: list index out of range")
    return my_list["elements"][my_list["size"] - 1]

def delete_element(my_list, pos):
    if pos < 0 or pos >= size(my_list):
        raise Exception("IndexError: list index out of range")
    my_list["elements"].pop(pos)
    my_list["size"] -= 1
    return my_list

def remove_first(my_list):
    if is_empty(my_list):
        raise Exception("IndexError: list index out of range")
    a=my_list["elements"].pop(0)
    my_list["size"] -= 1
    return a
    
def remove_last(my_list):
    if is_empty(my_list):
        raise Exception("IndexError: list index out of range")
    a=my_list["elements"].pop(my_list["size"]-1)
    my_list["size"] -= 1
    return a
    
def insert_element(my_list, pos, element):
    
    my_list["elements"].insert(pos, element)
    my_list["size"] += 1
    return my_list

def change_info(my_list, pos, element):
    if pos < 0 or pos >= size(my_list):
        raise Exception('IndexError: list index out of range')
    my_list["elements"][pos] = element
    return my_list

def exchange(my_list, pos1, pos2):
    if (pos1 < 0 or pos1 >= size(my_list)) or \
        (pos2 < 0 or pos2 >= size(my_list)):
        raise Exception('IndexError: list index out of range')
    temp = my_list["elements"][pos1]
    my_list["elements"][pos1] = my_list["elements"][pos2]
    my_list["elements"][pos2] = temp
    return my_list

def sub_list(my_list, pos, num_elements):
    if pos < 0 or pos >= my_list["size"] or (pos + num_elements > my_list["size"]):
        raise Exception('IndexError: list index out of range')
    sublist = {
        'elements': [],
        'size': 0,
    }
    for i in range(pos, pos + num_elements):
        sublist["elements"].append(my_list["elements"][i])
        sublist["size"] += 1
    return sublist

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
        for i in range(0, size_list - 1): # para que no se salga del rango en el segundo for (i+1)
            for j in range(i+1, size_list):
                base = my_list["elements"][i] # elemento base para comparar con los demás
                actual = my_list["elements"][j]  # elemento actual para comparar con el base       
                if sort_crit(actual, base):
                    exchange(my_list, i, j)
    return my_list


def insertion_sort(my_list, sort_crit):

    for i in range(1, size(my_list)):
        valor = get_element(my_list, i)
        posicion = i

        while posicion > 0 and sort_crit(valor, get_element(my_list, posicion - 1)):
            change_info(my_list, posicion, get_element(my_list, posicion - 1))
            posicion -= 1

        change_info(my_list, posicion, valor)

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
    resultado = merge(izq, der, sort_crit)
    
    my_list["elements"] = resultado["elements"]
    my_list["size"] = resultado["size"]
    return my_list

def merge(izq, der, sort_crit): # para array
    nueva = new_list()
    i = 0
    j = 0
    while i < size(izq) and j < size(der):
        dere = get_element(der, j)
        izqu = get_element(izq, i)
        if sort_crit(izqu, dere):
            add_last(nueva, izqu)
            i += 1
        else:
            add_last(nueva, dere)
            j += 1
    while i < size(izq):
        add_last(nueva, get_element(izq, i))
        i += 1
    while j < size(der):
        add_last(nueva, get_element(der, j))
        j += 1
    return nueva

def quick_sort(my_list, sort_crit):
    if size(my_list) <= 1:
        return my_list
    quick_sort_recursive(my_list, 0, size(my_list) - 1, sort_crit)
    return my_list


def quick_sort_recursive(my_list, low, high, sort_crit):
    if low < high:
        pivot_index = partition(my_list, low, high, sort_crit)
        quick_sort_recursive(my_list, low, pivot_index - 1, sort_crit)
        quick_sort_recursive(my_list, pivot_index + 1, high, sort_crit)


def partition(my_list, low, high, sort_crit):
    pivote = get_element(my_list, high)
    i = low - 1
    for j in range(low, high):
        if not sort_crit(pivote, get_element(my_list, j)):
            i += 1
            exchange(my_list, i, j)
    exchange(my_list, i + 1, high)
    return i + 1