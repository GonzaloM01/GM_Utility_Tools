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


#Get selected meshes for renamer tools
def get_options_for_renamer(filter_non_meshes, search_all):
    
    final_selection = []
    
    #Get all selected objects, or all scene objects, depending on user input
    if search_all is True:
        brute_selection = bpy.context.scene.objects
        
    else:
        brute_selection = bpy.context.selected_objects
        
    #If needed, clean the non meshes
    for obj in brute_selection:
        if filter_non_meshes is True:
            if obj.type != "MESH":
                continue
            
        final_selection.append(obj)
    
    return final_selection
    
    
    
    
