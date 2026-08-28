# Script to generate extensive real-world product catalog seed datasets for all 10 categories
from pathlib import Path
import json

BASE_DATA = Path(__file__).resolve().parent.parent / 'app' / 'seeds' / 'data'
BASE_DATA.mkdir(parents=True, exist_ok=True)

CATEGORIES = [
    ('laptops_catalog.py', 'LAPTOPS_CATALOG', 'Laptops & Computers', [
        ('ThinkPad X1 Carbon Gen 11', 'Lenovo', 149990.0, 129990.0, 110000.0, 'Intel Core i7-1365U, 32GB LPDDR5, 1TB NVMe, 14" 2.8K OLED 400 nits, 1.12kg ultralight carbon fiber chassis.', 'coding, business, travel, executive', 4.8, 145),
        ('MacBook Pro 14-inch M3 Pro', 'Apple', 199900.0, 184900.0, 158000.0, 'Apple M3 Pro chip (11-core CPU, 14-core GPU), 18GB Unified Memory, 512GB SSD, Liquid Retina XDR 120Hz display, Space Black.', 'creative, coding, 3d, video, high performance', 4.9, 210),
        ('Dell XPS 13 Plus 9320', 'Dell', 135990.0, 119990.0, 102000.0, '13.4" 3.5K OLED Touchscreen, 13th Gen Intel Core i7-1360P, 16GB LPDDR5, 1TB SSD, capacitive touch function row, invisible glass haptic trackpad.', 'executive, design, portability, travel', 4.5, 78),
        ('ASUS ROG Zephyrus G14 OLED', 'Asus', 174990.0, 154990.0, 132000.0, '14" 3K 120Hz OLED ROG Nebula display, AMD Ryzen 9 8945HS, 32GB LPDDR5X, 1TB SSD, NVIDIA GeForce RTX 4070 8GB, CNC Aluminum body.', 'gaming, creative, 3d, coding, portable power', 4.7, 132),
        ('HP Spectre x360 2-in-1 14', 'HP', 164990.0, 144990.0, 124000.0, 'Intel Core Ultra 7 155H with Intel AI Boost NPU, 32GB RAM, 1TB SSD, 14" 2.8K 120Hz OLED Touch, HP Rechargeable Tilt Pen included.', 'creative, student, presentation, ai dev', 4.7, 94),
        ('Acer Swift Go 14 OLED', 'Acer', 79990.0, 64990.0, 53000.0, 'Intel Core Ultra 5 125H, 16GB LPDDR5X, 512GB SSD, 14" 2.8K 90Hz OLED 100% DCI-P3, 1440p QHD webcam, dual fans cooling.', 'student, coding, budget oled, office', 4.4, 88),
        ('Microsoft Surface Laptop 5', 'Microsoft', 107990.0, 94990.0, 81000.0, '13.5" PixelSense Touchscreen, Intel Core i5-1235U, 8GB LPDDR5x, 512GB SSD, Alcantara palm rest, Omnisonic speakers with Dolby Atmos.', 'office, business, luxury, executive', 4.3, 62),
        ('Lenovo Legion Pro 5i Gen 9', 'Lenovo', 169990.0, 148990.0, 128000.0, '16" WQXGA 240Hz 500 nits IPS, Intel Core i7-14700HX, 32GB DDR5, 1TB Gen4 SSD, NVIDIA RTX 4070 8GB (140W), Legion Coldfront 5.0.', 'gaming, heavy compute, 3d rendering, simulation', 4.8, 164),
        ('ASUS Zenbook 14 OLED UX3405', 'Asus', 99990.0, 89990.0, 77000.0, '14" 3K 120Hz OLED 16:10, Intel Core Ultra 7 155H, 16GB LPDDR5X, 1TB SSD, 75Wh battery with 15hr endurance, 1.2kg metal body.', 'travel, coding, student, media', 4.6, 115),
        ('Dell G15 5530 Gaming Laptop', 'Dell', 89990.0, 74990.0, 63000.0, '15.6" FHD 120Hz, 13th Gen Intel Core i5-13450HX, 16GB DDR5, 1TB SSD, NVIDIA GeForce RTX 3050 6GB, Alienware-inspired thermal cooling.', 'gaming, budget gaming, student, coding', 4.4, 140),
        ('MacBook Air 15-inch M3', 'Apple', 134900.0, 124900.0, 107000.0, 'Apple M3 chip (8-core CPU, 10-core GPU), 16GB Unified Memory, 512GB SSD, 15.3" Liquid Retina display, six-speaker sound system with force-cancelling woofers.', 'portability, media, coding, business', 4.8, 180),
        ('HP Victus 16 Gaming Laptop', 'HP', 84990.0, 69990.0, 58000.0, '16.1" FHD 144Hz IPS, AMD Ryzen 7 7840HS, 16GB DDR5, 512GB SSD, NVIDIA GeForce RTX 3050 6GB, OMEN Tempest Cooling.', 'gaming, student, coding, multimedia', 4.4, 98),
        ('Lenovo IdeaPad Slim 3 15', 'Lenovo', 48990.0, 36990.0, 30000.0, '15.6" FHD Anti-glare, Intel Core i3-1215U, 8GB DDR4, 512GB SSD, Rapid Charge Boost, privacy camera shutter.', 'budget, basic office, schooling, browsing', 4.2, 110),
        ('ASUS Vivobook Pro 15 OLED', 'Asus', 94990.0, 79990.0, 68000.0, '15.6" FHD OLED 600 nits, AMD Ryzen 7 5800H, 16GB RAM, 512GB SSD, NVIDIA RTX 3050, Harman Kardon audio.', 'creator, video editing, photography, general', 4.5, 87),
        ('MSI Katana 15 B13V Gaming', 'MSI', 109990.0, 89990.0, 76000.0, '15.6" FHD 144Hz, 13th Gen Intel Core i7-13620H, 16GB DDR5, 1TB NVMe SSD, NVIDIA GeForce RTX 4060 8GB GDDR6 (105W).', 'gaming, high fps, 3d, vr', 4.5, 120)
    ]),
    ('smartphones_catalog.py', 'SMARTPHONES_CATALOG', 'Smartphones & Tablets', [
        ('Samsung Galaxy S24 Ultra 5G 256GB Titanium Gray', 'Samsung', 134999.0, 124999.0, 106000.0, '6.8" QHD+ Dynamic AMOLED 2X 120Hz, Snapdragon 8 Gen 3 for Galaxy, 200MP Quad Telephoto Camera, S-Pen included, Galaxy AI.', 'camera, executive, productivity, flagship', 4.8, 310),
        ('Apple iPhone 15 Pro Max 256GB Natural Titanium', 'Apple', 159900.0, 148900.0, 128000.0, '6.7" Super Retina XDR ProMotion 120Hz, A17 Pro 3nm chip, 48MP Main with 5x Optical Telephoto, Action button, Titanium frame.', 'camera, video, gaming, flagship, status', 4.9, 420),
        ('Google Pixel 8 Pro 128GB Obsidian', 'Google', 106999.0, 89999.0, 76000.0, '6.7" Super Actua LTPO OLED 120Hz, Google Tensor G3, 50MP + 48MP + 48MP Pro Triple Camera, Best Take & Magic Editor AI.', 'camera, ai, photography, clean android', 4.6, 175),
        ('OnePlus 12 5G 16GB/512GB Silky Black', 'OnePlus', 69999.0, 64999.0, 55000.0, '6.82" 2K 120Hz ProXDR Display (4500 nits peak), Snapdragon 8 Gen 3, 4th Gen Hasselblad Camera, 5400mAh, 100W wired + 50W wireless.', 'performance, fast charging, gaming, display', 4.7, 240),
        ('Nothing Phone (2) 12GB/256GB Dark Grey', 'Nothing', 49999.0, 36999.0, 30000.0, '6.7" 120Hz LTPO OLED, Glyph Interface LED notifications, Snapdragon 8+ Gen 1, 50MP Sony IMX890 Dual OIS, Nothing OS 2.5.', 'design, aesthetics, smooth, daily', 4.5, 160),
        ('Xiaomi 14 5G 12GB/512GB Jade Green', 'Xiaomi', 79999.0, 69999.0, 59000.0, '6.36" 1.5K 120Hz LTPO OLED, Snapdragon 8 Gen 3, Leica Summilux 50MP Triple OIS, 90W HyperCharge + 50W Wireless, IP68 compact.', 'compact flagship, leica camera, performance', 4.7, 130),
        ('Apple iPad Air 11-inch M2 128GB Space Grey', 'Apple', 59900.0, 55900.0, 47000.0, '11" Liquid Retina display with P3 wide color, Apple M2 chip, Landscape 12MP front camera with Center Stage, Apple Pencil Pro support.', 'student, drawing, note taking, portable compute', 4.8, 195),
        ('Samsung Galaxy Tab S9 FE 10.9-inch 128GB Wi-Fi', 'Samsung', 44999.0, 34999.0, 28000.0, '10.9" 90Hz Display, Exynos 1380, S-Pen in box, IP68 water & dust resistant, Dual AKG speakers, 8000mAh battery.', 'student, media, study, drawing', 4.5, 140),
        ('Realme GT 6T 5G 8GB/256GB Fluid Silver', 'Realme', 32999.0, 28999.0, 23500.0, '6.78" 1.5K 120Hz 8T LTPO AMOLED 6000 nits peak, Snapdragon 7+ Gen 3, 50MP Sony LYT-600 OIS, 5500mAh, 120W SUPERVOOC.', 'gaming, performance, display, fast charge', 4.5, 115),
        ('Motorola Edge 50 Pro 5G 12GB/256GB Luxe Lavender', 'Motorola', 35999.0, 31999.0, 26000.0, '6.7" 1.5K 144Hz 3D Curved pOLED (Pantone validated), Snapdragon 7 Gen 3, 50MP OIS + 3x Telephoto, 125W TurboPower, Vegan leather.', 'design, camera, display, wireless charging', 4.6, 125)
    ]),
    ('audio_catalog.py', 'AUDIO_CATALOG', 'Audio & Headphones', [
        ('Bose QuietComfort Ultra Wireless Headphones', 'Bose', 35900.0, 31900.0, 26000.0, 'World-class noise cancellation, breakthrough Bose Immersive Audio spatial sound, CustomTune sound calibration, 24-hour battery life.', 'anc, travel, executive, audiophile, comfort', 4.7, 185),
        ('Apple AirPods Pro 2nd Gen with USB-C MagSafe Case', 'Apple', 24900.0, 21900.0, 17800.0, 'Up to 2x more Active Noise Cancellation, Adaptive Audio, Transparency mode, Personalized Spatial Audio with dynamic head tracking.', 'anc, iphone, daily, workouts, calls', 4.8, 510),
        ('Sony WF-1000XM5 True Wireless Earbuds', 'Sony', 29990.0, 21990.0, 17200.0, 'Dynamic Driver X for rich vocals, dual feedback mics, Integrated Processor V2 + HD QN2e, AI noise reduction, LDAC Hi-Res.', 'audiophile, compact anc, commuting, calls', 4.6, 140),
        ('Marshall Stanmore III Bluetooth Home Speaker', 'Marshall', 36999.0, 31999.0, 25500.0, 'Iconic vintage Marshall aesthetic, wider soundstage with outward-angled tweeters, Bluetooth 5.2, 3.5mm and RCA inputs, 80W output.', 'home audio, room filling, design, bass', 4.7, 95),
        ('JBL Flip 6 Portable Waterproof Bluetooth Speaker', 'JBL', 13999.0, 9999.0, 7500.0, '2-way speaker system with racetrack woofer and separate tweeter, IP67 waterproof & dustproof, 12 hours playback, PartyBoost pairing.', 'outdoor, travel, beach, bass, party', 4.6, 320),
        ('Sennheiser Momentum 4 Wireless Headphones', 'Sennheiser', 34990.0, 24990.0, 19500.0, 'Audiophile-inspired 42mm transducer system, Adaptive Noise Cancellation, unmatched 60-hour marathon battery life, smart pause.', 'battery, audiophile, hi-res, studio, travel', 4.7, 160),
        ('Samsung Galaxy Buds2 Pro True Wireless', 'Samsung', 17999.0, 11999.0, 8800.0, '24-bit Hi-Fi audio, 3 high SNR microphones for intelligent ANC, 360 Audio with direct multi-channel, IPX7 water resistance.', 'samsung, anc, comfort, compact', 4.5, 170),
        ('Sony HT-S20R 5.1ch Dolby Digital Soundbar', 'Sony', 19990.0, 15990.0, 12500.0, '400W total output, 5.1 channel real surround sound with rear speakers and external subwoofer, Bluetooth & USB connectivity, HDMI ARC.', 'home theater, movies, gaming, living room', 4.4, 280),
        ('Audio-Technica ATH-M50x Professional Studio Monitor Headphones', 'Audio-Technica', 16200.0, 12490.0, 9800.0, 'Critically acclaimed 45mm large-aperture drivers, rare earth magnets, 90° swiveling earcups for one-ear monitoring, detachable cables.', 'studio, music production, mixing, pure sound', 4.8, 380),
        ('Anker Soundcore Space One ANC Headphones', 'Anker', 9999.0, 7499.0, 5400.0, '2x stronger voice reduction ANC, LDAC Hi-Res Wireless, 40-hour playtime with ANC on (55h off), 40mm dynamic drivers, comfortable fit.', 'budget anc, student, office, commute', 4.4, 110)
    ]),
    ('cameras_catalog.py', 'CAMERAS_CATALOG', 'Cameras & Photography', [
        ('Sony Alpha 7 IV Full-Frame Mirrorless Camera Body', 'Sony', 242990.0, 209990.0, 178000.0, '33MP BSI Exmor R CMOS sensor, 4K 60p 10-bit 4:2:2 video, 759-point Phase AF with Real-time Eye AF for birds/animals/humans, 5.5-axis IBIS.', 'photography, videography, professional, youtube', 4.8, 112),
        ('Canon EOS R6 Mark II Mirrorless with RF 24-105mm Lens', 'Canon', 279995.0, 244990.0, 208000.0, '24.2MP full-frame sensor, 40 fps electronic shutter, 6K oversampled uncropped 4K 60p video, Dual Pixel CMOS AF II with vehicle/horse detection.', 'events, sports, weddings, professional video', 4.9, 85),
        ('GoPro HERO12 Black Action Camera', 'GoPro', 45000.0, 36990.0, 29000.0, '5.3K 60fps & 4K 120fps video, HyperSmooth 6.0 video stabilization with 360° Horizon Lock, waterproof to 33ft, Bluetooth audio support for AirPods.', 'vlogging, sports, travel, underwater, action', 4.6, 215),
        ('DJI Osmo Pocket 3 4K Handheld Gimbal Camera', 'DJI', 44990.0, 41990.0, 34500.0, '1-inch CMOS sensor, 4K 120fps, 3-axis mechanical gimbal stabilization, 2-inch rotatable OLED touchscreen with ActiveTrack 6.0.', 'vlogging, travel, tiktok, youtube, cinematic', 4.9, 160),
        ('Fujifilm X-T5 Mirrorless Camera Body Silver', 'Fujifilm', 169999.0, 154999.0, 131000.0, '40.2MP X-Trans CMOS 5 HR sensor, classic dial-based analog operation, 7.0-stop 5-axis IBIS, 19 legendary Film Simulation modes, 6.2K 30p video.', 'street photography, portraits, aesthetics, enthusiasts', 4.8, 94)
    ]),
    ('monitors_catalog.py', 'MONITORS_CATALOG', 'Monitors & Displays', [
        ('Samsung Odyssey Neo G9 49-inch Dual QHD Curved 240Hz', 'Samsung', 185000.0, 154999.0, 128000.0, '49" 32:9 Super Ultrawide (5120x1440), Quantum Mini-LED with 2048 dimming zones, 240Hz, 1ms response, 1000R curvature, HDR2000.', 'ultrawide gaming, flight sim, multitasking, workstation', 4.7, 65),
        ('Dell UltraSharp U2724D 27-inch QHD Thunderbolt Monitor', 'Dell', 44990.0, 37990.0, 31000.0, '27" IPS Black panel with 2000:1 contrast ratio, 120Hz refresh rate, 98% DCI-P3, ambient light sensor, daisy chaining, USB-C 90W PD hub.', 'coding, graphic design, macbook hub, productivity', 4.8, 110),
        ('BenQ PD3205U 32-inch 4K UHD Designer Monitor', 'BenQ', 69990.0, 58990.0, 49000.0, '32" 4K UHD IPS, Calman Verified & Pantone Validated 99% sRGB/Rec.709, KVM switch, Hotkey Puck G2 controller, USB-C 90W delivery.', 'cad, video editing, graphic design, 4k productivity', 4.7, 74),
        ('Acer Nitro VG270 S 27-inch Full HD 165Hz IPS Gaming Monitor', 'Acer', 16999.0, 11999.0, 9200.0, '27" FHD (1920x1080) 165Hz IPS, 0.5ms response time, AMD FreeSync Premium, 2x HDMI, 1x DP, built-in stereo speakers.', 'budget gaming, student, esports, high refresh', 4.4, 290),
        ('ViewSonic ColorPro VP2768a-4K 27-inch 4K Color Accurate Monitor', 'ViewSonic', 52000.0, 42990.0, 35000.0, '4K UHD, 100% sRGB, Delta E < 2 color accuracy, hardware calibration support, integrated ethernet LAN port & 90W USB-C docking.', 'photography, print production, color grading', 4.6, 52)
    ]),
    ('peripherals_catalog.py', 'PERIPHERALS_CATALOG', 'Computer Peripherals', [
        ('Razer DeathAdder V3 Pro Wireless Ergonomic Esports Mouse', 'Razer', 13999.0, 11499.0, 8800.0, '63g ultra-lightweight ergonomic shape, Focus Pro 30K Optical Sensor, Gen-3 optical mouse switches (90M clicks), up to 90hr battery.', 'esports, competitive fps, lightweight, ergonomics', 4.8, 145),
        ('Keychron Q1 Pro Wireless Custom Mechanical Keyboard Fully Assembled', 'Keychron', 19999.0, 17499.0, 13800.0, 'CNC machined 6063 aluminum body, double-gasket acoustic mount, QMK/VIA programmable, hot-swappable, K Pro Red switches.', 'typing, programming, custom enthusiast, luxury', 4.9, 82),
        ('Elgato Stream Deck MK.2 15 Studio Controller', 'Elgato', 15999.0, 13499.0, 10500.0, '15 customizable LCD keys to trigger streaming scenes, mute mic, launch apps, adjust smart lights, integrate with OBS & Discord.', 'streaming, video editing shortcuts, productivity macros', 4.8, 160),
        ('Logitech Brio 4K Ultra HD Webcam with RightLight 3 HDR', 'Logitech', 21995.0, 16995.0, 13000.0, '4K Ultra HD at 30fps / 1080p at 60fps, dual omni-directional noise canceling mics, Windows Hello facial recognition login, adjustable FOV (90°/78°/65°).', 'video conference, streaming, executive zoom, secure login', 4.6, 120),
        ('Anker 575 USB-C Docking Station (13-in-1, Triple Display)', 'Anker', 21999.0, 17999.0, 13900.0, '85W laptop charging, 3x HDMI/DP triple display support, 18W Power Delivery USB-C, 1Gbps Ethernet, SD/microSD slots, 4x USB-A ports.', 'workstation hub, macbook dock, clean desk setup', 4.7, 95)
    ]),
    ('wearables_catalog.py', 'WEARABLES_CATALOG', 'Smart Wearables', [
        ('Apple Watch Series 9 GPS 45mm Midnight Aluminum', 'Apple', 44900.0, 41900.0, 35500.0, 'S9 SiP with Double Tap gesture, 2000 nits edge-to-edge display, ECG app, Blood Oxygen sensor, Crash Detection, all-day 18hr battery.', 'health, fitness, ios ecosystem, heart tracking', 4.8, 260),
        ('Samsung Galaxy Watch6 Classic 47mm Bluetooth Black', 'Samsung', 36999.0, 27999.0, 22000.0, 'Iconic rotating physical bezel, Sapphire Crystal glass, Body Composition BIA analysis, personalized heart rate zones, Wear OS 4.', 'fitness, business luxury, android, sleep coaching', 4.6, 170),
        ('Garmin Forerunner 265 GPS Running Smartwatch', 'Garmin', 50490.0, 44990.0, 36000.0, 'Vibrant AMOLED touchscreen display, training readiness score, multi-band GPS tracking, up to 13 days of battery life in smartwatch mode.', 'marathon, triathlon, running, elite athletes', 4.9, 110),
        ('OnePlus Watch 2 Dual-Engine Architecture', 'OnePlus', 27999.0, 22999.0, 18000.0, 'Dual-engine architecture (Snapdragon W5 + BES2700), up to 100 hours battery life in smart mode, military grade MIL-STD-810H, Wear OS 4.', 'battery, wear os, fitness, value luxury', 4.6, 85),
        ('Amazfit GTR 4 Smart Watch with Dual-Band GPS', 'Amazfit', 17999.0, 14999.0, 11200.0, '1.43" HD AMOLED display, 14-day ultra-long battery life, dual-band circularly polarized GPS antenna, 150+ sports modes, Bluetooth phone calls.', 'fitness, budget battery, workout, daily tracking', 4.5, 190)
    ]),
    ('consoles_catalog.py', 'CONSOLES_CATALOG', 'Gaming & Consoles', [
        ('Sony PlayStation 5 Slim Console (Disc Edition)', 'Sony', 54990.0, 49990.0, 42000.0, 'Ultra-high speed 1TB custom NVMe SSD, Ray Tracing, 4K-TV gaming up to 120fps with 120Hz output, HDR technology, Tempest 3D AudioTech, DualSense haptics.', 'gaming, 4k gaming, exclusives, family', 4.9, 520),
        ('Microsoft Xbox Series X 1TB Console', 'Microsoft', 55990.0, 48990.0, 41000.0, '12 Teraflops of raw graphic processing power, Xbox Velocity Architecture, Quick Resume for multiple games, backward compatibility 4 generations.', 'gaming, game pass, 4k 120fps, power', 4.8, 310),
        ('Nintendo Switch OLED Model with Neon Blue & Neon Red Joy-Con', 'Nintendo', 34990.0, 29990.0, 24500.0, '7-inch vibrant OLED screen, wide adjustable stand, wired LAN port dock, 64GB internal storage, enhanced audio in handheld mode.', 'portable gaming, family, nintendo exclusives, couch co-op', 4.8, 410),
        ('ASUS ROG Ally Z1 Extreme Handheld Gaming Console', 'Asus', 69990.0, 54990.0, 45000.0, 'AMD Ryzen Z1 Extreme processor (8C/16T, RDNA 3), 7" FHD 120Hz 500 nits FreeSync Premium touchscreen, 16GB LPDDR5, 512GB PCIe 4.0 SSD, Windows 11.', 'pc gaming handheld, portable, steam, game pass on go', 4.6, 135),
        ('Sony DualSense Edge Wireless Controller', 'Sony', 18990.0, 16990.0, 13800.0, 'Changeable stick caps, remappable back buttons, adjustable trigger stops & dead zones, replaceable stick modules, braided USB cable with lockable housing.', 'competitive gaming, pro esports, ps5 customization', 4.7, 88)
    ]),
    ('furniture_catalog.py', 'FURNITURE_CATALOG', 'Office & Study Furniture', [
        ('ErgoSmart Ultra Motorized Dual-Motor Height Adjustable Standing Desk', 'ErgoSmart', 32999.0, 24999.0, 18500.0, 'Solid engineered wooden top (140x70cm), dual quiet electric motors (<45dB), 4 memory height presets (71cm to 118cm), anti-collision sensor, 120kg payload.', 'ergonomics, work from home, coding, standing health', 4.8, 92),
        ('Green Soul Monster Ultimate Ergonomic Gaming Chair', 'Green Soul', 22990.0, 17490.0, 12500.0, 'Spagnolo breathable fabric upholstery, internal molded foam, 4D armrests, magnetic memory foam neck pillow, frog tilt mechanism with rocking lock.', 'gaming, long hours, streamers, lumbar comfort', 4.6, 175),
        ('Ikea Markus High-Back Swivel Desk Chair Vissle Dark Grey', 'Ikea', 15990.0, 13990.0, 10200.0, 'Synchronized tilt mechanism, height adjustable with safety casters that lock when standing up, mesh back for air circulation, 10-year warranty.', 'office, budget ergonomics, study, minimal', 4.5, 230),
        ('Wakefit Apollo Engineered Wood Study Table with Bookshelf', 'Wakefit', 11999.0, 7999.0, 5800.0, 'Integrated 4-tier bookshelf, cable management grommet, water-resistant matte walnut finish, sturdy scratch-resistant engineered board.', 'student, bedroom study, compact storage, study', 4.4, 160),
        ('Featherlite Helix High Back Mesh Office Chair', 'Featherlite', 16500.0, 13490.0, 9800.0, 'Self-calibrating weight sensing mechanism, height adjustable lumbar support, 2D PU armrests, nylon glass-filled base, heavy duty dual casters.', 'corporate, home office, daily coding, ergonomics', 4.7, 110)
    ]),
    ('appliances_catalog.py', 'APPLIANCES_CATALOG', 'Smart Home & Appliances', [
        ('Philips Hue Smart LED Starter Kit (3 Bulbs + Hue Bridge)', 'Philips', 14999.0, 11999.0, 8900.0, '16 million colors, White and Color Ambiance, sync with music and movies, compatible with Alexa, Google Assistant & Apple HomeKit.', 'smart home, ambience, desk setup lighting, automation', 4.7, 130),
        ('Mi Smart Air Purifier 4 with True HEPA Filter', 'Xiaomi', 16999.0, 12999.0, 9800.0, 'Filters 99.97% of particles down to 0.3 microns, CADR 400m³/h suitable for 516 sq.ft room, OLED touch display, laser particle sensor, low noise 32dB.', 'clean air, allergies, bedroom, smart app control', 4.6, 210),
        ('Ecovacs Deebot N8 Pro Robotic Vacuum and Mop', 'Ecovacs', 34900.0, 24900.0, 19200.0, 'TrueDetect 3D obstacle avoidance, TrueMapping laser LiDAR navigation, 2600Pa suction power, auto-recharge and resume, custom room cleaning.', 'smart cleaning, home automation, pet hair, automated mop', 4.5, 140),
        ('Dyson V8 Absolute Cordless Vacuum Cleaner', 'Dyson', 43900.0, 29900.0, 23000.0, 'Dyson digital motor V8 spins at up to 110,000rpm, de-tangling Motorbar cleaner head, 40 minutes fade-free suction, whole-machine filtration.', 'deep cleaning, premium home, carpets, dust mites', 4.8, 185),
        ('Amazon Echo Show 8 (2nd Gen) HD Smart Display with Alexa', 'Amazon', 13999.0, 8999.0, 6800.0, '8" HD touchscreen with adaptive color, 13MP camera with auto-framing, stereo speakers, smart home dashboard, video calls and recipes.', 'smart display, kitchen, bedside clock, smart home hub', 4.6, 310)
    ])
]

for filename, var_name, cat_title, items in CATEGORIES:
    code = f"# {cat_title} Rich Seed Dataset\n\n{var_name} = [\n"
    for title, brand, base_p, sale_p, cost_p, desc, usage, rating, rev_count in items:
        sku = f"{brand[:3].upper()}-{abs(hash(title)) % 9000 + 1000}"
        code += "    {\n"
        code += f'        "title": {json.dumps(title)},\n'
        code += f'        "brand": {json.dumps(brand)},\n'
        code += f'        "sku": {json.dumps(sku)},\n'
        code += f'        "base_price": {base_p},\n'
        code += f'        "sale_price": {sale_p},\n'
        code += f'        "cost_price": {cost_p},\n'
        code += f'        "short_description": {json.dumps(desc[:120] + "...")},\n'
        code += f'        "description": {json.dumps(desc)},\n'
        code += f'        "target_usage": {json.dumps(usage)},\n'
        code += f'        "average_rating": {rating},\n'
        code += f'        "total_reviews_count": {rev_count},\n'
        code += f'        "is_featured": {rating >= 4.7},\n'
        code += '        "key_features": [\n'
        code += f'            "Premium {brand} Engineering",\n'
        code += f'            "Targeted for {usage.split(",")[0].strip().title()} Workflows",\n'
        code += f'            "Verified {rating}★ Customer Satisfaction",\n'
        code += '            "Full Brand Warranty & Express Support"\n'
        code += '        ],\n'
        code += '        "aspect_sentiments": {"performance": 94, "build": 92, "battery": 90, "value": 88, "comfort": 91}\n'
        code += "    },\n"
    code += "]\n"
    (BASE_DATA / filename).write_text(code, encoding='utf-8')

print("All 10 category catalog files generated successfully!")
