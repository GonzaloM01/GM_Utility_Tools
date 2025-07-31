import bpy

def draw_export_tools(layout, context):
    scene = context.scene
    
    #Get custom properties
    props = scene.gm_props
    exp_settings = scene.export_settings
    

    export_box = layout.box()
    export_box.label(text="Export selection as multiple files")
    export_box.separator(factor=1, type="LINE")
    
    #Output folder selection
    export_box.prop(props, "export_folder_path", text="Output Folder")
    
    #File format selection
    file_format_row=export_box.row(align=True)
    file_format_row.prop(exp_settings, "export_formats_selection", expand=True)
    
    #Export operator
    export_box.operator("object.export_as_individual_files", icon="DISK_DRIVE")
    #Sufix and Prefix
    prefix_suffix_row=export_box.row(align=True)
    prefix_suffix_row.prop(exp_settings, "mesh_export_name_prefix", text="")
    prefix_suffix_row.label(text="+ Mesh Name +")
    prefix_suffix_row.prop(exp_settings, "mesh_export_name_suffix", text="")
    
    #Options drop down menu
    row = export_box.row(align=True)
    
    sub_row=row.row(align=True)
    sub_row.alignment = "LEFT"
    
    sub_row.prop(exp_settings, "show_export_options",
        text="",
        icon="TRIA_DOWN" if exp_settings.show_export_options else "TRIA_RIGHT",
        emboss=False
    )
    
    sub_row.label(text="Export Options:")
    
    #Draw options only if drop down menu is open
    if exp_settings.show_export_options:
        sub_col = export_box.column(align=True)
        
        #############################
        #EXPORT SETTINGS
        #############################
        common_options_box = sub_col.box()
        
        if exp_settings.export_formats_selection == "FBX" or exp_settings.export_formats_selection == "OBJ":
            #Scale
            scale_row = common_options_box.row(align=True)
            scale_row.prop(exp_settings, "export_scale", text="Export scale %")
        
        #Move to 0,0,0 position
        reset_position_row=common_options_box.row(align=True)
        reset_position_row.prop(exp_settings, "exporter_move_to_0")
        
        #Apply modifiers?
        apply_modifiers_row=common_options_box.row(align=True)
        apply_modifiers_row.prop(exp_settings, "apply_modifiers")
        
        if exp_settings.export_formats_selection == "FBX" or exp_settings.export_formats_selection == "OBJ":
            #Triangulate (added to apply modifiers row)
            apply_modifiers_row.prop(exp_settings,"use_triangles")
        
        #OBJ and FBX Axis order
        if exp_settings.export_formats_selection == "FBX": 
            #Forward and Up Axis
            fbx_axis_row=common_options_box.row(align=True)
            #Split up
            split_fbx_up_axis=fbx_axis_row.split(factor=0.2, align=True)
            split_fbx_up_axis.label(text="Up")
            split_fbx_up_axis.prop(exp_settings, "fbx_up_axis", text="")
            #Split forward
            split_fbx_forward_axis=fbx_axis_row.split(factor=0.6, align=True)
            split_fbx_forward_axis.label(text="     Forward")
            split_fbx_forward_axis.prop(exp_settings, "fbx_forward_axis", text="")
            
        if exp_settings.export_formats_selection == "OBJ":
            #Forward and Up Axis
            obj_axis_row=common_options_box.row(align=True)
            #Split up
            split_obj_up_axis=obj_axis_row.split(factor=0.2, align=True)
            split_obj_up_axis.label(text="Up")
            split_obj_up_axis.prop(exp_settings, "obj_up_axis", text="")
            #Split forward
            split_obj_forward_axis=obj_axis_row.split(factor=0.6, align=True)
            split_obj_forward_axis.label(text="     Forward")
            split_obj_forward_axis.prop(exp_settings, "obj_forward_axis", text="")


        
        #GLTF Y Option
        if exp_settings.export_formats_selection == "GLTF":
            #export Y up
            yup_gltf_row=common_options_box.row(align=True)
            yup_gltf_row.prop(exp_settings, "gltf_y_up")
        
        #FBX Only Options 
        if exp_settings.export_formats_selection == 'FBX':
            apply_unit_scale_row=common_options_box.row(align=True)
            apply_unit_scale_row.prop(exp_settings, "apply_unit_scale")
            
            #Use space transform
            use_space_transform_row=common_options_box.row(align=True)
            use_space_transform_row.prop(exp_settings, "use_space_transform")
            
            #bake space transform
            bake_space_transform_row=common_options_box.row(align=True)
            bake_space_transform_row.prop(exp_settings, "bake_space_transform")
            
            #Apply scale option
            apply_scale_option_row=common_options_box.row(align=True)
            #Split, for better reading
            split_scale_option=apply_scale_option_row.split(factor= 0.45, align=True)
            split_scale_option.label(text="Apply Scale Option")
            split_scale_option.prop(exp_settings, "apply_scale_option", text="")
            
            #Mesh smooth type
            mesh_smooth_type_row=common_options_box.row(align=True)
            #Split for better reading
            split_smooth_type=mesh_smooth_type_row.split(factor= 0.45, align=True)
            split_smooth_type.label(text="Mesh Smoothing Type")
            split_smooth_type.prop(exp_settings, "mesh_smooth_type", text="")
            
            #Vertex color export
            vertex_color_type_row=common_options_box.row(align=True)
            #Split for better reading
            split_vertex_color=vertex_color_type_row.split(factor=0.45, align=True)
            split_vertex_color.label(text="Vertex Color Export")
            split_vertex_color.prop(exp_settings, "vertex_color", text="")
        
        #GLTF Only options    
        if exp_settings.export_formats_selection == "GLTF":
            #export materials
            export_materials_row=common_options_box.row(align=True)
            split_export_materials=export_materials_row.split(factor=0.45, align=True)
            split_export_materials.label(text="Export Materials")
            split_export_materials.prop(exp_settings, "export_gltf_materials", text="")
            
            #export format
            export_format_row=common_options_box.row(align=True)
            split_export_format=export_format_row.split(factor=0.45, align=True)
            split_export_format.label(text="Export Format")
            split_export_format.prop(exp_settings, "export_format", text="")
            
            #export vertex color
            vertex_color_gltf_row=common_options_box.row(align=True)
            split_vertex_color_gltf=vertex_color_gltf_row.split(factor=0.45, align=True)
            split_vertex_color_gltf.label(text="Vertex Color Export")
            split_vertex_color_gltf.prop(exp_settings, "export_vertex_color", text="")
            
            #draco compression
            draco_compression_row=common_options_box.row(align=True)
            draco_compression_row.prop(exp_settings, "use_draco_compression")
            

        
        #OBJ Only options    
        if exp_settings.export_formats_selection == "OBJ":
            #export mtl
            mtl_export_row=common_options_box.row(align=True)
            mtl_export_row.prop(exp_settings, "export_obj_materials")
            
            #Vertex color export
            vertex_color_obj_row=common_options_box.row(align=True)
            vertex_color_obj_row.prop(exp_settings, "obj_export_vc")
            
            
            
    #####################################################
    #QUICK RENAME UI
    #####################################################
    
    rename_box = layout.box()
    rename_box.label(text="Mesh Rename tools:")
    rename_box.separator(factor=1, type="LINE")
    filter_non_meshes_row=rename_box.row(align=True)
    filter_non_meshes_row.prop(props, "filter_non_meshes", text="Filter Non Meshes")
    filter_non_meshes_row.operator("object.reset_rename_text_boxes")
    rename_box.prop(props, "rename_affect_all", text="Affect All Scene, not Only Selected")
    
    #Selection rename
    mesh_rename_row=rename_box.row(align=True)
    mesh_rename_row.label(text="Rename Selected:")
    mesh_rename_row.prop(props, "selected_meshes_general_rename", text="")
    #Show operator and separate from other tools
    mesh_rename_row_2=rename_box.row(align=True)
    mesh_rename_row_2.operator("object.mesh_renamer", icon="TEXT")
    rename_box.separator(factor=1, type="SPACE")
    
    #Prefix operator
    prefix_row=rename_box.row(align=True)
    prefix_row.label(text="Add Prefix to Selected:")
    prefix_row.prop(props, "selected_meshes_prefix", text="")
    
    prefix_row_2=rename_box.row(align=True)
    prefix_row_2.operator("object.mesh_add_prefix", icon="PROPERTIES")
    
    #Suffix operator
    suffix_row=rename_box.row(align=True)
    suffix_row.label(text="Add Suffix to Selected:")
    suffix_row.prop(props, "selected_meshes_suffix", text="")
    
    suffix_row_2=rename_box.row(align=True)
    suffix_row_2.operator("object.mesh_add_suffix", icon="PROPERTIES")
    
    rename_box.separator(factor=1, type="SPACE")
    
    #Replace text operator
    replace_text_row=rename_box.row(align=True)
    replace_text_row.label(text="Search for:")
    replace_text_row.prop(props, "replaced_text_from_name", text="")
    
    replace_text_row_2=rename_box.row(align=True)
    replace_text_row_2.label(text="And Replace With:")
    replace_text_row_2.prop(props, "replacement_text_for_name", text="")
    
    replace_text_row_3=rename_box.row(align=True)
    replace_text_row_3.operator("object.selected_mesh_name_replace", icon="VIEWZOOM")
    
    rename_box.separator(factor=1, type="SPACE")
    match_names_row=rename_box.row(align=True)
    match_names_row.operator("object.match_mesh_data_and_obj_names", icon = "OUTLINER_DATA_MESH")
    
    

    
    
    
    
    
    