from DataStructures.List import single_linked_list as lt

def new_queue():
    queue=lt.new_list()
    return queue

def enqueue(queue, element):
    lt.add_last(queue, element)
    return queue

def dequeue(queue):
    if lt.is_empty(queue):
        return None
    return lt.remove_first(queue)

def is_empty(queue):
    return lt.is_empty(queue)

def peek(queue):
    if lt.is_empty(queue):
        return None
    else:
        element=lt.first_element(queue)
        return element
    
def size(queue): 
    return lt.size(queue)    
