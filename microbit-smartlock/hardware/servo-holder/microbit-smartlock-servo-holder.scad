// microbit-smartlock-servo-holder.scad
// Magnetic coupling servo holder for MG90S servo
// Micro:bit Smart Lock Project
//
// Usage: 
// 1. Open in OpenSCAD (https://www.openscad.org/)
// 2. Adjust parameters below for your lock
// 3. Press F5 to preview, F6 to render
// 4. Export as STL for 3D printing

// ==================== PARAMETERS ====================
// Adjust these values for your specific lock

// Magnet specifications (Neodymium N52 recommended)
magnet_diameter = 6.5;  // mm (0.5mm clearance for 6mm magnet)
magnet_thickness = 3;   // mm
magnet_housing_depth = 3.5; // mm (slightly less than magnet thickness for tight fit)

// Servo specifications (MG90S / SG90)
servo_spline_diameter = 5.5;  // mm (MG90S spline size)
servo_spline_teeth = 24;      // Number of spline teeth
servo_mount_thickness = 4;    // mm (base plate thickness)

// Arm specifications
arm_length = 25;      // mm (servo to thumb-turn distance)
arm_width = 10;       // mm
arm_thickness = 4;    // mm

// Thumb-turn grip specifications (ADJUST FOR YOUR LOCK!)
thumb_turn_width = 10;   // mm (measure your lock)
thumb_turn_height = 6;   // mm (measure your lock)
grip_clearance = 1;      // mm (gap between grip and thumb-turn)

// Print settings
print_nozzle = 0.4;  // mm (for wall thickness optimization)
layer_height = 0.2;  // mm

// ==================== MODULES ====================

// MG90S servo spline mount
module servo_spline_mount() {
    difference() {
        // Base disk
        cylinder(h = servo_mount_thickness, d = 22, $fn = 60);
        
        // Spline hole (24 teeth for MG90S)
        cylinder(h = servo_mount_thickness + 2, d = servo_spline_diameter, $fn = 60);
        
        // Spline teeth cutout
        for(i = [0 : 360/servo_spline_teeth : 359]) {
            rotate([0, 0, i])
            translate([servo_spline_diameter/2 - 0.3, -0.5, -1])
            cube([1.5, 1, servo_mount_thickness + 4]);
        }
        
        // Mounting screw holes (optional, for M2 screws)
        for(i = [0, 120, 240]) {
            rotate([0, 0, i])
            translate([16, 0, -1])
            cylinder(h = servo_mount_thickness + 4, d = 2.2, $fn = 20);
        }
    }
    
    // Center post for alignment
    cylinder(h = 2, d = 8, $fn = 30);
}

// Magnet housing (servo side - rotating part)
module magnet_housing_servo() {
    difference() {
        // Main body
        cylinder(h = magnet_thickness + 1, d = 20, $fn = 60);
        
        // Magnet cavity
        cylinder(h = magnet_housing_depth, d = magnet_diameter, $fn = 30);
        
        // Polarity indicator (small notch)
        rotate([0, 0, 0])
        translate([8, -1, -1])
        cube([4, 2, magnet_housing_depth + 2]);
        
        // Weight reduction (optional)
        cylinder(h = magnet_thickness + 3, d = 12, $fn = 30);
    }
    
    // Rim to hold magnet in place
    difference() {
        cylinder(h = 1.5, d = 20, $fn = 60);
        cylinder(h = 2, d = magnet_diameter - 1, $fn = 30);
    }
}

// Magnet housing (thumb-turn side - fixed part)
module magnet_housing_thumbturn() {
    difference() {
        // Main body
        cylinder(h = magnet_thickness + 1, d = 20, $fn = 60);
        
        // Magnet cavity
        cylinder(h = magnet_housing_depth, d = magnet_diameter, $fn = 30);
        
        // Polarity indicator
        rotate([0, 0, 0])
        translate([8, -1, -1])
        cube([4, 2, magnet_housing_depth + 2]);
        
        // Thumb-turn grip slot (rectangular)
        translate([-(thumb_turn_width + grip_clearance)/2, 
                   -(thumb_turn_height + grip_clearance)/2, 
                   -2])
        cube([thumb_turn_width + grip_clearance, 
              thumb_turn_height + grip_clearance, 
              magnet_thickness + 4]);
    }
    
    // Rim to hold magnet
    difference() {
        cylinder(h = 1.5, d = 20, $fn = 60);
        cylinder(h = 2, d = magnet_diameter - 1, $fn = 30);
    }
    
    // Grip texture (ridges for better hold)
    for(i = [-5 : 2 : 5]) {
        translate([i, thumb_turn_height/2 + grip_clearance/2 + 1, 0])
        cube([0.5, 2, magnet_thickness + 1]);
    }
}

// Connection arm (connects servo to magnet housing)
module connection_arm() {
    length = arm_length;
    width = arm_width;
    thickness = arm_thickness;
    
    difference() {
        // Main arm body
        hull() {
            cylinder(h = thickness, d = width, $fn = 30);
            translate([length, 0, 0])
            cylinder(h = thickness, d = width, $fn = 30);
        }
        
        // Weight reduction slots
        translate([length/2, 0, -1])
        cube([length - 10, width - 4, thickness + 2], center = true);
        
        // Mounting holes (for M2 screws or servo horn screws)
        translate([2, 0, -1])
        cylinder(h = thickness + 4, d = 2.2, $fn = 20);
        
        translate([length - 2, 0, -1])
        cylinder(h = thickness + 4, d = 2.2, $fn = 20);
    }
}

// Complete assembly (for visualization)
module full_assembly() {
    // Servo mount at origin
    color("blue")
    servo_spline_mount();
    
    // Connection arm
    color("gray")
    translate([0, servo_mount_thickness/2, 0])
    rotate([90, 0, 0])
    connection_arm();
    
    // Servo-side magnet housing
    color("red")
    translate([arm_length, 0, servo_mount_thickness + magnet_thickness + 1])
    rotate([180, 0, 0])
    magnet_housing_servo();
    
    // Thumb-turn side magnet housing (showing separation)
    color("green")
    translate([arm_length + 15, 0, servo_mount_thickness + magnet_thickness + 1])
    rotate([180, 0, 0])
    magnet_housing_thumbturn();
    
    // Magnets (visualization only)
    color("silver")
    translate([arm_length, 0, servo_mount_thickness + 2])
    cylinder(h = magnet_thickness, d = magnet_diameter - 0.5, $fn = 30);
    
    color("silver")
    translate([arm_length + 15, 0, servo_mount_thickness + 2])
    cylinder(h = magnet_thickness, d = magnet_diameter - 0.5, $fn = 30);
}

// ==================== EXPORT OPTIONS ====================

// Uncomment ONE of the following lines to export:

// Full assembly (for visualization only - don't print this)
// full_assembly();

// Individual parts for printing:

// Servo mount
translate([-30, 0, 0])
servo_spline_mount();

// Connection arm
translate([0, 0, 0])
connection_arm();

// Magnet housing (servo side)
translate([30, 0, 0])
magnet_housing_servo();

// Magnet housing (thumb-turn side)
translate([60, 0, 0])
magnet_housing_thumbturn();

// ==================== NOTES ====================
/*
Printing Instructions:
1. Print all parts in PETG or PLA+ for durability
2. Use 100% infill for strength (especially the arm)
3. Orient flat side down for best bed adhesion
4. Support material not required for this design

Assembly Instructions:
1. Press magnets into housings (note polarity!)
2. Attach servo mount to MG90S servo horn
3. Connect arm to servo mount
4. Attach magnet housing to other end of arm
5. Position servo on door frame
6. Align thumb-turn housing with your lock
7. Test magnetic coupling (should slip when manually turned)

Safety Notes:
- Neodymium magnets are brittle - handle carefully
- Keep magnets away from electronics and credit cards
- Test manual override before final installation
*/
