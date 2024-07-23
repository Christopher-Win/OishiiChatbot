from config import app, db
from models import MenuItem

def delete_menu_items():
    with app.app_context():
        db.create_all()
        menu_items = MenuItem.query.all()
        for item in menu_items:
            db.session.delete(item)
        db.session.commit()
        print('Menu items deleted successfully!')


if __name__ == '__main__':
    delete_menu_items()
    #upload_menu_items()