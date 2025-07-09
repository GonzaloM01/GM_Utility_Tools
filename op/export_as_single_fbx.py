import bpy
import os

class single_file_exporter(bpy.types.Operator):
    bl_idname = "object.export_as_individual_files"
    bl_label = "Export selected Meshes as Single Files"
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
        settings = scene.export_settings 
        
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
        #EXPORT THE SELECTED
        ######################################
        #Deselect everything
        bpy.ops.object.select_all(action="DESELECT")
        
        ####################FBX EXPORTER####################
        if settings.export_formats_selection == 'FBX':
            for obj in objects_to_export:
                obj.select_set(True)
                
                #Prepare the name
                file_name = f"{obj.name}.fbx"
                #Prepare full export path
                full_export_path = os.path.join(export_path, file_name)
                
                #fbx export
                bpy.ops.export_scene.fbx(
                    #Properties
                    filepath=full_export_path,
                    global_scale=settings.export_scale/100,
                    apply_unit_scale=settings.apply_unit_scale,
                    use_space_transform=settings.use_space_transform,
                    apply_scale_options=settings.apply_scale_option,
                    bake_space_transform=settings.bake_space_transform,
                    mesh_smooth_type=settings.mesh_smooth_type,
                    colors_type=settings.vertex_color,
                    use_triangles=settings.use_triangles,
                    axis_forward=settings.fbx_forward_axis,
                    axis_up=settings.fbx_up_axis,
                    use_mesh_modifiers=settings.apply_modifiers,
                    
                    #NonProperties
                    check_existing=False,
                    use_selection=True,
                    prioritize_active_color=True,
                    use_subsurf=False,
                    use_mesh_edges=False,
                    use_tspace=True,
                    use_custom_props=True,
                )
                
                obj.select_set(False)
        
        ################GLTF EXPORTER#######################
        if settings.export_formats_selection == 'GLTF':
            for obj in objects_to_export:
                obj.select_set(True)
                
                #Prepare name
                file_name = f"{obj.name}.gltf"
                full_export_path = os.path.join(export_path, file_name)
                
                #gltf export
                bpy.ops.export_scene.gltf(
                    #Properties
                    filepath=full_export_path,
                    check_existing=False,
                    use_selection=True,
                    export_use_gltfpack=settings.use_gltfpack_compression,
                    export_format=settings.export_format,
                    export_materials=settings.export_gltf_materials,
                    export_vertex_color=settings.export_vertex_color,
                    export_apply=settings.apply_modifiers,
                    export_yup=settings.gltf_y_up,
                    
                    #Non properties
                    export_image_format="AUTO",
                    export_jpeg_quality=100,
                    export_image_quality=100,
                    export_texcoords=True,
                    export_normals=True,
                    export_tangents=True,
                    export_unused_images=False,
                    export_unused_textures=False,
                    export_attributes=True,
                    use_mesh_edges=False,
                    use_mesh_vertices=False,
                    export_extras=True,
                )
                
                
                obj.select_set(False)
        
        
        
        
        ################OBJ EXPORTER#####################
        if settings.export_formats_selection == 'OBJ':
            for obj in objects_to_export:
                obj.select_set(True)
                
                #Prepare name
                file_name = f"{obj.name}.obj"
                full_export_path = os.path.join(export_path, file_name)
                
                #obj export
                bpy.ops.wm.obj_export(
                    #Properties
                    filepath=full_export_path,
                    check_existing=False,
                    export_selected_objects=True,
                    global_scale=settings.export_scale/100,
                    forward_axis=settings.obj_forward_axis,
                    up_axis=settings.obj_up_axis,
                    apply_modifiers=settings.apply_modifiers,
                    export_colors=settings.obj_export_vc,
                    export_materials=settings.export_obj_materials,
                    export_triangulated_mesh=settings.use_triangles,
                    
                    
                    
                    #Non properties
                    export_uv=True,
                    export_normals=True,
                    export_object_groups=False,
                    export_material_groups=False,
                    export_vertex_groups=False,
                    
                
                )
                
                
                obj.select_set(False)
        
        
        
        
        #Restore selection, once all is exported
        for obj in selected_objects:
            obj.select_set(True)
            
        #Finished exporting
        self.report({"INFO"}, f"{settings.export_formats_selection.upper()} Files exported to {export_path}")
        return {"FINISHED"}