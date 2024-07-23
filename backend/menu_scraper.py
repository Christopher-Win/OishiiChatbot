import requests
from bs4 import BeautifulSoup
from models import MenuItem
from config import db, app

def convert_price(price_str):
    prices = []
    if '|' in price_str:
        parts = price_str.split('|')
        for part in parts:
            if part.strip().upper() == 'MKT' or part.strip() == '':
                prices.append(0.0)  # Convert 'MKT' or empty string to 0.0
            else:
                try:
                    prices.append(float(part.strip().replace('$', '').replace(',', '')))
                except ValueError:
                    raise ValueError(f"Could not convert string to float: '{part}'")
    else:
        if price_str.strip().upper() == 'MKT' or price_str.strip() == '':
            prices.append(0.0)  # Convert 'MKT' or empty string to 0.0
        else:
            try:
                prices.append(float(price_str.replace('$', '').replace(',', '')))
            except ValueError:
                raise ValueError(f"Could not convert string to float: '{price_str}'")
    return prices
# Scrape the menu from the given URL
def scrape_menu(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        menu_items = []
        for item_div in soup.select('.item'):
            name = item_div.find('h4').text.strip()
            price_str = item_div.find('span', class_='price').text.strip()
            prices = convert_price(price_str)
            description = item_div.find('p').text.strip()

            # Handle the case where category is not available
            category = item_div.find_previous('h3').text.strip() if item_div.find_previous('h3') else None
            if len(prices) > 1:
            # Handle multiple prices (e.g., regular and spicy)
                for i, price in enumerate(prices):
                    suffix = "Regular" if i == 0 else "Custom"
                    # Duplicate item for each price, appending a suffix to differentiate
                    if '|' in name:
                        menu_items.append(MenuItem(name=name.split('|')[0].strip() if i == 0 else name.split('|')[1].strip(), description=description, price=price, category=category))
                    else:
                        menu_items.append(MenuItem(name=name+" "+suffix, description=description, price=price, category=category))
                  # menu_items.append(MenuItem(name=name+" "+suffix, description=description, price=price, category=category))
             # Single price, add directly
            else:
                single_price = prices[0] if prices else None
                menu_items.append(MenuItem(name=name, description=description, price=single_price, category=category))
        return menu_items
    else:
        raise Exception('Failed to retrieve the webpage')
# Update the menu in the database with the scraped data
def update_menu(url): 
    with app.app_context(): # create an application context before interacting with the database
        db.create_all()
        menu_items = scrape_menu(url) 
        for item in menu_items:
            existing_item = MenuItem.query.filter_by(name=item.name, category = item.category).first()
            if existing_item:
                existing_item.description = item.description
                existing_item.price = item.price
            else:
                db.session.add(item)
        db.session.commit()
        print("Menu data scraped and stored successfully.")

if __name__ == '__main__':
    menu_url = 'https://oishiirestaurants.com/OishiiMenu.html'  # URL of the menu page
    update_menu(menu_url)
