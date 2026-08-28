import json
import random
import secrets
from datetime import datetime, timezone, timedelta, date
from app.extensions import db
from app.models.user import User, Role
from app.models.profile import CustomerProfile, SellerProfile
from app.models.category import Category
from app.models.product import Product, ProductAttribute, ProductImage
from app.models.inventory import ProductInventory, InventoryTransaction, InventoryAlert
from app.models.review import Review, ReviewAspectRating
from app.models.order import Order, OrderItem, OrderStatusHistory
from app.models.analytics import SellerMetricDaily, CustomerSegment, ProductPerformanceScore
from app.models.forecast import DemandForecast
from app.seeds.categories_seed import CATEGORIES_DATA


def run_full_seeder():
    """Generates complete, highly realistic, interconnected catalog, reviews, and historical sales."""
    print("Starting database seeding...")

    # 1. Roles
    roles = {
        'admin': Role(name='admin', display_name='Administrator', description='System Administrator'),
        'seller': Role(name='seller', display_name='Seller', description='Merchant/Seller Partner'),
        'customer': Role(name='customer', display_name='Customer', description='Standard Customer')
    }
    for r in roles.values():
        if not Role.query.filter_by(name=r.name).first():
            db.session.add(r)
    db.session.commit()

    # 2. Admin User
    admin_user = User.query.filter_by(email='admin@shopsense.ai').first()
    if not admin_user:
        admin_user = User(
            email='admin@shopsense.ai',
            first_name='ShopSense',
            last_name='Admin',
            role_id=roles['admin'].id,
            is_active=True,
            is_verified=True
        )
        admin_user.set_password('AdminSecure2026!')
        db.session.add(admin_user)
        db.session.commit()

    # 3. Sellers
    sellers_data = [
        {'name': 'Apex Tech India', 'slug': 'apex-tech-india', 'email': 'seller.apex@shopsense.ai', 'city': 'Bengaluru', 'state': 'Karnataka', 'rating': 4.8},
        {'name': 'Sonic Audio Hub', 'slug': 'sonic-audio-hub', 'email': 'seller.sonic@shopsense.ai', 'city': 'Mumbai', 'state': 'Maharashtra', 'rating': 4.7},
        {'name': 'ErgoLiving Studios', 'slug': 'ergoliving-studios', 'email': 'seller.ergo@shopsense.ai', 'city': 'Hyderabad', 'state': 'Telangana', 'rating': 4.9},
        {'name': 'Zenith Gadgets & Gear', 'slug': 'zenith-gadgets', 'email': 'seller.zenith@shopsense.ai', 'city': 'Delhi', 'state': 'Delhi', 'rating': 4.6}
    ]

    seller_profiles = []
    for s_info in sellers_data:
        s_user = User.query.filter_by(email=s_info['email']).first()
        if not s_user:
            s_user = User(
                email=s_info['email'],
                first_name=s_info['name'].split()[0],
                last_name='Merchant',
                role_id=roles['seller'].id,
                is_active=True,
                is_verified=True
            )
            s_user.set_password('SellerPass2026!')
            db.session.add(s_user)
            db.session.flush()

            profile = SellerProfile(
                user_id=s_user.id,
                business_name=s_info['name'],
                store_slug=s_info['slug'],
                business_email=s_info['email'],
                city=s_info['city'],
                state=s_info['state'],
                average_rating=s_info['rating'],
                total_ratings_count=random.randint(120, 850),
                is_verified_seller=True
            )
            db.session.add(profile)
            seller_profiles.append(profile)
        else:
            seller_profiles.append(s_user.seller_profile)
    db.session.commit()

    # 4. Customers
    demo_customer = User.query.filter_by(email='customer@shopsense.ai').first()
    if not demo_customer:
        demo_customer = User(
            email='customer@shopsense.ai',
            first_name='Rohan',
            last_name='Sharma',
            role_id=roles['customer'].id,
            is_active=True,
            is_verified=True
        )
        demo_customer.set_password('CustomerPass2026!')
        db.session.add(demo_customer)
        db.session.flush()

        c_prof = CustomerProfile(
            user_id=demo_customer.id,
            primary_usage='coding',
            budget_tier='balanced',
            shipping_address_line1='Flat 402, Green Glen Heights, Bellandur',
            shipping_city='Bengaluru',
            shipping_state='Karnataka',
            shipping_postal_code='560103'
        )
        db.session.add(c_prof)
        db.session.commit()

    # Additional sample customers
    customer_list = [demo_customer]
    for i in range(1, 25):
        c_email = f"user_{i}@example.com"
        u = User.query.filter_by(email=c_email).first()
        if not u:
            u = User(
                email=c_email,
                first_name=f"Shopper{i}",
                last_name="Test",
                role_id=roles['customer'].id,
                is_active=True,
                is_verified=True
            )
            u.set_password('Password123!')
            db.session.add(u)
            db.session.flush()
            cp = CustomerProfile(
                user_id=u.id,
                shipping_city=random.choice(['Bengaluru', 'Mumbai', 'Delhi', 'Hyderabad', 'Pune', 'Chennai']),
                shipping_state='Karnataka',
                shipping_postal_code='560001'
            )
            db.session.add(cp)
        customer_list.append(u)
    db.session.commit()

    # 5. Categories
    category_map = {}
    for cat_data in CATEGORIES_DATA:
        cat = Category.query.filter_by(slug=cat_data['slug']).first()
        if not cat:
            cat = Category(
                name=cat_data['name'],
                slug=cat_data['slug'],
                description=cat_data['description'],
                icon_name=cat_data['icon_name'],
                display_order=cat_data['display_order']
            )
            db.session.add(cat)
            db.session.flush()
        category_map[cat.name] = cat
    db.session.commit()

    # 6. Realistic 200+ Products across all 10 Categories
    if Product.query.count() < 50:
        print("Generating realistic catalog products...")
        raw_catalog = [
            # Laptops
            ('Laptops & Computers', 'ThinkPad E14 Gen 5 AMD', 'Lenovo', 64999.0, 56999.0, 48000.0, 1.41, 'coding, office, study',
             ['AMD Ryzen 7 7730U 8-Core', '16GB DDR4 RAM', '512GB NVMe SSD', '14-inch WUXGA IPS Display', 'Aluminium Top Cover'],
             {'battery': 88, 'performance': 92, 'build_quality': 94, 'comfort': 90, 'display': 84, 'value': 91}),

            ('Laptops & Computers', 'MacBook Air M2 13.6-inch', 'Apple', 99900.0, 89900.0, 78000.0, 1.24, 'coding, creative, travel, battery',
             ['Apple M2 Chip 8-Core CPU', '8GB Unified Memory', '256GB SSD', 'Liquid Retina Display', '18-Hour Battery Life', 'MagSafe 3'],
             {'battery': 98, 'performance': 94, 'build_quality': 98, 'comfort': 95, 'display': 96, 'value': 82}),

            ('Laptops & Computers', 'Dell Inspiron 15 3520', 'Dell', 48999.0, 41999.0, 36000.0, 1.65, 'office, study, budget',
             ['Intel Core i5-1235U 10-Core', '16GB RAM', '512GB SSD', '15.6-inch FHD 120Hz Anti-Glare Display', 'ExpressCharge'],
             {'battery': 74, 'performance': 84, 'build_quality': 79, 'comfort': 82, 'display': 78, 'value': 89}),

            ('Laptops & Computers', 'ASUS TUF Gaming A15', 'Asus', 78999.0, 68999.0, 58000.0, 2.20, 'gaming, coding, video editing',
             ['AMD Ryzen 7 7435HS', '16GB DDR5 RAM', '512GB Gen4 SSD', 'NVIDIA GeForce RTX 3050 4GB GPU', '144Hz FHD Display', 'Military Grade MIL-STD-810H'],
             {'battery': 62, 'performance': 95, 'build_quality': 88, 'comfort': 80, 'display': 86, 'value': 90}),

            ('Laptops & Computers', 'HP Pavilion 14 Aero', 'HP', 72999.0, 62999.0, 53000.0, 0.97, 'travel, coding, lightweight, battery',
             ['AMD Ryzen 5 7535U', '16GB LPDDR5 RAM', '512GB SSD', '13.3-inch WUXGA 400 nits 100% sRGB Display', 'Ultra-light 970g Magnesium Alloy'],
             {'battery': 90, 'performance': 88, 'build_quality': 86, 'comfort': 91, 'display': 93, 'value': 87}),

            # Audio & Headphones
            ('Audio & Headphones', 'Sony WH-1000XM5 Wireless ANC Headphones', 'Sony', 34990.0, 26990.0, 21000.0, 0.25, 'audiophile, travel, office, focus',
             ['Industry Leading Active Noise Cancelling (HD QN1 Processor)', '30-Hour Battery Life with Quick Charge', '8 Microphones for Crystal Clear Calls', 'Multipoint Connection', 'Hi-Res Audio Wireless LDAC'],
             {'battery': 95, 'performance': 96, 'build_quality': 91, 'comfort': 92, 'sound': 97, 'value': 84}),

            ('Audio & Headphones', 'Sennheiser Accentum Plus Wireless', 'Sennheiser', 15990.0, 12990.0, 9500.0, 0.22, 'sound, battery, travel',
             ['50-Hour Battery Playtime', 'Hybrid Adaptive ANC', 'Sennheiser Signature Sound', 'Touch Gesture Controls', 'Fast Charge (10 min for 5 hours)'],
             {'battery': 99, 'performance': 90, 'build_quality': 87, 'comfort': 89, 'sound': 94, 'value': 92}),

            ('Audio & Headphones', 'Anker Soundcore Space One', 'Anker', 9999.0, 7499.0, 5200.0, 0.26, 'budget, travel, battery',
             ['2X Stronger Voice Reduction ANC', '40-Hour ANC Battery Life', 'LDAC Hi-Res Audio Certification', 'Easy Chat Transparency Mode'],
             {'battery': 93, 'performance': 85, 'build_quality': 82, 'comfort': 84, 'sound': 87, 'value': 96}),

            # Smartphones
            ('Smartphones & Tablets', 'Samsung Galaxy S24 FE 5G', 'Samsung', 59999.0, 54999.0, 45000.0, 0.21, 'camera, gaming, daily',
             ['Exynos 2400e 4nm Flagship Chip', '8GB RAM', '128GB Storage', '6.7-inch Dynamic AMOLED 2X 120Hz Display', '50MP ProVisual Engine Camera', 'Galaxy AI Suite Built-in'],
             {'battery': 86, 'performance': 92, 'build_quality': 94, 'camera': 95, 'display': 97, 'value': 88}),

            ('Smartphones & Tablets', 'OnePlus 12R 5G', 'OnePlus', 42999.0, 37999.0, 31000.0, 0.20, 'gaming, battery, fast charging',
             ['Snapdragon 8 Gen 2 Mobile Platform', '16GB LPDDR5X RAM', '256GB UFS 3.1 Storage', '100W SUPERVOOC Fast Charging', '5500mAh Massive Battery', '1.5K ProXDR Display with LTPO4.0'],
             {'battery': 96, 'performance': 95, 'build_quality': 90, 'camera': 82, 'display': 94, 'value': 95}),

            # Monitors & Displays
            ('Monitors & Displays', 'LG 27-inch 4K UHD IPS Monitor (27UP650)', 'LG', 32000.0, 24999.0, 19000.0, 5.60, 'coding, creative, productivity',
             ['27-inch 4K (3840x2160) IPS Display', 'VESA DisplayHDR 400', 'DCI-P3 95% Color Gamut', 'AMD FreeSync', 'Height/Pivot/Tilt Ergonomic Stand'],
             {'build_quality': 91, 'display': 97, 'comfort': 93, 'value': 94}),

            ('Monitors & Displays', 'Dell S2722QC 27-inch 4K USB-C Hub Monitor', 'Dell', 44500.0, 36999.0, 29000.0, 6.10, 'coding, office, macbook companion',
             ['USB-C 65W Power Delivery Single Cable Setup', '4K UHD IPS Panel', 'Integrated Dual 3W Waves MaxxAudio Speakers', 'Height Adjustable Stand'],
             {'build_quality': 95, 'display': 96, 'comfort': 96, 'value': 88}),

            # Computer Peripherals
            ('Computer Peripherals', 'Keychron V1 QMK Custom Mechanical Keyboard', 'Keychron', 8999.0, 7499.0, 5500.0, 0.97, 'coding, typing, office',
             ['75% Compact Layout with Programmable Rotary Knob', 'Hot-Swappable Keychron K Pro Red Switches', 'South-Facing RGB Backlight', 'QMK/VIA Fully Programmable', 'Acoustic Sound Absorbing Silicone Pad'],
             {'build_quality': 97, 'comfort': 94, 'value': 93, 'performance': 95}),

            ('Computer Peripherals', 'Logitech MX Master 3S Wireless Mouse', 'Logitech', 10995.0, 8995.0, 6800.0, 0.14, 'coding, office, ergonomics',
             ['Quiet Clicks 90% Less Noise', '8000 DPI Any-Surface Tracking on Glass', 'MagSpeed Electromagnetic Scrolling (1000 lines/sec)', 'Ergonomic Thumb Rest & Gesture Button', '70-Day Battery Life on Full Charge'],
             {'battery': 97, 'build_quality': 96, 'comfort': 98, 'performance': 96, 'value': 89}),

            # Office Furniture
            ('Office & Study Furniture', 'ErgoPro High Back Mesh Ergonomic Chair', 'ErgoLiving Studios', 18999.0, 14999.0, 10500.0, 16.5, 'office, study, comfort',
             ['Dynamic Auto-Adaptive Lumbar Support', 'Breathable Korean Mesh Backrest', '3D Adjustable Armrests (Height, Angle, Depth)', 'Class 4 BIFMA Certified Gas Lift', '135-Degree Synchronized Tilt Mechanism'],
             {'build_quality': 92, 'comfort': 96, 'value': 93}),

            ('Office & Study Furniture', 'Motorized Dual-Motor Height Adjustable Standing Desk (140x70cm)', 'ErgoLiving Studios', 34999.0, 27999.0, 20000.0, 32.0, 'office, productivity, health',
             ['Dual Electric Motors with Smooth Silent Lifting (<48dB)', '4 Programmable Memory Height Presets (69cm to 118cm)', 'Anti-Collision Sensor Safety System', 'Solid 25mm Engineered Walnut Desktop', '100kg Heavy Duty Load Capacity'],
             {'build_quality': 96, 'comfort': 97, 'value': 89})
        ]

        # Generate expansion catalog to reach 200+ unique SKUs
        brands = ['Apple', 'Dell', 'HP', 'Lenovo', 'Asus', 'Acer', 'Samsung', 'Sony', 'Bose', 'Logitech', 'Keychron', 'LG', 'Canon', 'GoPro', 'HyperX', 'Anker', 'Ikea', 'OnePlus']
        
        all_products = []
        sku_counter = 1000

        # Add base products
        for cat_name, title, brand, base_p, sale_p, cost_p, wt, usage, features, aspects in raw_catalog:
            sku_counter += 1
            seller = random.choice(seller_profiles)
            category = category_map[cat_name]
            p = Product(
                sku=f"SKU-{sku_counter}",
                title=title,
                slug=f"{title.lower().replace(' ', '-').replace('/', '-')}-{sku_counter}",
                brand=brand,
                model_number=f"MOD-{sku_counter}",
                category_id=category.id,
                seller_id=seller.id,
                short_description=f"Premium {brand} {category.name[:-1] if category.name.endswith('s') else category.name} built for optimal {usage.split(',')[0]} performance.",
                description=f"Detailed overview of {title}. Engineered with top-grade components to deliver uncompromising speed, reliability, and ergonomic satisfaction. Designed specifically for {usage}.",
                base_price=base_p,
                sale_price=sale_p,
                cost_price=cost_p,
                discount_percentage=round(((base_p - sale_p) / base_p) * 100, 1),
                weight_kg=wt,
                warranty_months=12,
                average_rating=round(random.uniform(4.1, 4.9), 2),
                total_reviews_count=random.randint(25, 340),
                views_count=random.randint(400, 5200),
                purchases_count=random.randint(40, 680),
                target_usage=usage,
                is_active=True,
                is_featured=(sku_counter % 3 == 0)
            )
            p.set_key_features_list(features)
            p.aspect_sentiment_summary = json.dumps(aspects)
            db.session.add(p)
            all_products.append(p)

        # Procedurally expand to 180+ more diverse catalog products
        for i in range(1, 185):
            sku_counter += 1
            cat_name = random.choice(list(category_map.keys()))
            category = category_map[cat_name]
            brand = random.choice(brands)
            seller = random.choice(seller_profiles)
            
            base_p = round(random.uniform(1499.0, 89999.0), -2) - 1.0  # e.g. 2999, 14999
            sale_p = round(base_p * random.uniform(0.75, 0.95), -2) - 1.0
            cost_p = round(sale_p * 0.70, 2)
            
            p_title = f"{brand} {category.name.split()[0]} Pro Series {sku_counter}"
            usage_opts = ['coding, productivity', 'gaming, high-performance', 'study, budget-friendly', 'creative, photo-video', 'travel, lightweight']
            p_usage = random.choice(usage_opts)

            p = Product(
                sku=f"SKU-{sku_counter}",
                title=p_title,
                slug=f"{p_title.lower().replace(' ', '-').replace('/', '-')}-{sku_counter}",
                brand=brand,
                model_number=f"MOD-{sku_counter}",
                category_id=category.id,
                seller_id=seller.id,
                short_description=f"Reliable {brand} product tailored for {p_usage}.",
                description=f"Full specifications and performance review for {p_title}. Designed with high-durability materials and advanced modern features for demanding workloads.",
                base_price=base_p,
                sale_price=sale_p,
                cost_price=cost_p,
                discount_percentage=round(((base_p - sale_p) / base_p) * 100, 1),
                weight_kg=round(random.uniform(0.15, 8.5), 2),
                warranty_months=random.choice([12, 24, 36]),
                average_rating=round(random.uniform(3.8, 4.9), 2),
                total_reviews_count=random.randint(15, 210),
                views_count=random.randint(200, 3500),
                purchases_count=random.randint(10, 450),
                target_usage=p_usage,
                is_active=True,
                is_featured=(i % 7 == 0)
            )
            p.set_key_features_list([f"High grade {brand} engineering", "Optimized power efficiency", "Comprehensive 1-year warranty", "Plug-and-play compatibility"])
            p.aspect_sentiment_summary = json.dumps({'battery': random.randint(70, 95), 'performance': random.randint(75, 98), 'build_quality': random.randint(72, 96), 'value': random.randint(78, 96)})
            db.session.add(p)
            all_products.append(p)
        db.session.commit()

        # Add primary gallery images for all products
        print("Populating high-definition product images...")
        for p in all_products:
            img = ProductImage(
                product_id=p.id,
                image_url=p.primary_image_url,
                alt_text=f"{p.title} product image",
                is_primary=True,
                display_order=0
            )
            db.session.add(img)
        db.session.commit()

        # 7. Inventory for all products
        print("Initializing inventory levels and alerts...")
        for p in all_products:
            avail = random.randint(15, 120)
            # Create a few intentional low-stock and dead-stock items for analytics testing
            if p.id % 12 == 0:
                avail = random.randint(0, 4)  # low stock / stockout risk
            
            inv = ProductInventory(
                product_id=p.id,
                seller_id=p.seller_id,
                available_quantity=avail,
                reserved_quantity=random.randint(0, 5),
                safety_stock=10,
                reorder_point=20,
                reorder_quantity=50,
                supplier_lead_time_days=random.choice([5, 7, 10, 14]),
                daily_sales_velocity=round(p.purchases_count / 45.0, 2),
                stock_status='out_of_stock' if avail == 0 else ('low_stock' if avail <= 15 else 'in_stock'),
                last_restocked_at=datetime.now(timezone.utc) - timedelta(days=random.randint(2, 40))
            )
            db.session.add(inv)
            db.session.flush()

            # Inventory Alert if low
            if avail <= 10:
                alert = InventoryAlert(
                    inventory_id=inv.id,
                    seller_id=p.seller_id,
                    alert_type='stockout_risk',
                    severity='high' if avail > 0 else 'critical',
                    title=f"Low Stock Warning: {p.title}",
                    message=f"Only {avail} units left in stock. Reorder immediately to avoid stockout.",
                    action_recommended="Order 50 units from primary distributor"
                )
                db.session.add(alert)

            # Product Performance Score
            is_dead = (p.id % 20 == 0)
            score = ProductPerformanceScore(
                product_id=p.id,
                seller_id=p.seller_id,
                overall_score=round(random.uniform(70.0, 96.0) if not is_dead else random.uniform(25.0, 45.0), 1),
                sales_velocity_score=round(random.uniform(65.0, 95.0), 1),
                conversion_score=round(random.uniform(55.0, 92.0), 1),
                rating_sentiment_score=round(p.average_rating * 20.0, 1),
                profitability_score=round(random.uniform(60.0, 90.0), 1),
                performance_grade='A' if not is_dead else 'Dead',
                is_dead_stock=is_dead,
                days_since_last_sale=random.randint(2, 10) if not is_dead else random.randint(65, 120),
                action_recommendation='Maintain pricing strategy' if not is_dead else '15% Markdown clearance or bundle with high-velocity SKU'
            )
            db.session.add(score)

        db.session.commit()

        # 8. Aspect-Rated Reviews
        print("Populating customer reviews with aspect ratings...")
        review_snippets = [
            ("Outstanding build and battery life!", "The battery lasts easily through a full 10-hour workday of coding. Build quality is solid aluminium and keyboard travel is excellent.", 5),
            ("Great performance, slightly warm under heavy load", "Compiles large codebases very quickly without lag. Screen brightness is great for indoor study.", 4),
            ("Superb value for money", "Best in its price bracket. Sound is crisp, microphone clarity is great for remote meetings.", 5),
            ("Decent product but comfort could be improved", "Works well for short sessions, but after 4 hours of continuous use the ergonomics feel a bit stiff.", 3),
            ("Extremely satisfied with the purchase", "Fast shipping, impeccable performance, premium tactile feel. Highly recommended to anyone looking for a reliable daily driver.", 5)
        ]

        for p in all_products[:50]:
            num_revs = random.randint(3, 8)
            for _ in range(num_revs):
                title_s, text_s, stars = random.choice(review_snippets)
                reviewer = random.choice(customer_list)
                rev = Review(
                    product_id=p.id,
                    user_id=reviewer.id,
                    rating=stars,
                    title=title_s,
                    content=text_s,
                    sentiment_polarity=0.85 if stars >= 4 else 0.10,
                    sentiment_label='positive' if stars >= 4 else 'neutral',
                    created_at=datetime.now(timezone.utc) - timedelta(days=random.randint(5, 120))
                )
                rev.set_praises_list(['Long lasting battery backup', 'Sturdy build quality', 'Fast performance'])
                rev.set_complaints_list(['Slightly stiff initial ergonomics'] if stars < 4 else [])
                db.session.add(rev)
                db.session.flush()

                # Aspects
                aspects = [
                    ('battery', 0.90 if stars >= 4 else 0.60, 'positive'),
                    ('performance', 0.95 if stars >= 4 else 0.70, 'positive'),
                    ('build_quality', 0.88, 'positive')
                ]
                for aname, ascore, alabel in aspects:
                    ar = ReviewAspectRating(review_id=rev.id, aspect_name=aname, sentiment_score=ascore, sentiment_label=alabel)
                    db.session.add(ar)

        db.session.commit()

        # 9. Historical Orders spanning 180 days for dynamic analytics & forecasting
        print("Generating 180-day historical order transactions for time-series analytics...")
        now = datetime.now(timezone.utc)
        for d in range(180, 0, -1):
            order_date = now - timedelta(days=d)
            # Daily orders count
            daily_count = random.randint(3, 9)
            for _ in range(daily_count):
                cust = random.choice(customer_list)
                p_sample = random.sample(all_products, random.randint(1, 3))
                subtotal = sum(p.sale_price for p in p_sample)
                tax = round(subtotal * 0.18, 2)
                shipping = 0.0 if subtotal >= 1000.0 else 99.0
                total = subtotal + tax + shipping

                order_num = f"ORD-{secrets.token_hex(4).upper()}"
                order = Order(
                    order_number=order_num,
                    user_id=cust.id,
                    status='delivered' if d > 5 else 'processing',
                    subtotal_amount=subtotal,
                    tax_amount=tax,
                    shipping_fee=shipping,
                    total_amount=total,
                    payment_method='simulated_upi',
                    payment_status='paid',
                    shipping_name=cust.full_name,
                    shipping_address_line1='Flat 101, Prestige Palms',
                    shipping_city='Bengaluru',
                    shipping_state='Karnataka',
                    shipping_postal_code='560037',
                    created_at=order_date
                )
                db.session.add(order)
                db.session.flush()

                for p in p_sample:
                    qty = random.randint(1, 2)
                    item = OrderItem(
                        order_id=order.id,
                        product_id=p.id,
                        seller_id=p.seller_id,
                        product_title=p.title,
                        product_sku=p.sku,
                        quantity=qty,
                        unit_price=p.sale_price,
                        unit_cost=p.cost_price,
                        total_price=p.sale_price * qty,
                        item_status='delivered' if d > 5 else 'processing',
                        created_at=order_date
                    )
                    db.session.add(item)

        db.session.commit()

        # 10. Generate 30-day aggregated SellerMetricDaily records
        print("Compiling seller daily metric aggregates...")
        for seller in seller_profiles:
            for day_offset in range(30, 0, -1):
                m_date = date.today() - timedelta(days=day_offset)
                rev = round(random.uniform(45000.0, 185000.0), 2)
                profit = round(rev * 0.28, 2)
                units = random.randint(6, 25)
                orders_cnt = random.randint(4, 18)
                views = random.randint(350, 1800)
                metric = SellerMetricDaily(
                    seller_id=seller.id,
                    metric_date=m_date,
                    total_revenue=rev,
                    gross_profit=profit,
                    total_orders=orders_cnt,
                    units_sold=units,
                    page_views=views,
                    conversion_rate=round((orders_cnt / max(1, views)) * 100, 2),
                    average_order_value=round(rev / max(1, orders_cnt), 2),
                    returns_count=random.randint(0, 2)
                )
                db.session.add(metric)
        db.session.commit()

    print("Database seeding completed successfully!")
