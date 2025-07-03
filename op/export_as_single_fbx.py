import bpy
import os

class single_file_exporter(bpy.types.Operator):
    bl_idname = "object.export_as_individual_files"
    bl_label = "Export selected as Single Files"
    bl_description = "Export the selected meshes as their own individual .fbx file"
    bl_options = {"REGISTER"}

    #Deactivate operator if output folder not found
    @classmethod
    def poll(cls, context):
        #Get properties
        props=context.scene.gm_props
        return bool(props.export_folder_path)


    ######################################
    #EXPORTER LOGIC
    ######################################
    
    def execute(self, context):
        scene = context.scene
        props = scene.gm_props
        
        export_path = props.export_folder_path
        
        ######################
        #GET SELECTION
        ######################
        selected_objects = bpy.context.selected_objects
        #Filter everything that isn't a mesh
        selected_meshes = [obj for obj in selected_objects if obj.type == "MESH"]
        
        if not selected_meshes:    
            self.report({"WARNING"}, "You don't have any mesh selected")
            return {"FINISHED"}
        
        #=====================Emparented objects count as 1 mesh=====================     
        objects_to_export = []
        
        for obj in selected_meshes:
            objects_to_export.append(obj)
        
        ######################################
        #EXPORT THE FBX
        ######################################
        #Deselect everything
        bpy.ops.object.select_all(action="DESELECT")
        
        
        for obj in objects_to_export:
            obj.select_set(True)
            
            #Prepare the name
            file_name = f"{obj.name}.fbx"
            #Prepare full export path
            full_export_path = os.path.join(export_path, file_name)
            
            #fbx export
            bpy.ops.export_scene.fbx(
                filepath=full_export_path,
                use_selection=True,
                axis_forward="Z",
                axis_up="Y",
                global_scale=1.0,
                apply_unit_scale=True,
                bake_anim=False,
            )
            
            obj.select_set(False)
            
        #Restore selection, once all is exported
        for obj in selected_objects:
            obj.select_set(True)
            
                    

        #Finished exporting
        self.report({"INFO"}, "Files exported to...")
        return {"FINISHED"}