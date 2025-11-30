from database import SessionLocal
from models import Product, Category

def verify_data():
    db = SessionLocal()
    
    try:
        print("=== Categories ===")
        categories = db.query(Category).all()
        for cat in categories:
            print(f"ID: {cat.id}, Name: {cat.name}")
        
        print("\n=== Products ===")
        products = db.query(Product).all()
        for prod in products:
            print(f"ID: {prod.id}, Name: {prod.name}, Price: {prod.price}, Stock: {prod.stock}, Category ID: {prod.category_id}")
        
        print(f"\nTotal categories: {len(categories)}")
        print(f"Total products: {len(products)}")
        
        # Test the JOIN for the required screenshot
        print("\n=== JOIN Query Results (for db_proof.png) ===")
        joined_data = db.query(Product, Category.name.label('category_name'))\
            .join(Category, Product.category_id == Category.id)\
            .all()
        
        for product, category_name in joined_data:
            print(f"Product: {product.name}, Category: {category_name}, Price: {product.price}, Stock: {product.stock}")
        
    except Exception as e:
        print(f"Verification failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    verify_data()
