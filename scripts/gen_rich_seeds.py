# Generator for rich real-world category catalog seeds
from pathlib import Path

BASE_DATA = Path(__file__).resolve().parent.parent / 'app' / 'seeds' / 'data'
BASE_DATA.mkdir(parents=True, exist_ok=True)

# 1. laptops_seed.py
(BASE_DATA / 'laptops_seed.py').write_text('''# Rich Laptops & Computers Catalog Seed Dataset
LAPTOPS_DATA = [
    {
        "title": "Lenovo ThinkPad E14 Gen 5 AMD Ryzen 7 7730U",
        "brand": "Lenovo",
        "sku": "LAP-LNV-E14-G5",
        "base_price": 68990.0,
        "sale_price": 56999.0,
        "cost_price": 45000.0,
        "short_description": "14-inch FHD IPS anti-glare display, AMD Ryzen 7 7730U (8C/16T), 16GB DDR4, 512GB NVMe SSD, backlit keyboard, fingerprint reader, 57Wh battery with 11 hours life.",
        "description": "Engineered for high-productivity professionals and software developers. The ThinkPad E14 Gen 5 AMD combines military-grade MIL-STD-810H durability with a whisper-quiet thermal design. Features dual microphones with AI noise suppression for crystal clear video conferences, hardware TPM 2.0 security, and legendary ThinkPad keyboard travel.",
        "target_usage": "coding, business, programming, office",
        "average_rating": 4.6,
        "total_reviews_count": 84,
        "is_featured": True,
        "attributes": [
            {"name": "Processor", "value": "AMD Ryzen 7 7730U (8 cores, 16 threads, up to 4.5 GHz)"},
            {"name": "RAM", "value": "16 GB DDR4-3200 (expandable to 40 GB)"},
            {"name": "Storage", "value": "512 GB M.2 2242 PCIe 4.0 NVMe SSD"},
            {"name": "Display", "value": "14-inch WUXGA (1920x1200) IPS, 300 nits, Anti-glare"},
            {"name": "Graphics", "value": "Integrated AMD Radeon Graphics"},
            {"name": "Battery", "value": "57Wh, Rapid Charge support (80% in 60 mins)"},
            {"name": "Weight", "value": "1.41 kg (3.11 lbs)"},
            {"name": "Operating System", "value": "Windows 11 Pro"}
        ],
        "key_features": ["Ryzen 7 8-Core Powerhouse", "Legendary Ergonomic Keyboard", "11-Hour Real Battery Life", "1.41kg Lightweight Chassis", "Dual SSD Slots"],
        "aspect_sentiments": {"battery": 92, "performance": 94, "build": 96, "keyboard": 98, "display": 82, "value": 90}
    },
    {
        "title": "Apple MacBook Air M2 13.6-inch 8GB/256GB Midnight",
        "brand": "Apple",
        "sku": "LAP-APL-MBA-M2-256",
        "base_price": 99900.0,
        "sale_price": 89900.0,
        "cost_price": 76000.0,
        "short_description": "13.6-inch Liquid Retina display with True Tone, Apple M2 chip (8-core CPU/8-core GPU), 8GB Unified Memory, 256GB SSD, MagSafe 3 charging, 18-hour battery life.",
        "description": "Strikingly thin design in an all-aluminum enclosure. Supercharged by the next-generation M2 chip, MacBook Air delivers exceptional speed and power efficiency inside an ultraportable silent fanless design. Liquid Retina display supports 1 billion colors, 1080p FaceTime HD camera, and four-speaker sound system with Spatial Audio.",
        "target_usage": "creative, portability, college, coding, travel",
        "average_rating": 4.8,
        "total_reviews_count": 142,
        "is_featured": True,
        "attributes": [
            {"name": "Processor", "value": "Apple M2 (8-core CPU with 4 performance & 4 efficiency cores)"},
            {"name": "RAM", "value": "8 GB Unified Memory"},
            {"name": "Storage", "value": "256 GB High-speed SSD"},
            {"name": "Display", "value": "13.6-inch Liquid Retina (2560x1664), 500 nits, Wide color (P3)"},
            {"name": "Graphics", "value": "8-core GPU with hardware-accelerated ProRes"},
            {"name": "Battery", "value": "52.6Wh lithium-polymer, up to 18 hours wireless web"},
            {"name": "Weight", "value": "1.24 kg (2.7 lbs)"},
            {"name": "Operating System", "value": "macOS Sonoma"}
        ],
        "key_features": ["Ultra-thin 11.3mm Aluminum Body", "Up to 18 Hours Battery", "Silent Fanless Operation", "500 Nits Liquid Retina Display", "MagSafe 3 & Touch ID"],
        "aspect_sentiments": {"battery": 98, "performance": 96, "build": 99, "trackpad": 99, "display": 95, "value": 84}
    },
    {
        "title": "Dell Inspiron 15 3520 Intel Core i5-1235U",
        "brand": "Dell",
        "sku": "LAP-DEL-IN3520-I5",
        "base_price": 49990.0,
        "sale_price": 41999.0,
        "cost_price": 34000.0,
        "short_description": "15.6-inch FHD 120Hz display, 12th Gen Intel Core i5-1235U (10C/12T), 16GB DDR4, 512GB SSD, lift hinge ergonomics, ExpressCharge.",
        "description": "Daily computing champion featuring smooth 120Hz FHD refresh rate display and responsive 12th Gen Intel processing. Ergonomic lift hinge elevates typing posture for reduced wrist fatigue during prolonged study or spreadsheet work. Includes pre-installed MS Office Home & Student 2021.",
        "target_usage": "student, office, budget, study",
        "average_rating": 4.3,
        "total_reviews_count": 96,
        "is_featured": False,
        "attributes": [
            {"name": "Processor", "value": "Intel Core i5-1235U (10 cores, up to 4.4 GHz Turbo)"},
            {"name": "RAM", "value": "16 GB DDR4-2666 MHz"},
            {"name": "Storage", "value": "512 GB M.2 PCIe NVMe SSD"},
            {"name": "Display", "value": "15.6-inch FHD (1920x1080) 120Hz Anti-glare, 250 nits"},
            {"name": "Graphics", "value": "Intel Iris Xe Graphics"},
            {"name": "Battery", "value": "41Wh 3-cell battery"},
            {"name": "Weight", "value": "1.65 kg"},
            {"name": "Operating System", "value": "Windows 11 Home"}
        ],
        "key_features": ["Smooth 120Hz Display", "16GB RAM Standard", "Ergonomic Lift Hinge", "ExpressCharge 80% in 1 hr", "Numeric Keypad Included"],
        "aspect_sentiments": {"battery": 74, "performance": 86, "build": 78, "keyboard": 84, "display": 88, "value": 94}
    },
    {
        "title": "ASUS TUF Gaming A15 AMD Ryzen 7 7735HS RTX 4050",
        "brand": "Asus",
        "sku": "LAP-ASU-TUF-A15-4050",
        "base_price": 84990.0,
        "sale_price": 68999.0,
        "cost_price": 57000.0,
        "short_description": "15.6-inch FHD 144Hz G-Sync, AMD Ryzen 7 7735HS, 16GB DDR5, 512GB Gen4 SSD, NVIDIA GeForce RTX 4050 6GB (140W TGP), 90Wh Battery.",
        "description": "High-octane gaming and GPU-accelerated computing powerhouse. Armed with NVIDIA GeForce RTX 4050 GPU running at full 140W max TGP with MUX switch and NVIDIA Advanced Optimus. Massive 90Wh battery delivers unprecedented endurance for a gaming laptop. MIL-STD-810H certified chassis with dual 84-blade Arc Flow Fans.",
        "target_usage": "gaming, 3d, video editing, heavy compute",
        "average_rating": 4.6,
        "total_reviews_count": 118,
        "is_featured": True,
        "attributes": [
            {"name": "Processor", "value": "AMD Ryzen 7 7735HS (8 cores, 16 threads, 16MB cache, up to 4.75 GHz)"},
            {"name": "RAM", "value": "16 GB DDR5-4800 MHz (Expandable to 32 GB)"},
            {"name": "Storage", "value": "512 GB PCIe 4.0 NVMe M.2 SSD"},
            {"name": "Display", "value": "15.6-inch FHD (1920x1080) 144Hz IPS-level, 100% sRGB, G-Sync"},
            {"name": "Graphics", "value": "NVIDIA GeForce RTX 4050 6GB GDDR6 (140W TGP, MUX Switch)"},
            {"name": "Battery", "value": "90Wh 4-cell Li-ion"},
            {"name": "Weight", "value": "2.20 kg"},
            {"name": "Operating System", "value": "Windows 11 Home"}
        ],
        "key_features": ["Full 140W RTX 4050 with MUX Switch", "100% sRGB 144Hz Screen", "Massive 90Wh Battery", "Dual Fan Arc Flow Cooling", "RGB Backlit Keyboard"],
        "aspect_sentiments": {"battery": 82, "performance": 96, "build": 88, "cooling": 90, "display": 91, "value": 92}
    },
    {
        "title": "HP Pavilion 14 Aero AMD Ryzen 5 7535U Ultra-Light",
        "brand": "HP",
        "sku": "LAP-HP-AERO14-R5",
        "base_price": 69990.0,
        "sale_price": 62999.0,
        "cost_price": 51000.0,
        "short_description": "13.3-inch 2.5K (2560x1600) 16:10 400-nits IPS, AMD Ryzen 5 7535U, 16GB LPDDR5, 512GB SSD, Magnesium-Aluminum alloy sub-1kg chassis.",
        "description": "Impossibly light at just 970 grams without compromising performance. Magnesium-aluminum alloy unibody frame houses a gorgeous 16:10 2.5K high-brightness 400 nits display with 100% sRGB color gamut. Audio tuned by B&O and fast-charging USB-C PD deliver supreme travel agility.",
        "target_usage": "portability, travel, college, coding, business",
        "average_rating": 4.5,
        "total_reviews_count": 62,
        "is_featured": False,
        "attributes": [
            {"name": "Processor", "value": "AMD Ryzen 5 7535U (6 cores, 12 threads, up to 4.55 GHz)"},
            {"name": "RAM", "value": "16 GB LPDDR5-6400 MHz onboard"},
            {"name": "Storage", "value": "512 GB PCIe NVMe M.2 SSD"},
            {"name": "Display", "value": "13.3-inch 2.5K WQXGA (2560x1600) IPS, 400 nits, 100% sRGB, Anti-glare"},
            {"name": "Graphics", "value": "AMD Radeon 660M Graphics"},
            {"name": "Battery", "value": "43Wh, up to 10.5 hours battery life"},
            {"name": "Weight", "value": "0.97 kg (2.13 lbs)"},
            {"name": "Operating System", "value": "Windows 11 Home"}
        ],
        "key_features": ["Sub-1kg Featherlight 970g", "Stunning 2.5K 400 Nits 16:10 Display", "100% sRGB Color Accuracy", "Audio by Bang & Olufsen", "Fingerprint Security"],
        "aspect_sentiments": {"battery": 86, "performance": 90, "build": 92, "portability": 99, "display": 97, "value": 89}
    }
]
''', encoding='utf-8')

# 2. smartphones_seed.py
(BASE_DATA / 'smartphones_seed.py').write_text('''# Rich Smartphones & Tablets Catalog Seed Dataset
SMARTPHONES_DATA = [
    {
        "title": "Apple iPhone 15 128GB Blue",
        "brand": "Apple",
        "sku": "PHN-APL-IP15-128",
        "base_price": 79900.0,
        "sale_price": 71999.0,
        "cost_price": 61000.0,
        "short_description": "Dynamic Island, 48MP Main Camera with 2x Telephoto, A16 Bionic chip, USB-C connector, Ceramic Shield front, all-day battery life.",
        "description": "Dynamic Island bubbles up alerts and Live Activities so you never miss a beat. Durable color-infused glass and aluminum design. The 48MP Main camera shoots in super-high resolution, capturing striking detail with automated portrait mode focus switching.",
        "target_usage": "camera, performance, daily, video, social",
        "average_rating": 4.7,
        "total_reviews_count": 210,
        "is_featured": True,
        "attributes": [
            {"name": "Processor", "value": "A16 Bionic (6-core CPU, 5-core GPU, 16-core Neural Engine)"},
            {"name": "Display", "value": "6.1-inch Super Retina XDR OLED (2556x1179), 2000 nits peak outdoor brightness"},
            {"name": "Camera", "value": "48MP Main + 12MP Ultra Wide with Sensor-shift OIS, 4K Dolby Vision 60fps"},
            {"name": "Front Camera", "value": "12MP TrueDepth with Autofocus"},
            {"name": "Storage", "value": "128 GB NVMe"},
            {"name": "Battery", "value": "3349 mAh, USB-C 2.0 with 20W wired and 15W MagSafe"},
            {"name": "Durability", "value": "IP68 water/dust resistance, Ceramic Shield"}
        ],
        "key_features": ["Dynamic Island Experience", "48MP Super-High Res Camera", "2000 Nits Outdoor Display", "USB-C Universal Port", "A16 Bionic Performance"],
        "aspect_sentiments": {"battery": 88, "camera": 96, "display": 95, "build": 97, "performance": 98, "value": 85}
    },
    {
        "title": "Samsung Galaxy S23 FE 5G 128GB Graphite",
        "brand": "Samsung",
        "sku": "PHN-SAM-S23FE-128",
        "base_price": 59999.0,
        "sale_price": 41999.0,
        "cost_price": 33000.0,
        "short_description": "6.4-inch Dynamic AMOLED 2X 120Hz, Exynos 2200 4nm, 50MP OIS Triple Camera with 3x Optical Zoom, 4500mAh battery with wireless charging, IP68.",
        "description": "Flagship-grade mobile intelligence featuring pro-grade 50MP camera with Nightography and 3x optical telephoto lens. Armor Aluminum frame with Corning Gorilla Glass 5 protection and vapor chamber cooling for sustained performance.",
        "target_usage": "camera, multimedia, gaming, business",
        "average_rating": 4.4,
        "total_reviews_count": 134,
        "is_featured": True,
        "attributes": [
            {"name": "Processor", "value": "Samsung Exynos 2200 (4nm Octa-core with Xclipse 920 GPU)"},
            {"name": "Display", "value": "6.4-inch FHD+ Dynamic AMOLED 2X, 120Hz Adaptive, 1450 nits"},
            {"name": "Camera", "value": "50MP Main OIS + 12MP Ultra Wide + 8MP 3x Optical Telephoto OIS"},
            {"name": "Front Camera", "value": "10MP Dual Pixel AF"},
            {"name": "RAM & Storage", "value": "8GB LPDDR5 RAM, 128GB UFS 3.1"},
            {"name": "Battery", "value": "4500 mAh, 25W fast charge, 15W wireless charging"},
            {"name": "Durability", "value": "IP68 water & dust resistance"}
        ],
        "key_features": ["3x Optical Telephoto Zoom", "Dynamic AMOLED 2X 120Hz", "Nightography 50MP Sensor", "Wireless Charging & IP68", "Samsung DeX Desktop Mode"],
        "aspect_sentiments": {"battery": 80, "camera": 93, "display": 94, "build": 90, "performance": 88, "value": 92}
    },
    {
        "title": "OnePlus Nord CE4 5G 8GB/128GB Dark Chrome",
        "brand": "OnePlus",
        "sku": "PHN-1PL-CE4-128",
        "base_price": 24999.0,
        "sale_price": 21999.0,
        "cost_price": 17500.0,
        "short_description": "6.7-inch 120Hz AMOLED, Snapdragon 7 Gen 3 (4nm), 50MP Sony LYT-600 OIS, 5500mAh battery with 100W SUPERVOOC charging (1-100% in 29 mins).",
        "description": "Best-in-class value performance phone with massive 5500mAh battery paired with ultra-fast 100W wired flash charging. Powered by Qualcomm Snapdragon 7 Gen 3 platform with Aqua Touch screen technology for seamless wet-finger input.",
        "target_usage": "budget, battery, gaming, daily, student",
        "average_rating": 4.5,
        "total_reviews_count": 188,
        "is_featured": False,
        "attributes": [
            {"name": "Processor", "value": "Qualcomm Snapdragon 7 Gen 3 (4nm Octa-core)"},
            {"name": "Display", "value": "6.7-inch FHD+ AMOLED, 120Hz, 1.07B colors, HDR10+"},
            {"name": "Camera", "value": "50MP Sony LYT-600 with OIS + 8MP Ultra Wide (112°)"},
            {"name": "Front Camera", "value": "16MP 1080p"},
            {"name": "RAM & Storage", "value": "8GB LPDDR4X, 128GB UFS 3.1 (Expandable up to 1TB microSD)"},
            {"name": "Battery", "value": "5500 mAh with 100W SUPERVOOC (Charger in box)"},
            {"name": "Durability", "value": "IP54 water/dust resistance with Aqua Touch"}
        ],
        "key_features": ["100W SUPERVOOC Fast Charging", "Massive 5500mAh Battery", "Sony LYT-600 50MP OIS Sensor", "Snapdragon 7 Gen 3 Efficiency", "Aqua Touch Wet Display"],
        "aspect_sentiments": {"battery": 97, "camera": 87, "display": 91, "charging": 99, "performance": 90, "value": 96}
    }
]
''', encoding='utf-8')

# 3. audio_seed.py
(BASE_DATA / 'audio_seed.py').write_text('''# Rich Audio & Headphones Catalog Seed Dataset
AUDIO_DATA = [
    {
        "title": "Sony WH-1000XM5 Wireless Noise Cancelling Headphones",
        "brand": "Sony",
        "sku": "AUD-SNY-WH1000XM5",
        "base_price": 34990.0,
        "sale_price": 26990.0,
        "cost_price": 21000.0,
        "short_description": "Industry-leading Active Noise Cancellation with Auto NC Optimizer, 8 microphones, 30-hour battery life with quick charge, LDAC Hi-Res Wireless Audio.",
        "description": "Two processors control 8 microphones for unprecedented noise cancellation. Integrated Processor V1 unlocks the full potential of HD Noise Cancelling Processor QN1. Specially designed 30mm carbon fiber composite driver unit delivers natural sound quality with crystal-clear hands-free calling via Precise Voice Pickup technology.",
        "target_usage": "audiophile, travel, anc, office, calls, focus",
        "average_rating": 4.7,
        "total_reviews_count": 165,
        "is_featured": True,
        "attributes": [
            {"name": "Driver Unit", "value": "30mm specially engineered Carbon Fiber Composite dome"},
            {"name": "Noise Cancelling", "value": "Dual processors (QN1 + V1) with 8 microphones & Auto NC Optimizer"},
            {"name": "Codecs", "value": "LDAC, AAC, SBC with DSEE Extreme audio upscaling"},
            {"name": "Battery Life", "value": "30 hours (NC ON), 40 hours (NC OFF); 3 min charge = 3 hours playback"},
            {"name": "Microphones", "value": "4 beamforming mics with AI noise reduction algorithm"},
            {"name": "Connectivity", "value": "Bluetooth 5.2, Multipoint connection (2 devices simultaneously), 3.5mm jack"},
            {"name": "Weight", "value": "250 grams ultra-lightweight soft fit leather"}
        ],
        "key_features": ["Industry Leading Dual-Processor ANC", "30-Hour Battery with 3-Min Fast Charge", "Hi-Res LDAC Wireless Audio", "Multipoint Dual Device Pairing", "Speak-to-Chat & Wear Detection"],
        "aspect_sentiments": {"anc": 98, "sound": 96, "comfort": 94, "battery": 95, "mic": 91, "value": 87}
    },
    {
        "title": "Sennheiser Accentum Wireless ANC Headphones",
        "brand": "Sennheiser",
        "sku": "AUD-SNN-ACCENTUM",
        "base_price": 14990.0,
        "sale_price": 11990.0,
        "cost_price": 8800.0,
        "short_description": "Signature Sennheiser acoustics, Hybrid ANC, 50-hour marathon battery life, 37mm dynamic transducers, 5-band equalizer with Sound Check.",
        "description": "Unrivaled 50-hour battery playtime lets you listen for days without recharging. Engineered with Sennheiser's proprietary 37mm acoustic transducer for deep punchy bass and brilliant highs. Hybrid Active Noise Cancellation blocks outside chaos while Transparency Mode keeps you aware of your surroundings.",
        "target_usage": "battery, travel, audiophile, study, casual",
        "average_rating": 4.5,
        "total_reviews_count": 78,
        "is_featured": True,
        "attributes": [
            {"name": "Driver Unit", "value": "37mm dynamic driver"},
            {"name": "Battery Life", "value": "50 hours continuous playback (Bluetooth and ANC active)"},
            {"name": "Frequency Response", "value": "10 Hz to 22,000 Hz"},
            {"name": "Noise Cancelling", "value": "Hybrid Active Noise Cancellation with Transparency Mode"},
            {"name": "Connectivity", "value": "Bluetooth 5.2 (aptX HD, AAC, SBC) with Multipoint"},
            {"name": "Weight", "value": "222 grams"}
        ],
        "key_features": ["50-Hour Marathon Battery Life", "Sennheiser Signature Sound Stage", "Hybrid ANC with Transparency Mode", "aptX HD High Resolution Codec", "Custom 5-Band EQ via Smart Control App"],
        "aspect_sentiments": {"battery": 99, "sound": 93, "comfort": 88, "anc": 89, "value": 94}
    }
]
''', encoding='utf-8')

# 4. monitors_seed.py
(BASE_DATA / 'monitors_seed.py').write_text('''# Rich Monitors & Displays Catalog Seed Dataset
MONITORS_DATA = [
    {
        "title": "LG UltraGear 27GN800-B 27-inch QHD 144Hz IPS Gaming Monitor",
        "brand": "LG",
        "sku": "MON-LG-27GN800",
        "base_price": 28500.0,
        "sale_price": 21999.0,
        "cost_price": 16500.0,
        "short_description": "27-inch QHD (2560x1440) IPS display, 144Hz refresh rate, 1ms (GtG) response time, HDR10, sRGB 99%, NVIDIA G-Sync Compatible & AMD FreeSync Premium.",
        "description": "Step into total visual immersion. IPS 1ms response rate reduces reverse ghosting and provides fast response time to elevate your gameplay. 144Hz refresh rate combined with QHD resolution delivers fluid clarity for both competitive gaming and high-density productivity workflows.",
        "target_usage": "gaming, coding, productivity, office, photo editing",
        "average_rating": 4.6,
        "total_reviews_count": 92,
        "is_featured": True,
        "attributes": [
            {"name": "Screen Size", "value": "27 inch (68.5 cm) IPS panel"},
            {"name": "Resolution", "value": "QHD 2560 x 1440 pixels (16:9 aspect ratio)"},
            {"name": "Refresh Rate", "value": "144 Hz"},
            {"name": "Response Time", "value": "1ms (GtG at Faster)"},
            {"name": "Color Gamut", "value": "sRGB 99% (CIE1931), HDR10, 350 nits"},
            {"name": "Sync Technology", "value": "NVIDIA G-SYNC Compatible, AMD FreeSync Premium"},
            {"name": "Ports", "value": "2x HDMI 2.0, 1x DisplayPort 1.4, Headphone out"}
        ],
        "key_features": ["Crisp QHD 1440p Resolution", "Fast 1ms GtG IPS Panel", "144Hz Ultra-Smooth Refresh", "NVIDIA G-Sync & FreeSync", "HDR10 with 99% sRGB"],
        "aspect_sentiments": {"display": 96, "gaming": 95, "build": 89, "colors": 94, "value": 92}
    }
]
''', encoding='utf-8')

# 5. peripherals_seed.py
(BASE_DATA / 'peripherals_seed.py').write_text('''# Rich Computer Peripherals Catalog Seed Dataset
PERIPHERALS_DATA = [
    {
        "title": "Logitech MX Master 3S Wireless Performance Mouse",
        "brand": "Logitech",
        "sku": "PER-LOG-MXM3S",
        "base_price": 10995.0,
        "sale_price": 8995.0,
        "cost_price": 6800.0,
        "short_description": "Quiet Clicks, 8K DPI any-surface glass tracking, MagSpeed electromagnetic scrolling (1000 lines/sec), USB-C fast charging, Bluetooth & Logi Bolt.",
        "description": "An icon remastered. Feel every moment of your workflow with even more precision and tactility thanks to Quiet Clicks and an 8,000 DPI track-on-glass sensor. MagSpeed scrolling delivers 90% more speed and 87% more precision compared to regular mice. Customize thumb buttons via Logi Options+.",
        "target_usage": "coding, business, productivity, design, office",
        "average_rating": 4.8,
        "total_reviews_count": 174,
        "is_featured": True,
        "attributes": [
            {"name": "Sensor", "value": "Darkfield high precision, 200 to 8000 DPI (in increments of 50 DPI)"},
            {"name": "Scroll Wheel", "value": "MagSpeed Electromagnetic with SmartShift & Thumb wheel"},
            {"name": "Buttons", "value": "7 buttons (Left/Right, Back/Forward, App-Switch, Wheel mode, Middle)"},
            {"name": "Battery", "value": "500 mAh Li-Po, up to 70 days on full charge; 1 min charge = 3 hours"},
            {"name": "Connectivity", "value": "Bluetooth Low Energy & Logi Bolt USB Receiver (Multi-device up to 3 PCs)"},
            {"name": "Weight", "value": "141 grams"}
        ],
        "key_features": ["MagSpeed 1,000 Lines/Sec Scroll", "8K DPI Track-on-Glass Sensor", "90% Quieter Acoustic Clicks", "70-Day Battery on Single Charge", "Cross-Computer Flow Control"],
        "aspect_sentiments": {"ergonomics": 98, "battery": 97, "scroll": 99, "build": 96, "productivity": 99, "value": 89}
    },
    {
        "title": "Keychron K2 V2 Wireless Mechanical Keyboard Hot-Swappable",
        "brand": "Keychron",
        "sku": "PER-KEY-K2V2-GAT",
        "base_price": 9499.0,
        "sale_price": 7999.0,
        "cost_price": 5800.0,
        "short_description": "75% compact layout (84 keys), Gateron G Pro Brown switches, hot-swappable PCB, Mac and Windows keycaps, RGB backlight, 4000mAh battery.",
        "description": "The quintessential wireless mechanical keyboard for software engineers and mechanical keyboard enthusiasts. Features dual Bluetooth 5.1 and Type-C wired connectivity with seamless switching across 3 devices. Includes Mac layout multimedia keys and Windows replacement keycaps.",
        "target_usage": "coding, typing, gaming, office, programming",
        "average_rating": 4.7,
        "total_reviews_count": 112,
        "is_featured": True,
        "attributes": [
            {"name": "Layout", "value": "75% compact (84 keys with dedicated arrow & navigation cluster)"},
            {"name": "Switches", "value": "Hot-swappable Gateron G Pro Mechanical Brown (tactile 55g)"},
            {"name": "Backlight", "value": "18 types of RGB dynamic backlight effects"},
            {"name": "Battery", "value": "4000 mAh rechargeable li-polymer (up to 240 hours without backlight)"},
            {"name": "Connectivity", "value": "Bluetooth 5.1 & Type-C wired cable"},
            {"name": "Keycaps", "value": "Curved profile ABS keycaps with Mac & Windows legends"}
        ],
        "key_features": ["Hot-Swappable Switch Sockets", "Mac & Windows Native Support", "Massive 4000mAh Battery", "75% Space-Saving Layout", "Tactile Mechanical Feel"],
        "aspect_sentiments": {"typing": 97, "build": 95, "battery": 92, "lighting": 90, "value": 93}
    }
]
''', encoding='utf-8')

# 6. furniture_seed.py
(BASE_DATA / 'furniture_seed.py').write_text('''# Rich Office & Study Furniture Catalog Seed Dataset
FURNITURE_DATA = [
    {
        "title": "ErgoSmart Pro High-Back Mesh Ergonomic Office Chair",
        "brand": "ErgoSmart",
        "sku": "FUR-ERG-PRO-BLK",
        "base_price": 18999.0,
        "sale_price": 13999.0,
        "cost_price": 9500.0,
        "short_description": "Dynamic lumbar support, 3D adjustable armrests, breathable Korean mesh back, multi-lock recline mechanism (90°-135°), Class-4 gas lift.",
        "description": "Engineered for 10+ hour continuous coding or desk work. The dynamic self-adjusting lumbar curve cradles the lower spine preventing lower back fatigue. Korean high-elasticity mesh provides optimal thermal dissipation while 3D armrests adjust in height, angle, and depth.",
        "target_usage": "ergonomics, study, work from home, coding, office",
        "average_rating": 4.6,
        "total_reviews_count": 89,
        "is_featured": True,
        "attributes": [
            {"name": "Backrest", "value": "High-elasticity breathable mesh with integrated dynamic lumbar support"},
            {"name": "Armrests", "value": "3D adjustable (Height, Angle, Forward/Backward)"},
            {"name": "Recline", "value": "Synchro-tilt mechanism with 3-position lock (90°, 115°, 135°)"},
            {"name": "Gas Lift", "value": "BIFMA certified Class-4 hydraulic cylinder"},
            {"name": "Base & Casters", "value": "Heavy-duty nylon base with 60mm silent PU casters"},
            {"name": "Weight Capacity", "value": "Tested up to 135 kg (300 lbs)"}
        ],
        "key_features": ["Dynamic Adaptive Lumbar Support", "3D Multi-Directional Armrests", "Breathable Korean Mesh Back", "135° Synchro-Tilt Recline", "BIFMA Class-4 Certified Lift"],
        "aspect_sentiments": {"comfort": 96, "lumbar": 98, "build": 91, "assembly": 89, "value": 94}
    }
]
''', encoding='utf-8')

print('All rich category seed files generated successfully!')
