# Rapheal Vogue Event Inventory Tracker

A high-efficiency inventory management system for pop-up events, built with Python/FastAPI backend and Vue 3 frontend.

## Features

- **Bulk CSV Upload** - Import, transfer, and record sales in bulk
- **Real-time Stock Tracking** - View inventory across 4 event stores
- **Sales Analytics** - Track most/least moving items with date/store filtering
- **JWT Authentication** - Secure single-user access
- **Transaction Logging** - Complete audit trail of all inventory changes
- **Robust Validation** - Row-by-row error reporting with detailed feedback

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- SQLite3

### Setup

\`\`\`bash
# Run setup script
bash setup.sh

# Or manual setup:
# Backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install
cd ..
\`\`\`

### Run Locally

**Terminal 1 - Backend:**
\`\`\`bash
source venv/bin/activate
python run.py
\`\`\`

**Terminal 2 - Frontend:**
\`\`\`bash
cd frontend
npm run dev
\`\`\`

Then open:
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs

**Default credentials:**
- Username: `admin`
- Password: `admin123`

## Project Structure

\`\`\`
rapheal-vogue-inventory/
├── main.py                 # FastAPI application
├── database.py             # SQLite setup & utilities
├── models.py               # Pydantic models
├── auth.py                 # JWT authentication
├── requirements.txt        # Python dependencies
├── inventory.db            # SQLite database (auto-created)
├── frontend/
│   ├── src/
│   │   ├── App.vue         # Main app component
│   │   ├── main.js         # Vue entry point
│   │   ├── api.js          # API client
│   │   ├── store.js        # State management
│   │   ├── components/     # Reusable components
│   │   └── views/          # Page components
│   ├── package.json
│   └── vite.config.js
├── DEPLOYMENT.md           # Production deployment guide
├── CSV_TEMPLATES.md        # CSV format documentation
└── test_api.py             # API testing script
\`\`\`

## API Endpoints

### Authentication
- `POST /auth/login` - Login with username/password

### Inventory Management
- `POST /inventory/import` - Bulk import initial inventory
- `POST /inventory/transfer` - Bulk transfer between stores
- `POST /inventory/sales` - Record EOD sales

### Views
- `GET /inventory/stock-status` - Current stock levels
- `GET /inventory/analytics` - Sales analytics with filters

### Health
- `GET /health` - Health check

## CSV Upload Formats

See `CSV_TEMPLATES.md` for detailed format specifications.

### Import CSV
\`\`\`csv
ean,style_name,size,brand,style_design_code,model_no,store_id,quantity
EAN001,Dress A,M,Rapheal,RC001,M001,1,50
\`\`\`

### Transfer CSV
\`\`\`csv
ean,source_store_id,destination_store_id,quantity
EAN001,1,2,10
\`\`\`

### Sales CSV
\`\`\`csv
ean,store_id,quantity_sold
EAN001,1,5
\`\`\`

## Testing

\`\`\`bash
# Run API tests
python test_api.py
\`\`\`

## Deployment

See `DEPLOYMENT.md` for complete production deployment guide.

Quick start:
\`\`\`bash
# Backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app

# Frontend
cd frontend
npm run build
# Deploy frontend/dist/ to web server
\`\`\`

## Database

SQLite database is automatically created on first run. Schema includes:
- `product` - Product catalog
- `store` - Event stores
- `user` - User accounts
- `inventory` - Current stock levels
- `transaction` - Complete transaction history

## Security

- JWT token-based authentication (8-hour expiry)
- Password hashing with SHA256
- Row-level validation on all uploads
- Transaction logging for audit trail

## Performance

- Optimized for bulk operations (1000+ rows per upload)
- Efficient SQLite queries with proper indexing
- Stateless API design for horizontal scaling

## Support

For issues or questions:
1. Check API documentation at `/docs`
2. Review error messages in upload results
3. Check `DEPLOYMENT.md` troubleshooting section

## Timeline

- **Phase 1:** Database & API setup (4 hours)
- **Phase 2:** Core endpoints & validation (17 hours)
- **Phase 3:** Vue 3 frontend (10 hours)
- **Phase 4:** Testing & deployment (4 hours)

**Total: 35 hours**

---

Built for Rapheal Vogue Event - October 2025
