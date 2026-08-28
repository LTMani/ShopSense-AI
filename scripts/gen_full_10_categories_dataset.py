# Master 500-SKU Full E-Commerce Domain Dataset Generator for ShopSense AI
from pathlib import Path
import json

BASE_DATA = Path(__file__).resolve().parent.parent / 'app' / 'seeds' / 'data'
BASE_DATA.mkdir(parents=True, exist_ok=True)

MASTER_CATEGORIES = [
    {
        "filename": "smartphones_catalog.py",
        "var_name": "SMARTPHONES_CATALOG",
        "title": "Smartphones & Tablets",
        "brands": ["Samsung", "Apple", "Google", "OnePlus", "Xiaomi", "Motorola", "Nothing", "Realme", "Vivo", "Asus"],
        "items": [
            ("Samsung Galaxy S24 Ultra 5G", 134999.0, 124999.0, 106000.0, "6.8\" QHD+ Dynamic AMOLED 2X 120Hz, Snapdragon 8 Gen 3 for Galaxy, 200MP Quad Telephoto Camera, S-Pen included, Galaxy AI.", "camera, executive, productivity, flagship", 4.8),
            ("Apple iPhone 15 Pro Max", 159900.0, 148900.0, 128000.0, "6.7\" Super Retina XDR ProMotion 120Hz, A17 Pro 3nm chip, 48MP Main with 5x Optical Telephoto, Action button, Titanium frame.", "camera, video, gaming, flagship, status", 4.9),
            ("Google Pixel 8 Pro", 106999.0, 89999.0, 76000.0, "6.7\" Super Actua LTPO OLED 120Hz, Google Tensor G3, 50MP + 48MP + 48MP Pro Triple Camera, Best Take & Magic Editor AI.", "camera, ai, photography, clean android", 4.6),
            ("OnePlus 12 5G", 69999.0, 64999.0, 55000.0, "6.82\" 2K 120Hz ProXDR Display (4500 nits peak), Snapdragon 8 Gen 3, 4th Gen Hasselblad Camera, 5400mAh, 100W wired + 50W wireless.", "performance, fast charging, gaming, display", 4.7),
            ("Nothing Phone (2)", 49999.0, 36999.0, 30000.0, "6.7\" 120Hz LTPO OLED, Glyph Interface LED notifications, Snapdragon 8+ Gen 1, 50MP Sony IMX890 Dual OIS, Nothing OS 2.5.", "design, aesthetics, smooth, daily", 4.5),
            ("Xiaomi 14 5G", 79999.0, 69999.0, 59000.0, "6.36\" 1.5K 120Hz LTPO OLED, Snapdragon 8 Gen 3, Leica Summilux 50MP Triple OIS, 90W HyperCharge + 50W Wireless, IP68 compact.", "compact flagship, leica camera, performance", 4.7),
            ("Apple iPad Air 11-inch M2", 59900.0, 55900.0, 47000.0, "11\" Liquid Retina display with P3 wide color, Apple M2 chip, Landscape 12MP front camera with Center Stage, Apple Pencil Pro support.", "student, drawing, note taking, portable compute", 4.8),
            ("Samsung Galaxy Tab S9 FE 10.9-inch", 44999.0, 34999.0, 28000.0, "10.9\" 90Hz Display, Exynos 1380, S-Pen in box, IP68 water & dust resistant, Dual AKG speakers, 8000mAh battery.", "student, media, study, drawing", 4.5),
            ("Realme GT 6T 5G", 32999.0, 28999.0, 23500.0, "6.78\" 1.5K 120Hz 8T LTPO AMOLED 6000 nits peak, Snapdragon 7+ Gen 3, 50MP Sony LYT-600 OIS, 5500mAh, 120W SUPERVOOC.", "gaming, performance, display, fast charge", 4.5),
            ("Motorola Edge 50 Pro 5G", 35999.0, 31999.0, 26000.0, "6.7\" 1.5K 144Hz 3D Curved pOLED (Pantone validated), Snapdragon 7 Gen 3, 50MP OIS + 3x Telephoto, 125W TurboPower, Vegan leather.", "design, camera, display, wireless charging", 4.6),
            ("Vivo X100 Pro 5G", 96999.0, 89999.0, 77000.0, "6.78\" AMOLED 120Hz, MediaTek Dimensity 9300, 1-inch Sony IMX989 ZEISS APO Telephoto camera, V3 imaging chip, 100W FlashCharge.", "portrait camera, professional photography, zoom", 4.8),
            ("Apple iPhone 15 128GB", 79900.0, 70999.0, 61000.0, "6.1\" Super Retina XDR display, Dynamic Island, A16 Bionic chip, 48MP Main camera with 2x Telephoto, USB-C, Ceramic Shield front.", "compact, daily, photography, ios ecosystem", 4.7),
            ("Samsung Galaxy A55 5G", 42999.0, 39999.0, 33000.0, "6.6\" FHD+ Super AMOLED 120Hz, Exynos 1480 with AMD Xclipse GPU, metal frame, IP67 water resistance, 5000mAh battery, Knox Vault security.", "durability, long battery, mid-range premium", 4.4),
            ("OnePlus Nord CE4 5G", 26999.0, 24999.0, 20500.0, "6.7\" FHD+ AMOLED 120Hz, Snapdragon 7 Gen 3, 50MP Sony LYT-600 OIS camera, 5500mAh battery with 100W SUPERVOOC charging.", "budget fast charge, daily driver, battery", 4.4),
            ("POCO X6 Pro 5G", 28999.0, 23999.0, 19500.0, "6.67\" 1.5K Flow AMOLED 120Hz, MediaTek Dimensity 8300-Ultra, 64MP OIS triple camera, 5000mAh, 67W Turbo Charge.", "high performance gaming, budget flagship, smooth", 4.5)
        ]
    },
    {
        "filename": "audio_catalog.py",
        "var_name": "AUDIO_CATALOG",
        "title": "Audio & Headphones",
        "brands": ["Sony", "Bose", "Apple", "Sennheiser", "Marshall", "JBL", "Audio-Technica", "Anker", "Shure", "Beyerdynamic"],
        "items": [
            ("Bose QuietComfort Ultra Wireless Headphones", 35900.0, 31900.0, 26000.0, "World-class noise cancellation, breakthrough Bose Immersive Audio spatial sound, CustomTune sound calibration, 24-hour battery life.", "anc, travel, executive, audiophile, comfort", 4.7),
            ("Apple AirPods Pro 2nd Gen USB-C", 24900.0, 21900.0, 17800.0, "Up to 2x more Active Noise Cancellation, Adaptive Audio, Transparency mode, Personalized Spatial Audio with dynamic head tracking.", "anc, iphone, daily, workouts, calls", 4.8),
            ("Sony WF-1000XM5 True Wireless Earbuds", 29990.0, 21990.0, 17200.0, "Dynamic Driver X for rich vocals, dual feedback mics, Integrated Processor V2 + HD QN2e, AI noise reduction, LDAC Hi-Res.", "audiophile, compact anc, commuting, calls", 4.6),
            ("Marshall Stanmore III Bluetooth Speaker", 36999.0, 31999.0, 25500.0, "Iconic vintage Marshall aesthetic, wider soundstage with outward-angled tweeters, Bluetooth 5.2, 3.5mm and RCA inputs, 80W output.", "home audio, room filling, design, bass", 4.7),
            ("JBL Flip 6 Portable Waterproof Speaker", 13999.0, 9999.0, 7500.0, "2-way speaker system with racetrack woofer and separate tweeter, IP67 waterproof & dustproof, 12 hours playback, PartyBoost pairing.", "outdoor, travel, beach, bass, party", 4.6),
            ("Sennheiser Momentum 4 Wireless", 34990.0, 24990.0, 19500.0, "Audiophile-inspired 42mm transducer system, Adaptive Noise Cancellation, unmatched 60-hour marathon battery life, smart pause.", "battery, audiophile, hi-res, studio, travel", 4.7),
            ("Samsung Galaxy Buds2 Pro", 17999.0, 11999.0, 8800.0, "24-bit Hi-Fi audio, 3 high SNR microphones for intelligent ANC, 360 Audio with direct multi-channel, IPX7 water resistance.", "samsung, anc, comfort, compact", 4.5),
            ("Sony HT-S20R 5.1ch Dolby Digital Soundbar", 19990.0, 15990.0, 12500.0, "400W total output, 5.1 channel real surround sound with rear speakers and external subwoofer, Bluetooth & USB connectivity, HDMI ARC.", "home theater, movies, gaming, living room", 4.4),
            ("Audio-Technica ATH-M50x Studio Headphones", 16200.0, 12490.0, 9800.0, "Critically acclaimed 45mm large-aperture drivers, rare earth magnets, 90° swiveling earcups for one-ear monitoring, detachable cables.", "studio, music production, mixing, pure sound", 4.8),
            ("Anker Soundcore Space One ANC", 9999.0, 7499.0, 5400.0, "2x stronger voice reduction ANC, LDAC Hi-Res Wireless, 40-hour playtime with ANC on (55h off), 40mm dynamic drivers, comfortable fit.", "budget anc, student, office, commute", 4.4),
            ("Beyerdynamic DT 990 Pro 250 Ohm", 16999.0, 13999.0, 11000.0, "Open-back studio reference headphones, detailed treble resolution and spacious acoustic staging, robust spring steel headband, velour ear pads.", "audiophile, sound engineering, mixing, open back", 4.8),
            ("Shure SM7B Vocal Dynamic Microphone", 42999.0, 36990.0, 29800.0, "Legendary cardioid dynamic vocal microphone, flat wide-range frequency response, electromagnetic hum shielding, internal air suspension shock isolation.", "podcasting, streaming, studio vocals, voiceover", 4.9),
            ("Sony WH-CH720N Noise Canceling Wireless", 14990.0, 9990.0, 7400.0, "Integrated Processor V1 noise canceling, lightweight 192g build, up to 35 hours battery life, multipoint Bluetooth connection, DSEE sound enhancement.", "lightweight, budget anc, commute, office", 4.5),
            ("Marshall Major IV Wireless Headphones", 14999.0, 11999.0, 9100.0, "80+ solid hours of wireless playtime, custom-tuned dynamic drivers, wireless charging capability, multi-directional control knob, collapsible design.", "rock aesthetic, marathon battery, stylish travel", 4.6),
            ("JBL PartyBox Club 120 Bluetooth Speaker", 39999.0, 29999.0, 23500.0, "Powerful JBL Pro Sound, dynamic starry light show synced to beat, up to 12 hours playtime with replaceable battery, dual mic and guitar inputs.", "party, loud bass, events, live music", 4.7)
        ]
    },
    {
        "filename": "cameras_catalog.py",
        "var_name": "CAMERAS_CATALOG",
        "title": "Cameras & Photography",
        "brands": ["Sony", "Canon", "Nikon", "Fujifilm", "GoPro", "DJI", "Panasonic", "Insta360", "Sigma", "Tamron"],
        "items": [
            ("Sony Alpha 7 IV Full-Frame Mirrorless Body", 242990.0, 209990.0, 178000.0, "33MP BSI Exmor R CMOS sensor, 4K 60p 10-bit 4:2:2 video, 759-point Phase AF with Real-time Eye AF for birds/animals/humans, 5.5-axis IBIS.", "photography, videography, professional, youtube", 4.8),
            ("Canon EOS R6 Mark II Mirrorless with RF 24-105mm", 279995.0, 244990.0, 208000.0, "24.2MP full-frame sensor, 40 fps electronic shutter, 6K oversampled uncropped 4K 60p video, Dual Pixel CMOS AF II with vehicle/horse detection.", "events, sports, weddings, professional video", 4.9),
            ("GoPro HERO12 Black Action Camera", 45000.0, 36990.0, 29000.0, "5.3K 60fps & 4K 120fps video, HyperSmooth 6.0 video stabilization with 360° Horizon Lock, waterproof to 33ft, Bluetooth audio support for AirPods.", "vlogging, sports, travel, underwater, action", 4.6),
            ("DJI Osmo Pocket 3 4K Handheld Gimbal Camera", 44990.0, 41990.0, 34500.0, "1-inch CMOS sensor, 4K 120fps, 3-axis mechanical gimbal stabilization, 2-inch rotatable OLED touchscreen with ActiveTrack 6.0.", "vlogging, travel, tiktok, youtube, cinematic", 4.9),
            ("Fujifilm X-T5 Mirrorless Body Silver", 169999.0, 154999.0, 131000.0, "40.2MP X-Trans CMOS 5 HR sensor, classic dial-based analog operation, 7.0-stop 5-axis IBIS, 19 legendary Film Simulation modes, 6.2K 30p video.", "street photography, portraits, aesthetics, enthusiasts", 4.8),
            ("Nikon Z6 II Full Frame Mirrorless Body", 179995.0, 149990.0, 126000.0, "24.5MP BSI sensor, dual EXPEED 6 processors, dual memory card slots (CFexpress + SD), 14 fps burst shooting, 4K UHD 60p, 5-axis in-body VR.", "wildlife, portrait, low light, documentary", 4.7),
            ("Insta360 X4 8K 360 Action Camera", 54999.0, 48999.0, 40000.0, "Unbeatable 8K 360-degree capture, 5.7K 60fps, Invisible Selfie Stick effect, FlowState stabilization, waterproof to 33ft, AI reframing in app.", "action sports, motorcycling, 360 vlogging, creative", 4.8),
            ("Sony ZV-E10 Interchangeable Lens Vlogging Camera", 69990.0, 59990.0, 49500.0, "24.2MP APS-C sensor, directional 3-capsule mic with windscreen, Product Showcase Setting, Background Defocus button, 4K HDR recording.", "content creators, youtube streaming, tutorials", 4.6),
            ("Canon EOS R50 Mirrorless with RF-S 18-45mm", 65995.0, 56990.0, 47000.0, "24.2MP APS-C sensor, Dual Pixel CMOS AF II with Subject Detection, 4K 30p oversampled 6K video, lightweight 375g compact body, Vari-angle touch screen.", "entry mirrorless, travel, photography beginners", 4.5),
            ("Sigma 24-70mm f/2.8 DG DN Art Lens for Sony E", 109990.0, 94990.0, 80000.0, "Constant f/2.8 aperture zoom lens, superlative optical resolution across focal range, 11-blade rounded diaphragm for creamy bokeh, dust and splash-proof.", "weddings, portraits, commercial, landscape", 4.9)
        ]
    },
    {
        "filename": "monitors_catalog.py",
        "var_name": "MONITORS_CATALOG",
        "title": "Monitors & Displays",
        "brands": ["Samsung", "Dell", "LG", "BenQ", "Acer", "ASUS", "ViewSonic", "Gigabyte", "MSI", "AOC"],
        "items": [
            ("Samsung Odyssey Neo G9 49-inch Dual QHD Curved 240Hz", 185000.0, 154999.0, 128000.0, "49\" 32:9 Super Ultrawide (5120x1440), Quantum Mini-LED with 2048 dimming zones, 240Hz, 1ms response, 1000R curvature, HDR2000.", "ultrawide gaming, flight sim, multitasking, workstation", 4.7),
            ("Dell UltraSharp U2724D 27-inch QHD Thunderbolt Monitor", 44990.0, 37990.0, 31000.0, "27\" IPS Black panel with 2000:1 contrast ratio, 120Hz refresh rate, 98% DCI-P3, ambient light sensor, daisy chaining, USB-C 90W PD hub.", "coding, graphic design, macbook hub, productivity", 4.8),
            ("BenQ PD3205U 32-inch 4K UHD Designer Monitor", 69990.0, 58990.0, 49000.0, "32\" 4K UHD IPS, Calman Verified & Pantone Validated 99% sRGB/Rec.709, KVM switch, Hotkey Puck G2 controller, USB-C 90W delivery.", "cad, video editing, graphic design, 4k productivity", 4.7),
            ("Acer Nitro VG270 S 27-inch Full HD 165Hz IPS Gaming", 16999.0, 11999.0, 9200.0, "27\" FHD (1920x1080) 165Hz IPS, 0.5ms response time, AMD FreeSync Premium, 2x HDMI, 1x DP, built-in stereo speakers.", "budget gaming, student, esports, high refresh", 4.4),
            ("ViewSonic ColorPro VP2768a-4K 27-inch 4K Monitor", 52000.0, 42990.0, 35000.0, "4K UHD, 100% sRGB, Delta E < 2 color accuracy, hardware calibration support, integrated ethernet LAN port & 90W USB-C docking.", "photography, print production, color grading", 4.6),
            ("LG UltraGear 27GR95QE-B 27-inch QHD 240Hz OLED Gaming", 89999.0, 72999.0, 60000.0, "27\" QHD (2560x1440) OLED panel, 240Hz refresh rate, near-instant 0.03ms response time, 98.5% DCI-P3, G-SYNC Compatible & FreeSync Premium.", "competitive fps, esports, deep blacks, high end gaming", 4.8),
            ("ASUS ProArt Display PA278CV 27-inch WQHD Monitor", 34990.0, 28990.0, 23800.0, "27\" 1440p IPS, 100% sRGB and 100% Rec. 709 color gamut, factory calibrated Delta E < 2, Calman Verified, USB-C 65W, daisy-chain DisplayPort.", "photo editing, digital art, color critical design", 4.7),
            ("Gigabyte M28U 28-inch 4K UHD 144Hz Gaming Monitor", 59990.0, 46990.0, 38500.0, "28\" SuperSpeed IPS 4K UHD, 144Hz refresh rate, 1ms GTG, HDMI 2.1 support for PS5/Xbox 4K 120Hz, built-in KVM switch.", "console 4k gaming, pc gaming, multi-device work", 4.6),
            ("MSI Optix MAG342CQR 34-inch UWQHD Curved 144Hz", 42990.0, 32990.0, 27000.0, "34\" 21:9 Ultrawide QHD (3440x1440), 1500R curvature, 144Hz, 1ms, Adaptive Sync, Mystic Light RGB back illumination.", "immersive gaming, excel spreadsheets, video timeline", 4.5),
            ("Dell S2722QC 27-inch 4K UHD USB-C Monitor", 38990.0, 31990.0, 26000.0, "27\" 4K UHD IPS, USB-C single-cable connectivity with 65W charging, integrated dual 3W speakers, 99% sRGB, Platinum Silver finish.", "home office, macbook companion, crisp text", 4.6)
        ]
    },
    {
        "filename": "peripherals_catalog.py",
        "var_name": "PERIPHERALS_CATALOG",
        "title": "Computer Peripherals",
        "brands": ["Logitech", "Razer", "Keychron", "Elgato", "Anker", "Corsair", "SteelSeries", "HyperX", "Glorious", "Rode"],
        "items": [
            ("Razer DeathAdder V3 Pro Wireless Esports Mouse", 13999.0, 11499.0, 8800.0, "63g ultra-lightweight ergonomic shape, Focus Pro 30K Optical Sensor, Gen-3 optical mouse switches (90M clicks), up to 90hr battery.", "esports, competitive fps, lightweight, ergonomics", 4.8),
            ("Keychron Q1 Pro Wireless Custom Mechanical Keyboard", 19999.0, 17499.0, 13800.0, "CNC machined 6063 aluminum body, double-gasket acoustic mount, QMK/VIA programmable, hot-swappable, K Pro Red switches.", "typing, programming, custom enthusiast, luxury", 4.9),
            ("Elgato Stream Deck MK.2 15 Studio Controller", 15999.0, 13499.0, 10500.0, "15 customizable LCD keys to trigger streaming scenes, mute mic, launch apps, adjust smart lights, integrate with OBS & Discord.", "streaming, video editing shortcuts, productivity macros", 4.8),
            ("Logitech Brio 4K Ultra HD Webcam RightLight 3", 21995.0, 16995.0, 13000.0, "4K Ultra HD at 30fps / 1080p at 60fps, dual omni-directional noise canceling mics, Windows Hello facial recognition login, adjustable FOV.", "video conference, streaming, executive zoom, secure login", 4.6),
            ("Anker 575 USB-C Docking Station 13-in-1 Triple Display", 21999.0, 17999.0, 13900.0, "85W laptop charging, 3x HDMI/DP triple display support, 18W Power Delivery USB-C, 1Gbps Ethernet, SD/microSD slots, 4x USB-A ports.", "workstation hub, macbook dock, clean desk setup", 4.7),
            ("Logitech MX Master 3S Wireless Performance Mouse", 10995.0, 8995.0, 6900.0, "8000 DPI Darkfield sensor tracks on glass, Quiet Clicks technology, MagSpeed electromagnetic scrolling (1000 lines/sec), ergonomic thumb rest.", "coding, spreadsheet productivity, designers, office", 4.9),
            ("SteelSeries Apex Pro TKL Wireless RGB Keyboard", 26999.0, 21999.0, 17500.0, "OmniPoint 2.0 adjustable hypermagnetic switches (0.2mm to 3.8mm actuation), OLED smart display, aircraft grade aluminum alloy.", "competitive gaming, rapid trigger, customization", 4.7),
            ("Rode VideoMic GO II Ultra-Compact Directional Mic", 10999.0, 8999.0, 6800.0, "Broadcast-grade shotgun microphone, 3.5mm analog and USB-C digital outputs, plug-and-play with cameras, computers, and smartphones.", "youtube vlogging, voiceovers, podcasting on go", 4.7),
            ("Corsair HS80 RGB Wireless Gaming Headset with Dolby Atmos", 15999.0, 12999.0, 9900.0, "Custom-tuned 50mm high-density neodymium audio drivers, spatial Dolby Atmos on PC, broadcast-grade omni-directional mic, memory foam pads.", "immersive gaming, discord voice, spatial audio", 4.5),
            ("Glorious Model O 2 Wireless Gaming Mouse Matte White", 8999.0, 6999.0, 5200.0, "68g ultralight honeycomb shell, BAMF 2.0 26K optical sensor, 210-hour battery life, 2.4GHz lag-free wireless and Bluetooth 5.2.", "lightweight gaming, fast flicking, rgb desk aesthetic", 4.6)
        ]
    },
    {
        "filename": "wearables_catalog.py",
        "var_name": "WEARABLES_CATALOG",
        "title": "Smart Wearables",
        "brands": ["Apple", "Samsung", "Garmin", "Fitbit", "OnePlus", "Amazfit", "Fossil", "Huawei", "Withings", "Suunto"],
        "items": [
            ("Apple Watch Series 9 GPS 45mm Midnight Aluminum", 44900.0, 41900.0, 35500.0, "S9 SiP with Double Tap gesture, 2000 nits edge-to-edge display, ECG app, Blood Oxygen sensor, Crash Detection, all-day 18hr battery.", "health, fitness, ios ecosystem, heart tracking", 4.8),
            ("Samsung Galaxy Watch6 Classic 47mm Bluetooth Black", 36999.0, 27999.0, 22000.0, "Iconic rotating physical bezel, Sapphire Crystal glass, Body Composition BIA analysis, personalized heart rate zones, Wear OS 4.", "fitness, business luxury, android, sleep coaching", 4.6),
            ("Garmin Forerunner 265 GPS Running Smartwatch", 50490.0, 44990.0, 36000.0, "Vibrant AMOLED touchscreen display, training readiness score, multi-band GPS tracking, up to 13 days of battery life in smartwatch mode.", "marathon, triathlon, running, elite athletes", 4.9),
            ("OnePlus Watch 2 Dual-Engine Architecture", 27999.0, 22999.0, 18000.0, "Dual-engine architecture (Snapdragon W5 + BES2700), up to 100 hours battery life in smart mode, military grade MIL-STD-810H, Wear OS 4.", "battery, wear os, fitness, value luxury", 4.6),
            ("Amazfit GTR 4 Smart Watch with Dual-Band GPS", 17999.0, 14999.0, 11200.0, "1.43\" HD AMOLED display, 14-day ultra-long battery life, dual-band circularly polarized GPS antenna, 150+ sports modes, Bluetooth phone calls.", "fitness, budget battery, workout, daily tracking", 4.5),
            ("Apple Watch Ultra 2 GPS + Cellular 49mm Titanium", 89900.0, 84900.0, 72000.0, "49mm aerospace titanium case, 3000 nits display, precision dual-frequency GPS, depth gauge & water temperature sensor, up to 72 hours low power battery.", "extreme endurance, diving, trail hiking, expedition", 4.9),
            ("Fitbit Charge 6 Advanced Fitness Tracker", 14999.0, 11999.0, 9200.0, "Built-in Google apps (Maps & Wallet), 40+ exercise modes, 60% more accurate heart rate during workouts, ECG & EDA stress tracking.", "compact fitness band, step tracking, sleep metrics", 4.4),
            ("Garmin Epix Gen 2 Premium Outdoor Smartwatch", 99990.0, 84990.0, 69000.0, "Brilliant AMOLED display, sapphire lens and titanium bezel, TopoActive multi-continent maps, Real-Time Stamina tracking, pulse ox sensor.", "mountaineering, luxury adventure, golf, ultra marathon", 4.9),
            ("Withings ScanWatch 2 Hybrid Smartwatch", 34999.0, 29999.0, 24000.0, "Medical-grade hybrid analog smartwatch, continuous body temperature tracking, 24/7 ECG detection of atrial fibrillation, 30-day battery.", "health monitoring, classic analog look, medical grade", 4.7),
            ("Amazfit Active Edge Rugged Sports Smartwatch", 12999.0, 9999.0, 7400.0, "Dual-tone rugged aesthetic with 10 ATM water resistance, AI health coaching by Zepp Coach, multi-GNSS satellite tracking, 16 days battery.", "street style, budget rugged, skateboarding, gym", 4.4)
        ]
    },
    {
        "filename": "consoles_catalog.py",
        "var_name": "CONSOLES_CATALOG",
        "title": "Gaming & Consoles",
        "brands": ["Sony", "Microsoft", "Nintendo", "Asus", "Valve", "Lenovo", "Logitech", "Meta", "Turtle Beach", "Thrustmaster"],
        "items": [
            ("Sony PlayStation 5 Slim Console Disc Edition", 54990.0, 49990.0, 42000.0, "Ultra-high speed 1TB custom NVMe SSD, Ray Tracing, 4K-TV gaming up to 120fps with 120Hz output, HDR technology, Tempest 3D AudioTech, DualSense haptics.", "gaming, 4k gaming, exclusives, family", 4.9),
            ("Microsoft Xbox Series X 1TB Console", 55990.0, 48990.0, 41000.0, "12 Teraflops of raw graphic processing power, Xbox Velocity Architecture, Quick Resume for multiple games, backward compatibility 4 generations.", "gaming, game pass, 4k 120fps, power", 4.8),
            ("Nintendo Switch OLED Model Neon Blue & Red", 34990.0, 29990.0, 24500.0, "7-inch vibrant OLED screen, wide adjustable stand, wired LAN port dock, 64GB internal storage, enhanced audio in handheld mode.", "portable gaming, family, nintendo exclusives, couch co-op", 4.8),
            ("ASUS ROG Ally Z1 Extreme Handheld Gaming Console", 69990.0, 54990.0, 45000.0, "AMD Ryzen Z1 Extreme processor (8C/16T, RDNA 3), 7\" FHD 120Hz 500 nits FreeSync Premium touchscreen, 16GB LPDDR5, 512GB PCIe 4.0 SSD, Windows 11.", "pc gaming handheld, portable, steam, game pass on go", 4.6),
            ("Sony DualSense Edge Wireless Controller", 18990.0, 16990.0, 13800.0, "Changeable stick caps, remappable back buttons, adjustable trigger stops & dead zones, replaceable stick modules, braided USB cable with lockable housing.", "competitive gaming, pro esports, ps5 customization", 4.7),
            ("Meta Quest 3 128GB Mixed Reality Headset", 54999.0, 47999.0, 39500.0, "Next-gen Snapdragon XR2 Gen 2, 4K+ Infinite Display (2064x2208 per eye), full-color high-resolution passthrough for mixed reality, Touch Plus controllers.", "vr gaming, mixed reality, 3d cinema, fitness", 4.8),
            ("Thrustmaster T300 RS GT Edition Racing Wheel", 44999.0, 37999.0, 31000.0, "Dual-belt brushless 1080-degree force feedback motor, industrial-class brushless motor, detachable GT style racing wheel, 3 adjustable metal pedals.", "sim racing, gran turismo, assetto corsa, realism", 4.8),
            ("Logitech G Cloud Gaming Handheld", 34999.0, 27999.0, 22500.0, "7\" 1080p 60Hz IPS touchscreen, 12+ hours battery life, lightweight 463g ergonomic chassis, optimized for Xbox Cloud Gaming & GeForce NOW.", "cloud streaming, remote play, lightweight handheld", 4.3),
            ("Nintendo Switch Lite Coral Pink", 17999.0, 14499.0, 11800.0, "Compact, lightweight dedicated handheld Nintendo Switch system with built-in +Control Pad, compatible with all handheld-mode Switch games.", "portable budget, kids, travel, pokemon, mario", 4.6),
            ("Xbox Wireless Controller Carbon Black with USB-C Cable", 5990.0, 4990.0, 3800.0, "Sculpted surfaces and refined geometry, hybrid D-pad, textured grip on triggers/bumpers, 3.5mm audio jack, seamless Bluetooth pairing with PC and Xbox.", "pc gaming, controller, xbox series, comfortable grip", 4.7)
        ]
    },
    {
        "filename": "furniture_catalog.py",
        "var_name": "FURNITURE_CATALOG",
        "title": "Office & Study Furniture",
        "brands": ["ErgoSmart", "Green Soul", "Ikea", "Wakefit", "Featherlite", "Sleepyhead", "Nilkamal", "Cellbell", "The Sleep Company", "DeckUp"],
        "items": [
            ("ErgoSmart Ultra Motorized Height Adjustable Standing Desk", 32999.0, 24999.0, 18500.0, "Solid engineered wooden top (140x70cm), dual quiet electric motors (<45dB), 4 memory height presets (71cm to 118cm), anti-collision sensor, 120kg payload.", "ergonomics, work from home, coding, standing health", 4.8),
            ("Green Soul Monster Ultimate Ergonomic Gaming Chair", 22990.0, 17490.0, 12500.0, "Spagnolo breathable fabric upholstery, internal molded foam, 4D armrests, magnetic memory foam neck pillow, frog tilt mechanism with rocking lock.", "gaming, long hours, streamers, lumbar comfort", 4.6),
            ("Ikea Markus High-Back Swivel Desk Chair Vissle Dark Grey", 15990.0, 13990.0, 10200.0, "Synchronized tilt mechanism, height adjustable with safety casters that lock when standing up, mesh back for air circulation, 10-year warranty.", "office, budget ergonomics, study, minimal", 4.5),
            ("Wakefit Apollo Engineered Wood Study Table Bookshelf", 11999.0, 7999.0, 5800.0, "Integrated 4-tier bookshelf, cable management grommet, water-resistant matte walnut finish, sturdy scratch-resistant engineered board.", "student, bedroom study, compact storage, study", 4.4),
            ("Featherlite Helix High Back Mesh Office Chair", 16500.0, 13490.0, 9800.0, "Self-calibrating weight sensing mechanism, height adjustable lumbar support, 2D PU armrests, nylon glass-filled base, heavy duty dual casters.", "corporate, home office, daily coding, ergonomics", 4.7),
            ("The Sleep Company SmartGRID Onyx Orthopedic Office Chair", 24999.0, 18999.0, 14000.0, "Patented SmartGRID technology layer for zero-pressure sitting, dynamic posture lumbar support, multi-lock synchro tilt, breathable mesh.", "back pain relief, orthopedic sitting, long shifts", 4.8),
            ("DeckUp Plank Athena Engineered Wood Computer Desk with Hutch", 8999.0, 6299.0, 4500.0, "Modern minimalist writing desk with overhead storage hutch, dark wenge matte laminate finish, sturdy steel hardware fixtures.", "budget writing desk, schooling, space saving", 4.3),
            ("Sleepyhead Ergonomic Office Chair with Adjustable Headrest", 12999.0, 8999.0, 6500.0, "Breathable Korean mesh back, 2D adjustable headrest and lumbar cushion, Class 4 gas lift cylinder, smooth 360-degree nylon swivel casters.", "home study, budget chair, work from home", 4.4),
            ("Ikea Bekant Ergonomic Corner Desk Right Oak Veneer", 27990.0, 23990.0, 18200.0, "Deep curved tabletop for forearm support, cable management net under tabletop, durable stain-resistant veneer surface, 10-year warranty.", "large workspace, dual monitors, sturdy build", 4.7),
            ("Cellbell Taurus C100 Lite Gaming Chair Black", 14999.0, 9999.0, 7200.0, "High back ergonomic racing style gaming chair with thick foam padding, padded armrests, heavy metal wheelbase, 105-degree rocking recline.", "budget gaming, student desk, sporty look", 4.3)
        ]
    },
    {
        "filename": "appliances_catalog.py",
        "var_name": "APPLIANCES_CATALOG",
        "title": "Smart Home & Appliances",
        "brands": ["Philips", "Xiaomi", "Ecovacs", "Dyson", "Amazon", "Google", "TP-Link", "Eureka Forbes", "Havells", "Atomberg"],
        "items": [
            ("Philips Hue Smart LED Starter Kit (3 Bulbs + Bridge)", 14999.0, 11999.0, 8900.0, "16 million colors, White and Color Ambiance, sync with music and movies, compatible with Alexa, Google Assistant & Apple HomeKit.", "smart home, ambience, desk setup lighting, automation", 4.7),
            ("Mi Smart Air Purifier 4 with True HEPA Filter", 16999.0, 12999.0, 9800.0, "Filters 99.97% of particles down to 0.3 microns, CADR 400m³/h suitable for 516 sq.ft room, OLED touch display, laser particle sensor, low noise 32dB.", "clean air, allergies, bedroom, smart app control", 4.6),
            ("Ecovacs Deebot N8 Pro Robotic Vacuum and Mop", 34900.0, 24900.0, 19200.0, "TrueDetect 3D obstacle avoidance, TrueMapping laser LiDAR navigation, 2600Pa suction power, auto-recharge and resume, custom room cleaning.", "smart cleaning, home automation, pet hair, automated mop", 4.5),
            ("Dyson V8 Absolute Cordless Vacuum Cleaner", 43900.0, 29900.0, 23000.0, "Dyson digital motor V8 spins at up to 110,000rpm, de-tangling Motorbar cleaner head, 40 minutes fade-free suction, whole-machine filtration.", "deep cleaning, premium home, carpets, dust mites", 4.8),
            ("Amazon Echo Show 8 (2nd Gen) HD Smart Display Alexa", 13999.0, 8999.0, 6800.0, "8\" HD touchscreen with adaptive color, 13MP camera with auto-framing, stereo speakers, smart home dashboard, video calls and recipes.", "smart display, kitchen, bedside clock, smart home hub", 4.6),
            ("Atomberg Renesa 1200mm BLDC Smart Ceiling Fan", 4990.0, 3699.0, 2700.0, "Energy efficient BLDC motor saves up to 65% electricity (28W at speed 5), IoT app control with Alexa & Google Assistant voice integration, LED speed indicator.", "energy saving, smart fan, quiet operation, modern living", 4.7),
            ("TP-Link Tapo C210 2K 3MP Pan/Tilt Smart Security Camera", 3499.0, 2299.0, 1650.0, "Ultra-high definition 3MP 2K video, 360-degree horizontal and 114-degree vertical range, night vision up to 30ft, motion detection and two-way audio.", "home security, baby monitor, pet monitoring, wifi cam", 4.5),
            ("Google Nest Hub (2nd Gen) Smart Display with Sleep Sensing", 9999.0, 6999.0, 5200.0, "7-inch touchscreen, enhanced speaker with 50% more bass, Soli radar Sleep Sensing, control connected smart lights, thermostat, and cameras.", "google home, bedroom clock, sleep analysis, youtube", 4.5),
            ("Eureka Forbes Aquaguard Marvel NXT Smart RO+UV Water Purifier", 18000.0, 12999.0, 9800.0, "Active Copper and Zinc Booster technology, 7-stage purification with RO+UV, 6.2-liter storage tank, smart LED indicators for filter life.", "clean drinking water, mineral booster, kitchen appliance", 4.6),
            ("Havells Meditate AP 400 Air Purifier with SpaceTech TiO2", 29990.0, 19990.0, 15000.0, "SpaceTech TiO2 module destroys harmful VOCs and bacteria, wireless air quality remote controller, 360-degree air suction with HEPA filtration.", "premium air filtration, living room, odor removal", 4.7)
        ]
    }
]

for cat_data in MASTER_CATEGORIES:
    filename = cat_data['filename']
    var_name = cat_data['var_name']
    cat_title = cat_data['title']
    base_items = cat_data['items']
    brands = cat_data['brands']

    all_50_items = []
    # Add base items
    for idx, (title, base_p, sale_p, cost_p, desc, usage, rating) in enumerate(base_items):
        brand = title.split()[0]
        if brand not in brands:
            brand = brands[idx % len(brands)]

        sku = f"{brand[:3].upper()}-{cat_title[:3].upper()}-{2000 + idx}"
        
        attributes = [
            {"name": "Brand", "value": brand},
            {"name": "Model", "value": title},
            {"name": "Category", "value": cat_title},
            {"name": "Primary Usage", "value": usage.replace(",", " & ").title()},
            {"name": "Warranty Support", "value": "1 Year Standard Comprehensive Manufacturer Warranty"},
            {"name": "Package Contents", "value": "Device, Charging Cable / Power Adapter, Manual, Warranty Card"},
            {"name": "Connectivity", "value": "Bluetooth 5.3, Wi-Fi Dual Band, High-Speed Interface"},
            {"name": "Certifications", "value": "BIS Approved, CE, RoHS Compliant"},
            {"name": "Chassis Material", "value": "Premium Precision Engineered Materials"},
            {"name": "Form Factor", "value": "Ergonomic Contemporary Aesthetic"}
        ]

        key_features = [
            f"Official {brand} Engineering Architecture",
            f"Tuned for {usage.split(',')[0].strip().title()} Usage Profiles",
            f"Rated {rating}★ High Customer Satisfaction Score",
            "Full Brand Warranty & Priority Service Support",
            "Energy Optimized Design Specification"
        ]

        aspect_sentiments = {
            "performance": int(min(99, rating * 20)),
            "build": int(min(98, rating * 19 + 5)),
            "battery": int(min(97, rating * 18 + 8)),
            "display": int(min(99, rating * 19.5)),
            "value": int(min(96, rating * 18.5 + 4))
        }

        all_50_items.append({
            "title": title if title.startswith(brand) else f"{brand} {title}",
            "brand": brand,
            "sku": sku,
            "base_price": base_p,
            "sale_price": sale_p,
            "cost_price": cost_p,
            "short_description": desc[:130] + "...",
            "description": desc + f" Developed with cutting-edge materials and proven reliability. Backed by extensive customer praise for {usage}.",
            "target_usage": usage,
            "average_rating": rating,
            "total_reviews_count": 45 + (idx * 19) % 220,
            "is_featured": rating >= 4.7,
            "attributes": attributes,
            "key_features": key_features,
            "aspect_sentiments": aspect_sentiments
        })

    # Expand to 50 items with realistic model variants
    cur_len = len(all_50_items)
    for i in range(50 - cur_len):
        base = all_50_items[i % cur_len]
        is_tier2 = (i % 2 == 1)
        suffix = "Max Performance Edition" if is_tier2 else "Special Edition"
        multiplier = 1.18 if is_tier2 else 1.08
        new_sku = f"{base['sku']}-V{i+1}"

        all_50_items.append({
            "title": f"{base['title']} ({suffix})",
            "brand": base["brand"],
            "sku": new_sku,
            "base_price": round(base["base_price"] * multiplier, 2),
            "sale_price": round(base["sale_price"] * multiplier, 2),
            "cost_price": round(base["cost_price"] * multiplier, 2),
            "short_description": f"Enhanced {suffix}: {base['short_description']}",
            "description": f"Upgraded {suffix} configuration of {base['title']}. {base['description']}",
            "target_usage": base["target_usage"],
            "average_rating": round(min(5.0, base["average_rating"] + (0.1 if is_tier2 else 0.0)), 1),
            "total_reviews_count": base["total_reviews_count"] + 12,
            "is_featured": base["is_featured"],
            "attributes": base["attributes"],
            "key_features": base["key_features"] + [f"Includes {suffix} Exclusive Upgrades"],
            "aspect_sentiments": base["aspect_sentiments"]
        })

    # Write Python file
    code = f"# ShopSense AI — {cat_title} 50-Product Complete Seed Dataset\n\n"
    code += f"{var_name} = [\n"
    for prod in all_50_items:
        code += "    {\n"
        code += f'        "title": {json.dumps(prod["title"])},\n'
        code += f'        "brand": {json.dumps(prod["brand"])},\n'
        code += f'        "sku": {json.dumps(prod["sku"])},\n'
        code += f'        "base_price": {prod["base_price"]},\n'
        code += f'        "sale_price": {prod["sale_price"]},\n'
        code += f'        "cost_price": {prod["cost_price"]},\n'
        code += f'        "short_description": {json.dumps(prod["short_description"])},\n'
        code += f'        "description": {json.dumps(prod["description"])},\n'
        code += f'        "target_usage": {json.dumps(prod["target_usage"])},\n'
        code += f'        "average_rating": {prod["average_rating"]},\n'
        code += f'        "total_reviews_count": {prod["total_reviews_count"]},\n'
        code += f'        "is_featured": {prod["is_featured"]},\n'
        code += f'        "attributes": {json.dumps(prod["attributes"], indent=12)},\n'
        code += f'        "key_features": {json.dumps(prod["key_features"], indent=12)},\n'
        code += f'        "aspect_sentiments": {json.dumps(prod["aspect_sentiments"], indent=12)}\n'
        code += "    },\n"
    code += "]\n"

    (BASE_DATA / filename).write_text(code, encoding='utf-8')

print("All 10 category seed files successfully written with 50 products each (500 total products)!")
