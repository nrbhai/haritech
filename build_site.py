import csv
import os

def generate_products_html(products, limit=None):
    html = ""
    display_products = products[:limit] if limit else products
    for p in display_products:
        specs_html = ""
        if p['Features']:
            for spec in p['Features'].split('|'):
                specs_html += f"                            <li>{spec.strip()}</li>\n"
        
        badge_html = ""
        if p['Badge']:
            badge_html = f'<div class="warranty-badge">{p["Badge"]}</div>'

        html += f"""
                <!-- {p['Name']} -->
                <div class="product-card">
                    <div class="product-image">
                        <img src="{p['Image']}" alt="{p['Name']}" loading="lazy">
                        {badge_html}
                    </div>
                    <div class="product-info">
                        <h3>{p['Name']}</h3>
                        <ul class="product-specs">
{specs_html}                        </ul>
                        <div class="product-price">₹{p['Price']}</div>
                        <a href="{p['LinkURL']}" target="_blank" class="btn btn-primary btn-small">{p['LinkText']}</a>
                    </div>
                </div>
"""
    return html

def generate_it_services_html(services):
    html = ""
    for s in services:
        features_html = ""
        if s['Features']:
            for feature in s['Features'].split('|'):
                features_html += f"                        <li>{feature.strip()}</li>\n"
        
        badge_html = ""
        featured_class = ""
        if s['Badge']:
            badge_html = f'<div class="service-badge">{s["Badge"]}</div>'
            featured_class = " featured"

        price_display = f"{s['PriceUnit']}{s['Price']}"
        if s['PriceUnit'] == "Starting at ₹":
             price_display = f"Starting at ₹{s['Price']}"

        html += f"""
                <!-- {s['Name']} -->
                <div class="service-card{featured_class}">
                    {badge_html}
                    <div class="service-icon">{s['Image']}</div>
                    <h3>{s['Name']}</h3>
                    <p>{s['Description']}</p>
                    <ul class="service-features">
{features_html}                    </ul>
                    <div class="service-price">{price_display}</div>
                </div>
"""
    return html

def generate_web_services_html(services):
    html = ""
    for s in services:
        features_html = ""
        if s['Features']:
            for feature in s['Features'].split('|'):
                features_html += f"                        <li>{feature.strip()}</li>\n"
        
        badge_html = ""
        featured_class = ""
        if s['Badge']:
            badge_html = f'<div class="service-badge">{s["Badge"]}</div>'
            featured_class = " featured"
        
        # Web services use emojis in image field
        icon = s['Image'] 

        price_display = f"{s['PriceUnit']}{s['Price']}"
        if s['PriceUnit'] == "Starting at ₹":
             price_display = f"Starting at ₹{s['Price']}"
        elif s['PriceUnit'] == "/month":
             price_display = f"Starting at ₹{s['Price']}/month"

        html += f"""
                <!-- {s['Name']} -->
                <div class="service-card{featured_class}">
                    {badge_html}
                    <div class="service-icon">{icon}</div>
                    <h3>{s['Name']}</h3>
                    <p>{s['Description']}</p>
                    <ul class="service-features">
{features_html}                    </ul>
                    <div class="service-price">{price_display}</div>
                </div>
"""
    return html

def generate_web_packages_html(packages):
    html = ""
    for p in packages:
        features_html = ""
        if p['Features']:
            for feature in p['Features'].split('|'):
                features_html += f"                        <li>✓ {feature.strip()}</li>\n"
        
        badge_html = ""
        featured_class = ""
        btn_class = "btn-secondary"
        if p['Badge']:
            badge_html = f'<div class="package-badge">{p["Badge"]}</div>'
            featured_class = " featured"
            btn_class = "btn-primary"

        html += f"""
                <!-- {p['Name']} -->
                <div class="package-card{featured_class}">
                    {badge_html}
                    <h3>{p['Name']}</h3>
                    <div class="package-price">{p['PriceUnit']}{p['Price']}</div>
                    <p class="package-subtitle">{p['Description']}</p>
                    <ul class="package-features">
{features_html}                    </ul>
                    <a href="{p['LinkURL']}" target="_blank" class="btn {btn_class}">{p['LinkText']}</a>
                </div>
"""
    return html

def update_file(filename, replacements):
    print(f"Reading {filename}...")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
        return

    new_content = content
    for marker_name, new_html in replacements.items():
        start_marker = f"<!-- DYNAMIC_{marker_name}_START -->"
        end_marker = f"<!-- DYNAMIC_{marker_name}_END -->"
        
        start_idx = new_content.find(start_marker)
        end_idx = new_content.find(end_marker)
        
        if start_idx == -1 or end_idx == -1:
            # print(f"Info: Markers for {marker_name} not found in {filename}. Skipping section.")
            continue
        
        new_content = new_content[:start_idx + len(start_marker)] + "\n" + new_html + "                " + new_content[end_idx:]

    if new_content != content:
        print(f"Updating {filename}...")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ {filename} updated.")
    else:
        print(f"ℹ️  No changes needed for {filename} (or markers missing).")

def build_site():
    print("Reading data.csv...")
    products = []
    it_services = []
    web_services = []
    web_packages = []

    try:
        with open('data.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Type'] == 'Product':
                    products.append(row)
                elif row['Type'] == 'Service' and row['Category'] == 'IT Service':
                    it_services.append(row)
                elif row['Type'] == 'Service' and row['Category'] == 'Web Service':
                    web_services.append(row)
                elif row['Type'] == 'Service' and row['Category'] == 'Web Package':
                    web_packages.append(row)
    except FileNotFoundError:
        print("Error: data.csv not found!")
        return

    print(f"Found {len(products)} products, {len(it_services)} IT services, {len(web_services)} web services, {len(web_packages)} web packages.")

    # Generate HTML content
    products_html_all = generate_products_html(products)
    products_html_home = generate_products_html(products, limit=8)
    it_services_html = generate_it_services_html(it_services)
    web_services_html = generate_web_services_html(web_services)
    web_packages_html = generate_web_packages_html(web_packages)

    # Define replacements for each section
    # Replacements dict: { MARKER_NAME: HTML_CONTENT }
    
    # 1. Update index.html (One Page)
    # index.html uses: PRODUCTS, IT_SERVICES, WEB_PACKAGES
    # It does NOT use WEB_SERVICES currently.
    update_file('index.html', {
        'PRODUCTS': products_html_home,
        'IT_SERVICES': it_services_html,
        'WEB_PACKAGES': web_packages_html
    })

    # 2. Update products.html
    # products.html uses: PRODUCTS
    update_file('products.html', {
        'PRODUCTS': products_html_all
    })

    # 3. Update website-solutions.html
    # website-solutions.html uses: WEB_SERVICES, WEB_PACKAGES
    update_file('website-solutions.html', {
        'WEB_SERVICES': web_services_html,
        'WEB_PACKAGES': web_packages_html
    })
    
    print("\n🎉 Build complete! All pages synced with data.csv.")

if __name__ == "__main__":
    build_site()
