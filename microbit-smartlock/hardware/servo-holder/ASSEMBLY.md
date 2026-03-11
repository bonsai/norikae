# Assembly Instructions - Micro:bit Smart Lock Servo Holder
# Complete Guide with UX Considerations

---

## 📦 Before You Start

### Check Your Parts
- [ ] MG90S (or SG90) servo motor
- [ ] Micro:bit v2 board
- [ ] Neodymium magnets (6mm × 3mm) × 2 pieces
- [ ] 3D printed or laser-cut holder parts
- [ ] M2 screws (6mm length) × 4
- [ ] Servo horn (standard, comes with servo)
- [ ] Double-sided tape (Command strips recommended)
- [ ] Jumper wires (female-to-female) × 3
- [ ] AA battery box (4× AA) with JST connector

### Tools Needed
- [ ] Small Phillips screwdriver
- [ ] Sandpaper (220 grit)
- [ ] Rubbing alcohol (for cleaning surfaces)
- [ ] Ruler or caliper
- [ ] Marker pencil

---

## 🔧 Step 1: Prepare the Servo Holder

### For 3D Printed Parts:
1. **Remove support material** (if any)
   - Use flush cutters or hobby knife
   - Be careful around magnet holes

2. **Test fit magnets**
   - Press magnet into housing
   - Should fit snugly (not too loose, not too tight)
   - If too tight: sand inside of hole
   - If too loose: add a drop of super glue

3. **Smooth contact surfaces**
   - Lightly sand surfaces that touch each other
   - This ensures good magnetic coupling

### For Laser-Cut Parts:
1. **Deburr all edges**
   - Sand cut edges with 220 grit sandpaper
   - Acrylic edges should be smooth, not sharp

2. **Test layer alignment**
   - Stack all 3 layers
   - Ensure screw holes align
   - Check U-slot is clear of obstructions

3. **Clean surfaces**
   - Wipe with rubbing alcohol
   - Remove any protective film (if acrylic)

---

## 🔧 Step 2: Install Magnets (CRITICAL STEP)

### ⚠️ Safety Warning
Neodymium magnets are powerful and brittle:
- Keep away from electronics (including Micro:bit!)
- Keep away from credit cards and magnetic strips
- Wear eye protection (they can shatter if they snap together)
- Keep away from children and pets

### Polarity Marking:
```
    ┌─────────────┐
    │   Housing   │
    │  ╔═══════╗  │
    │  ║  N ↑  ║  │  ← North pole facing UP
    │  ╚═══════╝  │
    └─────────────┘
    
    ┌─────────────┐
    │   Housing   │
    │  ╔═══════╗  │
    │  ║  S ↑  ║  │  ← South pole facing UP
    │  ╚═══════╝  │
    └─────────────┘
```

### Installation:
1. **Mark polarity** on both magnet housings with a marker
   - Both magnets must have SAME pole facing each other
   - This creates repulsion = spring-loaded coupling

2. **Insert first magnet** (servo side)
   - North pole facing outward (toward other magnet)
   - Press gently until flush with housing rim

3. **Insert second magnet** (thumb-turn side)
   - North pole facing outward (toward first magnet)
   - The magnets should REPEL each other when aligned

4. **Test magnetic coupling**
   - Bring both housings close (2-3mm gap)
   - Feel the magnetic resistance
   - Rotate one - the other should follow

---

## 🔧 Step 3: Assemble the Holder

### 3D Print Version:
1. **Attach arm to servo mount**
   - Use M2 screws (don't overtighten)
   - Arm should be firmly attached, not loose

2. **Attach magnet housing (servo side)**
   - Screw into other end of arm
   - Ensure magnet faces away from arm

3. **Check alignment**
   - All parts should be in same plane
   - No twisting or bending

### Laser Cut Version:
1. **Stack layers in order**
   - Layer 1 (base with servo hole) - bottom
   - Layer 2 (U-slot spacer) - middle
   - Layer 3 (top with grip) - top

2. **Insert screws**
   - M2 screws from bottom
   - Add nuts on top
   - Tighten evenly (acrylic cracks if overtightened)

3. **Verify U-slot movement**
   - Thumb-turn should slide in U-slot freely
   - About 1mm play on each side is ideal

---

## 🔧 Step 4: Mount to Servo

1. **Select correct servo horn**
   - Use the straight arm (single arm) horn
   - Remove other horns (save for later)

2. **Attach holder to servo horn**
   - Align center holes
   - Use smallest screw (comes with servo)
   - Don't overtighten - servo shaft is delicate

3. **Check rotation**
   - Servo should rotate 0° to 90° freely
   - Holder should not hit servo body

---

## 🔧 Step 5: Install on Door

### Positioning (UX Critical!)

```
    DOOR FRAME (side view)
    
    ┌─────────────────────────────────────┐
    │                                     │
    │    Servo                            │
    │    ┌───┐                            │
    │    │███│ ← Mount here               │
    │    └─┬─┘                            │
    │      │ Arm                          │
    │      └──────────┐                   │
    │                 │ Thumb-turn        │
    │              ┌──┴──┐                │
    │              │ LOCK│                │
    │              └─────┘                │
    │                                     │
    └─────────────────────────────────────┘
    
    ✓ Good: Servo mounted on door frame (stationary)
    ✗ Bad: Servo mounted on door (moves with door)
```

### Mounting Steps:

1. **Clean mounting surface**
   - Wipe door frame with rubbing alcohol
   - Let dry completely (1 minute)

2. **Apply Command strips**
   - Cut to size if needed
   - Apply to servo bottom
   - Press firmly for 30 seconds

3. **Position servo**
   - Align arm with thumb-turn
   - Ensure 90° rotation covers lock/unlock positions
   - Mark position with pencil before final attachment

4. **Wait before use**
   - Command strips need 1 hour to fully bond
   - Don't operate servo during this time

---

## 🔧 Step 6: Wire Connections

### Wiring Diagram:
```
    Micro:bit          Servo (MG90S)
    ┌─────────┐        ┌──────────┐
    │         │        │          │
    │   P0    │────────│ Orange   │  Signal
    │         │        │          │
    │   3V    │────────│ Red      │  Power*
    │         │        │          │
    │   GND   │────────│ Brown    │  Ground
    │         │        │          │
    └─────────┘        └──────────┘
    
    * For AA battery box:
      - Red wire → Servo Red (VCC)
      - Black wire → Servo Brown (GND)
      - Connect Micro:bit GND to battery GND (common ground)
```

### Important Power Notes:
- **Servos draw high current** (up to 500mA when moving)
- **Micro:bit 3V pin cannot supply enough power**
- **Use separate battery box for servo**
- **Connect grounds together** (common ground required)

---

## 🔧 Step 7: Test and Calibrate

### Manual Override Test (UX Critical):
1. **Power off servo**
2. **Try to turn thumb-turn by hand**
   - Should turn freely (magnetic slip or U-slot play)
   - Should NOT feel binding or resistance
   - If stiff: check alignment, increase clearance

3. **Turn thumb-turn fully**
   - Lock should operate smoothly
   - Holder should move with thumb-turn (not fight it)

### Servo Operation Test:
1. **Upload test program** (see below)
2. **Press A button** → servo rotates to 0° (unlock)
3. **Press B button** → servo rotates to 90° (lock)
4. **Listen for binding**
   - Smooth whirring = good
   - Grinding/stalling = bad (check alignment)

### Test Program (MakeCode):
```javascript
// Basic servo test
radio.setGroup(1)

basic.showIcon(IconNames.Happy)

input.onButtonPressed(Button.A, function () {
    pins.servoWritePin(AnalogPin.P0, 0)
    basic.showIcon(IconNames.Yes)
})

input.onButtonPressed(Button.B, function () {
    pins.servoWritePin(AnalogPin.P0, 90)
    basic.showIcon(IconNames.No)
})
```

---

## 🎯 UX Validation Checklist

After assembly, verify these UX requirements:

| Requirement | Test Method | Pass/Fail |
|-------------|-------------|-----------|
| Manual override works | Turn thumb-turn by hand with servo off | ☐ |
| No servo damage from manual | Manually turn, then power on - servo still works | ☐ |
| Reliable servo operation | Press button - lock turns every time | ☐ |
| Visual feedback | Micro:bit LED shows lock/unlock state | ☐ |
| No binding/jamming | Full rotation smooth, no grinding sounds | ☐ |
| Family can use normally | Untrained person can operate manually | ☐ |
| Emergency access | Physical key works from outside | ☐ |

---

## 🔍 Troubleshooting

### Problem: Servo can't turn the lock
**Causes:**
- Thumb-turn is too stiff (common with new locks)
- Servo arm is too short (not enough torque)
- Battery is weak

**Solutions:**
1. Try a stronger servo (MG996R - high torque)
2. Use longer servo arm (more leverage)
3. Replace batteries
4. Lubricate thumb-turn mechanism

### Problem: Manual operation is stiff
**Causes:**
- Magnets too strong (too close)
- U-slot too tight
- Holder rubbing on door

**Solutions:**
1. Increase gap between magnets (add spacer)
2. Enlarge U-slot by 1-2mm
3. Add clearance around holder

### Problem: Micro:bit resets when servo moves
**Causes:**
- Power draw too high for Micro:bit
- Missing common ground

**Solutions:**
1. Use separate battery box for servo (required!)
2. Connect servo GND to battery GND and Micro:bit GND
3. Add capacitor (100μF) across servo power lines

### Problem: Magnetic coupling slips during operation
**Causes:**
- Magnets too weak
- Gap too large
- Thumb-turn friction too high

**Solutions:**
1. Use stronger magnets (N52 grade)
2. Reduce gap to 2-3mm
3. Reduce thumb-turn friction (lubricate)

---

## 📱 Next Steps

After successful assembly:

1. **Upload the full Blynk integration code**
2. **Configure GPS automation**
3. **Test with povo gateway**
4. **Set up heartbeat monitoring**
5. **Add family member access**

---

## 📞 Support

If you encounter issues:
- Check all connections are secure
- Verify battery voltage (should be 5-6V for 4× AA)
- Test servo separately (direct connection)
- Review troubleshooting section above

Good luck with your smart lock build! 🏠🔐
