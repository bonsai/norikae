#!/usr/bin/env python3
"""
Generate GLB (binary glTF) files for micro:bit smart lock servo holder assembly.
"""

import struct
import json
import math
import os

OUTPUT_DIR = r"I:\My Drive\microbit-smartlock\hardware\servo-holder"

def generate_cylinder(radius, height, segments=32):
    """Generate vertices and indices for a cylinder."""
    vertices = []
    normals = []
    indices = []
    
    half_height = height / 2
    
    # Top cap vertices
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        vertices.extend([x, y, half_height])
        normals.extend([0, 0, 1])
    
    # Bottom cap vertices
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        vertices.extend([x, y, -half_height])
        normals.extend([0, 0, -1])
    
    # Side vertices (top and bottom for each segment)
    side_start = len(vertices) // 3
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        vertices.extend([x, y, half_height])
        nx = math.cos(angle)
        ny = math.sin(angle)
        normals.extend([nx, ny, 0])
    
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        vertices.extend([x, y, -half_height])
        nx = math.cos(angle)
        ny = math.sin(angle)
        normals.extend([nx, ny, 0])
    
    # Top cap indices
    center_top = len(vertices) // 3
    for i in range(segments):
        next_i = (i + 1) % segments
        indices.extend([center_top, i, next_i])
    
    # Bottom cap indices
    center_bottom = center_top + segments
    for i in range(segments):
        next_i = (i + 1) % segments
        indices.extend([center_bottom, segments + next_i, segments + i])
    
    # Side indices
    side_top_start = center_top + segments
    side_bottom_start = side_top_start + segments
    for i in range(segments):
        next_i = (i + 1) % segments
        indices.extend([
            side_top_start + i,
            side_bottom_start + i,
            side_top_start + next_i,
            side_top_start + next_i,
            side_bottom_start + i,
            side_bottom_start + next_i,
        ])
    
    return vertices, normals, indices


def generate_box(width, height, depth):
    """Generate vertices and indices for a box."""
    hw, hh, hd = width / 2, height / 2, depth / 2
    
    # 8 corners
    corners = [
        [-hw, -hh, -hd], [hw, -hh, -hd], [hw, hh, -hd], [-hw, hh, -hd],
        [-hw, -hh, hd], [hw, -hh, hd], [hw, hh, hd], [-hw, hh, hd],
    ]
    
    # 6 faces with indices (counter-clockwise)
    faces = [
        [0, 1, 2, 0, 2, 3],  # Back
        [4, 6, 5, 4, 7, 6],  # Front
        [0, 4, 5, 0, 5, 1],  # Bottom
        [3, 2, 6, 3, 6, 7],  # Top
        [1, 5, 6, 1, 6, 2],  # Right
        [0, 3, 7, 0, 7, 4],  # Left
    ]
    
    vertices = []
    normals = []
    indices = []
    
    face_normals = [
        [0, 0, -1], [0, 0, 1], [0, -1, 0], [0, 1, 0], [1, 0, 0], [-1, 0, 0]
    ]
    
    for face_idx, face in enumerate(faces):
        for vertex_idx in face:
            vertices.extend(corners[vertex_idx])
            normals.extend(face_normals[face_idx])
            indices.append(len(vertices) // 3 - 1)
    
    return vertices, normals, indices


def create_glb(parts, output_path):
    """Create a GLB file from the given parts."""
    
    all_vertices = []
    all_normals = []
    all_indices = []
    mesh_primitives = []
    
    vertex_offset = 0
    index_offset = 0
    
    for part in parts:
        if part['type'] == 'cylinder':
            verts, norms, inds = generate_cylinder(part['radius'], part['height'])
        elif part['type'] == 'box':
            verts, norms, inds = generate_box(part['width'], part['height'], part['depth'])
        else:
            continue
        
        # Apply translation
        tx, ty, tz = part['position']
        for i in range(0, len(verts), 3):
            verts[i] += tx
            verts[i + 1] += ty
            verts[i + 2] += tz
        
        # Adjust indices
        adjusted_inds = [idx + vertex_offset for idx in inds]
        
        all_vertices.extend(verts)
        all_normals.extend(norms)
        all_indices.extend(adjusted_inds)
        
        # Create primitive for this part
        primitive = {
            "attributes": {
                "POSITION": len(mesh_primitives) * 2,  # Will be updated
                "NORMAL": len(mesh_primitives) * 2 + 1,
            },
            "indices": len(mesh_primitives) * 2 + 2,
            "material": part.get('material', 0),
        }
        mesh_primitives.append(primitive)
        
        vertex_offset += len(verts) // 3
        index_offset += len(inds)
    
    # Create accessors
    accessors = []
    buffer_views = []
    byte_offset = 0
    
    # Position accessor
    pos_byte_len = len(all_vertices) * 4
    buffer_views.append({
        "buffer": 0,
        "byteOffset": byte_offset,
        "byteLength": pos_byte_len,
        "target": 34962,  # ARRAY_BUFFER
    })
    accessors.append({
        "bufferView": len(buffer_views) - 1,
        "byteOffset": 0,
        "componentType": 5126,  # FLOAT
        "count": len(all_vertices) // 3,
        "type": "VEC3",
        "max": [max(all_vertices[i::3]) for i in range(3)],
        "min": [min(all_vertices[i::3]) for i in range(3)],
    })
    byte_offset += pos_byte_len
    # Pad to 4-byte alignment
    padding = (4 - (byte_offset % 4)) % 4
    byte_offset += padding
    
    # Normal accessor
    norm_byte_len = len(all_normals) * 4
    buffer_views.append({
        "buffer": 0,
        "byteOffset": byte_offset,
        "byteLength": norm_byte_len,
        "target": 34962,
    })
    accessors.append({
        "bufferView": len(buffer_views) - 1,
        "byteOffset": 0,
        "componentType": 5126,
        "count": len(all_normals) // 3,
        "type": "VEC3",
    })
    byte_offset += norm_byte_len
    padding = (4 - (byte_offset % 4)) % 4
    byte_offset += padding
    
    # Index accessor
    idx_byte_len = len(all_indices) * 2  # USHORT
    buffer_views.append({
        "buffer": 0,
        "byteOffset": byte_offset,
        "byteLength": idx_byte_len,
        "target": 34963,  # ELEMENT_ARRAY_BUFFER
    })
    accessors.append({
        "bufferView": len(buffer_views) - 1,
        "byteOffset": 0,
        "componentType": 5123,  # UNSIGNED_SHORT
        "count": len(all_indices),
        "type": "SCALAR",
    })
    byte_offset += idx_byte_len
    
    # Update accessor indices in primitives
    for i, prim in enumerate(mesh_primitives):
        prim["attributes"]["POSITION"] = i * 2
        prim["attributes"]["NORMAL"] = i * 2 + 1
        prim["indices"] = i * 2 + 2
    
    # Create materials
    materials = []
    for part in parts:
        color = part.get('color', [1, 1, 1, 1])
        materials.append({
            "pbrMetallicRoughness": {
                "baseColorFactor": color,
                "metallicFactor": 0.1,
                "roughnessFactor": 0.5,
            },
            "doubleSided": True,
        })
    
    # Create nodes
    nodes = []
    for i, part in enumerate(parts):
        node = {
            "mesh": 0,
            "translation": [0, 0, 0],  # Already baked into vertices
        }
        nodes.append(node)
    
    # Build glTF JSON
    gltf = {
        "asset": {"version": "2.0", "generator": "microbit-smartlock-glb-generator"},
        "scene": 0,
        "scenes": [{"nodes": list(range(len(nodes)))}],
        "nodes": nodes,
        "meshes": [{
            "primitives": mesh_primitives,
        }],
        "materials": materials,
        "accessors": accessors,
        "bufferViews": buffer_views,
        "buffers": [{
            "byteLength": byte_offset,
        }],
    }
    
    # Build binary buffer
    buffer_data = bytearray()
    
    # Add vertices
    for v in all_vertices:
        buffer_data.extend(struct.pack('<f', v))
    
    # Pad to 4-byte alignment
    while len(buffer_data) % 4 != 0:
        buffer_data.append(0)
    
    # Add normals
    for n in all_normals:
        buffer_data.extend(struct.pack('<f', n))
    
    # Pad to 4-byte alignment
    while len(buffer_data) % 4 != 0:
        buffer_data.append(0)
    
    # Add indices
    for idx in all_indices:
        buffer_data.extend(struct.pack('<H', idx))
    
    # Pad buffer to 4-byte alignment
    while len(buffer_data) % 4 != 0:
        buffer_data.append(0)
    
    # Create JSON string
    json_str = json.dumps(gltf, separators=(',', ':'))
    # Pad JSON to 4-byte alignment
    while len(json_str) % 4 != 0:
        json_str += ' '
    json_bytes = json_str.encode('utf-8')
    
    # Build GLB file
    glb = bytearray()
    
    # Header (12 bytes)
    glb.extend(struct.pack('<I', 0x46546C67))  # Magic: "glTF"
    glb.extend(struct.pack('<I', 2))  # Version
    total_length = 12 + 8 + len(json_bytes) + 8 + len(buffer_data)
    glb.extend(struct.pack('<I', total_length))
    
    # JSON chunk
    glb.extend(struct.pack('<I', len(json_bytes)))
    glb.extend(struct.pack('<I', 0x4E4F534A))  # Chunk type: "JSON"
    glb.extend(json_bytes)
    
    # BIN chunk
    glb.extend(struct.pack('<I', len(buffer_data)))
    glb.extend(struct.pack('<I', 0x004E4942))  # Chunk type: "BIN\0"
    glb.extend(buffer_data)
    
    # Write file
    with open(output_path, 'wb') as f:
        f.write(glb)
    
    return len(glb)


def main():
    # Define parts with colors (RGBA)
    # Blue: [0.2, 0.4, 0.8, 1.0]
    # Gray: [0.5, 0.5, 0.5, 1.0]
    # Red: [0.8, 0.2, 0.2, 1.0]
    # Silver: [0.8, 0.8, 0.85, 1.0]
    # Green: [0.2, 0.7, 0.3, 1.0]
    
    parts_template = [
        {"type": "cylinder", "radius": 11, "height": 4, "color": [0.2, 0.4, 0.8, 1.0], "name": "servo_mount"},
        {"type": "cylinder", "radius": 4, "height": 2, "color": [0.2, 0.4, 0.8, 1.0], "name": "center_post"},
        {"type": "box", "width": 25, "height": 10, "depth": 4, "color": [0.5, 0.5, 0.5, 1.0], "name": "connection_arm"},
        {"type": "cylinder", "radius": 10, "height": 4, "color": [0.8, 0.2, 0.2, 1.0], "name": "magnet_housing_servo"},
        {"type": "cylinder", "radius": 3, "height": 3, "color": [0.8, 0.8, 0.85, 1.0], "name": "magnet_1"},
        {"type": "cylinder", "radius": 3, "height": 3, "color": [0.8, 0.8, 0.85, 1.0], "name": "magnet_2"},
        {"type": "cylinder", "radius": 10, "height": 4, "color": [0.2, 0.7, 0.3, 1.0], "name": "magnet_housing_thumb"},
        {"type": "box", "width": 8, "height": 6, "depth": 4, "color": [0.2, 0.7, 0.3, 1.0], "name": "thumb_grip"},
    ]
    
    # Assembled positions
    assembled_positions = [
        (0, 0, 0),      # servo_mount
        (0, 0, -1),     # center_post
        (12.5, 0, 0),   # connection_arm
        (25, 0, 2),     # magnet_housing_servo
        (25, 0, 5),     # magnet_1
        (40, 0, 5),     # magnet_2
        (40, 0, 2),     # magnet_housing_thumb
        (45, 0, 1),     # thumb_grip
    ]
    
    # Exploded positions
    exploded_positions = [
        (-30, 0, 0),    # servo_mount
        (-30, 0, -2),   # center_post
        (-5, 0, 0),     # connection_arm
        (20, 0, 0),     # magnet_housing_servo
        (20, 0, 6),     # magnet_1
        (35, 0, 6),     # magnet_2
        (35, 0, 0),     # magnet_housing_thumb
        (48, 0, 0),     # thumb_grip
    ]
    
    # Generate assembled GLB
    assembled_parts = []
    for i, template in enumerate(parts_template):
        part = template.copy()
        part['position'] = assembled_positions[i]
        assembled_parts.append(part)
    
    assembled_path = os.path.join(OUTPUT_DIR, "servo-holder-assembled.glb")
    assembled_size = create_glb(assembled_parts, assembled_path)
    print(f"Created: {assembled_path} ({assembled_size} bytes)")
    
    # Generate exploded GLB
    exploded_parts = []
    for i, template in enumerate(parts_template):
        part = template.copy()
        part['position'] = exploded_positions[i]
        exploded_parts.append(part)
    
    exploded_path = os.path.join(OUTPUT_DIR, "servo-holder-exploded.glb")
    exploded_size = create_glb(exploded_parts, exploded_path)
    print(f"Created: {exploded_path} ({exploded_size} bytes)")
    
    print("\nGLB files generated successfully!")


if __name__ == "__main__":
    main()
