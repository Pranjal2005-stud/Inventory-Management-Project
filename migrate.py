import json
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Category, Product

def migrate_data():
    # Create tables
    from models import Base
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Load categories and create a name-to-id mapping
        print("Loading categories...")
        with open('categories.json', 'r') as f:
            categories_data = json.load(f)
        
        category_name_to_id = {}
        for cat_data in categories_data:
            if isinstance(cat_data, dict):
                category_id = cat_data.get('id')
                category_name = cat_data.get('name')
                
                if category_id is not None and category_name is not None:
                    category = Category(id=category_id, name=category_name)
                    db.merge(category)
                    category_name_to_id[category_name] = category_id
                    print(f"Added category: {category_name} (ID: {category_id})")
        
        db.commit()
        print("Categories migrated successfully!")
        print(f"Category mapping: {category_name_to_id}")
        
        # Load products and map category names to IDs
        print("\nLoading products...")
        with open('inventory.json', 'r') as f:
            products_data = json.load(f)
        
        products_added = 0
        for prod_data in products_data:
            if isinstance(prod_data, dict):
                product_id = prod_data.get('id')
                product_name = prod_data.get('name')
                product_price = prod_data.get('price')
                product_stock = prod_data.get('stock')
                category_name = prod_data.get('category')  # Get category name from JSON
                
                # Map category name to category ID
                category_id = category_name_to_id.get(category_name)
                
                if all([product_id, product_name, product_price is not None, product_stock is not None, category_id]):
                    product = Product(
                        id=product_id,
                        name=product_name,
                        price=float(product_price),
                        stock=int(product_stock),
                        category_id=int(category_id)
                    )
                    db.merge(product)
                    products_added += 1
                    print(f"Added product: {product_name} (Category: '{category_name}' → ID: {category_id})")
                else:
                    print(f"Skipping invalid product data: {prod_data}")
                    if not category_id:
                        print(f"  Could not find category ID for: '{category_name}'")
        
        db.commit()
        print(f"\nMigration completed successfully!")
        print(f"Products added: {products_added}")
        
    except Exception as e:
        db.rollback()
        print(f"Migration failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    migrate_data()
