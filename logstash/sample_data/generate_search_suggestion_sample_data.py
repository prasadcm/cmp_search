import json
from datetime import datetime, timedelta
import random

# Linked items for name, type, product_id, category_id, icon_url
search_scenarios = [
    {
        "name": "Nike Red Shoes",
        "type": "product",
        "product_id": "prod-001",
        "category_id": "",
        "icon_url": "assets/icons/products/bath.jpg",
        "tags": ["shoe", "leather", "sport"],
    },
    {
        "name": "Levis Blue Jeans",
        "type": "product",
        "product_id": "prod-002",
        "category_id": "",
        "icon_url": "assets/icons/products/bath.jpg",
        "tags": ["jeans", "denim", "cotton"],
    },
    {
        "name": "Puma Green Shirt",
        "type": "product",
        "product_id": "prod-003",
        "category_id": "",
        "icon_url": "assets/icons/products/bath.jpg",
        "tags": ["shirt", "cotton", "casual"],
    },
    {
        "name": "sugar",
        "type": "category",
        "product_id": "",
        "category_id": "cat-001",
        "icon_url": "assets/icons/products/biscuit.jpg",
        "tags": ["biscuit", "chocolate", "snack"],
    },
    {
        "name": "madhur sugar",
        "type": "product",
        "product_id": "sugar-001",
        "category_id": "",
        "icon_url": "assets/icons/products/biscuit.jpg",
        "tags": ["sweet"],
    },
    {
        "name": "parrys",
        "type": "brand",
        "product_id": "",
        "category_id": "",
        "icon_url": "assets/icons/products/biscuit.jpg",
        "tags": ["sweet", "bestseller", "sugar"],
    },
    {
        "name": "shampoo",
        "type": "category",
        "product_id": "",
        "category_id": "cat-002",
        "icon_url": "assets/icons/products/hair.jpg",
        "tags": ["shampoo", "hair", "conditioner"],
    },
    {
        "name": "goodlife",
        "type": "brand",
        "product_id": "",
        "category_id": "",
        "icon_url": "assets/icons/products/dairy.jpg",
        "tags": ["milk", "dairy", "cheese"],
    },
    {
        "name": "nandini",
        "type": "brand",
        "product_id": "",
        "category_id": "",
        "icon_url": "assets/icons/products/dairy.jpg",
        "tags": ["milk", "dairy", "cheese"],
    },
    {
        "name": "kitkat",
        "type": "product",
        "product_id": "prod-004",
        "category_id": "",
        "icon_url": "assets/icons/products/biscuit.jpg",
        "tags": ["biscuit", "chocolate", "snack"],
    },
    {
        "name": "chocolate",
        "type": "category",
        "product_id": "",
        "category_id": "cat-003",
        "icon_url": "assets/icons/products/biscuit.jpg",
        "tags": ["chocolate", "snack", "sweet"],
    },
    {
        "name": "best sellers",
        "type": "collection",
        "product_id": "",
        "category_id": "",
        "icon_url": "",
    },
    {
        "name": "organic",
        "type": "tag",
        "product_id": "",
        "category_id": "",
        "icon_url": "",
    },
    {
        "name": "vegan",
        "type": "tag",
        "product_id": "",
        "category_id": "",
        "icon_url": "",
    },
    {
        "name": "new arrivals",
        "type": "collection",
        "product_id": "",
        "category_id": "",
        "icon_url": "",
    },
    {
        "name": "buy 1 get 1 free",
        "type": "promotion",
        "product_id": "",
        "category_id": "",
        "icon_url": "",
    },
    {
        "name": "affordable dresses under 1000",
        "type": "keyword",
        "product_id": "",
        "category_id": "",
        "icon_url": "",
    },
    {
        "name": "eco friendly kitchen items",
        "type": "keyword",
        "product_id": "",
        "category_id": "",
        "icon_url": "",
    },
]

search_counts = [0, 1, 20, 30, 4, 0, 6, 70, 800, 90, 10]

bestsellers = [True, False]
new_arrivals = [True, False]
featureds = [True, False]
in_stocks = [True, False]
discounts = [10.0, 20.0, 30.0, 40.0, 50.0]

with open("search_suggestion_sample.json", "w") as f:
    for i in range(1, 101):
        scenario = random.choice(search_scenarios)
        search_count = random.choice(search_counts)
        name = scenario["name"]
        type_ = scenario["type"]
        icon_url = scenario["icon_url"]
        product_id = scenario["product_id"]
        category_id = scenario["category_id"]
        tags = scenario.get("tags", [])
        is_bestseller = random.choice(bestsellers)
        new_arrival = random.choice(new_arrivals)
        is_featured = random.choice(featureds)
        in_stock = random.choice(in_stocks)
        discount = random.choice(discounts)
        slug = name.lower().replace(" ", "_")
        doc = {
            "name": name,
            "icon_url": icon_url,
            "type": type_,
            "slug": slug,
            "product_id": product_id,
            "category_id": category_id,
            "search_count": search_count,
            "is_bestseller": is_bestseller,
            "new_arrival": new_arrival,
            "is_featured": is_featured,
            "in_stock": in_stock,
            "discount": discount,
            "tags": tags,
        }
        f.write(json.dumps(doc) + "\n")
