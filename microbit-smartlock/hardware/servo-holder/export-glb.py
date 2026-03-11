#!/usr/bin/env python3
"""
Export OpenSCAD servo holder design to GLB format
Micro:bit Smart Lock Project

Requirements:
    pip install trimesh numpy

Usage:
    1. Export STL from OpenSCAD first (or use included STL)
    2. Run: python export-glb.py servo-holder.stl servo-holder.glb

Alternative: Direct Blender Python script included below
"""

import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import trimesh
        import numpy
        return True
    except ImportError:
        print("Missing dependencies. Install with:")
        print("  pip install trimesh numpy")
        return False

def stl_to_glb(stl_path, glb_path):
    """Convert STL file to GLB format"""
    import trimesh
    
    print(f"Loading STL: {stl_path}")
    mesh = trimesh.load(stl_path)
    
    # If multiple meshes, combine them
    if isinstance(mesh, trimesh.Scene):
        meshes = [g.geometry for g in mesh.geometry.values() if isinstance(g, trimesh.Trimesh)]
        if meshes:
            mesh = trimesh.util.concatenate(meshes)
    
    print(f"Vertices: {len(mesh.vertices)}")
    print(f"Faces: {len(mesh.faces)}")
    
    # Add basic material
    mesh.visual.material = trimesh.visual.material.SimpleMaterial(
        diffuse=[100, 100, 100, 255],  # Gray color
        ambient=[50, 50, 50, 255],
        specular=[150, 150, 150, 255],
        glossiness=50
    )
    
    print(f"Exporting GLB: {glb_path}")
    mesh.export(glb_path, file_type='glb')
    print("Done!")

def create_servo_holder_glb(output_path):
    """
    Create servo holder GLB programmatically using trimesh
    This creates a simplified version without needing OpenSCAD
    """
    import trimesh
    import numpy as np
    
    meshes = []
    
    # === Servo Mount Base ===
    cylinder = trimesh.creation.cylinder(
        radius=11,
        height=4,
        sections=60
    )
    cylinder.visual.material = trimesh.visual.material.SimpleMaterial(
        diffuse=[60, 100, 200, 255],  # Blue
        ambient=[30, 50, 100, 255],
        specular=[100, 150, 200, 255],
        glossiness=60
    )
    meshes.append(cylinder)
    
    # Center post
    post = trimesh.creation.cylinder(
        radius=4,
        height=2,
        sections=30
    )
    post.visual.material = cylinder.visual.material
    meshes.append(post)
    
    # === Connection Arm ===
    arm_box = trimesh.creation.box(
        extents=[25, 10, 4]
    )
    # Move arm to correct position
    arm_box.apply_translation([12.5, 0, 2])
    arm_box.visual.material = trimesh.visual.material.SimpleMaterial(
        diffuse=[80, 80, 80, 255],  # Gray
        ambient=[40, 40, 40, 255],
        specular=[120, 120, 120, 255],
        glossiness=50
    )
    meshes.append(arm_box)
    
    # === Magnet Housing (Servo Side) ===
    magnet_housing = trimesh.creation.cylinder(
        radius=10,
        height=4,
        sections=60
    )
    magnet_housing.apply_translation([25, 0, 5])
    magnet_housing.visual.material = trimesh.visual.material.SimpleMaterial(
        diffuse=[200, 80, 80, 255],  # Red
        ambient=[100, 40, 40, 255],
        specular=[180, 100, 100, 255],
        glossiness=70
    )
    meshes.append(magnet_housing)
    
    # Magnet (silver cylinder)
    magnet1 = trimesh.creation.cylinder(
        radius=3,
        height=3,
        sections=30
    )
    magnet1.apply_translation([25, 0, 3.5])
    magnet1.visual.material = trimesh.visual.material.SimpleMaterial(
        diffuse=[180, 180, 180, 255],  # Silver
        ambient=[100, 100, 100, 255],
        specular=[220, 220, 220, 255],
        glossiness=90,
        metallic=0.8
    )
    meshes.append(magnet1)
    
    # === Magnet Housing (Thumb-turn Side) ===
    thumb_housing = trimesh.creation.cylinder(
        radius=10,
        height=4,
        sections=60
    )
    thumb_housing.apply_translation([40, 0, 5])
    thumb_housing.visual.material = trimesh.visual.material.SimpleMaterial(
        diffuse=[80, 200, 80, 255],  # Green
        ambient=[40, 100, 40, 255],
        specular=[100, 180, 100, 255],
        glossiness=70
    )
    meshes.append(thumb_housing)
    
    # Thumb-turn grip (box)
    grip = trimesh.creation.box(
        extents=[10, 6, 4]
    )
    grip.apply_translation([45, 0, 3])
    grip.visual.material = thumb_housing.visual.material
    meshes.append(grip)
    
    # Second magnet
    magnet2 = trimesh.creation.cylinder(
        radius=3,
        height=3,
        sections=30
    )
    magnet2.apply_translation([40, 0, 3.5])
    magnet2.visual.material = magnet1.visual.material
    meshes.append(magnet2)
    
    # === Create Scene ===
    scene = trimesh.Scene()
    for mesh in meshes:
        scene.add_geometry(mesh)
    
    # Add lights
    from trimesh.visual.light import PointLight, AmbientLight
    
    ambient = AmbientLight(color=[255, 255, 255], intensity=0.5)
    scene.add_geometry(ambient)
    
    point_light = trimesh.creation.light.PointLight(color=[255, 255, 255], intensity=1.0)
    point_light.apply_translation([50, 50, 50])
    scene.add_geometry(point_light)
    
    # Export
    print(f"Exporting GLB: {output_path}")
    scene.export(output_path, file_type='glb')
    print("GLB export complete!")
    print(f"  Total meshes: {len(meshes)}")
    
    return output_path

def create_exploded_view_glb(output_path):
    """
    Create exploded view GLB showing all components separated
    """
    import trimesh
    import numpy as np
    
    meshes = []
    
    # Color scheme
    colors = {
        'servo_mount': [60, 100, 200, 255],      # Blue
        'arm': [80, 80, 80, 255],                 # Gray
        'magnet_housing_servo': [200, 80, 80, 255],  # Red
        'magnet_housing_thumb': [80, 200, 80, 255],  # Green
        'magnet': [180, 180, 180, 255],           # Silver
        'thumb_grip': [80, 180, 80, 255],         # Light green
    }
    
    def create_material(color):
        return trimesh.visual.material.SimpleMaterial(
            diffuse=color[:3],
            ambient=[c//2 for c in color[:3]],
            specular=[min(c+50, 255) for c in color[:3]],
            glossiness=60
        )
    
    # 1. Servo Mount (leftmost in exploded view)
    servo_mount = trimesh.creation.cylinder(radius=11, height=4, sections=60)
    servo_mount.apply_translation([-30, 0, 0])
    servo_mount.visual.material = create_material(colors['servo_mount'])
    meshes.append(servo_mount)
    
    # Center post
    post = trimesh.creation.cylinder(radius=4, height=2, sections=30)
    post.apply_translation([-30, 0, -1])
    post.visual.material = create_material(colors['servo_mount'])
    meshes.append(post)
    
    # 2. Connection Arm
    arm = trimesh.creation.box(extents=[25, 10, 4])
    arm.apply_translation([-5, 0, 0])
    arm.visual.material = create_material(colors['arm'])
    meshes.append(arm)
    
    # 3. Magnet Housing (Servo Side)
    mag_house_servo = trimesh.creation.cylinder(radius=10, height=4, sections=60)
    mag_house_servo.apply_translation([20, 0, 0])
    mag_house_servo.visual.material = create_material(colors['magnet_housing_servo'])
    meshes.append(mag_house_servo)
    
    # 4. Magnet 1
    magnet1 = trimesh.creation.cylinder(radius=3, height=3, sections=30)
    magnet1.apply_translation([20, 0, 5])
    magnet1.visual.material = create_material(colors['magnet'])
    meshes.append(magnet1)
    
    # 5. Magnet 2
    magnet2 = trimesh.creation.cylinder(radius=3, height=3, sections=30)
    magnet2.apply_translation([35, 0, 5])
    magnet2.visual.material = create_material(colors['magnet'])
    meshes.append(magnet2)
    
    # 6. Magnet Housing (Thumb Side)
    mag_house_thumb = trimesh.creation.cylinder(radius=10, height=4, sections=60)
    mag_house_thumb.apply_translation([35, 0, 0])
    mag_house_thumb.visual.material = create_material(colors['magnet_housing_thumb'])
    meshes.append(mag_house_thumb)
    
    # 7. Thumb Grip
    grip = trimesh.creation.box(extents=[8, 6, 4])
    grip.apply_translation([48, 0, 0])
    grip.visual.material = create_material(colors['thumb_grip'])
    meshes.append(grip)
    
    # Create scene
    scene = trimesh.Scene()
    for mesh in meshes:
        scene.add_geometry(mesh)
    
    # Add lights
    ambient = trimesh.visual.light.AmbientLight(color=[255, 255, 255], intensity=0.6)
    scene.add_geometry(ambient)
    
    point_light = trimesh.creation.light.PointLight(color=[255, 255, 255], intensity=1.0)
    point_light.apply_translation([100, 100, 100])
    scene.add_geometry(point_light)
    
    print(f"Exporting exploded view GLB: {output_path}")
    scene.export(output_path, file_type='glb')
    print("Exploded view GLB export complete!")
    
    return output_path

if __name__ == "__main__":
    if not check_dependencies():
        print("\nInstalling dependencies...")
        os.system("pip install trimesh numpy")
    
    import trimesh
    
    # Output paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create assembled view
    assembled_path = os.path.join(base_dir, "servo-holder-assembled.glb")
    create_servo_holder_glb(assembled_path)
    
    # Create exploded view
    exploded_path = os.path.join(base_dir, "servo-holder-exploded.glb")
    create_exploded_view_glb(exploded_path)
    
    print("\n✓ GLB files created successfully!")
    print(f"  - {assembled_path}")
    print(f"  - {exploded_path}")
    print("\nOpen these files in:")
    print("  - Windows 3D Viewer")
    print("  - Blender")
    print("  - Online: https://gltf.report/")
    print("  - Three.js viewer")
