import bpy
import bmesh
from mathutils import Matrix, Vector


#=========================QUICK LATTICE BASE===========================
class quick_lattice_base(bpy.types.Operator):
    bl_idname = "object.quick_lattice_base"
    bl_label = "Quick Lattice"
    bl_description = "Quickly create a lattice that covers the selection. Works in edit or object mode"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props=context.scene.gm_props
        
        ###########################
        # OBJECT MODE
        ###########################
        if bpy.context.mode == "OBJECT":
            selection = bpy.context.active_object
            check_active = bpy.context.selected_objects
            
            #If there isn't selected object
            if not check_active:
                self.report({"WARNING"}, "There isn't any selected mesh")
                return {"CANCELLED"}
            
            #If there isn't active objects, error
            if not selection:
                self.report({"WARNING"}, "There isn't any selected mesh")
                return {"CANCELLED"}
            
           
           
            #Logic to create the lattice if there is a selection
            #Deselect everything
            bpy.ops.object.select_all(action="DESELECT")
                
            #Get object bbox in world coordinates
            selection_bbox = [selection.matrix_world @ Vector(corner) for corner in selection.bound_box]
                
            #Get min and max coords
            min_coords = Vector((float("inf"), float("inf"), float("inf")))
            max_coords = Vector((float("-inf"), float("-inf"), float("-inf")))
                
            for corner in selection_bbox:
                min_coords.x = min(min_coords.x, corner.x)
                min_coords.y = min(min_coords.y, corner.y)
                min_coords.z = min(min_coords.z, corner.z)
                    
                max_coords.x = max(max_coords.x, corner.x)
                max_coords.y = max(max_coords.y, corner.y)
                max_coords.z = max(max_coords.z, corner.z) 
                    
                    
            #Get bbox center and dimensions
            lattice_location = (min_coords + max_coords)/2
            lattice_dimensions = (max_coords - min_coords)
                
                
            ###########################
            # CREATE THE LATTICE
            ###########################
            #Make sure the active object is none
            context.view_layer.objects.active = None
            #Create lattice, and add it to variable
            bpy.ops.object.add(type="LATTICE", enter_editmode=False, align="WORLD", location=lattice_location)
            lattice_obj = context.active_object
            #Name the lattice
            lattice_name=selection.name + "_Lattice"
            lattice_obj.name = lattice_name
                
            #Scale the lattice to match the bbox
            lattice_obj.scale = lattice_dimensions
                
            #Config the lattice subdivisions
            lattice_subdivisions = props.lattice_divisions
                
            lattice_obj.data.points_u = lattice_subdivisions
            lattice_obj.data.points_v = lattice_subdivisions
            lattice_obj.data.points_w = lattice_subdivisions
                
            ###########################################
            #APPLY LATTICE MODIFIER TO SELECTION
            ###########################################
            context.view_layer.objects.active = selection
            selection.select_set(True)
            
            #Check if there is other lattice modifiers applied to the mesh
            #base lattice count = 0
            lattice_position = 0
            lattice_number = 0
            
            #check position from latest lattice modifier
            for i,modifier in enumerate(selection.modifiers):
                if modifier.type == "LATTICE":
                    lattice_number = i + 1
                    
            lattice_position += lattice_number
            
            mod=selection.modifiers.new(name=f"Lattice_{lattice_name}", type="LATTICE")
            mod.object = lattice_obj
            #Move to stack desired position
            bpy.ops.object.modifier_move_to_index(modifier=mod.name, index=lattice_position)

    
            #########################################
            #DESELECT OBJECT AND EDIT LATTICE
            #########################################
            selection.select_set(False)
            context.view_layer.objects.active = lattice_obj
            lattice_obj.select_set(True)
            #Enter edit mode
            bpy.ops.object.mode_set(mode="EDIT")
            
            self.report({"INFO"}, f"Lattice created and applied to {selection}")
            return {"FINISHED"}
            
                
            
        ###########################
        # EDIT MODE
        ###########################
        elif bpy.context.mode == "EDIT_MESH":
            #create bmesh
            obj = bpy.context.edit_object
            bm = bmesh.from_edit_mesh(obj.data)
            
            #check selected vertices
            selected_vertices = []
            selected_vertices_index = []
            for v in bm.verts:
                if v.select:
                    selected_vertices.append(v.co)
                    selected_vertices_index.append(v.index)
            
            #Check if you selected at least 2 vertices 
            if not selected_vertices:
                self.report({"WARNING"}, "There isn't any selected vertices")
                return {"FINISHED"}
            if len(selected_vertices) == 1:
                self.report({"WARNING"}, "Do you really need a lattice for just 1 vertex?")
                return {"FINISHED"}
            
            ################################
            # Get Bbox
            ################################
            #Get world coords
            min_coords_world = Vector((float("inf"), float("inf"), float("inf")))
            max_coords_world = Vector((float("-inf"), float("-inf"), float("-inf")))
            
            for v_co_local in selected_vertices:
                #Transform into world coordinates
                v_co_world = obj.matrix_world @ v_co_local
                
                min_coords_world.x = min(min_coords_world.x, v_co_world.x)
                min_coords_world.y = min(min_coords_world.y, v_co_world.y)
                min_coords_world.z = min(min_coords_world.z, v_co_world.z)
                
                max_coords_world.x = max(max_coords_world.x, v_co_world.x)
                max_coords_world.y = max(max_coords_world.y, v_co_world.y)
                max_coords_world.z = max(max_coords_world.z, v_co_world.z)
                
            #Get bbox center and dimensions
            lattice_location = (min_coords_world + max_coords_world) / 2
            lattice_dimensions = max_coords_world - min_coords_world
            
            #free bmesh from memory
            bm.free()
            
            ##################################
            #CREATE THE LATTICE
            ##################################
            bpy.ops.object.editmode_toggle()
            
            #Make sure the active object is none
            context.view_layer.objects.active = None
            
            #Create lattice, and add it to variable
            bpy.ops.object.add(type="LATTICE", enter_editmode=False, align="WORLD", location=lattice_location)
            lattice_obj = context.active_object
            #Name the lattice
            lattice_name=obj.name + "_Lattice"
            lattice_obj.name = lattice_name
            
            #Scale the lattice to match the bbox
            lattice_obj.scale = lattice_dimensions
            
            #Config the lattice subdivisions
            lattice_subdivisions = props.lattice_divisions
                
            lattice_obj.data.points_u = lattice_subdivisions
            lattice_obj.data.points_v = lattice_subdivisions
            lattice_obj.data.points_w = lattice_subdivisions
            
            ###########################################
            #APPLY LATTICE MODIFIER TO SELECTION
            ###########################################
            context.view_layer.objects.active = obj
            obj.select_set(True)
            
            #Check if there is other lattice modifiers applied to the mesh
            #base lattice count = 0
            lattice_position = 0
            lattice_number = 0
            
            #check position from latest lattice modifier
            for i,modifier in enumerate(obj.modifiers):
                if modifier.type == "LATTICE":
                    lattice_number = i + 1
            
            lattice_position += lattice_number
            
            mod=obj.modifiers.new(name=f"Lattice_{lattice_name}", type="LATTICE")
            mod.object = lattice_obj
            #Move to stack desired position
            bpy.ops.object.modifier_move_to_index(modifier=mod.name, index=lattice_position)
            
            #Create vertex group
            vertex_group = obj.vertex_groups.new(name=lattice_name)
            vertex_group.add(selected_vertices_index, 1.0, "REPLACE")
            #Assign vertex group to lattice
            mod.vertex_group = vertex_group.name
            
            
            
            #########################################
            #DESELECT OBJECT AND EDIT LATTICE
            #########################################
            obj.select_set(False)
            context.view_layer.objects.active = lattice_obj
            lattice_obj.select_set(True)
            #Enter edit mode
            bpy.ops.object.mode_set(mode="EDIT")
            
            self.report({"INFO"}, f"Lattice created and applied to selected verts")
            return {"FINISHED"}
            
            
        #####################################
        #NOT IN EDIT MODE
        #####################################   
        #Not in edit or object mode
        else:
            self.report({"WARNING"}, "This Operator only works within EDIT or OBJECT mode")
            return {"CANCELLED"}
        
               
        

############################################################################
#=========================EXTRA QUICK LATTICE===========================
############################################################################

#Planned feature, still WIP

class fast_quick_lattice(bpy.types.Operator):
    bl_idname = "object.fast_quick_lattice"
    bl_label = "EXTRA Quick Lattice"
    bl_description = "Quickly create a lattice that covers the selection. Works in edit or object mode, and applies automatically when edit stops. Better for quick iterations and changes,offering a faster, but destructive workflow"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        print("test")
        
        props=context.scene.gm_props
        
        
        
        
