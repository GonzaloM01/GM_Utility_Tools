import bpy
import random
import mathutils

#Import create_random_vector function
from ..utils.functions import create_random_color

class quick_random_vertex_color(bpy.types.Operator):
    bl_idname = "object.quick_random_vertex_color"
    bl_label = "Random Vertex Color"
    bl_description = "Adds a random vertex color to every selected mesh"
    bl_options = {"REGISTER"}
    
    
    def execute(self, context):
        
        #######################
        #GET SELECTED MESHES
        #######################
        selected_objects = bpy.context.selected_objects
        #Filter everything that isn't a mesh
        selected_meshes = [obj for obj in selected_objects if obj.type == "MESH"]
        
        if bpy.context.mode != "OBJECT":
            self.report({"WARNING"}, "You need to be in object mode first")
            return {"FINISHED"}
        
        if not selected_meshes:    
            self.report({"WARNING"}, "You don't have any mesh selected")
            return {"FINISHED"}
        
        ##################################
        #SET RANDOM VERTEX COLORS
        ##################################
        for obj in selected_meshes:
            #Generate a random value for each color channel
            #vertex_color=create_random_color()
            vertex_color=create_random_color()
            
            mesh = obj.data
            color_attribute_name = "Attribute"
            
            #check if there is a previous color attribute layer
            color_attribute = mesh.color_attributes.get(color_attribute_name)
                
            if color_attribute:
                pass #If already exists, use it
            else:
                color_attribute = mesh.color_attributes.new(name=color_attribute_name, type='BYTE_COLOR', domain='CORNER')
            
            #Assign new color
            for i in range(len(color_attribute.data)):
                color_attribute.data[i].color = vertex_color
                
        
        self.report({"INFO"}, "Added Vertex Paint to all selected meshes")
        return {"FINISHED"}