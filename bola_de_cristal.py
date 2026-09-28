"""
Bola de cristal en Blender.

Uso:
  - Desde Blender: abre la pestaña "Scripting", carga este archivo y pulsa "Run Script".
  - Desde terminal:  blender --background --python bola_de_cristal.py
  - Con el módulo bpy de pip:  python bola_de_cristal.py

Genera la escena (bola de cristal sobre un pedestal, suelo, luces y cámara),
la guarda en bola_de_cristal.blend y renderiza bola_de_cristal.png con Cycles.
"""

import math
import os

import bpy

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLES = 128
RES = (1280, 960)


def limpiar_escena():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def nodo(nodes, tipo, loc):
    n = nodes.new(tipo)
    n.location = loc
    return n


def material_cristal():
    mat = bpy.data.materials.new("Cristal")
    mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    bsdf = nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.95, 0.97, 1.0, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.0
    bsdf.inputs["IOR"].default_value = 1.5
    bsdf.inputs["Transmission Weight"].default_value = 1.0
    return mat


def material_niebla():
    """Volumen interior con remolinos para darle un toque 'mágico'."""
    mat = bpy.data.materials.new("NieblaMagica")
    mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    nodes.remove(nodes["Principled BSDF"])
    out = nodes["Material Output"]

    coord = nodo(nodes, "ShaderNodeTexCoord", (-1000, 0))
    twist = nodo(nodes, "ShaderNodeTexNoise", (-800, 0))
    twist.inputs["Scale"].default_value = 1.5
    twist.inputs["Detail"].default_value = 4.0
    mix_vec = nodo(nodes, "ShaderNodeMix", (-600, 0))
    mix_vec.data_type = "VECTOR"
    mix_vec.inputs["Factor"].default_value = 0.6

    noise = nodo(nodes, "ShaderNodeTexNoise", (-400, 0))
    noise.inputs["Scale"].default_value = 3.0
    noise.inputs["Detail"].default_value = 8.0
    noise.inputs["Distortion"].default_value = 1.5

    ramp = nodo(nodes, "ShaderNodeValToRGB", (-200, 100))
    ramp.color_ramp.elements[0].position = 0.5
    ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    ramp.color_ramp.elements[1].position = 0.75
    ramp.color_ramp.elements[1].color = (1, 1, 1, 1)

    color = nodo(nodes, "ShaderNodeValToRGB", (-200, -200))
    color.color_ramp.elements[0].color = (0.25, 0.05, 0.9, 1)
    color.color_ramp.elements[1].color = (0.1, 0.8, 1.0, 1)

    dens = nodo(nodes, "ShaderNodeMath", (0, 150))
    dens.operation = "MULTIPLY"
    dens.inputs[1].default_value = 6.0

    vol = nodo(nodes, "ShaderNodeVolumePrincipled", (200, 0))
    vol.inputs["Emission Strength"].default_value = 3.0

    links.new(coord.outputs["Object"], twist.inputs["Vector"])
    links.new(coord.outputs["Object"], mix_vec.inputs["A"])
    links.new(twist.outputs["Color"], mix_vec.inputs["B"])
    links.new(mix_vec.outputs["Result"], noise.inputs["Vector"])
    links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    links.new(noise.outputs["Fac"], color.inputs["Fac"])
    links.new(ramp.outputs["Color"], dens.inputs[0])
    links.new(dens.outputs["Value"], vol.inputs["Density"])
    links.new(color.outputs["Color"], vol.inputs["Color"])
    links.new(color.outputs["Color"], vol.inputs["Emission Color"])
    links.new(ramp.outputs["Color"], vol.inputs["Emission Strength"])
    links.new(vol.outputs["Volume"], out.inputs["Volume"])
    return mat


def material_metal(nombre, color, rugosidad):
    mat = bpy.data.materials.new(nombre)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = 1.0
    bsdf.inputs["Roughness"].default_value = rugosidad
    return mat


def material_suelo():
    mat = bpy.data.materials.new("Suelo")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.02, 0.02, 0.025, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.25
    return mat


def suavizar(obj):
    for p in obj.data.polygons:
        p.use_smooth = True


def crear_objetos():
    # Bola de cristal
    bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=48, radius=1.0, location=(0, 0, 1.35))
    bola = bpy.context.object
    bola.name = "BolaDeCristal"
    suavizar(bola)
    bola.data.materials.append(material_cristal())

    # Niebla interior (ligeramente más pequeña que el cristal)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=0.94, location=(0, 0, 1.35))
    niebla = bpy.context.object
    niebla.name = "Niebla"
    suavizar(niebla)
    niebla.data.materials.append(material_niebla())

    oro = material_metal("OroViejo", (0.8, 0.55, 0.22), 0.3)
    bronce = material_metal("BronceOscuro", (0.25, 0.14, 0.08), 0.4)

    # Pedestal: aro de sujeción + cuello + base
    bpy.ops.mesh.primitive_torus_add(major_radius=0.62, minor_radius=0.07, location=(0, 0, 0.55),
                                     major_segments=96, minor_segments=24)
    aro = bpy.context.object
    aro.name = "Aro"
    suavizar(aro)
    aro.data.materials.append(oro)

    bpy.ops.mesh.primitive_cone_add(vertices=96, radius1=0.35, radius2=0.6, depth=0.35, location=(0, 0, 0.35))
    cuello = bpy.context.object
    cuello.name = "Cuello"
    suavizar(cuello)
    cuello.data.materials.append(bronce)

    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=0.85, depth=0.18, location=(0, 0, 0.09))
    base = bpy.context.object
    base.name = "Base"
    bevel = base.modifiers.new("Bisel", "BEVEL")
    bevel.width = 0.04
    bevel.segments = 4
    suavizar(base)
    base.data.materials.append(bronce)

    bpy.ops.mesh.primitive_torus_add(major_radius=0.85, minor_radius=0.04, location=(0, 0, 0.18),
                                     major_segments=96, minor_segments=16)
    filete = bpy.context.object
    filete.name = "FileteBase"
    suavizar(filete)
    filete.data.materials.append(oro)

    # Suelo
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
    suelo = bpy.context.object
    suelo.name = "Suelo"
    suelo.data.materials.append(material_suelo())

    return bola


def crear_luces_y_camara(objetivo):
    def area(nombre, loc, energia, color, tam):
        bpy.ops.object.light_add(type="AREA", location=loc)
        luz = bpy.context.object
        luz.name = nombre
        luz.data.energy = energia
        luz.data.color = color
        luz.data.size = tam
        c = luz.constraints.new("TRACK_TO")
        c.target = objetivo
        return luz

    area("LuzPrincipal", (4, -3, 5), 800, (1.0, 0.92, 0.8), 3)
    area("LuzRelleno", (-5, -2, 2.5), 200, (0.6, 0.7, 1.0), 4)
    area("LuzContra", (0, 5, 4), 600, (0.8, 0.5, 1.0), 2)

    bpy.ops.object.camera_add(location=(0, -6.5, 2.4))
    cam = bpy.context.object
    cam.name = "Camara"
    cam.data.lens = 55
    c = cam.constraints.new("TRACK_TO")
    c.target = objetivo
    bpy.context.scene.camera = cam


def configurar_mundo_y_render():
    scene = bpy.context.scene
    world = bpy.data.worlds.new("Mundo")
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (0.01, 0.008, 0.02, 1.0)
    bg.inputs["Strength"].default_value = 1.0
    scene.world = world

    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = SAMPLES
    scene.cycles.use_denoising = True
    scene.cycles.max_bounces = 16
    scene.cycles.transmission_bounces = 16
    scene.cycles.volume_bounces = 2
    scene.cycles.caustics_refractive = True
    scene.render.resolution_x, scene.render.resolution_y = RES
    scene.render.resolution_percentage = 100
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.render.filepath = os.path.join(OUT_DIR, "bola_de_cristal.png")


def main():
    limpiar_escena()
    bola = crear_objetos()
    crear_luces_y_camara(bola)
    configurar_mundo_y_render()
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT_DIR, "bola_de_cristal.blend"))
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    main()
