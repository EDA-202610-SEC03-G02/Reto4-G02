from DataStructures.Tree import rbt_node as rbt
from DataStructures.List import single_linked_list as sl

def new_map():
  my_rbt = {
    "root": None,
    "type": "RBT"
  }
  return my_rbt

def default_compare(key, element):
  node_key= element["key"]
  if key<node_key:
    return -1
  elif key>node_key:
    return 1
  else:
    return 0
  
def rotate_left(node_rbt):
  if node_rbt is None or node_rbt["right"] is None:
    return node_rbt
  
  new_root= node_rbt["right"]
  node_rbt["right"]= new_root["left"]
  new_root["left"]= node_rbt
  new_root["color"]= node_rbt["color"]
  node_rbt["color"]= rbt.RED
  
  new_root["size"]= node_rbt["size"]
  size_left= size_tree(node_rbt["left"])
  size_right= size_tree(node_rbt["right"])
  node_rbt["size"]= 1 + size_left + size_right
  return new_root

def rotate_right(node_rbt):
  if node_rbt is None or node_rbt["left"] is None:
    return node_rbt
  new_root= node_rbt["left"]
  node_rbt["left"]= new_root["right"]
  new_root["right"]= node_rbt
  new_root["color"]= node_rbt["color"]
  node_rbt["color"]= rbt.RED
  
  new_root["size"]= node_rbt["size"]
  size_left= size_tree(node_rbt["left"])
  size_right= size_tree(node_rbt["right"])
  node_rbt["size"]= 1 + size_left + size_right
  return new_root

def flip_node_color(node_rbt):
  if node_rbt["color"]==rbt.RED:
    node_rbt["color"]=rbt.BLACK
  else:
    node_rbt["color"]=rbt.RED
  return node_rbt

def flip_colors(node_rbt):
  node_rbt= flip_node_color(node_rbt)
  if node_rbt["left"] is not None:
    node_rbt["left"]= flip_node_color(node_rbt["left"])
  if node_rbt["right"] is not None:
    node_rbt["right"]= flip_node_color(node_rbt["right"])
  return node_rbt
  
def size_tree(node_rbt):
  if node_rbt is None:
    return 0
  else:
    return node_rbt["size"]
  
def insert_node(root, key, value):
  if root is None:
    return rbt.new_node(key, value)
  
  comp = default_compare(key, root)
  if comp<0:
    root["left"]= insert_node(root["left"], key, value)
  elif comp>0:
    root["right"]= insert_node(root["right"], key, value)
  else:
    root["value"]= value
  
  if rbt.is_red(root["right"]) and not rbt.is_red(root["left"]):
    root = rotate_left(root)
  if rbt.is_red(root["left"]) and rbt.is_red(root["left"]["left"]):
    root = rotate_right(root)
  if rbt.is_red(root["left"]) and rbt.is_red(root["right"]):
    root = flip_colors(root)
  
  root["size"]= 1 + size_tree(root["left"]) + size_tree(root["right"])
  return root

def put(my_rbt, key, value):
  my_rbt["root"]= insert_node(my_rbt["root"], key, value)
  if my_rbt["root"] is not None:
    my_rbt["root"]["color"]= rbt.BLACK
  return my_rbt

def get(my_rbt, key):
  return get_node(my_rbt["root"], key)

def get_node(root, key):
  while root is not None:
    if key<root["key"]:
      root = root["left"]
    elif key > root["key"]:
      root = root["right"]
    else:
      return root["value"]
  return None

def contains(my_rbt, key):
  return get(my_rbt, key) is not None

def size(my_rbt):
  return size_tree(my_rbt["root"])

def is_empty(my_rbt):
  return size(my_rbt) == 0

def key_set(my_rbt):
  key_list = sl.new_list()
  return key_set_tree(my_rbt["root"], key_list)

def key_set_tree(root, key_list):
  if root is not None:
    key_set_tree(root["left"], key_list)
    sl.add_last(key_list, root["key"])
    key_set_tree(root["right"], key_list)
  return key_list
  
def value_set(my_rbt):
  value_list = sl.new_list()
  return value_set_tree(my_rbt["root"], value_list)

def value_set_tree(root, value_list):
  if root is not None:
    value_set_tree(root["left"], value_list)
    sl.add_last(value_list, root["value"])
    value_set_tree(root["right"], value_list)
  return value_list

def get_min(my_rbt):
  return get_min_node(my_rbt["root"])

def get_min_node(root):
  if root is None:
    return None
  while root["left"] is not None:
    root = root["left"]
  return root["key"]

def get_max(my_rbt):
  return get_max_node(my_rbt["root"])

def get_max_node(root):
  if root is None:
    return None
  while root["right"] is not None:
    root = root["right"]
  return root["key"]

def height(my_rbt):
  return height_tree(my_rbt["root"])

def height_tree(root):
  if root is None:
    return -1
  
  altura_izq = height_tree(root["left"])
  altura_der = height_tree(root["right"])
  
  if altura_izq > altura_der:
    return 1 + altura_izq
  else:
    return 1 + altura_der

def keys(my_rbt, key_initial, key_final):
  lista_llaves = sl.new_list()
  return keys_range(my_rbt["root"], key_initial, key_final, lista_llaves)

def keys_range(root, key_initial, key_final, key_list):
  if root is None:
    return key_list
  
  if key_initial < root["key"]:
    keys_range(root["left"], key_initial, key_final, key_list)
  
  if key_initial <= root["key"] and root["key"] <= key_final:
    sl.add_last(key_list, root["key"])
  
  if root["key"] < key_final:
    keys_range(root["right"], key_initial, key_final, key_list)
  
  return key_list

def values(my_rbt, key_initial, key_final):
  lista_valores = sl.new_list()
  return values_range(my_rbt["root"], key_initial, key_final, lista_valores)

def values_range(root, key_initial, key_final, value_list):
  if root is None:
    return value_list
  
  if key_initial < root["key"]:
    values_range(root["left"], key_initial, key_final, value_list)
  
  if key_initial <= root["key"] and root["key"] <= key_final:
    sl.add_last(value_list, root["value"])
  
  if root["key"] < key_final:
    values_range(root["right"], key_initial, key_final, value_list)
  
  return value_list