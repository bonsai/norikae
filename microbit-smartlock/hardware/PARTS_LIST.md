# Parts List - Micro:bit Smart Lock
# Complete Shopping Guide with Specifications

---

## 🛒 Essential Components

### 1. Micro:bit v2
| Specification | Details |
|---------------|---------|
| Model | BBC micro:bit v2 |
| MCU | nRF52833 (ARM Cortex-M4) |
| Bluetooth | BLE 5.0 |
| LED Matrix | 5×5 red LEDs |
| Buttons | 2 programmable (A, B) |
| Pins | 25 gold-edge pins |
| Power | 3V from USB or battery |

**Where to buy:**
- Official store: microbit.org
- Amazon: Search "micro:bit v2"
- Price range: ¥2,000 - ¥3,000

**Note:** v2 has built-in speaker and microphone - useful for audio feedback!

---

### 2. Servo Motor (CRITICAL COMPONENT)

#### Recommended: MG90S (Metal Gear)
| Specification | Details |
|---------------|---------|
| Model | MG90S |
| Type | Metal gear (durability) |
| Torque | 2.5 kgf·cm @ 4.8V |
| Speed | 0.12 sec/60° @ 4.8V |
| Weight | 13.4g |
| Dimensions | 22.8 × 12.2 × 28.5 mm |
| Wire Length | ~150mm |
| Connector | Standard servo (3-pin) |
| Price | ¥800 - ¥1,500 |

#### Alternative: SG90 (Plastic Gear - Budget)
| Specification | Details |
|---------------|---------|
| Model | SG90 (9g servo) |
| Type | Plastic gear |
| Torque | 1.6 kgf·cm @ 4.8V |
| Price | ¥300 - ¥500 |

**⚠️ Warning:** SG90 may not have enough torque for stiff locks. MG90S recommended.

#### High-Torque Option: MG996R (For Heavy Doors)
| Specification | Details |
|---------------|---------|
| Model | MG996R |
| Torque | 10 kgf·cm @ 4.8V |
| Size | Larger (40.7 × 19.7 × 42.9 mm) |
| Price | ¥1,500 - ¥2,500 |

**Where to buy servos:**
- Amazon Japan: Search "MG90S"
- AliExpress: Cheaper but longer shipping
- Akihabara shops (if in Tokyo): Marutsu, Akizuki Denshi

---

### 3. Neodymium Magnets (For Magnetic Coupling)

| Specification | Details |
|---------------|---------|
| Material | Neodymium (NdFeB) N52 grade |
| Shape | Disc |
| Diameter | 6mm |
| Thickness | 3mm |
| Quantity | 2 pieces minimum (buy 10 for spares) |
| Price | ¥500 - ¥1,000 for 10pcs |

**Where to buy:**
- Amazon: "Neodymium magnet 6mm 3mm"
- AliExpress: Search "N52 magnet 6x3"
- Price: ¥50-100 per piece

**⚠️ Safety:**
- Keep away from electronics
- Keep away from children
- Can shatter if snapped together - wear eye protection

---

### 4. Power Supply

#### Servo Battery Box (REQUIRED)
| Specification | Details |
|---------------|---------|
| Type | AA battery box × 4 |
| Output | 6V (4 × 1.5V) |
| Connector | JST-PH 2.0mm or bare wires |
| Switch | On/off switch preferred |
| Price | ¥200 - ¥500 |

**Why separate power?**
- Servos draw 500mA+ when moving
- Micro:bit 3V pin can only supply ~100mA
- Without separate power: Micro:bit will reset

#### Rechargeable Option: NiMH AA Batteries
| Specification | Details |
|---------------|---------|
| Type | NiMH (Nickel-Metal Hydride) |
| Capacity | 2000-2500 mAh |
| Voltage | 1.2V per cell (4.8V total) |
| Quantity | 4 × AA |
| Price | ¥1,000 - ¥2,000 for set |

**Recommended brands:**
- Eneloop (Panasonic) - best quality
- Amazon Basics - good value
- IKEA LADDA - budget option (same as Eneloop)

---

### 5. Mounting Hardware

#### Command Strips (Recommended - No Damage)
| Specification | Details |
|---------------|---------|
| Brand | 3M Command |
| Type | Picture hanging strips (large) |
| Weight rating | 1.5kg+ (servo is only 13g) |
| Quantity | 2 sets (4 strips total) |
| Price | ¥500 - ¥800 |

**Benefits:**
- No drilling required
- Removable without damage
- Strong enough for servo
- Renters-friendly

#### Alternative: Double-Sided Tape
| Specification | Details |
|---------------|---------|
| Type | 3M VHB tape |
| Width | 10-20mm |
| Price | ¥300 - ¥600 |

---

### 6. Wiring

#### Jumper Wires (Female-to-Female)
| Specification | Details |
|---------------|---------|
| Type | Dupont connector, female-to-female |
| Length | 20cm (standard) |
| Quantity | 3 wires minimum (buy 10-20 for spares) |
| Color | Red (VCC), Black (GND), Other (Signal) |
| Price | ¥300 - ¥600 for 40pcs |

#### Servo Extension Cables (Optional)
| Specification | Details |
|---------------|---------|
| Length | 30cm or 50cm |
| Use case | If servo wires too short |
| Price | ¥200 - ¥400 each |

---

## 🛒 Optional but Recommended

### 7. 3D Printing Service (If No Printer)

#### Online Services (Japan)
| Service | URL | Price Range |
|---------|-----|-------------|
| DMM Make | dmm-make.com | ¥1,000 - ¥3,000 |
| JLCPCB | jlcpcb.com | ¥500 - ¥2,000 + shipping |
| PCBWay | pcbway.com | ¥500 - ¥2,000 + shipping |

**File needed:** `microbit-smartlock-servo-holder.stl`

**Material recommendation:**
- PLA: Cheapest, fine for indoor use
- PETG: Stronger, more durable (recommended)
- ABS: Strongest, but warps easily

---

### 8. Laser Cutting Service (Alternative to 3D Print)

#### Online Services
| Service | Material | Price |
|---------|----------|-------|
| Local maker space | 3mm acrylic | ¥1,000 - ¥2,000 |
| DMM Make | 3mm acrylic | ¥1,500 - ¥3,000 |

**File needed:** DXF format (convert from design)

---

### 9. Old Smartphone (Gateway)

#### Minimum Requirements
| Spec | Requirement |
|------|-------------|
| OS | Android 8.0+ or iOS 12+ |
| Bluetooth | BLE support |
| GPS | Required for geofence |
| Data | povo 2.0 SIM (nano-SIM) |
| Condition | Screen cracks OK, battery must hold charge |

**Budget options:**
- Used Android phones: ¥3,000 - ¥10,000
- iPhone 6s/7: ¥5,000 - ¥15,000
- Ask friends/family for old phones (free!)

---

### 10. povo 2.0 SIM

| Item | Details |
|------|---------|
| Provider | KDDI (au network) |
| Initial cost | ¥550 (SIM card) |
| Monthly fee | ¥0 (base plan) |
| Data speed | 128kbps (unlimited) |
| Requirement | Top-up once per 180 days |
| Minimum top-up | ¥330 (24-hour data boost) |

**Where to get:**
- povo.jp (official)
- Amazon (SIM card only)
- Electronics stores (Bic Camera, Yodobashi)

---

## 📊 Total Cost Estimate

### Budget Build (Using existing phone)
| Item | Cost (¥) |
|------|----------|
| Micro:bit v2 | 2,500 |
| MG90S Servo | 1,000 |
| Magnets (10pcs) | 500 |
| Battery box + batteries | 700 |
| Command strips | 500 |
| Jumper wires | 300 |
| 3D print (service) | 1,500 |
| povo SIM | 550 |
| **Total** | **¥7,550** |

### If buying used phone
| Additional item | Cost (¥) |
|-----------------|----------|
| Used Android phone | 5,000 |
| **New Total** | **¥12,550** |

### Comparison to Commercial Smart Locks
| Product | Price (¥) |
|---------|-----------|
| SwitchBot Lock | 12,800 |
| SESAME 5 | 19,800 |
| Native (Amazon) | 29,800 |
| **This DIY Project** | **¥7,550 - ¥12,550** |

**Savings:** ¥5,000 - ¥20,000+ compared to commercial options!

---

## 🛍️ Shopping List (Copy-Paste for Online Orders)

### Amazon Japan Search Terms:
```
1. "micro:bit v2"
2. "MG90S サーボ"
3. "ネオジム磁石 6mm 3mm"
4. "単三電池ボックス 4本"
5. "単三充電池 エネループ"
6. "ジャンパーワイヤー メス メス"
7. "コマンドストリップ 大"
8. "povo SIM"
```

### Akihabara Store List (if in Tokyo):
| Store | Specializes in | Location |
|-------|----------------|----------|
| Akizuki Denshi | Components, servos | Sotokanda |
| Marutsu | Micro:bit, Arduino | Sotokanda |
| Tsukumo | General electronics | Sotokanda |
| Radio Kaikan | Multiple floors | Akihabara station |

---

## 📦 Delivery Timeline

| Item | Delivery Time |
|------|---------------|
| Amazon Japan | 1-2 days (Prime) |
| AliExpress | 2-4 weeks |
| 3D print service | 1 week + shipping |
| povo SIM | 3-5 business days |

**Recommended order:** Start with Amazon for fast items, order AliExpress parts early.

---

## ✅ Pre-Purchase Checklist

Before ordering, verify:
- [ ] Thumb-turn dimensions measured (width × height)
- [ ] Door frame material (for mounting method)
- [ ] Available space near lock (for servo placement)
- [ ] Old phone compatibility (unlocked, GSM bands)
- [ ] povo coverage in your area (au network)

---

## 🔗 Useful Links

- Micro:bit official: https://microbit.org/
- Blynk IoT: https://blynk.io/
- povo 2.0: https://povo.jp/
- MG90S datasheet: Search "MG90S datasheet PDF"
- MakeCode editor: https://makecode.microbit.org/

---

## 💡 Money-Saving Tips

1. **Buy servo multipacks** - Often cheaper per unit
2. **Use existing phone** - Biggest cost saver
3. **Skip 3D print** - Use cardboard for prototype
4. **AliExpress bulk orders** - Magnets, wires much cheaper
5. **Maker spaces** - Free 3D printer access in some cities
6. **Recycle batteries** - Use old NiMH from other devices

---

Happy building! 🛠️
