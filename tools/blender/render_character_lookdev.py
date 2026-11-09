"""Procedural 3D look-development and animated shot scene for EnglishTale Episode 001.

Run:
  blender -b -t 2 --python tools/blender/render_character_lookdev.py -- --output build/episode-001-3d-lookdev.png

All geometry and materials are original and generated procedurally. This is a
look-development still, not a finished episode shot or final character model.
"""
import argparse
import math
import os
import sys
from pathlib import Path

import bpy
from mathutils import Vector


def args_after_separator():
    raw = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="build/episode-001-3d-lookdev.png")
    parser.add_argument("--animation", action="store_true", help="Render a short procedural 3D motion study as MP4")
    parser.add_argument("--shot-library", action="store_true", help="Render 18 camera angles for the hybrid episode pipeline")
    parser.add_argument("--animated-shot-library", action="store_true", help="Render 18 short animated 3D MP4 clips")
    parser.add_argument("--shots-dir", default="build/3d-shots", help="Output folder for the 3D shot library")
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    parser.add_argument("--duration", type=int, default=4, help="Animation duration in seconds")
    parser.add_argument("--fps", type=int, default=24, help="Animation frame rate")
    return parser.parse_args(raw)


def material(name, color, metallic=0.0, roughness=0.48):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    return mat


def assign(obj, mat):
    obj.data.materials.append(mat)
    return obj


def uv_sphere(name, loc, scale, mat, segments=32, rings=20):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.shade_smooth()
    return assign(obj, mat)


def cube(name, loc, scale, mat, bevel=0.08):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = obj.modifiers.new("Soft rounded edges", "BEVEL")
        mod.width = bevel
        mod.segments = 3
        obj.modifiers.new("Weighted corner normals", "WEIGHTED_NORMAL")
    return assign(obj, mat)


def cylinder(name, loc, radius, depth, mat, rotation=(0, 0, 0), vertices=32):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth,
                                       location=loc, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    bevel = obj.modifiers.new("Soft edges", "BEVEL")
    bevel.width = 0.035
    bevel.segments = 3
    obj.modifiers.new("Weighted normals", "WEIGHTED_NORMAL")
    return assign(obj, mat)


def text_obj(body, loc, size, mat, align="CENTER"):
    curve = bpy.data.curves.new("Typography", "FONT")
    curve.body = body
    curve.size = size
    curve.align_x = align
    curve.extrude = 0.008
    obj = bpy.data.objects.new(body, curve)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    obj.rotation_euler = (math.radians(90), 0, 0)
    return assign(obj, mat)


def light(name, loc, energy, size, color, target=(0, 0, 2)):
    data = bpy.data.lights.new(name, "AREA")
    data.energy = energy
    data.shape = "DISK"
    data.size = size
    data.color = color
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def build_person(x, name, body_mat, pants_mat, hair_mat, skin_mat, accent_mat):
    # Canonical 19-year-old proportions: large expressive head, compact stylized body.
    uv_sphere(name + " torso", (x, 0, 1.45), (0.48, 0.34, 0.68), body_mat)
    uv_sphere(name + " neck", (x, -0.01, 2.06), (0.16, 0.15, 0.22), skin_mat)
    uv_sphere(name + " head", (x, -0.03, 2.55), (0.43, 0.38, 0.52), skin_mat)
    uv_sphere(name + " hair cap", (x, 0.0, 2.89), (0.44, 0.39, 0.25), hair_mat)
    if name == "Emma":
        # Shoulder-length hair and a soft fringe distinguish Emma from Leo.
        uv_sphere("Emma shoulder hair left", (x - 0.35, 0.015, 2.35), (0.14, 0.35, 0.57), hair_mat)
        uv_sphere("Emma shoulder hair right", (x + 0.35, 0.015, 2.35), (0.14, 0.35, 0.57), hair_mat)
        uv_sphere("Emma soft fringe", (x, -0.32, 2.83), (0.32, 0.075, 0.13), hair_mat)
    else:
        uv_sphere(name + " hair left", (x - 0.34, 0.0, 2.66), (0.13, 0.34, 0.35), hair_mat)
        uv_sphere(name + " hair right", (x + 0.34, 0.0, 2.66), (0.13, 0.34, 0.35), hair_mat)
    # Face points toward the camera (-Y); brows add expression.
    for dx in (-0.16, 0.16):
        uv_sphere(name + " eye white", (x + dx, -0.385, 2.61), (0.075, 0.035, 0.095), M["white"])
        uv_sphere(name + " iris", (x + dx, -0.418, 2.60), (0.036, 0.022, 0.052), M["iris"])
        uv_sphere(name + " pupil", (x + dx, -0.438, 2.60), (0.017, 0.012, 0.027), M["dark"])
        uv_sphere(name + " eyebrow", (x + dx, -0.414, 2.745), (0.085, 0.024, 0.023), hair_mat)
    uv_sphere(name + " nose", (x, -0.425, 2.48), (0.055, 0.05, 0.07), skin_mat)
    # Smile as a thin dark curved tube.
    curve = bpy.data.curves.new(name + " smile", "CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = 0.012
    curve.bevel_resolution = 3
    spline = curve.splines.new("BEZIER")
    spline.bezier_points.add(2)
    for point, co in zip(spline.bezier_points,
                         [(x - 0.09, -0.405, 2.39), (x, -0.43, 2.36), (x + 0.09, -0.405, 2.39)]):
        point.co = co
        point.handle_left_type = "AUTO"
        point.handle_right_type = "AUTO"
    smile = bpy.data.objects.new(name + " smile", curve)
    bpy.context.collection.objects.link(smile)
    assign(smile, M["dark"])
    # Arms, hands, legs and white trainers.
    for side in (-1, 1):
        arm = uv_sphere(name + " sleeve", (x + side * 0.53, 0, 1.52), (0.17, 0.20, 0.52), body_mat)
        arm.rotation_euler[1] = side * math.radians(-17)
        uv_sphere(name + " hand", (x + side * 0.60, -0.02, 1.04), (0.13, 0.13, 0.14), skin_mat)
        cube(name + " trouser leg", (x + side * 0.20, 0.02, 0.55), (0.24, 0.30, 0.78), pants_mat, 0.10)
        uv_sphere(name + " white shoe", (x + side * 0.20, -0.13, 0.16), (0.22, 0.34, 0.14), M["white"])
    if name == "Leo":
        cube("Leo hoodie pocket", (x, -0.335, 1.30), (0.42, 0.035, 0.20), accent_mat, 0.035)
        # Drawstrings
        for dx in (-0.07, 0.07):
            cylinder("Hoodie drawstring", (x + dx, -0.36, 1.82), 0.012, 0.25, M["white"])
    else:
        uv_sphere("Emma sweater collar", (x, -0.08, 1.98), (0.23, 0.20, 0.11), accent_mat)


def build_ollie(x):
    uv_sphere("Ollie body", (x, 0, 1.15), (0.53, 0.42, 0.72), M["owl_brown"])
    uv_sphere("Ollie head", (x, -0.02, 1.92), (0.58, 0.47, 0.55), M["owl_brown"])
    for side in (-1, 1):
        uv_sphere("Ollie ear tuft", (x + side * 0.38, 0.0, 2.31), (0.17, 0.15, 0.30), M["owl_brown"])
        uv_sphere("Ollie cream eye patch", (x + side * 0.22, -0.40, 1.99), (0.24, 0.12, 0.30), M["cream"])
        uv_sphere("Ollie eye", (x + side * 0.22, -0.51, 2.01), (0.105, 0.055, 0.13), M["white"])
        uv_sphere("Ollie pupil", (x + side * 0.22, -0.56, 2.01), (0.052, 0.03, 0.075), M["dark"])
        # Round glasses rings.
        bpy.ops.mesh.primitive_torus_add(major_radius=0.145, minor_radius=0.018,
                                         major_segments=40, minor_segments=10,
                                         location=(x + side * 0.22, -0.59, 2.01),
                                         rotation=(math.radians(90), 0, 0))
        assign(bpy.context.object, M["gold"])
    uv_sphere("Ollie beak", (x, -0.53, 1.82), (0.11, 0.12, 0.14), M["beak"])
    # Navy scarf with a small gold trim.
    cube("Ollie scarf", (x, -0.43, 1.47), (0.75, 0.10, 0.17), M["navy"], 0.06)
    cube("Ollie scarf gold stripe", (x, -0.49, 1.47), (0.75, 0.018, 0.035), M["gold"], 0.01)
    uv_sphere("Ollie belly", (x, -0.36, 1.05), (0.37, 0.10, 0.48), M["cream"])


def main():
    args = args_after_separator()
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    global M
    M = {
        "blue": material("Leo cobalt hoodie", (0.035, 0.20, 0.72), roughness=0.38),
        "pink": material("Emma rose sweater", (0.90, 0.20, 0.42), roughness=0.42),
        "jeans": material("Deep indigo denim", (0.025, 0.055, 0.15)),
        "hair": material("Warm brown hair", (0.12, 0.045, 0.02)),
        "skin": material("Warm skin", (0.72, 0.42, 0.27)),
        "owl_brown": material("Ollie chestnut feathers", (0.24, 0.095, 0.035)),
        "cream": material("Ollie cream plumage", (0.92, 0.78, 0.56)),
        "beak": material("Ollie warm orange beak", (0.95, 0.38, 0.055)),
        "navy": material("Ollie navy scarf", (0.015, 0.045, 0.15)),
        "gold": material("Warm gold trim", (0.88, 0.52, 0.10), metallic=0.55),
        "white": material("Soft white", (0.92, 0.94, 0.98)),
        "iris": material("Hazel iris", (0.18, 0.10, 0.04)),
        "dark": material("Deep dark details", (0.018, 0.012, 0.01)),
        "glass": material("Airport blue glass", (0.12, 0.34, 0.48), metallic=0.15, roughness=0.22),
        "metal": material("Brushed terminal metal", (0.25, 0.31, 0.38), metallic=0.7),
        "floor": material("Polished warm stone", (0.32, 0.38, 0.44), roughness=0.24),
        "sign": material("Deep navy signage", (0.012, 0.035, 0.12)),
        "text": material("Sign lettering", (0.95, 0.78, 0.30), metallic=0.2),
    }

    # Terminal architecture and reflective floor.
    cube("Airport floor", (0, 1.4, -0.12), (18, 15, 0.22), M["floor"], 0.04)
    cube("Rear terminal wall", (0, 4.1, 3.0), (18, 0.30, 6.2), M["glass"], 0.05)
    for x in range(-8, 9, 2):
        cube("Window mullion", (x, 3.88, 3.0), (0.07, 0.12, 6.0), M["metal"], 0.02)
    cube("Ceiling beam", (0, 2.7, 6.05), (18, 3.2, 0.18), M["metal"], 0.05)
    # Gate 12 sign.
    cube("Gate 12 sign", (0, 3.65, 4.65), (4.0, 0.22, 0.85), M["sign"], 0.12)
    text_obj("GATE 12", (0, 3.51, 4.48), 0.52, M["text"])
    text_obj("LONDON  •  BOARDING", (0, 3.50, 4.18), 0.16, M["white"])
    # Check-in counter and monitor.
    cube("Check-in counter", (-5.2, 0.8, 0.72), (3.2, 1.0, 1.35), M["sign"], 0.12)
    cube("Counter front panel", (-5.2, 0.27, 0.72), (2.65, 0.05, 0.78), M["glass"], 0.04)
    cube("Counter monitor", (-5.5, 1.15, 1.75), (0.72, 0.14, 0.52), M["metal"], 0.06)
    # Distant airplane seen through windows.
    uv_sphere("Airplane fuselage", (5.5, 3.1, 2.4), (2.2, 0.25, 0.35), M["white"])
    cube("Airplane wing", (5.3, 3.0, 2.35), (2.0, 0.22, 0.08), M["metal"], 0.03)
    uv_sphere("Airplane tail", (7.3, 3.05, 2.7), (0.18, 0.12, 0.65), M["white"])

    # Check-in and security staff use the same canonical stylized proportions.
    build_person(-5.8, "Airport Agent", M["navy"], M["jeans"], M["hair"], M["skin"], M["navy"])
    for agent_part in bpy.data.objects:
        if agent_part.name.startswith("Airport Agent"):
            agent_part.location.y += 1.55
    build_person(5.7, "Security Officer", M["navy"], M["jeans"], M["hair"], M["skin"], M["navy"])

    # Security scanner, conveyor, tray, and a small cabin suitcase.
    cube("Security scanner left pillar", (3.55, 0.65, 1.55), (0.18, 0.32, 3.0), M["metal"], 0.06)
    cube("Security scanner right pillar", (4.85, 0.65, 1.55), (0.18, 0.32, 3.0), M["metal"], 0.06)
    cube("Security scanner top beam", (4.20, 0.65, 3.02), (1.48, 0.32, 0.18), M["metal"], 0.06)
    cube("Security conveyor", (4.20, 0.55, 0.78), (2.1, 0.9, 0.28), M["sign"], 0.08)
    cube("Security tray", (3.9, -0.02, 1.02), (0.82, 0.55, 0.07), M["metal"], 0.025)
    text_obj("SECURITY", (4.2, 0.46, 2.78), 0.18, M["text"])
    cube("Leo cabin suitcase", (-3.25, 0.38, 0.55), (0.62, 0.42, 0.98), M["sign"], 0.10)
    cylinder("Suitcase handle", (-3.25, 0.38, 1.10), 0.025, 0.36, M["metal"])
    cube("Passport", (-5.05, 0.18, 1.49), (0.52, 0.06, 0.38), M["gold"], 0.025)
    text_obj("PASSPORT", (-5.05, 0.145, 1.47), 0.075, M["white"])
    cube("Boarding pass", (-4.15, 0.18, 1.49), (0.88, 0.06, 0.38), M["white"], 0.025)
    text_obj("LONDON  •  GATE 12", (-4.15, 0.145, 1.52), 0.075, M["sign"])
    text_obj("BOARDING PASS", (-4.15, 0.145, 1.40), 0.055, M["sign"])

    # Canonical characters. Their outfit palette is deliberately fixed.
    build_person(-2.3, "Leo", M["blue"], M["jeans"], M["hair"], M["skin"], M["blue"])
    build_person(0.0, "Emma", M["pink"], M["jeans"], M["hair"], M["skin"], M["pink"])
    build_ollie(2.25)

    # Soft cinematic lighting.
    light("Key softbox", (-4.5, -6.0, 8.0), 1250, 6.0, (1.0, 0.82, 0.68))
    light("Cool fill", (5.5, -3.0, 5.0), 900, 5.0, (0.62, 0.78, 1.0))
    light("Warm rim", (0, 3.0, 6.0), 1500, 4.0, (1.0, 0.72, 0.42))

    world = bpy.data.worlds.new("Airport ambient")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.12, 0.18, 0.28, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.45
    bpy.context.scene.world = world

    camera_data = bpy.data.cameras.new("Episode camera")
    camera = bpy.data.objects.new("Episode camera", camera_data)
    bpy.context.collection.objects.link(camera)
    camera.location = (0, -14.8, 4.1)
    target = Vector((0, 1.4, 2.3))
    camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Y").to_euler()
    camera_data.lens = 48
    bpy.context.scene.camera = camera

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items.keys() else "BLENDER_EEVEE"
    scene.render.resolution_x = args.width
    scene.render.resolution_y = args.height
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.view_settings.view_transform = "AgX"
    scene.render.filepath = str(output)
    scene.camera.data.dof.use_dof = True
    scene.camera.data.dof.focus_object = bpy.data.objects.get("Emma torso")
    scene.camera.data.dof.aperture_fstop = 5.6
    scene.render.film_transparent = False
    scene.render.resolution_percentage = 100
    scene.render.image_settings.color_depth = "8"

    if args.shot_library or args.animated_shot_library:
        if args.shot_library and args.animated_shot_library:
            raise SystemExit("Choose one shot-library mode.")
        if args.animation:
            raise SystemExit("Choose either --shot-library or --animation, not both.")
        if args.width < 640 or args.height < 360 or args.width > 2560 or args.height > 1440:
            raise SystemExit("Shot-library dimensions must be between 640x360 and 2560x1440.")
        shot_dir = Path(args.shots_dir).resolve()
        shot_dir.mkdir(parents=True, exist_ok=True)
        scene.camera.data.dof.use_dof = False
        if hasattr(scene, "eevee") and hasattr(scene.eevee, "taa_render_samples"):
            scene.eevee.taa_render_samples = 8
        scene.render.resolution_percentage = 100
        scene.render.image_settings.file_format = "PNG"
        scene.render.image_settings.color_mode = "RGBA"
        # Large in-world teaching boards for the phrase-review and quiz sections.
        phrase_card_objects = []
        quiz_card_objects = []

        phrase_card_objects.append(cube("Phrase lesson board", (0.0, -0.86, 2.55),
                                         (6.8, 0.14, 3.55), M["sign"], 0.16))
        phrase_card_objects.append(cube("Phrase board gold header", (0.0, -0.95, 4.12),
                                         (6.35, 0.035, 0.055), M["gold"], 0.02))
        phrase_card_objects.append(text_obj("5 USEFUL AIRPORT PHRASES", (0.0, -0.965, 3.82),
                                            0.30, M["text"]))
        phrase_lines = [
            "1. Where is the check-in counter?",
            "2. May I see your passport?",
            "3. Here you are.",
            "4. Where is Gate 12?",
            "5. Have a wonderful trip!",
        ]
        for phrase, z in zip(phrase_lines, (3.22, 2.72, 2.22, 1.72, 1.22)):
            phrase_card_objects.append(text_obj(phrase, (-2.85, -0.966, z),
                                                0.205, M["white"], align="LEFT"))

        quiz_card_objects.append(cube("Quiz board", (0.0, -0.86, 2.55),
                                       (6.8, 0.14, 3.55), M["sign"], 0.16))
        quiz_card_objects.append(cube("Quiz board gold header", (0.0, -0.95, 4.12),
                                      (6.35, 0.035, 0.055), M["gold"], 0.02))
        quiz_card_objects.append(text_obj("QUICK ENGLISH QUIZ", (0.0, -0.965, 3.82),
                                          0.32, M["text"]))
        quiz_card_objects.append(text_obj("WHAT DOES BOARDING PASS MEAN?",
                                          (0.0, -0.966, 3.12), 0.235, M["white"]))
        for option, z in zip(
            ("A) A passport", "B) A boarding document", "C) A suitcase"),
            (2.48, 1.98, 1.48)
        ):
            quiz_card_objects.append(text_obj(option, (-2.2, -0.966, z),
                                              0.25, M["white"], align="LEFT"))
        for obj in phrase_card_objects + quiz_card_objects:
            obj.hide_render = True

        camera_shots = [
            ((0.0, -17.0, 5.0), (0.0, 1.4, 2.5), 42),       # 01 airport establishing
            ((-2.3, -5.6, 2.8), (-2.3, 0.0, 2.55), 68),     # 02 Leo worried close-up
            ((0.0, -5.6, 2.8), (0.0, 0.0, 2.55), 68),       # 03 Emma reassurance
            ((-1.0, -8.5, 3.4), (-1.0, 0.0, 2.15), 54),     # 04 arrival two-shot
            ((-5.2, -8.0, 3.1), (-5.2, 0.8, 1.45), 52),     # 05 check-in counter
            ((-6.0, -6.0, 2.8), (-6.0, 0.5, 2.0), 58),      # 06 airport agent
            ((-4.0, -4.8, 2.3), (-5.2, 0.7, 1.65), 72),     # 07 passport handoff
            ((-3.4, -4.6, 1.8), (-5.2, 0.7, 1.45), 78),     # 08 boarding pass/counter detail
            ((0.0, -8.0, 5.0), (0.0, 3.6, 4.45), 62),      # 09 Gate 12 sign
            ((-1.0, -10.0, 3.5), (0.0, 0.5, 2.0), 48),      # 10 walk to gate
            ((4.2, -9.0, 3.6), (4.2, 0.6, 1.9), 50),        # 11 security area
            ((4.1, -4.5, 1.9), (4.2, 0.4, 1.1), 76),        # 12 security tray detail
            ((4.2, -7.0, 3.0), (4.2, 0.6, 1.8), 58),        # 13 scanner walk-through
            ((2.25, -4.5, 2.7), (2.25, 0.0, 1.95), 72),     # 14 Ollie close-up
            ((0.0, -15.0, 4.5), (0.0, 2.3, 2.8), 44),       # 15 departure gate wide
            ((0.0, -10.0, 4.0), (0.0, -0.8, 2.55), 48),    # 16 five airport phrases board
            ((0.0, -10.0, 4.0), (0.0, -0.8, 2.55), 48),    # 17 boarding-pass quiz board
            ((-1.0, -8.0, 3.2), (-1.0, 0.0, 2.1), 56),      # 18 story ending two-shot
        ]
        for index, (location, target_point, lens) in enumerate(camera_shots, start=1):
            for obj in phrase_card_objects:
                obj.hide_render = index != 16
            for obj in quiz_card_objects:
                obj.hide_render = index != 17
            camera.location = location
            camera.rotation_euler = (Vector(target_point) - camera.location).to_track_quat("-Z", "Y").to_euler()
            camera.data.lens = lens
            scene.camera = camera
            if args.animated_shot_library:
                # Real frame-by-frame 3D animation for every story shot.
                frames = 36
                rigs = []
                for prefix in ("Leo", "Emma", "Ollie"):
                    rig = bpy.data.objects.new(prefix + f" animated shot {index:02d}", None)
                    bpy.context.collection.objects.link(rig)
                    for part in list(bpy.data.objects):
                        if part is rig or not part.name.startswith(prefix):
                            continue
                        matrix = part.matrix_world.copy()
                        part.parent = rig
                        part.matrix_world = matrix
                    rigs.append((prefix, rig))
                for ci, (prefix, rig) in enumerate(rigs):
                    for frame, amount in ((1, 0.0), (18, 1.0), (36, 0.0)):
                        scene.frame_set(frame)
                        rig.location.z = amount * (0.07 if prefix == "Ollie" else 0.045)
                        rig.rotation_euler[1] = math.radians(amount * (3.0 if ci != 1 else -3.0))
                        rig.keyframe_insert(data_path="location", frame=frame)
                        rig.keyframe_insert(data_path="rotation_euler", frame=frame)
                for part in list(bpy.data.objects):
                    if any(tag in part.name for tag in ("Leo sleeve", "Emma sleeve", "Ollie ear tuft")):
                        base = part.rotation_euler.copy()
                        for frame, amount in ((1, 0.0), (18, 0.25), (36, 0.0)):
                            part.rotation_euler[1] = base[1] + amount
                            part.keyframe_insert(data_path="rotation_euler", frame=frame)
                camera.location = Vector(location)
                camera.keyframe_insert(data_path="location", frame=1)
                camera.location = Vector(location) + Vector((0.12, 0.0, 0.04))
                camera.keyframe_insert(data_path="location", frame=36)
                scene.frame_start, scene.frame_end, scene.render.fps = 1, 36, 12
                scene.render.resolution_percentage = 100
                scene.render.image_settings.file_format = "FFMPEG"
                scene.render.image_settings.color_mode = "RGB"
                scene.render.ffmpeg.format = "MPEG4"
                scene.render.ffmpeg.codec = "H264"
                scene.render.ffmpeg.constant_rate_factor = "MEDIUM"
                scene.render.ffmpeg.ffmpeg_preset = "GOOD"
                shot_path = shot_dir / f"shot-{index:02d}.mp4"
                scene.render.filepath = str(shot_path)
                scene.frame_set(1)
                bpy.ops.render.render(animation=True)
            else:
                scene.frame_set(1)
                shot_path = shot_dir / f"shot-{index:02d}.png"
                scene.render.filepath = str(shot_path)
                bpy.ops.render.render(write_still=True)
            if not shot_path.is_file() or shot_path.stat().st_size < 10000:
                raise SystemExit(f"3D shot render missing or too small: {shot_path}")
            print(f"ENGLISHTALE_3D_SHOT_{index:02d}={shot_path}")

        print(f"ENGLISHTALE_3D_SHOT_LIBRARY={shot_dir}")
    elif args.animation:
        if args.duration < 2 or args.duration > 12 or args.fps < 12 or args.fps > 30:
            raise SystemExit("Animation settings out of range: use 2–12 seconds and 12–30 fps.")
        # Keep the CI motion proof CPU-friendly while preserving the 1280x720 frame.
        scene.camera.data.dof.use_dof = False
        if hasattr(scene, "eevee") and hasattr(scene.eevee, "taa_render_samples"):
            scene.eevee.taa_render_samples = 8
        scene.render.resolution_percentage = 50

        def character_root(prefix, label):
            root = bpy.data.objects.new(label + " animation root", None)
            bpy.context.collection.objects.link(root)
            root.empty_display_type = "PLAIN_AXES"
            root.location = (0, 0, 0)
            for obj in list(bpy.data.objects):
                if obj is root or not obj.name.startswith(prefix):
                    continue
                world_matrix = obj.matrix_world.copy()
                obj.parent = root
                obj.matrix_world = world_matrix
            return root

        roots = [
            character_root("Leo", "Leo"),
            character_root("Emma", "Emma"),
            character_root("Ollie", "Ollie"),
        ]
        midpoint = max(2, (args.duration * args.fps) // 2)
        last_frame = args.duration * args.fps
        for index, root in enumerate(roots):
            root.location.z = 0.0
            root.rotation_euler[1] = 0.0
            root.keyframe_insert(data_path="location", frame=1)
            root.keyframe_insert(data_path="rotation_euler", frame=1)
            root.location.z = 0.055 if index < 2 else 0.085
            root.rotation_euler[1] = math.radians(2.0 if index != 1 else -2.0)
            root.keyframe_insert(data_path="location", frame=midpoint)
            root.keyframe_insert(data_path="rotation_euler", frame=midpoint)
            root.location.z = 0.0
            root.rotation_euler[1] = 0.0
            root.keyframe_insert(data_path="location", frame=last_frame)
            root.keyframe_insert(data_path="rotation_euler", frame=last_frame)

        camera.location = (0, -14.8, 4.1)
        camera.keyframe_insert(data_path="location", frame=1)
        camera.data.lens = 48
        camera.data.keyframe_insert(data_path="lens", frame=1)
        camera.location = (0, -13.9, 4.1)
        camera.keyframe_insert(data_path="location", frame=last_frame)
        camera.data.lens = 50
        camera.data.keyframe_insert(data_path="lens", frame=last_frame)

        scene.frame_start = 1
        scene.frame_end = last_frame
        scene.render.fps = args.fps
        scene.render.image_settings.file_format = "FFMPEG"
        scene.render.image_settings.color_mode = "RGB"
        scene.render.ffmpeg.format = "MPEG4"
        scene.render.ffmpeg.codec = "H264"
        scene.render.ffmpeg.constant_rate_factor = "MEDIUM"
        scene.render.ffmpeg.ffmpeg_preset = "GOOD"
        scene.render.filepath = str(output)
        scene.frame_set(1)
        bpy.ops.render.render(animation=True)
        print("ENGLISHTALE_3D_MOTION_OUTPUT=" + str(output))
    else:
        bpy.ops.render.render(write_still=True)
        print("ENGLISHTALE_3D_LOOKDEV_OUTPUT=" + str(output))


if __name__ == "__main__":
    main()
