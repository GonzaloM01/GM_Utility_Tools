import bpy

from ..utils.functions import get_options_for_renamer

##############################################################################
#=============================MESH RENAMER================================
##############################################################################
class mesh_renamer(bpy.types.Operator):
    bl_idname = "object.mesh_renamer"
    bl_label = "Rename Selected"
    bl_description = "Rename the meshes into the input written by the user"
    bl_options = {"REGISTER"}
    
    def execute(self,context):
        scene = context.scene
        props = scene.gm_props
        
        #Get properties to filter selection
        filter_non_meshes = props.filter_non_meshes
        search_all = props.rename_affect_all
        
        
        #Store the selected object(if there is one)
        active_object = context.active_object
        
        #Use defined function to get the objects that will be affected
        selected_objects = get_options_for_renamer(filter_non_meshes, search_all)
        if not selected_objects:    
            self.report({"WARNING"}, "Couldn't get a valid selection")
            return {"FINISHED", "UNDO"}
        
        
        #Get the first input, that will be used as a base for rename
        if active_object and active_object in selected_objects:
            first_input = active_object
            selected_objects.remove(active_object)
        else:
            first_input = selected_objects.pop(0)
           
        
        #=============================CHECK IF IT'S AN INT OR STRING====================
        
        user_input = props.selected_meshes_general_rename
        final_input = None
        
        
        #Check if the input is an integer
        try:
            converted_input = int(user_input)
            final_input = converted_input
        except ValueError:
            final_input = user_input.strip()
            
            #Check that the input isn't blank
            if len(final_input) == 0:
                self.report({"WARNING"}, "The 'Rename selected' box is blank. Input a valid name")
                return {"FINISHED"}
            
            
        
        #======================RENAME MESHES===================================
        
        rename_index = 1
        
        #Loop if the input was an int
        if isinstance(final_input, int):
            #Rename the first input
            first_input.name = str(final_input)
            
            for obj in selected_objects:
                int_input = final_input + rename_index
                obj.name = str(int_input)
                rename_index += 1
                
                
        #Loop if the input was a string
        if isinstance(final_input, str):
            #Rename the first input
            first_input.name = final_input
            
            for obj in selected_objects:
                string_name = f"{final_input}.{rename_index}"
                obj.name = string_name
                rename_index += 1
                
        self.report({"INFO"}, "All meshes renamed")
        return {"FINISHED"}
                
        
            


##############################################################################
#=============================ADD PREFIX================================   
############################################################################## 
class mesh_add_prefix(bpy.types.Operator):
    bl_idname = "object.mesh_add_prefix"
    bl_label = "Add Prefix to Selected"
    bl_description = "Adds a prefix to the selected meshes"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self,context):
        scene = context.scene
        props = scene.gm_props
        
        #Get properties to filter selection
        filter_non_meshes = props.filter_non_meshes
        search_all = props.rename_affect_all
        
        
        #Use defined function to get the objects that will be affected
        selected_objects = get_options_for_renamer(filter_non_meshes, search_all)
        if not selected_objects:    
            self.report({"WARNING"}, "Couldn't get a valid selection")
            return {"FINISHED"}
        
        #========================LOOP AND ADD PREFIX=========================
        user_prefix_input = props.selected_meshes_prefix.strip()
        
        if len(user_prefix_input) == 0:
            self.report({"WARNING"}, "The 'Add Prefix to selected' box is blank. Input a valid name")
            return {"FINISHED"}
        
        for obj in selected_objects:
            file_name = f"{user_prefix_input}{obj.name}"
            obj.name = file_name
            
        self.report({"INFO"}, "All Prefixes Added")
        return {"FINISHED"}
    


##############################################################################
#=============================ADD SUFFIX================================    
##############################################################################
class mesh_add_suffix(bpy.types.Operator):
    bl_idname = "object.mesh_add_suffix"
    bl_label = "Add Suffix to Selected"
    bl_description = "Adds a suffix to the selected meshes"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self,context):
        scene = context.scene
        props = scene.gm_props
        
        #Get properties to filter selection
        filter_non_meshes = props.filter_non_meshes
        search_all = props.rename_affect_all
        
        #Use defined function to get the objects that will be affected
        selected_objects = get_options_for_renamer(filter_non_meshes, search_all)
        if not selected_objects:    
            self.report({"WARNING"}, "Couldn't get a valid selection")
            return {"FINISHED"}
        
        
        #========================LOOP AND ADD SUFFIX=========================
        user_suffix_input = props.selected_meshes_suffix.strip()
        
        if len(user_suffix_input) == 0:
            self.report({"WARNING"}, "The 'Add Suffix to selected' box is blank. Input a valid name")
            return {"FINISHED"}
        
        for obj in selected_objects:
            file_name = f"{obj.name}{user_suffix_input}"
            obj.name = file_name
            
        self.report({"INFO"}, "All Suffixes Added")
        return {"FINISHED"}



##############################################################################
#=============================STRING REPLACER================================ 
##############################################################################   
class selected_mesh_name_replace(bpy.types.Operator):
    bl_idname = "object.selected_mesh_name_replace"
    bl_label = "Replace Selected"
    bl_description = "Takes two inputs written by the user. This tool will search for the first text between the selected objects, and will replace it with the second text input(if the second text input is left blank, then it will delete the first text when found"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self,context):
        scene = context.scene
        props = scene.gm_props
        
        #Get properties to filter selection
        filter_non_meshes = props.filter_non_meshes
        search_all = props.rename_affect_all
        
        #Use defined function to get the objects that will be affected
        selected_objects = get_options_for_renamer(filter_non_meshes, search_all)
        if not selected_objects:    
            self.report({"WARNING"}, "Couldn't get a valid selection")
            return {"FINISHED"}
        
        #========================SEARCH FOR INFO TO REPLACE========================
        text_to_search = props.replaced_text_from_name.strip()
        text_replace = props.replacement_text_for_name.strip()
        
        if len(text_to_search) == 0:
            self.report({"WARNING"}, "The 'Search for' box is blank. Input a valid name")
            return {"FINISHED"}
        
        #Set count to 0 and start searching
        renamed_count = 0
        for obj in selected_objects:
            if text_to_search in obj.name:
                old_name = obj.name
                new_name = obj.name.replace(text_to_search, text_replace)
                obj.name = new_name
                renamed_count += 1
        
        #Different exit messages depending if there were changes or not
        if renamed_count == 0:
            self.report({"WARNING"}, "Couldn't find the text you searched for.")
            return {"FINISHED"}
        else:
            self.report({"INFO"}, f"Input text found and replaced in {renamed_count} different objects")
            return {"FINISHED"}
            
        
        
        
#####################################################################################################################        
#=============================MATCH MESH DATA BLOCK AND OBJ NAMES================================         
#####################################################################################################################
class match_mesh_data_and_obj_names(bpy.types.Operator):
    bl_idname = "object.match_mesh_data_and_obj_names"
    bl_label = "Match Mesh Data to Obj Names"
    bl_description = "Checks the selection, and changes the mesh data block name to match the object name. WILL IGNORE INSTANCIATED MESHES"
    bl_options = {"REGISTER", "UNDO"}
    
    
    def execute(self,context):
        scene = context.scene
        props = scene.gm_props
        
        #Get properties to filter selection
        filter_non_meshes = props.filter_non_meshes
        search_all = props.rename_affect_all
        
        #Use defined function to get the objects that will be affected. Always filter non meshes
        selected_objects = get_options_for_renamer(True, search_all)
        if not selected_objects:    
            self.report({"WARNING"}, "Couldn't get a valid selection")
            return {"FINISHED"}
        
        
        #========================DESELECT INSTANCED OBJECTS========================
        #Check for objects that share the same data block
        
        final_selection = []
        
        for obj in selected_objects:
            if obj.data.users == 1:
                final_selection.append(obj)
                
        if not final_selection:    
            self.report({"WARNING"}, "Couldn't get a valid selection(All selected meshes were instanced)")
            return {"FINISHED"}
        
        #========================MATCH MESH DATA AND OBJ NAMES========================
        
        for obj in final_selection:
            obj.data.name = obj.name
            
        self.report({"INFO"}, "Now Data block mesh name are matching their object names")
        return {"FINISHED"}


class reset_rename_text_boxes(bpy.types.Operator):
    bl_idname = "object.reset_rename_text_boxes"
    bl_label = "Reset Text"
    bl_description = "Clear all text boxes inside the rename tools"
    bl_options = {"REGISTER"}
    
    
    def execute(self, context):
        scene = context.scene
        props = scene.gm_props
        
        
        #Get all properties and reset
        props.selected_meshes_general_rename = ""
        props.selected_meshes_prefix = ""
        props.selected_meshes_suffix = ""
        props.replaced_text_from_name = ""
        props.replacement_text_for_name = ""
        
        return {"FINISHED"}