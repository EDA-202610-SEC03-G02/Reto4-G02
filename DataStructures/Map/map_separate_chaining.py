from DataStructures.Map import map_functions as mf
from DataStructures.Map import map_entry as me
import random as rd
from DataStructures.List import array_list as al


def new_map(num_elements, load_factor, prime=109345121):
   capacity = mf.next_prime(num_elements/load_factor)
   scale = rd.randint(1,prime-1) # a en la funcion MAD
   shift = rd.randint(0,prime-1) # b en la funcion MAD
   mi_lista = al.new_list()
  
   for i in range(capacity):
       bucket = al.new_list()
       al.add_last(mi_lista, bucket)
      
   return {"prime": prime,
           "capacity" : capacity,
           "scale": scale,
           "shift": shift,
           "table": mi_lista,
           "current_factor": 0,
           "limit_factor": load_factor,
           "size": 0
   }
  
def default_compare(key, entry):
   if key == me.get_key(entry):
       return 0
   elif key > me.get_key(entry):
       return 1
   return -1


def rehash(my_map):
   mapa_viejo = my_map["table"]
   mapa_nuevo = new_map(my_map["size"]*2, my_map["limit_factor"], my_map["prime"])
  
   my_map["table"] = mapa_nuevo["table"]
   my_map["capacity"] = mapa_nuevo["capacity"]
   my_map["size"] = 0
  
  
   for i in range(al.size(mapa_viejo)):
       bucket = al.get_element(mapa_viejo, i)
       for j in range(al.size(bucket)):
           entry = al.get_element(bucket, j)
          
           put_n_rehash(my_map, me.get_key(entry), me.get_value(entry))
  
   return my_map


def put(my_map, key, value):
   hash_key = mf.hash_value(my_map, key)
   bucket = al.get_element(my_map["table"], hash_key)
  
   for i in range(al.size(bucket)):
       entry = al.get_element(bucket, i)
       if default_compare(key, entry) == 0:
           me.set_value(entry, value)
           return my_map
          
   new_entry = me.new_map_entry(key, value)
   al.add_last(bucket, new_entry)
   my_map["size"] += 1
      
   if my_map["size"]/my_map["capacity"] > my_map["limit_factor"]:
       rehash(my_map)
  
   return my_map


def put_n_rehash(my_map, key, value):
   hash_key = mf.hash_value(my_map, key)
   bucket = al.get_element(my_map["table"], hash_key)
  
   for i in range(al.size(bucket)):
       entry = al.get_element(bucket, i)
       if default_compare(key, entry) == 0:
           me.set_value(entry, value)
           return my_map
          
   new_entry = me.new_map_entry(key, value)
   al.add_last(bucket, new_entry)
   my_map["size"] += 1
  
   return my_map


def contains (my_map, key):
   hash_key = mf.hash_value(my_map, key)
   bucket = al.get_element(my_map["table"], hash_key)
  
   for i in range(al.size(bucket)):
       entry = al.get_element(bucket, i)
       if default_compare(key, entry) == 0:
           return True
   return False


def get(my_map, key):
  pos = mf.hash_value(my_map, key)
  bucket = al.get_element(my_map["table"], pos)


  for i in range(al.size(bucket)):
      elem = al.get_element(bucket, i)
      if elem["key"] == key:
          return elem["value"]  
  return None


def remove(my_map, key):
  pos = mf.hash_value(my_map, key)
  bucket = al.get_element(my_map["table"], pos)




  for i in range(al.size(bucket)):
      entry = al.get_element(bucket, i)
      if entry["key"] == key:
          removed_value = entry["value"]
          al.delete_element(bucket, i)
          my_map["size"] -= 1
          return removed_value
  return None


def size(my_map):
   return my_map["size"]


def is_empty(my_map):
   return size(my_map) == 0


def key_set(my_map):
   keys= al.new_list()
  
   for i in range(al.size(my_map["table"])):
       bucket = al.get_element(my_map["table"], i)
       for j in range(al.size(bucket)):
           entry = al.get_element(bucket, j)
           al.add_last(keys, me.get_key(entry))
   return keys


def value_set(my_map):
   values= al.new_list()
  
   for i in range(al.size(my_map["table"])):
       bucket = al.get_element(my_map["table"], i)
       for j in range(al.size(bucket)):
           entry = al.get_element(bucket, j)
           al.add_last(values, me.get_value(entry))
   return values