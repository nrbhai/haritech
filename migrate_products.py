import re
import csv
import os

def migrate():
    print("Reading products.html...")
    try:
        with open('products.html', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("Error: products.html not found!")
        return

    # Split to get only static part
    parts = content.split('<!-- DYNAMIC_PRODUCTS_END -->')
    if len(parts) < 2:
        print("Error: Could not find DYNAMIC_PRODUCTS_END marker.")
        return
    
    static_content = parts[1]

    # Regex patterns
    # Note: The HTML structure varies slightly (h2 vs h3).
    # We'll try to match product blocks.
    
    # We iterate over product-cards
    product_cards = static_content.split('<div class="product-card">')
    
    new_products = []
    
    # Skip the first split item as it's before the first card
    for card in product_cards[1:]:
        # Extract ID/Name
        # Try h2 first, then h3
        name_match = re.search(r'<h[23]>(.*?)</h[23]>', card)
        if not name_match:
            continue # Not a valid product block
        name = name_match.group(1).strip()
        
        # Extract Image
        img_match = re.search(r'<img src="(.*?)"', card)
        image = img_match.group(1) if img_match else ""
        
        # Extract Price
        price_match = re.search(r'<div class="product-price">₹?(.*?)</div>', card)
        price_raw = price_match.group(1).strip() if price_match else "0"
        # Clean price (remove commas)
        price = price_raw.replace(',', '')
        
        # Extract Features
        specs_match = re.search(r'<ul class="product-specs">(.*?)</ul>', card, re.DOTALL)
        features = ""
        if specs_match:
            specs_content = specs_match.group(1)
            # Find all li
            lis = re.findall(r'<li>(.*?)</li>', specs_content)
            features = " | ".join([li.strip() for li in lis])
            
        # Extract Link
        link_match = re.search(r'<a href="(.*?)"', card)
        link_url = link_match.group(1) if link_match else ""
        
        # Extract Link Text
        link_text_match = re.search(r'<a .*?>(.*?)</a>', card)
        link_text = link_text_match.group(1) if link_text_match else "Buy Now"
        
        # Badge (Optional, default empty)
        badge = ""

        # Create CSV Row dict
        row = {
            'Type': 'Product',
            'Category': 'Laptops', # Default category
            'Name': name,
            'Price': price,
            'PriceUnit': '₹',
            'Description': '', # Description is implicit in features usually
            'Features': features,
            'Image': image,
            'Badge': badge,
            'LinkText': link_text,
            'LinkURL': link_url
        }
        
        new_products.append(row)
        print(f"Parsed: {name}")

    if not new_products:
        print("No new products found to migrate.")
        return

    # Check existing data.csv to avoid duplicates
    existing_names = set()
    try:
        with open('data.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                if row['Type'] == 'Product':
                    existing_names.add(row['Name'])
    except FileNotFoundError:
        print("data.csv not found, starting fresh?")
        return

    # Append new products
    added_count = 0
    with open('data.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        for p in new_products:
            if p['Name'] not in existing_names:
                writer.writerow(p)
                added_count += 1
                print(f"Added to CSV: {p['Name']}")
            else:
                print(f"Skipped duplicate: {p['Name']}")

    print(f"\nMigration Complete. Added {added_count} new products.")

if __name__ == "__main__":
    migrate()
