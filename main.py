from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import csv
import io
from datetime import datetime
from database import init_db, seed_initial_data, get_db
from models import (
    UserLogin, TokenResponse, UploadSummary, StockStatusResponse, 
    AnalyticsResponse, ImportRow, TransferRow, SalesRow
)
from auth import create_access_token, authenticate_user, verify_token

app = FastAPI(title="Rapheal Vogue Inventory Tracker")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup():
    init_db()
    seed_initial_data()

# ============ AUTH ENDPOINTS ============

@app.post("/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """Authenticate user and return JWT token."""
    if not authenticate_user(credentials.username, credentials.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = create_access_token(credentials.username)
    return TokenResponse(access_token=token)

# ============ BULK UPLOAD ENDPOINTS ============

@app.post("/inventory/import")
async def import_inventory(file: UploadFile = File(...), username: str = Depends(verify_token)):
    """
    Bulk import initial inventory from CSV.
    CSV columns: ean, style_name, size, brand, style_design_code, model_no, store_id, quantity
    """
    errors = []
    success_count = 0
    
    try:
        contents = await file.read()
        stream = io.StringIO(contents.decode('utf-8'))
        reader = csv.DictReader(stream)
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                try:
                    # Validate required fields
                    ean = row.get('ean', '').strip()
                    store_id = row.get('store_id', '').strip()
                    quantity = row.get('quantity', '').strip()
                    
                    if not ean or not store_id or not quantity:
                        errors.append({"row": row_num, "error": "Missing required fields"})
                        continue
                    
                    # Validate data types
                    try:
                        store_id = int(store_id)
                        quantity = int(quantity)
                    except ValueError:
                        errors.append({"row": row_num, "error": "Invalid store_id or quantity format"})
                        continue
                    
                    # Validate quantity > 0
                    if quantity <= 0:
                        errors.append({"row": row_num, "error": "Quantity must be greater than 0"})
                        continue
                    
                    # Check if store exists
                    cursor.execute("SELECT store_id FROM store WHERE store_id = ?", (store_id,))
                    if not cursor.fetchone():
                        errors.append({"row": row_num, "error": f"Store {store_id} does not exist"})
                        continue
                    
                    # Check if product exists, if not create it
                    cursor.execute("SELECT ean FROM product WHERE ean = ?", (ean,))
                    if not cursor.fetchone():
                        cursor.execute("""
                            INSERT INTO product (ean, style_name, size, brand, style_design_code, model_no)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (
                            ean,
                            row.get('style_name', '').strip(),
                            row.get('size', '').strip(),
                            row.get('brand', '').strip(),
                            row.get('style_design_code', '').strip() or None,
                            row.get('model_no', '').strip() or None
                        ))
                    
                    # Insert or update inventory
                    cursor.execute("""
                        INSERT INTO inventory (product_ean, store_id, quantity)
                        VALUES (?, ?, ?)
                        ON CONFLICT(product_ean, store_id) DO UPDATE SET quantity = quantity + excluded.quantity
                    """, (ean, store_id, quantity))
                    
                    # Log transaction
                    cursor.execute("""
                        INSERT INTO transaction (product_ean, store_id, quantity_change, transaction_type)
                        VALUES (?, ?, ?, 'Import')
                    """, (ean, store_id, quantity))
                    
                    success_count += 1
                
                except Exception as e:
                    errors.append({"row": row_num, "error": str(e)})
            
            conn.commit()
        
        status_code = "success" if not errors else "partial"
        return UploadSummary(
            success_count=success_count,
            error_count=len(errors),
            errors=errors,
            status=status_code
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"File processing error: {str(e)}")

@app.post("/inventory/transfer")
async def transfer_inventory(file: UploadFile = File(...), username: str = Depends(verify_token)):
    """
    Bulk transfer inventory between stores from CSV.
    CSV columns: ean, source_store_id, destination_store_id, quantity
    """
    errors = []
    success_count = 0
    
    try:
        contents = await file.read()
        stream = io.StringIO(contents.decode('utf-8'))
        reader = csv.DictReader(stream)
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            for row_num, row in enumerate(reader, start=2):
                try:
                    ean = row.get('ean', '').strip()
                    source_store_id = row.get('source_store_id', '').strip()
                    destination_store_id = row.get('destination_store_id', '').strip()
                    quantity = row.get('quantity', '').strip()
                    
                    # Validate required fields
                    if not all([ean, source_store_id, destination_store_id, quantity]):
                        errors.append({"row": row_num, "error": "Missing required fields"})
                        continue
                    
                    # Validate data types
                    try:
                        source_store_id = int(source_store_id)
                        destination_store_id = int(destination_store_id)
                        quantity = int(quantity)
                    except ValueError:
                        errors.append({"row": row_num, "error": "Invalid store_id or quantity format"})
                        continue
                    
                    # Validate quantity > 0
                    if quantity <= 0:
                        errors.append({"row": row_num, "error": "Quantity must be greater than 0"})
                        continue
                    
                    # Check if stores exist
                    cursor.execute("SELECT store_id FROM store WHERE store_id IN (?, ?)", 
                                 (source_store_id, destination_store_id))
                    if len(cursor.fetchall()) != 2:
                        errors.append({"row": row_num, "error": "Invalid source or destination store"})
                        continue
                    
                    # Check if product exists
                    cursor.execute("SELECT ean FROM product WHERE ean = ?", (ean,))
                    if not cursor.fetchone():
                        errors.append({"row": row_num, "error": f"Product {ean} does not exist"})
                        continue
                    
                    # Check if source has sufficient quantity
                    cursor.execute("""
                        SELECT quantity FROM inventory 
                        WHERE product_ean = ? AND store_id = ?
                    """, (ean, source_store_id))
                    inv_row = cursor.fetchone()
                    current_qty = inv_row[0] if inv_row else 0
                    
                    if current_qty < quantity:
                        errors.append({
                            "row": row_num, 
                            "error": f"Insufficient stock. Available: {current_qty}, Requested: {quantity}"
                        })
                        continue
                    
                    # Perform transfer (deduct from source, add to destination)
                    cursor.execute("""
                        UPDATE inventory SET quantity = quantity - ?
                        WHERE product_ean = ? AND store_id = ?
                    """, (quantity, ean, source_store_id))
                    
                    cursor.execute("""
                        INSERT INTO inventory (product_ean, store_id, quantity)
                        VALUES (?, ?, ?)
                        ON CONFLICT(product_ean, store_id) DO UPDATE SET quantity = quantity + excluded.quantity
                    """, (ean, destination_store_id, quantity))
                    
                    # Log transactions
                    cursor.execute("""
                        INSERT INTO transaction (product_ean, store_id, quantity_change, transaction_type)
                        VALUES (?, ?, ?, 'Transfer')
                    """, (ean, source_store_id, -quantity))
                    
                    cursor.execute("""
                        INSERT INTO transaction (product_ean, store_id, quantity_change, transaction_type)
                        VALUES (?, ?, ?, 'Transfer')
                    """, (ean, destination_store_id, quantity))
                    
                    success_count += 1
                
                except Exception as e:
                    errors.append({"row": row_num, "error": str(e)})
            
            conn.commit()
        
        status_code = "success" if not errors else "partial"
        return UploadSummary(
            success_count=success_count,
            error_count=len(errors),
            errors=errors,
            status=status_code
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"File processing error: {str(e)}")

@app.post("/inventory/sales")
async def record_sales(file: UploadFile = File(...), username: str = Depends(verify_token)):
    """
    Bulk record EOD sales from CSV.
    CSV columns: ean, store_id, quantity_sold
    """
    errors = []
    success_count = 0
    
    try:
        contents = await file.read()
        stream = io.StringIO(contents.decode('utf-8'))
        reader = csv.DictReader(stream)
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            for row_num, row in enumerate(reader, start=2):
                try:
                    ean = row.get('ean', '').strip()
                    store_id = row.get('store_id', '').strip()
                    quantity_sold = row.get('quantity_sold', '').strip()
                    
                    # Validate required fields
                    if not all([ean, store_id, quantity_sold]):
                        errors.append({"row": row_num, "error": "Missing required fields"})
                        continue
                    
                    # Validate data types
                    try:
                        store_id = int(store_id)
                        quantity_sold = int(quantity_sold)
                    except ValueError:
                        errors.append({"row": row_num, "error": "Invalid store_id or quantity format"})
                        continue
                    
                    # Validate quantity > 0
                    if quantity_sold <= 0:
                        errors.append({"row": row_num, "error": "Quantity sold must be greater than 0"})
                        continue
                    
                    # Check if store exists
                    cursor.execute("SELECT store_id FROM store WHERE store_id = ?", (store_id,))
                    if not cursor.fetchone():
                        errors.append({"row": row_num, "error": f"Store {store_id} does not exist"})
                        continue
                    
                    # Check if product exists
                    cursor.execute("SELECT ean FROM product WHERE ean = ?", (ean,))
                    if not cursor.fetchone():
                        errors.append({"row": row_num, "error": f"Product {ean} does not exist"})
                        continue
                    
                    # Check if final quantity would be >= 0
                    cursor.execute("""
                        SELECT quantity FROM inventory 
                        WHERE product_ean = ? AND store_id = ?
                    """, (ean, store_id))
                    inv_row = cursor.fetchone()
                    current_qty = inv_row[0] if inv_row else 0
                    
                    if current_qty < quantity_sold:
                        errors.append({
                            "row": row_num, 
                            "error": f"Insufficient stock. Available: {current_qty}, Sold: {quantity_sold}"
                        })
                        continue
                    
                    # Deduct from inventory
                    cursor.execute("""
                        UPDATE inventory SET quantity = quantity - ?
                        WHERE product_ean = ? AND store_id = ?
                    """, (quantity_sold, ean, store_id))
                    
                    # Log transaction
                    cursor.execute("""
                        INSERT INTO transaction (product_ean, store_id, quantity_change, transaction_type)
                        VALUES (?, ?, ?, 'Sale')
                    """, (ean, store_id, -quantity_sold))
                    
                    success_count += 1
                
                except Exception as e:
                    errors.append({"row": row_num, "error": str(e)})
            
            conn.commit()
        
        status_code = "success" if not errors else "partial"
        return UploadSummary(
            success_count=success_count,
            error_count=len(errors),
            errors=errors,
            status=status_code
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"File processing error: {str(e)}")

# ============ VIEW ENDPOINTS ============

@app.get("/inventory/stock-status", response_model=list[StockStatusResponse])
async def get_stock_status(username: str = Depends(verify_token)):
    """Get current stock levels across all stores."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT p.ean, p.style_name, p.brand
            FROM product p
            ORDER BY p.ean
        """)
        products = cursor.fetchall()
        
        result = []
        for product in products:
            ean, style_name, brand = product
            cursor.execute("""
                SELECT store_id, quantity FROM inventory
                WHERE product_ean = ?
                ORDER BY store_id
            """, (ean,))
            
            stores = {}
            total = 0
            for store_id, qty in cursor.fetchall():
                stores[str(store_id)] = qty
                total += qty
            
            result.append(StockStatusResponse(
                ean=ean,
                style_name=style_name,
                brand=brand,
                stores=stores,
                total_quantity=total
            ))
        
        return result

@app.get("/inventory/analytics")
async def get_analytics(
    store_id: int = None,
    start_date: str = None,
    end_date: str = None,
    username: str = Depends(verify_token)
):
    """Get most/least moving items with optional filters."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Build query with filters
        query = """
            SELECT product_ean, SUM(ABS(quantity_change)) as total_movement
            FROM transaction
            WHERE transaction_type IN ('Sale', 'Transfer')
        """
        params = []
        
        if store_id:
            query += " AND store_id = ?"
            params.append(store_id)
        
        if start_date:
            query += " AND DATE(timestamp) >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND DATE(timestamp) <= ?"
            params.append(end_date)
        
        query += " GROUP BY product_ean ORDER BY total_movement DESC"
        
        cursor.execute(query, params)
        movements = cursor.fetchall()
        
        most_moving = []
        least_moving = []
        
        for i, (ean, movement) in enumerate(movements):
            cursor.execute("SELECT style_name, brand FROM product WHERE ean = ?", (ean,))
            product = cursor.fetchone()
            if product:
                item = {"ean": ean, "style_name": product[0], "brand": product[1], "movement": movement}
                if i < 5:
                    most_moving.append(item)
                if i >= len(movements) - 5:
                    least_moving.append(item)
        
        least_moving.reverse()
        
        return AnalyticsResponse(most_moving=most_moving, least_moving=least_moving)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
