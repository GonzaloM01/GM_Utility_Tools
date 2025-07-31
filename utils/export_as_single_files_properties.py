import bpy
from bpy.props import EnumProperty, IntProperty, StringProperty, PointerProperty, BoolProperty, FloatProperty



#========================EXPORT OPTIONS PROPERTIES======================
class export_formats(bpy.types.PropertyGroup):
    export_formats_selection: bpy.props.EnumProperty(
        name="Export formats",
        items=[
            ("OBJ", "OBJ", "Export in OBJ format"),
            ("FBX", "FBX", "Export in FBX format"),
            ("GLTF", "GLTF", "Export in GLTF format"),
        ],
        default="FBX"
    )

    show_export_options: BoolProperty(
        name="Show Export Options",
        description="Toggle visibility of advanced export options",
        default=True
    )
###########################GENERAL OPTIONS###########################
    export_scale: FloatProperty(
        name="Export Scale %",
        description= "Select the export scale for all the meshes (uses %, so 100 will be the default scale)",
        default = 100,
        min = 0.01,
        max = 100000
        )
        
    apply_modifiers: BoolProperty(
        name="Apply Modifiers",
        description="Apply Modifiers, Apply modifiers to mesh objects",
        default=True
    )
    
    use_triangles: BoolProperty(
        name="Triangulate Meshes",
        description="Triangulate Faces, Convert all faces to triangles",
        default=False
    )
    
    exporter_move_to_0: BoolProperty(
        name="Move to 0,0,0 position",
        description="Move every mesh to the 0,0,0 position, based on it's pivot point(Only while exporting, then it will recover the previous mesh position",
        default=True
    )
    
    mesh_export_name_suffix: StringProperty(
        name="Suffix",
        description="Write a Suffix to add it after all the meshes name(not mandatory, leave blank for not adding anything",
        subtype="NONE",
        default=""
    )
    
    mesh_export_name_prefix: StringProperty(
        name="Prefix",
        description="Write a Prefix to add it before all meshes names(not mandatory, leave blank for not adding anything",
        subtype="NONE",
        default=""
    
    )
    

##########################FBX ONLY OPTIONS##########################
    apply_unit_scale: BoolProperty(
        name="Apply Unit Scale",
        description="When active, FBX format will take into account Blender's scene units",
        default=True
    )
    
    use_space_transform: BoolProperty(
        name="Use Space Transform",
        description="Use Space Transform, Apply global space transform to the object rotations. When disabled only the axis space is written to the file and all object transforms are left as-is",
        default=True
    )
    
    bake_space_transform: BoolProperty(
        name="Bake Space Transform",
        description="Apply Transform, Bake space transform into object data, avoids getting unwanted rotations to objects when target space is not aligned with Blender’s space (WARNING! experimental option, use at own risk, known to be broken with armatures/animations)",
        default=False
    )
    
    apply_scale_option: EnumProperty(
        name="Apply Scale Option",
        items=[
            ("FBX_SCALE_NONE", "All local", "Apply custom scaling and units scaling to each object transformation, FBX scale remains at 1.0."),
            ("FBX_SCALE_UNITS", "FBX Units Scale", "Apply custom scaling to each object transformation, and units scaling to FBX scale."),
            ("FBX_SCALE_CUSTOM", "FBX Custom Scale", "Apply custom scaling to FBX scale, and units scaling to each object transformation."),
            ("FBX_SCALE_ALL", "FBX All", "Apply custom scaling and units scaling to FBX scale."),
        ],
        default="FBX_SCALE_NONE"
    )
    
    mesh_smooth_type: EnumProperty(
        name="Mesh Smoothing Type",
        items=[
            ("OFF", "Normals Only", "Export only normals instead of writing edge or face smoothing data."),
            ("FACE", "Face", "Write face smoothing."),
            ("EDGE", "Edge", "Write edge smoothing."),
        ],
        default="OFF"
    )
    
    vertex_color: EnumProperty(
        name="Export Vertex Color",
        items=[
            ("NONE", "Don't Export", "Do not export color attributes"),
            ("SRGB", "sRGB", "Export colors in sRGB color space"),
            ("LINEAR", "Linear", "Export colors in linear color space"),
        ],
        default="LINEAR"
    )
    
    fbx_up_axis: EnumProperty(
        name="Up axis",
        description="Select Up Axis",
        items=[
            ("Z","Z","Z Up"),
            ("-Z","-Z","-Z Up"),
            ("X","X","X Up"),
            ("-X","-X","-X Up"),
            ("Y","Y","Y Up"),
            ("-Y","-Y","-Y Up"),
        ],
        default="-Z"
    )
    fbx_forward_axis: EnumProperty(
        name="Up axis",
        description="Select Forward Axis",
        items=[
            ("Z","Z","Z Forward"),
            ("-Z","-Z","-Z Forward"),
            ("X","X","X Forward"),
            ("-X","-X","-X Forward"),
            ("Y","Y","Y Forward"),
            ("-Y","-Y","-Y Forward"),
        ],
        default="Y"
    )


##########################GLTF ONLY OPTIONS##########################
    use_draco_compression: BoolProperty(
        name="Use Draco Compression",
        description="Use draco to simplify the mesh",
        default=False
    )
    
    export_format: EnumProperty(
        name="Export Format",
        items=[
            ("GLB","Binary file (.glb)","Creates a .glb file per mesh, that contains everything (geometry, materials...)"),
            ("GLTF_SEPARATE","Gltf Separate","Creates a .gltf file per mesh, with separate texture files"),
        ],
        default="GLTF_SEPARATE"
    )
    
    export_gltf_materials: EnumProperty(
        name="Export Materials",
        items=[
            ("EXPORT","Export","Export all materials used by included objects."),
            ("PLACEHOLDER","Placeholder","Do not export materials, but write multiple primitive groups per mesh, keeping material slot information."),
            ("NONE","Don't export","Do not export materials, and combine mesh primitive groups, losing material slot information."),
        ],
        default="EXPORT"
    )
    
    export_vertex_color: EnumProperty(
        name="Export Vertex Color",
        items=[
            ("ACTIVE","Active","Export all vertex color, independent if it's used or not"),
            ("MATERIAL","Material","Export vertex color only where it's used by a material"),
            ("NONE","Don't Export","Don't export vertex color"),
        ],
        default="ACTIVE"
    )
    
    gltf_y_up: BoolProperty(
        name="Y Up",
        description="Export Y axis Up, following the glTF convention",
        default=True
    )


##########################OBJ ONLY OPTIONS#########################
    obj_export_vc: BoolProperty(
        name="Export Vertex Color",
        description="Export per-vertex colors",
        default=True
    )
    
    export_obj_materials: BoolProperty(
        name= "Export MTL library",
        description="Export Materials, Export MTL library. There must be a Principled-BSDF node for image textures to be exported to the MTL file",
        default=False
    )
    
    obj_up_axis: EnumProperty(
        name="Up axis",
        description="Select Up Axis",
        items=[
            ("Z","Z","Z Up"),
            ("NEGATIVE_Z","-Z","-Z Up"),
            ("X","X","X Up"),
            ("NEGATIVE_X","-X","-X Up"),
            ("Y","Y","Y Up"),
            ("NEGATIVE_Y","-Y","-Y Up"),
        ],
        default="NEGATIVE_Z"
    )
    obj_forward_axis: EnumProperty(
        name="Up axis",
        description="Select Forward Axis",
        items=[
            ("Z","Z","Z Forward"),
            ("NEGATIVE_Z","-Z","-Z Forward"),
            ("X","X","X Forward"),
            ("NEGATIVE_X","-X","-X Forward"),
            ("Y","Y","Y Forward"),
            ("NEGATIVE_Y","-Y","-Y Forward"),
        ],
        default="Y"
    )