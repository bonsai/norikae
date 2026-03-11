"""
Generate PNG visualization for Micro:bit Smart Lock Servo Holder
Creates orthographic views and isometric view
"""

import struct
import math
import zlib
import os

def create_png(width, height, pixels):
    """Create PNG file from pixel data (list of RGB tuples)"""
    
    def png_chunk(chunk_type, data):
        chunk_len = struct.pack('>I', len(data))
        chunk_crc = struct.pack('>I', zlib.crc32(chunk_type + data) & 0xffffffff)
        return chunk_len + chunk_type + data + chunk_crc
    
    # PNG signature
    signature = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr = png_chunk(b'IHDR', ihdr_data)
    
    # IDAT chunk (image data)
    raw_data = b''
    for y in range(height):
        raw_data += b'\x00'  # Filter type: None
        for x in range(width):
            idx = y * width + x
            r, g, b = pixels[idx]
            raw_data += bytes([r, g, b])
    
    compressed = zlib.compress(raw_data, 9)
    idat = png_chunk(b'IDAT', compressed)
    
    # IEND chunk
    iend = png_chunk(b'IEND', b'')
    
    return signature + ihdr + idat + iend

def create_cylinder_pixels(cx, cy, radius, color, width, height, pixels):
    """Draw filled cylinder (circle from top view)"""
    for y in range(height):
        for x in range(width):
            dx = x - cx
            dy = y - cy
            if dx * dx + dy * dy <= radius * radius:
                idx = y * width + x
                pixels[idx] = color

def create_box_pixels(x, y, w, h, color, width, height, pixels):
    """Draw filled rectangle"""
    for py in range(max(0, y), min(height, y + h)):
        for px in range(max(0, x), min(width, x + w)):
            pixels[py * width + px] = color

def create_isometric_view():
    """Create isometric view of the assembly"""
    width, height = 800, 600
    pixels = [(245, 245, 250)] * (width * height)  # Light gray background
    
    # Colors
    blue = (60, 100, 200)
    gray = (80, 80, 80)
    red = (200, 80, 80)
    green = (80, 200, 80)
    silver = (180, 180, 180)
    
    # Isometric projection helper
    def iso_x(x, y, z):
        return int(400 + (x - y) * 0.866)
    
    def iso_y(x, y, z):
        return int(300 + (x + y) * 0.5 - z)
    
    # Draw parts (back to front order)
    parts = [
        # (x, y, z, size_x, size_y, size_z, color, name)
        (0, 0, 0, 22, 22, 4, blue, "Servo Mount"),
        (0, 0, -1, 8, 8, 2, blue, "Center Post"),
        (12.5, 0, 0, 25, 10, 4, gray, "Connection Arm"),
        (25, 0, 2, 20, 20, 4, red, "Magnet Housing (Servo)"),
        (25, 0, 5, 6, 6, 3, silver, "Magnet 1"),
        (40, 0, 5, 6, 6, 3, silver, "Magnet 2"),
        (40, 0, 2, 20, 20, 4, green, "Magnet Housing (Thumb)"),
        (45, 0, 1, 8, 6, 4, green, "Thumb Grip"),
    ]
    
    # Simple isometric boxes
    for px, py, pz, sx, sy, sz, color, name in parts:
        # Project corners
        corners = [
            (px - sx/2, py - sy/2, pz),
            (px + sx/2, py - sy/2, pz),
            (px + sx/2, py + sy/2, pz),
            (px - sx/2, py + sy/2, pz),
            (px - sx/2, py - sy/2, pz + sz),
            (px + sx/2, py - sy/2, pz + sz),
            (px + sx/2, py + sy/2, pz + sz),
            (px - sx/2, py + sy/2, pz + sz),
        ]
        
        projected = [(iso_x(x, y, z), iso_y(x, y, z)) for x, y, z in corners]
        
        # Draw top face (filled polygon - simplified as rectangle)
        min_x = min(p[0] for p in projected[:4])
        max_x = max(p[0] for p in projected[:4])
        min_y = min(p[1] for p in projected[:4])
        max_y = max(p[1] for p in projected[:4])
        
        # Draw simple representation
        cx, cy = iso_x(px, py, pz + sz/2), iso_y(px, py, pz + sz/2)
        size = int(max(sx, sy) * 0.7)
        
        for y in range(max(0, cy - size), min(height, cy + size)):
            for x in range(max(0, cx - size), min(width, cx + size)):
                dx = x - cx
                dy = y - cy
                if dx * dx * 0.5 + dy * dy <= size * size:
                    idx = y * width + x
                    # Add shading based on position
                    r, g, b = color
                    shade = 1.0 - (y - (cy - size)) / (2 * size) * 0.3
                    pixels[idx] = (int(r * shade), int(g * shade), int(b * shade))
    
    return pixels, width, height

def create_exploded_view():
    """Create exploded view (parts separated along X axis)"""
    width, height = 900, 400
    pixels = [(245, 245, 250)] * (width * height)
    
    # Colors
    blue = (60, 100, 200)
    gray = (80, 80, 80)
    red = (200, 80, 80)
    green = (80, 200, 80)
    silver = (180, 180, 180)
    
    # Parts with exploded positions
    parts = [
        (-30, 0, 0, 22, 22, 4, blue, "Servo Mount"),
        (-30, 0, -2, 8, 8, 2, blue, "Center Post"),
        (-5, 0, 0, 25, 10, 4, gray, "Connection Arm"),
        (20, 0, 0, 20, 20, 4, red, "Magnet Housing (S)"),
        (20, 0, 6, 6, 6, 3, silver, "Magnet 1"),
        (35, 0, 6, 6, 6, 3, silver, "Magnet 2"),
        (35, 0, 0, 20, 20, 4, green, "Magnet Housing (T)"),
        (48, 0, 0, 8, 6, 4, green, "Thumb Grip"),
    ]
    
    offset_x = 100
    scale = 8
    
    for px, py, pz, sx, sy, sz, color, name in parts:
        cx = int(offset_x + px * scale)
        cy = int(height / 2 - pz * scale)
        w = int(sx * scale)
        h = int(sy * scale)
        
        # Draw 3D-like box
        # Top face (lighter)
        for y in range(max(0, cy - h), min(height, cy)):
            for x in range(max(0, cx - w), min(width, cx + w)):
                idx = y * width + x
                r, g, b = color
                pixels[idx] = (min(255, int(r * 1.2)), min(255, int(g * 1.2)), min(255, int(b * 1.2)))
        
        # Front face
        for y in range(max(0, cy), min(height, cy + int(sz * scale))):
            for x in range(max(0, cx - w), min(width, cx + w)):
                idx = y * width + x
                pixels[idx] = color
        
        # Side face (darker)
        for y in range(max(0, cy - h), min(height, cy + int(sz * scale))):
            for x in range(max(0, cx + w), min(width, cx + w + int(sz * scale))):
                idx = y * width + x
                r, g, b = color
                pixels[idx] = (int(r * 0.7), int(g * 0.7), int(b * 0.7))
    
    return pixels, width, height

def create_orthographic_views():
    """Create orthographic projections (top, front, side)"""
    width, height = 1000, 700
    pixels = [(245, 245, 250)] * (width * height)
    
    # Colors
    outline = (50, 50, 50)
    blue = (60, 100, 200)
    gray = (80, 80, 80)
    red = (200, 80, 80)
    green = (80, 200, 80)
    silver = (180, 180, 180)
    
    scale = 10
    margin = 50
    
    def draw_circle(cx, cy, radius, color, thickness=2):
        for angle in range(0, 360):
            rad = math.radians(angle)
            x = int(cx + radius * math.cos(rad))
            y = int(cy + radius * math.sin(rad))
            for t in range(-thickness//2, thickness//2):
                for dy in range(-thickness//2, thickness//2):
                    if 0 <= x+t < width and 0 <= y+dy < height:
                        pixels[(y+dy) * width + (x+t)] = color
    
    def draw_filled_circle(cx, cy, radius, color):
        for y in range(int(cy - radius), int(cy + radius)):
            for x in range(int(cx - radius), int(cx + radius)):
                if (x - cx)**2 + **(y - cy)2 <= radius**2:
                    if 0 <= x < width and 0 <= y < height:
                        pixels[y * width + x] = color
    
    def draw_rect(x, y, w, h, color, filled=True):
        if filled:
            for py in range(max(0, y), min(height, y + h)):
                for px in range(max(0, x), min(width, x + w)):
                    pixels[py * width + px] = color
        else:
            for px in range(x, x + w):
                if 0 <= px < width:
                    pixels[y * width + px] = color
                    pixels[(y + h - 1) * width + px] = color
            for py in range(y, y + h):
                if 0 <= py < height:
                    pixels[py * width + x] = color
                    pixels[py * width + (x + w - 1)] = color
    
    # TOP VIEW (left)
    top_label = "TOP VIEW"
    for i, c in enumerate(top_label):
        # Simple text placeholder (just colored area)
        pass
    
    top_parts = [
        (150, 350, 22*scale, 22*scale, blue),    # Servo mount
        (150, 350, 8*scale, 8*scale, blue),      # Center post
        (150 + 12.5*scale, 350, 25*scale, 10*scale, gray),  # Arm
        (150 + 25*scale, 350, 20*scale, 20*scale, red),     # Magnet housing S
        (150 + 25*scale, 350, 6*scale, 6*scale, silver),    # Magnet 1
        (150 + 40*scale, 350, 6*scale, 6*scale, silver),    # Magnet 2
        (150 + 40*scale, 350, 20*scale, 20*scale, green),   # Magnet housing T
        (150 + 45*scale, 350, 8*scale, 6*scale, green),     # Thumb grip
    ]
    
    # Draw top view label background
    draw_rect(50, 50, 200, 40, (200, 200, 200))
    
    for x, y, w, h, color in top_parts:
        draw_filled_circle(x, y, min(w, h)/2, color)
    
    # FRONT VIEW (center)
    draw_rect(400, 50, 250, 40, (200, 200, 200))
    
    front_parts = [
        (500, 350, 22*scale, 4*scale, blue),     # Servo mount
        (500, 350-10*scale, 8*scale, 2*scale, blue),  # Center post
        (500 + 12.5*scale, 350, 25*scale, 4*scale, gray),  # Arm
        (500 + 25*scale, 350 + 20, 20*scale, 4*scale, red),
        (500 + 25*scale, 350 + 50, 6*scale, 3*scale, silver),
        (500 + 40*scale, 350 + 50, 6*scale, 3*scale, silver),
        (500 + 40*scale, 350 + 20, 20*scale, 4*scale, green),
        (500 + 45*scale, 350 + 10, 8*scale, 4*scale, green),
    ]
    
    for x, y, w, h, color in front_parts:
        draw_rect(int(x), int(y), int(w), int(h), color)
    
    # SIDE VIEW (right)
    draw_rect(750, 50, 200, 40, (200, 200, 200))
    
    side_parts = [
        (850, 350, 22*scale, 4*scale, blue),
        (850, 350-10*scale, 8*scale, 2*scale, blue),
        (850, 350, 25*scale, 4*scale, gray),
        (850, 350 + 20, 20*scale, 4*scale, red),
        (850, 350 + 50, 6*scale, 3*scale, silver),
        (850, 350 + 20, 20*scale, 4*scale, green),
    ]
    
    for x, y, w, h, color in side_parts:
        draw_rect(int(x), int(y), int(w), int(h), color)
    
    # Add dimension lines
    dimension_color = (100, 100, 100)
    
    # Overall length dimension
    y_dim = 500
    draw_rect(150, y_dim, 400, 2, dimension_color)
    draw_rect(150, y_dim - 10, 2, 10, dimension_color)
    draw_rect(550, y_dim - 10, 2, 10, dimension_color)
    
    return pixels, width, height

def create_dimensions_diagram():
    """Create dimensioned technical drawing"""
    width, height = 1200, 800
    pixels = [(250, 250, 255)] * (width * height)
    
    # Colors
    black = (30, 30, 30)
    blue = (60, 100, 200)
    gray = (80, 80, 80)
    red = (200, 80, 80)
    green = (80, 200, 80)
    silver = (180, 180, 180)
    dimension = (100, 100, 100)
    
    scale = 12
    base_x, base_y = 100, 400
    
    def draw_line(x1, y1, x2, y2, color, thickness=2):
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        for i in range(steps):
            x = int(x1 + dx * i / steps)
            y = int(y1 + dy * i / steps)
            for t in range(-thickness//2, thickness//2+1):
                for tt in range(-thickness//2, thickness//2+1):
                    if 0 <= x+t < width and 0 <= y+tt < height:
                        pixels[(y+tt) * width + (x+t)] = color
    
    def draw_filled_rect(x, y, w, h, color):
        for py in range(max(0, y), min(height, y + h)):
            for px in range(max(0, x), min(width, x + w)):
                pixels[py * width + px] = color
    
    def draw_text_bg(x, y, text, color):
        # Simple colored background for text
        draw_filled_rect(x, y, len(text) * 12, 20, color)
    
    # Title
    draw_filled_rect(50, 30, 500, 50, (40, 60, 100))
    
    # Draw main assembly (front view)
    parts = [
        (base_x, base_y, 22*scale, 4*scale, blue, "Servo Mount"),
        (base_x, base_y - 10*scale, 8*scale, 2*scale, blue, "Center Post"),
        (base_x + 12.5*scale, base_y, 25*scale, 4*scale, gray, "Arm"),
        (base_x + 25*scale, base_y + 20, 20*scale, 4*scale, red, "Magnet Housing (S)"),
        (base_x + 25*scale, base_y + 50, 6*scale, 3*scale, silver, "Magnet"),
        (base_x + 40*scale, base_y + 50, 6*scale, 3*scale, silver, "Magnet"),
        (base_x + 40*scale, base_y + 20, 20*scale, 4*scale, green, "Magnet Housing (T)"),
        (base_x + 45*scale, base_y + 10, 8*scale, 4*scale, green, "Thumb Grip"),
    ]
    
    for x, y, w, h, color, name in parts:
        draw_filled_rect(int(x), int(y), int(w), int(h), color)
    
    # Dimension lines
    # Overall length
    dim_y = base_y + 150
    draw_line(base_x, dim_y, base_x + 53*scale, dim_y, dimension)
    draw_line(base_x, dim_y - 10, base_x, dim_y + 10, dimension)
    draw_line(base_x + 53*scale, dim_y - 10, base_x + 53*scale, dim_y + 10, dimension)
    
    # Parts list (right side)
    parts_list_x = 800
    parts_list_y = 150
    
    part_colors = [blue, blue, gray, red, silver, silver, green, green]
    part_names = ["Servo Mount (22mm dia)", "Center Post (8mm dia)", 
                  "Connection Arm (25x10mm)", "Magnet Housing - Servo Side",
                  "Neodymium Magnet 6x3mm", "Neodymium Magnet 6x3mm",
                  "Magnet Housing - Thumb Side", "Thumb Grip"]
    
    for i, (color, name) in enumerate(zip(part_colors, part_names)):
        y = parts_list_y + i * 35
        draw_filled_rect(parts_list_x, y, 30, 25, color)
        # Text background
        draw_filled_rect(parts_list_x + 40, y + 5, len(name) * 10, 20, (240, 240, 240))
    
    # Key dimensions callout
    callout_x = 800
    callout_y = 450
    draw_filled_rect(callout_x, callout_y, 350, 200, (240, 245, 250))
    draw_filled_rect(callout_x, callout_y, 350, 40, (40, 60, 100))
    
    dimensions = [
        "KEY DIMENSIONS:",
        "Servo Mount: 22mm diameter",
        "Magnet: 6mm diameter x 3mm",
        "Arm Length: 25mm",
        "Material: PLA/PETG",
        "Layer Height: 0.2mm",
        "Infill: 100%",
    ]
    
    return pixels, width, height

if __name__ == "__main__":
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("Generating PNG visualizations...")
    print()
    
    # Isometric view
    print("1. Creating isometric view...")
    pixels, w, h = create_isometric_view()
    png_data = create_png(w, h, pixels)
    with open(os.path.join(output_dir, "servo-holder-isometric.png"), 'wb') as f:
        f.write(png_data)
    print(f"   Created: servo-holder-isometric.png ({w}x{h})")
    
    # Exploded view
    print("2. Creating exploded view...")
    pixels, w, h = create_exploded_view()
    png_data = create_png(w, h, pixels)
    with open(os.path.join(output_dir, "servo-holder-exploded.png"), 'wb') as f:
        f.write(png_data)
    print(f"   Created: servo-holder-exploded.png ({w}x{h})")
    
    # Orthographic views
    print("3. Creating orthographic views...")
    pixels, w, h = create_orthographic_views()
    png_data = create_png(w, h, pixels)
    with open(os.path.join(output_dir, "servo-holder-orthographic.png"), 'wb') as f:
        f.write(png_data)
    print(f"   Created: servo-holder-orthographic.png ({w}x{h})")
    
    # Dimensions diagram
    print("4. Creating dimensions diagram...")
    pixels, w, h = create_dimensions_diagram()
    png_data = create_png(w, h, pixels)
    with open(os.path.join(output_dir, "servo-holder-dimensions.png"), 'wb') as f:
        f.write(png_data)
    print(f"   Created: servo-holder-dimensions.png ({w}x{h})")
    
    print()
    print("All PNG files created successfully!")
    print()
    print("Files created:")
    print("  - servo-holder-isometric.png (3D view)")
    print("  - servo-holder-exploded.png (parts separated)")
    print("  - servo-holder-orthographic.png (top/front/side views)")
    print("  - servo-holder-dimensions.png (technical drawing)")
