from DataStructures.List import array_list as al
from DataStructures.Priority_queue import pq_entry as pqe

def default_compare_higher_value(father_node, child_node):
    if pqe.get_priority(father_node) >= pqe.get_priority(child_node):
        return True
    else:
        return False

def default_compare_lower_value(father_node, child_node):
    if pqe.get_priority(father_node) <= pqe.get_priority(child_node):
        return True
    else:
        return False
    
def priority(my_heap, parent, child):
    return my_heap["cmp_function"](parent, child)    

def new_heap(is_min_pq=True):
    cmp_function = default_compare_lower_value if is_min_pq else default_compare_higher_value
    heap_list = al.new_list()
    al.add_last(heap_list, None)   
    return {
        "elements": heap_list,     
        "size": 0,
        "cmp_function": cmp_function 
    }

def swim(my_heap, pos):
    j = pos
    while j // 2 >= 1:
        padre = al.get_element(my_heap["elements"], j // 2)
        hijo  = al.get_element(my_heap["elements"], j)
        if not priority(my_heap, padre, hijo):
            al.exchange(my_heap["elements"], j // 2, j)  
            j = j // 2
        else:
            break
    return my_heap

def sink(my_heap, pos):
    j = pos
    n = my_heap["size"]
    while 2 * j <= n:
        k = 2 * j                          
        if k < n:                          
            izq = al.get_element(my_heap["elements"], k)
            der = al.get_element(my_heap["elements"], k + 1)
            if not priority(my_heap, izq, der):   
                k += 1
        padre = al.get_element(my_heap["elements"], j)
        hijo  = al.get_element(my_heap["elements"], k)
        if not priority(my_heap, padre, hijo):  
            al.exchange(my_heap["elements"], j, k)
            j = k
        else:
            break
    return my_heap

def insert(my_heap, priority_val, value):
    nuevo = pqe.new_pq_entry(priority_val, value)
    al.add_last(my_heap["elements"], nuevo)
    my_heap["size"] += 1                   
    swim(my_heap, my_heap["size"])         
    return my_heap

def size(my_heap):
    return my_heap["size"]

def is_empty(my_heap):
    return size(my_heap)==0

def remove(my_heap):
    if is_empty(my_heap):
        return None
    al.exchange(my_heap["elements"], 1, my_heap["size"])
    eliminado = al.remove_last(my_heap["elements"])
    my_heap["size"] -= 1
    if not is_empty(my_heap):
        sink(my_heap, 1)
    return pqe.get_value(eliminado) 

def get_first_priority(my_heap):
    if is_empty(my_heap):
        return None
    return pqe.get_value(al.get_element(my_heap["elements"], 1))

def is_present_value(my_heap, value):
    for i in range(1, size(my_heap)+1):
        if pqe.get_value(al.get_element(my_heap["elements"], i))==value:
            return i
    return -1

def improve_priority(my_heap, priority_val, value):
    pos = is_present_value(my_heap, value)
    if pos == -1:
        return None
    entrada = al.get_element(my_heap["elements"], pos)   
    pqe.set_priority(entrada, priority_val)
    swim(my_heap, pos)
    return my_heap

def contains(my_heap, value):
    return is_present_value(my_heap, value) != -1