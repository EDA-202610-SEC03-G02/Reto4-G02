from DataStructures.List import single_linked_list as lt

def new_stack():
    return lt.new_list()

def size(my_stack):
    return lt.size(my_stack)

def is_empty(my_stack):
    return size(my_stack)==0

def push(my_stack, element):
    return lt.add_first(my_stack, element) # se deja como tope el inicio, se añade al inicio

def pop(my_stack):
    if is_empty(my_stack):
        raise Exception('EmptyStructureError: stack is empty')
    return lt.remove_first(my_stack) # LIFO, se borra el ultimo en entrar al tope

def top(my_stack):
    if is_empty(my_stack):
        raise Exception('EmptyStructureError: stack is empty')
    return lt.first_element(my_stack)