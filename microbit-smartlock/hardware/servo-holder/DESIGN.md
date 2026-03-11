# Servo Holder Design for Micro:bit Smart Lock

## Overview
This design focuses on a **magnetic coupling mechanism** that allows manual override without damaging the servo gears - critical for UX synchronization.

## Design Philosophy
- **UX Priority**: Family members can still use physical key normally
- **Safety**: Servo doesn't break when manually operated
- **Reliability**: Strong enough torque to turn typical thumb-turns

---

## Mechanism Types

### Type A: Magnetic Coupling (Recommended)

```
┌─────────────────────────────────────────────────────────┐
│                    DOOR SURFACE                         │
│  ┌─────────┐     ┌─────────────┐     ┌─────────────┐   │
│  │  Servo  │────▶│  Magnet A   │ ◯ │  Magnet B   │──▶│ Thumb-turn │
│  │ (fixed) │     │ (on servo)  │ ◯ │ (on holder) │   │            │
│  └─────────┘     └─────────────┘     └─────────────┘   │
│                         │                    │          │
│                    [Air Gap]              [Fixed]       │
│                        2-3mm                            │
└─────────────────────────────────────────────────────────┘
```

**How it works:**
1. Servo rotates Magnet A
2. Magnetic force transfers rotation to Magnet B
3. When manual force is applied, magnets slip (clutch effect)
4. No gear damage from manual operation

**Parts needed:**
- Neodymium magnets: 6mm diameter × 3mm thick × 2 pieces
- Servo horn (standard MG90S type)
- PLA/PETG filament or 3mm acrylic

---

### Type B: U-Slot Coupler (Simple)

```
┌─────────────────────────────────────────────────────────┐
│                    DOOR SURFACE                         │
│  ┌─────────┐     ┌─────────────────┐     ┌─────────┐   │
│  │  Servo  │────▶│   U-shaped      │────▶│Thumb-turn│   │
│  │         │     │   slot (play)   │     │         │   │
│  └─────────┘     │   ╔═══════╗     │     └─────────┘   │
│                  │   ║       ║     │                   │
│                  │   ╚═══════╝     │                   │
│                  └─────────────────┘                   │
│                      [3mm play each side]              │
└─────────────────────────────────────────────────────────┘
```

**How it works:**
1. U-slot has intentional "play" (looseness)
2. Servo rotates within the slot range
3. Manual operation moves freely within slot
4. Simple to make with basic materials

---

## 3D Print Files

### Type A: Magnetic Coupler (OpenSCAD)

```openscad
// microbit-smartlock-servo-holder.scad
// Magnetic coupling servo holder for MG90S

$fn = 50;

// Parameters
magnet_diameter = 6.5;  // Slightly larger than 6mm magnet
magnet_thickness = 3;
servo_horn_hole = 5.5;  // MG90S spline size
holder_thickness = 4;
distance_to_door = 15;  // mm from servo center to door surface

// Servo horn mount
module servo_mount() {
    difference() {
        cylinder(h = holder_thickness, d = 20);
        cylinder(h = holder_thickness + 2, d = servo_horn_hole);
        // Spline for MG90S
        for(i = [0:24]) {
            rotate([0, 0, i * 15])
            translate([3, 0, -1])
            cube([2, 1, holder_thickness + 4], center = true);
        }
    }
}

// Magnet housing (servo side)
module magnet_housing_servo() {
    difference() {
        cylinder(h = magnet_thickness + 2, d = 18);
        cylinder(h = magnet_thickness + 4, d = magnet_diameter);
        // Screw holes for mounting
        for(i = [0, 180]) {
            rotate([0, 0, i])
            translate([12, 0, -1])
            cylinder(h = magnet_thickness + 6, d = 2.5);
        }
    }
}

// Magnet housing (door side)
module magnet_housing_door() {
    difference() {
        cylinder(h = magnet_thickness + 2, d = 18);
        cylinder(h = magnet_thickness + 4, d = magnet_diameter);
        // Thumb-turn attachment (adjust to your lock)
        translate([0, 0, -2])
        cube([10, 6, magnet_thickness + 6], center = true);
    }
}

// Connection arm
module connection_arm() {
    translate([0, 0, holder_thickness/2])
    difference() {
        cube([25, 8, holder_thickness], center = true);
        // Weight reduction slots
        translate([0, 0, 1])
        cube([20, 4, holder_thickness + 2], center = true);
    }
}

// Assemble
translate([0, 0, 0]) servo_mount();
translate([0, 0, holder_thickness + 5]) magnet_housing_servo();
translate([30, 0, holder_thickness + 5]) magnet_housing_door();
translate([15, 0, holder_thickness/2]) connection_arm();
```

---

### Type B: U-Slot Coupler (Fusion 360 Sketch)

**Dimensions for typical thumb-turn (10mm × 6mm):**
- U-slot width: 12mm (1mm clearance each side)
- U-slot depth: 15mm
- Arm length: 20-30mm (adjustable)
- Material thickness: 4mm minimum

**Laser cut template (3mm acrylic × 3 layers):**
```
Layer 1: Base plate with servo mounting holes
Layer 2: U-slot spacer (creates the play gap)
Layer 3: Top plate with thumb-turn grip
```

---

## Installation Guide

### Step 1: Measure Your Thumb-turn
```
┌──────────────────┐
│   Thumb-turn     │
│   dimensions:    │
│   Width:  ___mm  │
│   Height: ___mm  │
│   Depth:  ___mm  │
└──────────────────┘
```

### Step 2: Print/Assemble Holder
- Print with 100% infill for strength
- Use PETG for durability (PLA can become brittle)
- Test fit before final installation

### Step 3: Install Servo
1. Mount MG90S servo to door frame using double-sided tape (Command strips recommended)
2. Attach servo horn with magnet/coupler
3. Align with thumb-turn

### Step 4: Test Manual Override
- Turn thumb-turn by hand - should slip/move freely
- Run servo - should turn thumb-turn reliably

---

## UX Considerations Built Into Design

| UX Requirement | Mechanical Solution |
|----------------|---------------------|
| Family can use normally | Magnetic slip / U-slot play |
| No damage from manual use | Clutch mechanism |
| Reliable operation | 100% infill, metal gears servo |
| Easy installation | Command strips, no drilling |
| Visual feedback | Micro:bit LED visible through holder |

---

## Parts Shopping List

| Item | Specification | Qty | Notes |
|------|---------------|-----|-------|
| Servo | MG90S (metal gear) | 1 | Torque: 2.5kgf·cm min |
| Magnets | Neodymium N52, 6×3mm | 2 | For magnetic coupling |
| Filament | PETG or PLA+ | 50g | Black or match door color |
| Mounting | Command strips large | 2 sets | Removable, no damage |
| Power | AA battery box 4× | 1 | Separate from Micro:bit |
| Wires | Jumper wires F-F | 3 | Servo connections |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Servo can't turn lock | Increase torque (better servo) or reduce friction |
| Manual operation stiff | Increase air gap or magnet distance |
| Coupler falls off | Add retention ring or increase friction fit |
| Battery drains fast | Use separate servo power supply |

---

## Next Steps

1. **Download OpenSCAD** (free): https://www.openscad.org/
2. **Copy the code above** and adjust dimensions for your lock
3. **Export as STL** and 3D print
4. **Test fit** before final installation

For laser cut users: I can create DXF files - let me know your thumb-turn dimensions!
