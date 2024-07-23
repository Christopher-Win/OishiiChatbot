from config import app, db
from models import MenuItem

def upload_menu_items():
    # Define your menu items
    menu_items = [
        {'name': '42 Roll', 'description': 'spicy shrimp and tempura flakes, topped with avocado and crabmeat mix, serrano peppers and sriracha'},
        {'name': '44 Roll', 'description': 'spicy shrimp and tempura flakes, topped with avocado and crabmeat mix, thinly sliced lemon, yellowtail and serrano peppers, drizzled with eel sauce and spicy ponzu sauce'},
        {'name': 'Ceviche', 'description': 'yellowtail, snapper, scallops and avocado, mixed with olive oil, salt, pico de gallo, serrano peppers, cilantro, smelt fish roe and chili powder'},
        # Add more items as needed
    ]
  # Upload menu items to the database
    with app.app_context():
        db.create_all()
        for item in menu_items:
            menu_item = MenuItem(name=item['name'], description=item['description'])
            db.session.add(menu_item)
        db.session.commit()
        print('Menu items uploaded successfully!')

if __name__ == '__main__':
    upload_menu_items()