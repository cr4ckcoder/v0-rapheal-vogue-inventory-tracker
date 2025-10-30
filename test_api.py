"""
Quick test script for API endpoints.
Run: python test_api.py
"""
import requests
import csv
import io
import json

BASE_URL = "http://localhost:8000"
TOKEN = None

def login():
    """Test login endpoint."""
    global TOKEN
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": "admin", "password": "password123"}
    )
    if response.status_code == 200:
        TOKEN = response.json()["access_token"]
        print("✓ Login successful")
        return True
    else:
        print(f"✗ Login failed: {response.text}")
        return False

def create_test_csv(filename, rows):
    """Create a test CSV file."""
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"✓ Created {filename}")

def test_import():
    """Test inventory import."""
    rows = [
        {"ean": "EAN001", "style_name": "Dress A", "size": "M", "brand": "Rapheal", 
         "style_design_code": "RC001", "model_no": "M001", "store_id": "1", "quantity": "50"},
        {"ean": "EAN002", "style_name": "Shirt B", "size": "L", "brand": "Vogue", 
         "style_design_code": "VC002", "model_no": "M002", "store_id": "1", "quantity": "30"},
    ]
    create_test_csv("test_import.csv", rows)
    
    with open("test_import.csv", "rb") as f:
        files = {"file": f}
        headers = {"Authorization": f"Bearer {TOKEN}"}
        response = requests.post(f"{BASE_URL}/inventory/import", files=files, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Import successful: {result['success_count']} rows")
        if result['errors']:
            print(f"  Errors: {result['errors']}")
    else:
        print(f"✗ Import failed: {response.text}")

def test_stock_status():
    """Test stock status endpoint."""
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(f"{BASE_URL}/inventory/stock-status", headers=headers)
    
    if response.status_code == 200:
        stocks = response.json()
        print(f"✓ Stock status retrieved: {len(stocks)} products")
        for stock in stocks[:2]:
            print(f"  - {stock['ean']}: {stock['total_quantity']} units")
    else:
        print(f"✗ Stock status failed: {response.text}")

def test_analytics():
    """Test analytics endpoint."""
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(f"{BASE_URL}/inventory/analytics", headers=headers)
    
    if response.status_code == 200:
        analytics = response.json()
        print(f"✓ Analytics retrieved")
        print(f"  Most moving: {len(analytics['most_moving'])} items")
        print(f"  Least moving: {len(analytics['least_moving'])} items")
    else:
        print(f"✗ Analytics failed: {response.text}")

if __name__ == "__main__":
    print("Testing Rapheal Vogue Inventory API\n")
    
    if login():
        test_import()
        test_stock_status()
        test_analytics()
    
    print("\nTest complete!")
