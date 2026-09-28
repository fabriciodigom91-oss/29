"""
Animación en bucle de la bola de cristal.

La cámara da una vuelta completa alrededor del pedestal mientras la niebla
interior gira y se retuerce. El último fotograma enlaza con el primero, así
que el vídeo se puede reproducir en bucle sin saltos.

Uso:
  blender --background --python animacion.py
  python animacion.py            (con el módulo bpy de pip)

Renderiza los fotogramas PNG en render_frames/ y guarda bola_de_cristal_animada.blend.
"""

import math
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bola_de_cristal as escena  # noqa: E402

FRAMES = 120
FPS = 24
SAMPLES = 32
RES = (800, 600)


def animar():
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = FRAMES
    scene.render.fps = FPS

    # La cámara orbita alrededor de un vacío en el centro de la bola.
    bpy.ops.object.empty_add(location=(0, 0, 0))
    pivote = bpy.context.object
    pivote.name = "PivoteCamara"
    cam = scene.camera
    cam.parent = pivote

    niebla = bpy.data.objects["Niebla"]

    for frame, angulo in ((1, 0.0), (FRAMES + 1, 2 * math.pi)):
        pivote.rotation_euler = (0, 0, angulo)
        pivote.keyframe_insert("rotation_euler", index=2, frame=frame)
        niebla.rotation_euler = (angulo, 0, -angulo)
        niebla.keyframe_insert("rotation_euler", frame=frame)

    # Interpolación lineal para que el bucle no frene en los extremos.
    _lineal(pivote)
    _lineal(niebla)


def _lineal(obj):
    """Pone todos los keyframes en LINEAR (compatible con Blender 4.x y 5.x)."""
    action = obj.animation_data.action
    curvas = []
    if hasattr(action, "layers"):  # acciones por capas (Blender 4.4+)
        for layer in action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    curvas.extend(bag.fcurves)
    if not curvas and hasattr(action, "fcurves"):
        curvas = list(action.fcurves)
    for fc in curvas:
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"


def main():
    escena.limpiar_escena()
    bola = escena.crear_objetos()
    escena.crear_luces_y_camara(bola)
    escena.configurar_mundo_y_render()

    scene = bpy.context.scene
    scene.cycles.samples = SAMPLES
    scene.render.resolution_x, scene.render.resolution_y = RES
    scene.cycles.volume_step_rate = 2.0
    animar()

    out = os.path.join(escena.OUT_DIR, "render_frames")
    os.makedirs(out, exist_ok=True)
    scene.render.filepath = os.path.join(out, "frame_")
    scene.render.image_settings.file_format = "PNG"
    scene.render.use_overwrite = False  # permite retomar un render interrumpido
    scene.render.use_placeholder = True

    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(escena.OUT_DIR, "bola_de_cristal_animada.blend"))
    if "--solo-prueba" in sys.argv:
        scene.frame_end = 1
    bpy.ops.render.render(animation=True)


if __name__ == "__main__":
    main()
