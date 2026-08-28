# Realistic Aspect-Based Review Corpus Generator for ShopSense AI
from pathlib import Path
import json

BASE_DATA = Path(__file__).resolve().parent.parent / 'app' / 'seeds' / 'data'
BASE_DATA.mkdir(parents=True, exist_ok=True)

CUST_NAMES = [
    "Aarav Sharma", "Priya Nair", "Rohan Mehta", "Neha Gupta", "Vikram Malhotra",
    "Ananya Iyer", "Kavya Reddy", "Siddharth Rao", "Divya Joshi", "Rahul Kapoor",
    "Sneha Verma", "Aditya Sen", "Pooja Deshmukh", "Manish Tiwari", "Tanvi Bhat",
    "Gaurav Pillai", "Ishita Saxena", "Varun Chauhan", "Shreya Das", "Nikhil Hegde"
]

FEEDBACK_TEMPLATES = [
    (
        "Phenomenal build quality and lightning-fast speed!",
        "I've been using this daily for over 2 months now and it has completely exceeded my expectations. The responsiveness and thermal efficiency under sustained workload are stellar. Battery easily lasts through a full workday without charging.",
        5,
        {"performance": 96, "battery": 92, "build": 95, "value": 90},
        ["Exceptional processing velocity", "Solid aluminum unibody build", "All-day endurance"],
        ["Slightly heavy charging brick"]
    ),
    (
        "Impressive performance, outstanding value for money",
        "Great display clarity and crisp audio. Setup was instantaneous. For the price bracket, the feature set and build fit and finish rival options costing 30% more. Highly recommended for students and professionals.",
        5,
        {"performance": 92, "battery": 88, "build": 90, "value": 98},
        ["Unbeatable price to performance", "Crisp high-resolution display", "Intuitive ergonomics"],
        ["No bundled protective sleeve"]
    ),
    (
        "Good overall, minor software quirks",
        "The hardware is top-notch and premium in hand. I encountered a minor driver glitch initially, but a quick firmware patch resolved it. Thermals remain comfortable during long multitasking sessions.",
        4,
        {"performance": 85, "battery": 80, "build": 88, "value": 82},
        ["Clean modern aesthetic", "Low acoustic noise profile"],
        ["Initial setup required manual firmware update", "Occasional warm spots under peak load"]
    ),
    (
        "Solid daily driver with dependable battery life",
        "Very practical design with great attention to ergonomic details. Typing experience and screen color calibration are spot-on. Definitely one of the better purchases in this category.",
        5,
        {"performance": 90, "battery": 94, "build": 91, "value": 89},
        ["Superb battery retention", "Color-accurate panel", "Sturdy hinge mechanism"],
        ["Limited color options available at launch"]
    ),
    (
        "Decent hardware, but expected slightly better battery",
        "Build is robust and materials feel durable. However, under heavy load with max brightness, the battery drains quicker than advertised. Still a capable machine for standard desk usage.",
        3,
        {"performance": 78, "battery": 62, "build": 84, "value": 70},
        ["Sturdy structural chassis", "Bright anti-glare screen"],
        ["Higher power consumption at full brightness", "Speaker bass response could be deeper"]
    )
]

code = "# ShopSense AI — Verified Customer Aspect Reviews Corpus (1,500 Reviews)\n\n"
code += "REVIEWS_CORPUS = [\n"

total_reviews = 1500
for i in range(total_reviews):
    prod_sku_idx = (i // 3) % 500 + 1
    cust_name = CUST_NAMES[i % len(CUST_NAMES)]
    title_tpl, body_tpl, rating, aspects, praises, complaints = FEEDBACK_TEMPLATES[i % len(FEEDBACK_TEMPLATES)]

    code += "    {\n"
    code += f'        "review_id": {i + 1},\n'
    code += f'        "product_target_index": {prod_sku_idx},\n'
    code += f'        "customer_name": {json.dumps(cust_name)},\n'
    code += f'        "customer_email": {json.dumps(f"customer.{i+1}@shopsense.ai")},\n'
    code += f'        "rating": {rating},\n'
    code += f'        "title": {json.dumps(title_tpl)},\n'
    code += f'        "content": {json.dumps(body_tpl)},\n'
    code += f'        "is_verified_purchase": True,\n'
    code += f'        "helpful_votes": {(i * 7) % 45},\n'
    code += f'        "unhelpful_votes": {(i * 2) % 6},\n'
    code += f'        "aspect_ratings": {json.dumps(aspects)},\n'
    code += f'        "praises": {json.dumps(praises)},\n'
    code += f'        "complaints": {json.dumps(complaints)},\n'
    code += f'        "days_ago": {(i * 3) % 180}\n'
    code += "    },\n"

code += "]\n"

(BASE_DATA / 'reviews_corpus.py').write_text(code, encoding='utf-8')
print("Generated 1,500 aspect-based review corpus file successfully!")
