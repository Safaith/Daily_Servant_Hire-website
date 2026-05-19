# 🏠 Daily Servant — ডেইলি সার্ভেন্ট

A full-stack Django web application that connects **Hirers** with verified **Servants** for one-day home services across Bangladesh.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Seed Demo Data (optional — already done)
```bash
python manage.py shell < seed_data.py
```

### 4. Start the Server
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

---

## 🔑 Demo Login Credentials

| Role     | Username         | Password   |
|----------|-----------------|------------|
| Admin    | `admin`          | `admin123` |
| Hirer    | `rahman_hirer`   | `demo123`  |
| Servant  | `fatima_servant` | `demo123`  |

---

## 👥 User Roles

### 1. Hirer (হায়ার কারী)
- Register/login as Hirer
- Browse servants by category, location, rating, price
- Book a servant for a specific date
- Pay via bKash / Nagad / Rocket / Cash (mock demo)
- Track bookings on dashboard
- Leave reviews after job completion

### 2. Servant (সার্ভেন্ট)
- Register/login as Servant
- Create profile: categories, daily rate, skills, NID
- Wait for admin approval
- Accept/reject/complete bookings from dashboard
- View ratings and earnings

### 3. Admin (এডমিন)
- View all platform stats
- Approve/reject servant registrations
- Monitor all bookings and users
- Access Django Admin panel at `/django-admin/`

---

## 🗺️ URL Structure

### Public Pages
| URL | Description |
|-----|-------------|
| `/` | Home page with hero, categories, featured servants |
| `/servants/` | Browse all approved servants (filter/search) |
| `/servants/<id>/` | Servant detail page + booking button |

### Auth
| URL | Description |
|-----|-------------|
| `/accounts/register/` | Register as Hirer or Servant |
| `/accounts/login/` | Login |
| `/accounts/logout/` | Logout |
| `/accounts/profile/` | User profile |

### Hirer
| URL | Description |
|-----|-------------|
| `/bookings/book/<servant_id>/` | Book a servant |
| `/bookings/hirer-dashboard/` | View all my bookings |
| `/payments/<booking_id>/` | Pay for confirmed booking |
| `/payments/<booking_id>/success/` | Payment confirmation page |

### Servant
| URL | Description |
|-----|-------------|
| `/servants/register-profile/` | Create/edit servant profile |
| `/servants/dashboard/` | Servant dashboard (bookings, stats) |
| `/bookings/respond/<id>/` | Confirm / reject / complete bookings |

### Admin
| URL | Description |
|-----|-------------|
| `/admin-panel/` | Custom admin dashboard |
| `/admin-panel/approve-servant/<id>/` | Approve a servant |
| `/django-admin/` | Django built-in admin |

---

## 🔌 REST API Endpoints

### Auth API
```
POST /api/accounts/register/     — Register new user
POST /api/accounts/login/        — Login, get token
POST /api/accounts/logout/       — Logout
GET/PUT /api/accounts/profile/   — View/update profile
```

### Servants API
```
GET  /api/servants/              — List all approved servants
     ?category=<id>              — Filter by category
     ?search=<text>              — Search by name/skill/location
     ?ordering=daily_rate        — Sort by price/rating/experience
GET  /api/servants/<id>/         — Servant detail + reviews
GET  /api/servants/categories/   — All service categories
POST /api/servants/<id>/review/  — Submit a review (hirer only)
```

### Bookings API
```
POST /api/bookings/create/           — Create booking (hirer only)
GET  /api/bookings/                  — My bookings
PATCH /api/bookings/<id>/status/     — Update booking status
```

### Payments API
```
POST /api/payments/initiate/   — Start mock payment, returns OTP
POST /api/payments/confirm/    — Confirm with OTP, completes payment
```

---

## 📁 Project Structure

```
daily_servant/
├── daily_servant_config/     # Django config (settings, urls)
├── accounts/                 # User model, auth (register/login)
├── servants/                 # Servant profiles, categories, reviews
├── bookings/                 # Booking logic
├── payments/                 # Mock payment flow (bKash/Nagad/Rocket)
├── templates/
│   ├── base.html             # Nav, footer, messages
│   ├── home.html             # Landing page
│   ├── accounts/             # Register, Login, Profile
│   ├── servants/             # List, Detail, Dashboard, Register Profile
│   ├── bookings/             # Book form, Hirer dashboard
│   ├── payments/             # Payment page, Success page
│   └── admin_panel/          # Admin dashboard
├── static/                   # CSS/JS/images
├── media/                    # Uploaded profile pictures
├── requirements.txt
└── manage.py
```

---

## 💳 Payment Flow (Mock/Demo)

1. Hirer selects payment method (bKash/Nagad/Rocket/Cash)
2. System returns a mock OTP (shown on screen for demo)
3. Hirer enters OTP
4. Payment marked complete, transaction ID generated
5. Success page shown with confetti 🎉

---

## 🛡️ Business Logic

- Servants must be **admin-approved** before appearing in listings
- A servant can only be booked once per date (conflict check)
- Only hirers who completed a booking can **review** a servant
- Booking status flow: `pending → confirmed → in_progress → completed`
- Servants can: confirm, reject, or mark complete
- Hirers can: cancel pending/confirmed bookings
- Ratings auto-recalculated on every new review

---

## 🌐 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2+, Django REST Framework |
| Auth | Token-based (DRF) + Session |
| Database | SQLite (dev), PostgreSQL (prod) |
| Frontend | Django Templates, Vanilla JS, CSS animations |
| Fonts | Playfair Display + DM Sans (Google Fonts) |
| Icons | Font Awesome 6 |
| Payment | Mock OTP flow (bKash/Nagad/Rocket/Cash) |
| Currency | BDT (৳) |
| Timezone | Asia/Dhaka |

---

Made with ❤️ in Chittagong, Bangladesh 🇧🇩
