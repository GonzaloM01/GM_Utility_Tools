import bpy
import random
import mathutils

#Use MATHUTILS and RANDOM to create a random vector
def create_random_color():
    r_value = random.random()
    g_value = random.random()
    b_value = random.random()
    
    random_color = mathutils.Vector((r_value, g_value, b_value,1.0))
    return random_color
    
    
