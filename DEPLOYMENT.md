# Rapheal Vogue Inventory Tracker - Deployment Guide

## Quick Start

### Backend Setup (Python/FastAPI)

1. **Install dependencies:**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

2. **Run the server:**
   \`\`\`bash
   python run.py
   \`\`\`
   The API will be available at `http://localhost:8000`

3. **API Documentation:**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Frontend Setup (Vue 3/Vite)

1. **Navigate to frontend directory:**
   \`\`\`bash
   cd frontend
   \`\`\`

2. **Install dependencies:**
   \`\`\`bash
   npm install
   \`\`\`

3. **Run development server:**
   \`\`\`bash
   npm run dev
   \`\`\`
   The frontend will be available at `http://localhost:5173`

4. **Build for production:**
   \`\`\`bash
   npm run build
   \`\`\`
   Output will be in `frontend/dist/`

---

## Production Deployment

### Backend Deployment (Linux VPS)

1. **SSH into your VPS:**
   \`\`\`bash
   ssh user@your-vps-ip
   \`\`\`

2. **Clone repository and setup:**
   \`\`\`bash
   git clone <your-repo-url>
   cd rapheal-vogue-inventory
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   \`\`\`

3. **Run with Gunicorn (production WSGI server):**
   \`\`\`bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 main:app
   \`\`\`

4. **Setup Nginx reverse proxy:**
   Create `/etc/nginx/sites-available/inventory`:
   \`\`\`nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   \`\`\`

   Enable the site:
   \`\`\`bash
   sudo ln -s /etc/nginx/sites-available/inventory /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   \`\`\`

5. **Setup systemd service for auto-restart:**
   Create `/etc/systemd/system/inventory.service`:
   \`\`\`ini
   [Unit]
   Description=Rapheal Vogue Inventory API
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/path/to/rapheal-vogue-inventory
   Environment="PATH=/path/to/rapheal-vogue-inventory/venv/bin"
   ExecStart=/path/to/rapheal-vogue-inventory/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 main:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   \`\`\`

   Enable and start:
   \`\`\`bash
   sudo systemctl enable inventory
   sudo systemctl start inventory
   \`\`\`

### Frontend Deployment

1. **Build the frontend:**
   \`\`\`bash
   cd frontend
   npm run build
   \`\`\`

2. **Deploy `frontend/dist/` to your web server:**
   \`\`\`bash
   scp -r frontend/dist/* user@your-vps-ip:/var/www/html/
   \`\`\`

3. **Configure Nginx for SPA routing:**
   \`\`\`nginx
   server {
       listen 80;
       server_name your-domain.com;
       root /var/www/html;

       location / {
           try_files $uri $uri/ /index.html;
       }

       location /api {
           proxy_pass http://127.0.0.1:8000;
       }
   }
   \`\`\`

---

## Database

SQLite database (`inventory.db`) is automatically created on first run. For production, consider migrating to PostgreSQL:

1. **Install psycopg2:**
   \`\`\`bash
   pip install psycopg2-binary
   \`\`\`

2. **Update `database.py` to use PostgreSQL connection string**

---

## Environment Variables (Production)

Create a `.env` file:
\`\`\`
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///inventory.db  # or PostgreSQL URL
\`\`\`

Update `auth.py` to load from environment:
\`\`\`python
import os
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
\`\`\`

---

## Testing the System

### 1. Create a test user (via database):
\`\`\`python
from database import get_db
from auth import hash_password

with get_db() as conn:
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user (username, password_hash) VALUES (?, ?)",
        ("admin", hash_password("password123"))
    )
    conn.commit()
\`\`\`

### 2. Test login:
\`\`\`bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password123"}'
\`\`\`

### 3. Test import endpoint with sample CSV:
\`\`\`bash
# Create test_import.csv
ean,style_name,size,brand,style_design_code,model_no,store_id,quantity
EAN001,Dress A,M,Rapheal,RC001,M001,1,50
EAN002,Shirt B,L,Vogue,VC002,M002,1,30

# Upload
curl -X POST http://localhost:8000/inventory/import \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@test_import.csv"
\`\`\`

---

## Monitoring & Logs

### Backend logs:
\`\`\`bash
journalctl -u inventory -f  # systemd service logs
\`\`\`

### Check API health:
\`\`\`bash
curl http://localhost:8000/health
\`\`\`

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| CORS errors | Update `main.py` CORS origins for production domain |
| Database locked | Ensure only one process accesses `inventory.db` |
| Token expired | Frontend will auto-redirect to login after 8 hours |
| File upload fails | Check file size limits in Nginx (`client_max_body_size`) |

---

## Security Checklist

- [ ] Change `SECRET_KEY` in production
- [ ] Use HTTPS (Let's Encrypt)
- [ ] Set strong database password if using PostgreSQL
- [ ] Restrict API access by IP if needed
- [ ] Enable firewall rules
- [ ] Regular backups of `inventory.db`
- [ ] Monitor disk space for CSV uploads

---

## Support

For issues or questions, check the API documentation at `/docs` endpoint.
