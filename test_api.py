import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    try:
        # Test GET /api/products
        print("=== Testing GET /api/products ===")
        response = requests.get(f"{base_url}/api/products")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            products = response.json()
            print(f"Retrieved {len(products)} products")
            for product in products[:2]:  # Show first 2 products
                print(f"  - {product['name']}: ${product['price']} (Stock: {product['stock']})")
        
        # Test POST /api/order
        print("\n=== Testing POST /api/order ===")
        order_data = {
            "product_id": 1,
            "quantity": 2
        }
        response = requests.post(f"{base_url}/api/order", json=order_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            order_result = response.json()
            print("Order successful!")
            print(f"Product: {order_result['product_name']}")
            print(f"Quantity: {order_result['quantity']}")
            print(f"Total Price: ${order_result['total_price']}")
            print(f"Remaining Stock: {order_result['remaining_stock']}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"API test failed: {e}")

if __name__ == "__main__":
    test_api()
