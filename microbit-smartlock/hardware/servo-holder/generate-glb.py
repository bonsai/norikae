"""
Generate GLB file for Micro:bit Smart Lock Servo Holder
Run this script to create servo-holder.glb
"""

import struct
import math
import os

def create_glb():
    """Create a minimal GLB file with basic shapes for the servo holder assembly"""
    
    # Helper function to create a cylinder mesh
    def create_cylinder(radius, height, sections, z_offset=0):
        vertices = []
        indices = []
        
        # Top cap center
        vertices.append([0, 0, height/2 + z_offset])
        # Bottom cap center
        vertices.append([0, 0, -height/2 + z_offset])
        
        # Top ring
        for i in range(sections):
            angle = 2 * math.pi * i / sections
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            vertices.append([x, y, height/2 + z_offset])
        
        # Bottom ring
        for i in range(sections):
            angle = 2 * math.pi * i / sections
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            vertices.append([x, y, -height/2 + z_offset])
        
        # Top cap indices
        for i in range(sections):
            indices.append(0)
            indices.append(2 + i)
            indices.append(2 + (i + 1) % sections)
        
        # Bottom cap indices
        for i in range(sections):
            indices.append(1)
            indices.append(2 + sections + (i + 1) % sections)
            indices.append(2 + sections + i)
        
        # Side indices
        for i in range(sections):
            indices.append(2 + i)
            indices.append(2 + sections + i)
            indices.append(2 + (i + 1) % sections)
            
            indices.append(2 + (i + 1) % sections)
            indices.append(2 + sections + i)
            indices.append(2 + sections + (i + 1) % sections)
        
        return vertices, indices
    
    # Helper function to create a box mesh
    def create_box(width, height, depth):
        w, h, d = width/2, height/2, depth/2
        vertices = [
            [-w, -h, -d], [w, -h, -d], [w, h, -d], [-w, h, -d],
            [-w, -h, d], [w, -h, d], [w, h, d], [-w, h, d]
        ]
        indices = [
            0, 1, 2, 0, 2, 3,  # Back
            5, 4, 7, 5, 7, 6,  # Front
            4, 0, 3, 4, 3, 7,  # Left
            1, 5, 6, 1, 6, 2,  # Right
            3, 2, 6, 3, 6, 7,  # Top
            4, 5, 1, 4, 1, 0   # Bottom
        ]
        return vertices, indices
    
    # Create meshes
    all_vertices = []
    all_indices = []
    mesh_ranges = []  # (vertex_start, vertex_count, index_start, index_count)
    
    # 1. Servo Mount (blue cylinder)
    verts, inds = create_cylinder(11, 4, 32)
    vertex_start = len(all_vertices)
    index_start = len(all_indices)
    all_vertices.extend(verts)
    all_indices.extend(inds)
    mesh_ranges.append((vertex_start, len(verts), index_start, len(inds)))
    
    # 2. Center Post (blue)
    verts, inds = create_cylinder(4, 2, 16)
    vertex_start = len(all_vertices)
    index_start = len(all_indices)
    all_vertices.extend(verts)
    all_indices.extend(inds)
    mesh_ranges.append((vertex_start, len(verts), index_start, len(inds)))
    
    # 3. Connection Arm (gray box)
    verts, inds = create_box(25, 10, 4)
    # Translate arm
    verts = [[v[0] + 12.5, v[1], v[2]] for v in verts]
    vertex_start = len(all_vertices)
    index_start = len(all_indices)
    all_vertices.extend(verts)
    all_indices.extend(inds)
    mesh_ranges.append((vertex_start, len(verts), index_start, len(inds)))
    
    # 4. Magnet Housing Servo (red cylinder)
    verts, inds = create_cylinder(10, 4, 32, z_offset=2)
    verts = [[v[0] + 25, v[1], v[2]] for v in verts]
    vertex_start = len(all_vertices)
    index_start = len(all_indices)
    all_vertices.extend(verts)
    all_indices.extend(inds)
    mesh_ranges.append((vertex_start, len(verts), index_start, len(inds)))
    
    # 5. Magnet 1 (silver cylinder)
    verts, inds = create_cylinder(3, 3, 16, z_offset=3.5)
    verts = [[v[0] + 25, v[1], v[2]] for v in verts]
    vertex_start = len(all_vertices)
    index_start = len(all_indices)
    all_vertices.extend(verts)
    all_indices.extend(inds)
    mesh_ranges.append((vertex_start, len(verts), index_start, len(inds)))
    
    # 6. Magnet 2 (silver cylinder)
    verts, inds = create_cylinder(3, 3, 16, z_offset=3.5)
    verts = [[v[0] + 40, v[1], v[2]] for v in verts]
    vertex_start = len(all_vertices)
    index_start = len(all_indices)
    all_vertices.extend(verts)
    all_indices.extend(inds)
    mesh_ranges.append((vertex_start, len(verts), index_start, len(inds)))
    
    # 7. Magnet Housing Thumb (green cylinder)
    verts, inds = create_cylinder(10, 4, 32, z_offset=2)
    verts = [[v[0] + 40, v[1], v[2]] for v in verts]
    vertex_start = len(all_vertices)
    index_start = len(all_indices)
    all_vertices.extend(verts)
    all_indices.extend(inds)
    mesh_ranges.append((vertex_start, len(verts), index_start, len(inds)))
    
    # 8. Thumb Grip (green box)
    verts, inds = create_box(8, 6, 4)
    verts = [[v[0] + 45, v[1], v[2]] for v in verts]
    vertex_start = len(all_vertices)
    index_start = len(all_indices)
    all_vertices.extend(verts)
    all_indices.extend(inds)
    mesh_ranges.append((vertex_start, len(verts), index_start, len(inds)))
    
    # Convert to binary
    vertex_data = b''
    for v in all_vertices:
        vertex_data += struct.pack('<3f', v[0], v[1], v[2])
    
    index_data = b''
    for i in all_indices:
        index_data += struct.pack('<I', i)
    
    # GLB Structure
    JSON_TEMPLATE = '''{
  "asset": {"version": "2.0", "generator": "Micro:bit Smart Lock"},
  "scene": 0,
  "scenes": [{"nodes": [0,1,2,3,4,5,6,7]}],
  "nodes": [
    {"name": "Servo Mount", "mesh": 0},
    {"name": "Center Post", "mesh": 1},
    {"name": "Connection Arm", "mesh": 2},
    {"name": "Magnet Housing (Servo)", "mesh": 3},
    {"name": "Magnet 1", "mesh": 4},
    {"name": "Magnet 2", "mesh": 5},
    {"name": "Magnet Housing (Thumb)", "mesh": 6},
    {"name": "Thumb Grip", "mesh": 7}
  ],
  "meshes": [MESHES],
  "materials": [
    {"name": "Blue PLA", "pbrMetallicRoughness": {"baseColorFactor": [0.25, 0.45, 0.75, 1.0], "metallicFactor": 0.1, "roughnessFactor": 0.5}},
    {"name": "Gray PETG", "pbrMetallicRoughness": {"baseColorFactor": [0.35, 0.35, 0.35, 1.0], "metallicFactor": 0.2, "roughnessFactor": 0.6}},
    {"name": "Red PLA", "pbrMetallicRoughness": {"baseColorFactor": [0.75, 0.35, 0.35, 1.0], "metallicFactor": 0.1, "roughnessFactor": 0.5}},
    {"name": "Silver Magnet", "pbrMetallicRoughness": {"baseColorFactor": [0.7, 0.7, 0.7, 1.0], "metallicFactor": 0.9, "roughnessFactor": 0.2}},
    {"name": "Green PLA", "pbrMetallicRoughness": {"baseColorFactor": [0.35, 0.75, 0.35, 1.0], "metallicFactor": 0.1, "roughnessFactor": 0.5}}
  ],
  "buffers": [{"byteLength": BUFFER_LENGTH}],
  "bufferViews": [VIEWS],
  "accessors": [ACCESSORS]
}'''
    
    # Build mesh JSON
    meshes_json = []
    views_json = []
    accessors_json = []
    
    byte_offset = 0
    for i, (v_start, v_count, i_start, i_count) in enumerate(mesh_ranges):
        # Determine material
        if i == 0 or i == 1:
            mat_idx = 0  # Blue
        elif i == 2:
            mat_idx = 1  # Gray
        elif i == 3:
            mat_idx = 2  # Red
        elif i == 4 or i == 5:
            mat_idx = 3  # Silver
        else:
            mat_idx = 4  # Green
        
        # Vertex buffer view
        v_byte_offset = byte_offset
        v_byte_length = v_count * 3 * 4  # 3 floats per vertex, 4 bytes each
        byte_offset += v_byte_length
        
        # Index buffer view
        i_byte_offset = byte_offset
        i_byte_length = i_count * 4  # 4 bytes per index
        byte_offset += i_byte_length
        
        mesh_json = f'{{"primitives": [{{"attributes": {{"POSITION": {len(accessors_json)}}, "material": {mat_idx}}}], "indices": {len(accessors_json)+1}}}'
        meshes_json.append(mesh_json)
        
        # Vertex accessor
        v_min = [0.0, 0.0, 0.0]
        v_max = [0.0, 0.0, 0.0]
        accessors_json.append(f'{{"bufferView": {len(views_json)}, "componentType": 5126, "count": {v_count}, "type": "VEC3", "min": {v_min}, "max": {v_max}}}')
        views_json.append(f'{{"buffer": 0, "byteOffset": {v_byte_offset}, "byteLength": {v_byte_length}, "target": 34962}}')
        
        # Index accessor
        accessors_json.append(f'{{"bufferView": {len(views_json)}, "componentType": 5125, "count": {i_count}, "type": "SCALAR"}}')
        views_json.append(f'{{"buffer": 0, "byteOffset": {i_byte_offset}, "byteLength": {i_byte_length}, "target": 34963}}')
    
    json_str = JSON_TEMPLATE.replace('MESHES', ','.join(meshes_json))
    json_str = json_str.replace('VIEWS', ','.join(views_json))
    json_str = json_str.replace('ACCESSORS', ','.join(accessors_json))
    json_str = json_str.replace('BUFFER_LENGTH', str(byte_offset))
    
    # Pad JSON to 4-byte alignment
    json_bytes = json_str.encode('utf-8')
    json_padding = (4 - len(json_bytes) % 4) % 4
    json_bytes += b' ' * json_padding
    
    # Build GLB file
    header = struct.pack('<4sII', b'glTF', 2, 12 + 8 + len(json_bytes) + 8 + byte_offset)
    json_chunk = struct.pack('<II', len(json_bytes), 0x4E4F534A)  # JSON chunk
    bin_chunk = struct.pack('<II', byte_offset, 0x004E4942)  # BIN chunk
    
    glb_data = header + json_chunk + json_bytes + bin_chunk + vertex_data + index_data
    
    return glb_data

def create_exploded_glb():
    """Create exploded view GLB"""
    
    def create_cylinder(radius, height, sections, z_offset=0):
        vertices = []
        indices = []
        
        vertices.append([0, 0, height/2 + z_offset])
        vertices.append([0, 0, -height/2 + z_offset])
        
        for i in range(sections):
            angle = 2 * math.pi * i / sections
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            vertices.append([x, y, height/2 + z_offset])
        
        for i in range(sections):
            angle = 2 * math.pi * i / sections
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            vertices.append([x, y, -height/2 + z_offset])
        
        for i in range(sections):
            indices.append(0)
            indices.append(2 + i)
            indices.append(2 + (i + 1) % sections)
        
        for i in range(sections):
            indices.append(1)
            indices.append(2 + sections + (i + 1) % sections)
            indices.append(2 + sections + i)
        
        for i in range(sections):
            indices.append(2 + i)
            indices.append(2 + sections + i)
            indices.append(2 + (i + 1) % sections)
            indices.append(2 + (i + 1) % sections)
            indices.append(2 + sections + i)
            indices.append(2 + sections + (i + 1) % sections)
        
        return vertices, indices
    
    def create_box(width, height, depth):
        w, h, d = width/2, height/2, depth/2
        vertices = [
            [-w, -h, -d], [w, -h, -d], [w, h, -d], [-w, h, -d],
            [-w, -h, d], [w, -h, d], [w, h, d], [-w, h, d]
        ]
        indices = [
            0, 1, 2, 0, 2, 3, 5, 4, 7, 5, 7, 6,
            4, 0, 3, 4, 3, 7, 1, 5, 6, 1, 6, 2,
            3, 2, 6, 3, 6, 7, 4, 5, 1, 4, 1, 0
        ]
        return vertices, indices
    
    all_vertices = []
    all_indices = []
    mesh_ranges = []
    
    # Exploded positions (spread along X axis)
    positions = [
        (-30, 0, 0),   # Servo mount
        (-30, 0, -2),  # Center post
        (-5, 0, 0),    # Arm
        (20, 0, 0),    # Magnet housing servo
        (20, 0, 6),    # Magnet 1
        (35, 0, 6),    # Magnet 2
        (35, 0, 0),    # Magnet housing thumb
        (48, 0, 0),    # Thumb grip
    ]
    
    sizes = [
        ('cyl', 11, 4, 32),
        ('cyl', 4, 2, 16),
        ('box', 25, 10, 4),
        ('cyl', 10, 4, 32),
        ('cyl', 3, 3, 16),
        ('cyl', 3, 3, 16),
        ('cyl', 10, 4, 32),
        ('box', 8, 6, 4),
    ]
    
    for pos, (shape, *args) in zip(positions, sizes):
        if shape == 'cyl':
            verts, inds = create_cylinder(*args)
        else:
            verts, inds = create_box(*args)
        
        verts = [[v[0] + pos[0], v[1] + pos[1], v[2] + pos[2]] for v in verts]
        
        vertex_start = len(all_vertices)
        index_start = len(all_indices)
        all_vertices.extend(verts)
        all_indices.extend(inds)
        mesh_ranges.append((vertex_start, len(verts), index_start, len(inds)))
    
    vertex_data = b''
    for v in all_vertices:
        vertex_data += struct.pack('<3f', v[0], v[1], v[2])
    
    index_data = b''
    for i in all_indices:
        index_data += struct.pack('<I', i)
    
    JSON_TEMPLATE = '''{
  "asset": {"version": "2.0", "generator": "Micro:bit Smart Lock Exploded"},
  "scene": 0,
  "scenes": [{"nodes": [0,1,2,3,4,5,6,7]}],
  "nodes": [
    {"name": "Servo Mount", "mesh": 0},
    {"name": "Center Post", "mesh": 1},
    {"name": "Connection Arm", "mesh": 2},
    {"name": "Magnet Housing (Servo)", "mesh": 3},
    {"name": "Magnet 1", "mesh": 4},
    {"name": "Magnet 2", "mesh": 5},
    {"name": "Magnet Housing (Thumb)", "mesh": 6},
    {"name": "Thumb Grip", "mesh": 7}
  ],
  "meshes": [MESHES],
  "materials": [
    {"name": "Blue PLA", "pbrMetallicRoughness": {"baseColorFactor": [0.25, 0.45, 0.75, 1.0], "metallicFactor": 0.1, "roughnessFactor": 0.5}},
    {"name": "Gray PETG", "pbrMetallicRoughness": {"baseColorFactor": [0.35, 0.35, 0.35, 1.0], "metallicFactor": 0.2, "roughnessFactor": 0.6}},
    {"name": "Red PLA", "pbrMetallicRoughness": {"baseColorFactor": [0.75, 0.35, 0.35, 1.0], "metallicFactor": 0.1, "roughnessFactor": 0.5}},
    {"name": "Silver Magnet", "pbrMetallicRoughness": {"baseColorFactor": [0.7, 0.7, 0.7, 1.0], "metallicFactor": 0.9, "roughnessFactor": 0.2}},
    {"name": "Green PLA", "pbrMetallicRoughness": {"baseColorFactor": [0.35, 0.75, 0.35, 1.0], "metallicFactor": 0.1, "roughnessFactor": 0.5}}
  ],
  "buffers": [{"byteLength": BUFFER_LENGTH}],
  "bufferViews": [VIEWS],
  "accessors": [ACCESSORS]
}'''
    
    meshes_json = []
    views_json = []
    accessors_json = []
    
    byte_offset = 0
    for i, (v_start, v_count, i_start, i_count) in enumerate(mesh_ranges):
        mat_idx = [0, 0, 1, 2, 3, 3, 4, 4][i]
        
        v_byte_offset = byte_offset
        v_byte_length = v_count * 3 * 4
        byte_offset += v_byte_length
        
        i_byte_offset = byte_offset
        i_byte_length = i_count * 4
        byte_offset += i_byte_length
        
        mesh_json = f'{{"primitives": [{{"attributes": {{"POSITION": {len(accessors_json)}}, "material": {mat_idx}}}], "indices": {len(accessors_json)+1}}}'
        meshes_json.append(mesh_json)
        
        accessors_json.append(f'{{"bufferView": {len(views_json)}, "componentType": 5126, "count": {v_count}, "type": "VEC3"}}')
        views_json.append(f'{{"buffer": 0, "byteOffset": {v_byte_offset}, "byteLength": {v_byte_length}, "target": 34962}}')
        
        accessors_json.append(f'{{"bufferView": {len(views_json)}, "componentType": 5125, "count": {i_count}, "type": "SCALAR"}}')
        views_json.append(f'{{"buffer": 0, "byteOffset": {i_byte_offset}, "byteLength": {i_byte_length}, "target": 34963}}')
    
    json_str = JSON_TEMPLATE.replace('MESHES', ','.join(meshes_json))
    json_str = json_str.replace('VIEWS', ','.join(views_json))
    json_str = json_str.replace('ACCESSORS', ','.join(accessors_json))
    json_str = json_str.replace('BUFFER_LENGTH', str(byte_offset))
    
    json_bytes = json_str.encode('utf-8')
    json_padding = (4 - len(json_bytes) % 4) % 4
    json_bytes += b' ' * json_padding
    
    header = struct.pack('<4sII', b'glTF', 2, 12 + 8 + len(json_bytes) + 8 + byte_offset)
    json_chunk = struct.pack('<II', len(json_bytes), 0x4E4F534A)
    bin_chunk = struct.pack('<II', byte_offset, 0x004E4942)
    
    glb_data = header + json_chunk + json_bytes + bin_chunk + vertex_data + index_data
    
    return glb_data

if __name__ == "__main__":
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create assembled GLB
    glb_data = create_glb()
    output_path = os.path.join(output_dir, "servo-holder-assembled.glb")
    with open(output_path, 'wb') as f:
        f.write(glb_data)
    print(f"Created: {output_path}")
    print(f"  Size: {len(glb_data) / 1024:.1f} KB")
    
    # Create exploded view GLB
    exploded_data = create_exploded_glb()
    exploded_path = os.path.join(output_dir, "servo-holder-exploded.glb")
    with open(exploded_path, 'wb') as f:
        f.write(exploded_data)
    print(f"Created: {exploded_path}")
    print(f"  Size: {len(exploded_data) / 1024:.1f} KB")
    
    print("\nOpen these files in:")
    print("  - Windows 3D Viewer (double-click)")
    print("  - Blender")
    print("  - Online: https://gltf.report/ or https://sandbox.babylonjs.com/")
    print("  - Three.js viewer")
