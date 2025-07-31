import bpy

def draw_modeling_tools(layout, context):
    scene = context.scene
    
    #Get custom properties
    props = scene.gm_props
    
    #Pivot tools
    pivot_box = layout.box()
    pivot_box.label(text="Pivot Tools")
    pivot_box.separator(factor=1, type="LINE")
    pivot_box.operator("object.quick_pivot_to_selection", icon="DOT")
    
    #Lattice tools
    lattice_box = layout.box()
    lattice_box.label(text="Lattice Tools")
    lattice_box.separator(factor=1, type="LINE")
    lattice_box.operator("object.quick_lattice_base", icon ="MESH_CUBE")
    #Lattice selector
    row = lattice_box.row()
    row.prop(props, "lattice_divisions", text="Lattice Points")
    
    
    
    """
    modifiers_box = layout.box()
    modifiers_box.label(text="Apply All modifiers from Selection")
    """