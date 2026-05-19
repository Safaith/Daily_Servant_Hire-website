#!/bin/bash
# Daily Servant — Quick Start Script
echo "🏠 Starting Daily Servant — ডেইলি সার্ভেন্ট"
echo "============================================"

# Install deps
echo "📦 Installing dependencies..."
pip install -r requirements.txt -q --break-system-packages

# Migrate
echo "🗄️  Running migrations..."
python manage.py migrate --run-syncdb

# Create superuser if not exists
echo "👤 Checking admin user..."
python manage.py shell -c "
from accounts.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin','admin@dailyservant.com','admin123',
        first_name='Admin', last_name='User', role='admin')
    print('Admin created: admin / admin123')
else:
    print('Admin already exists.')
"

echo ""
echo "✅ Ready! Starting server..."
echo ""
echo "🌐 Open: http://127.0.0.1:8000"
echo "🔑 Admin login: admin / admin123"
echo "🔑 Demo hirer:  rahman_hirer / demo123"
echo "🔑 Demo servant: fatima_servant / demo123"
echo "📚 API docs: http://127.0.0.1:8000/api/"
echo ""
python manage.py runserver
