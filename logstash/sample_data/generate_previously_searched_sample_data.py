import json
from datetime import datetime, timedelta
import random

emails = [
    "prasadcoorgi@yahoo.com",
    "prasadmuddappa@gmail.com",
    "prasadcoorgi@outlook.com",
    "prasadcoorgi@hotmail.com",
    "pramodcoorgi@yahoo.com",
    "pramodcoorgi@gmail.com",
    "lavanya6_12@yahoo.com",
    "pramodcoorgi@hotmail.com",
    "pramodcoorgi@gmail.com",
    "pramodcoorgi@outlook.com",
]
phone_numbers = ["9845893885", "9980200445", "9945303149", "1234500004", "1234500005"]
names = [
    "Prasad CM",
    "Prasad Chekkera Muddappa",
    "Pramod CM",
    "Lavanya PB",
    "Manith CM",
    "Novika Muthappa",
]

# Linked scenarios for search_text, type, product_id, category_id, icon_url
search_scenarios = [
    {
        "search_text": "Nike Red Shoes",
        "type": "product",
        "product_id": "prod-001",
        "category_id": "",
        "icon_url": "assets/icons/products/bath.jpg",
    },
    {
        "search_text": "Levis Blue Jeans",
        "type": "product",
        "product_id": "prod-002",
        "category_id": "",
        "icon_url": "assets/icons/products/bath.jpg",
    },
    {
        "search_text": "Puma Green Shirt",
        "type": "product",
        "product_id": "prod-003",
        "category_id": "",
        "icon_url": "assets/icons/products/bath.jpg",
    },
    {
        "search_text": "sugar",
        "type": "category",
        "product_id": "",
        "category_id": "cat-001",
        "icon_url": "assets/icons/products/biscuit.jpg",
    },
    {
        "search_text": "shampoo",
        "type": "category",
        "product_id": "",
        "category_id": "cat-002",
        "icon_url": "assets/icons/products/hair.jpg",
    },
    {
        "search_text": "goodlife",
        "type": "brand",
        "product_id": "",
        "category_id": "",
        "icon_url": "assets/icons/products/dairy.jpg",
    },
    {
        "search_text": "nandini",
        "type": "brand",
        "product_id": "",
        "category_id": "",
        "icon_url": "assets/icons/products/dairy.jpg",
    },
    {
        "search_text": "kitkat",
        "type": "product",
        "product_id": "prod-004",
        "category_id": "",
        "icon_url": "assets/icons/products/biscuit.jpg",
    },
    {
        "search_text": "chocolate",
        "type": "category",
        "product_id": "",
        "category_id": "cat-003",
        "icon_url": "assets/icons/products/biscuit.jpg",
    },
    {
        "search_text": "best sellers",
        "type": "collection",
        "product_id": "",
        "category_id": "",
        "icon_url": "",
    },
    {
        "search_text": "organic",
        "type": "tag",
        "product_id": "",
        "category_id": "",
        "icon_url": "",
    },
    {
        "search_text": "vegan",
        "type": "tag",
        "product_id": "",
        "category_id": "",
        "icon_url": "",
    },
    {
        "search_text": "new arrivals",
        "type": "collection",
        "product_id": "",
        "category_id": "",
        "icon_url": "",
    },
    {
        "search_text": "buy 1 get 1 free",
        "type": "promotion",
        "product_id": "",
        "category_id": "",
        "icon_url": "",
    },
    {
        "search_text": "affordable dresses under 1000",
        "type": "keyword",
        "product_id": "",
        "category_id": "",
        "icon_url": "",
    },
    {
        "search_text": "eco friendly kitchen items",
        "type": "keyword",
        "product_id": "",
        "category_id": "",
        "icon_url": "",
    },
    {
        "search_text": "gifts for mother’s day",
        "type": "keyword",
        "product_id": "",
        "category_id": "",
        "icon_url": "",
    },
]

search_counts = [0, 1, 20, 30, 4, 0, 6, 70, 800, 90, 10]

base_date = datetime(2024, 3, 1)

with open("previously_searched_sample.json", "w") as f:
    for i in range(1, 101):
        email = random.choice(emails)
        phone_number = random.choice(phone_numbers)
        name = random.choice(names)
        scenario = random.choice(search_scenarios)
        search_count = random.choice(search_counts)
        search_text = scenario["search_text"]
        type_ = scenario["type"]
        icon_url = scenario["icon_url"]
        product_id = scenario["product_id"]
        category_id = scenario["category_id"]
        slug = search_text.lower().replace(" ", "_")
        doc = {
            "phone_number": phone_number,
            "email": email,
            "name": name,
            "updated_at": (base_date + timedelta(days=i)).strftime(
                "%Y-%m-%dT12:00:00Z"
            ),
            "search_text": search_text,
            "icon_url": icon_url,
            "type": type_,
            "slug": slug,
            "product_id": product_id,
            "category_id": category_id,
            "search_count": search_count,
        }
        f.write(json.dumps(doc) + "\n")
