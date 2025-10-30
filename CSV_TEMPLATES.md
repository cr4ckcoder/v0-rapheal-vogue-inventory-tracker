# CSV Upload Templates

## 1. Initial Inventory Import

**Endpoint:** `POST /inventory/import`

**CSV Columns:**
- `ean` (required) - Product EAN/SKU
- `style_name` (required) - Product style name
- `size` (required) - Size
- `brand` (required) - Brand name
- `style_design_code` (optional) - Design code
- `model_no` (optional) - Model number
- `store_id` (required) - Store ID (1-4)
- `quantity` (required) - Initial quantity (must be > 0)

**Example:**
\`\`\`csv
ean,style_name,size,brand,style_design_code,model_no,store_id,quantity
EAN001,Dress A,M,Rapheal,RC001,M001,1,50
EAN001,Dress A,M,Rapheal,RC001,M001,2,30
EAN002,Shirt B,L,Vogue,VC002,M002,1,25
\`\`\`

---

## 2. Store Transfer

**Endpoint:** `POST /inventory/transfer`

**CSV Columns:**
- `ean` (required) - Product EAN/SKU
- `source_store_id` (required) - Source store ID
- `destination_store_id` (required) - Destination store ID
- `quantity` (required) - Quantity to transfer (must be > 0 and <= available stock)

**Example:**
\`\`\`csv
ean,source_store_id,destination_store_id,quantity
EAN001,1,2,10
EAN002,1,3,5
EAN001,2,4,8
\`\`\`

**Validation:**
- Source store must have sufficient quantity
- Both stores must exist
- Product must exist in inventory

---

## 3. End-of-Day Sales

**Endpoint:** `POST /inventory/sales`

**CSV Columns:**
- `ean` (required) - Product EAN/SKU
- `store_id` (required) - Store where sale occurred
- `quantity_sold` (required) - Quantity sold (must be > 0 and <= available stock)

**Example:**
\`\`\`csv
ean,store_id,quantity_sold
EAN001,1,5
EAN002,1,3
EAN001,2,2
\`\`\`

**Validation:**
- Store must have sufficient quantity
- Store must exist
- Product must exist in inventory

---

## Error Handling

All endpoints return detailed error reports:

\`\`\`json
{
  "success_count": 2,
  "error_count": 1,
  "errors": [
    {
      "row": 3,
      "error": "Insufficient stock. Available: 10, Requested: 15"
    }
  ],
  "status": "partial"
}
\`\`\`

**Common Errors:**
- `Missing required fields` - CSV missing required columns
- `Invalid store_id or quantity format` - Non-numeric values
- `Quantity must be greater than 0` - Zero or negative quantity
- `Store X does not exist` - Invalid store ID
- `Product EAN does not exist` - Product not in system
- `Insufficient stock` - Not enough inventory for transfer/sale
