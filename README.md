# 💼 JobBoard API

> **Author:** RaviVarma

A full-stack **Job Portal** built with **Django + Django REST Framework** where:

- 🧑‍💼 **Recruiters** can post jobs and manage applications
- 👤 **Applicants** can browse jobs, apply with their resume, and track status
- 🔐 **JWT Authentication** with role-based access
- 🌐 **Bootstrap 5** frontend with clean, responsive pages

This project demonstrates real-world backend + frontend skills using only beginner-friendly concepts.

---

## 📚 Table of Contents

1. [What This Project Does](#-what-this-project-does)
2. [How the Application Runs (Flow Diagram)](#-how-the-application-runs-flow-diagram)
3. [Tech Stack](#-tech-stack)
4. [Project Structure](#-project-structure)
5. [File-by-File Explanation](#-file-by-file-explanation)
6. [Database Models](#-database-models)
7. [REST API Endpoints](#-rest-api-endpoints)
8. [Function Reference](#-function-reference)
9. [Frontend Pages](#-frontend-pages)
10. [How to Run Locally](#-how-to-run-locally)
11. [How to Use the App](#-how-to-use-the-app)
12. [Common Errors & Fixes](#-common-errors--fixes)
13. [What I Learned](#-what-i-learned)

---

## 🎯 What This Project Does

JobBoard is a **mini version of Naukri/Indeed** with two user roles:

### 🧑‍💼 Recruiter
- Register / Login
- Post new jobs
- View own posted jobs
- Delete own jobs
- View applications for their jobs
- Shortlist or reject applicants

### 👤 Applicant
- Register / Login
- Browse all jobs (public)
- Apply with full profile (name, contact, experience, skills, cover letter, resume)
- Track application status (pending / shortlisted / rejected)

### 🔐 Security
- JWT-based authentication (access + refresh tokens)
- Role-based permissions (recruiters can't apply, applicants can't post)
- Ownership checks (only job owners can edit/delete/view applications)
- Duplicate application prevention

---

## 🔄 How the Application Runs (Flow Diagram)

```
┌──────────────────────────────────────────────────────────────────┐
│                         BROWSER (User)                            │
│  ┌────────────┐   ┌─────────────┐   ┌───────────────┐            │
│  │  Login     │   │  Register   │   │  Jobs /       │            │
│  │  Page      │   │  Page       │   │  Dashboard    │            │
│  └─────┬──────┘   └──────┬──────┘   └───────┬───────┘            │
│        │                 │                  │                     │
│        └─────────────────┴──────────────────┘                     │
│                          │                                        │
│                          │  fetch() with JWT token                │
│                          ▼                                        │
└──────────────────────────────────────────────────────────────────┘
                           │
                           │ HTTP (JSON / multipart)
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                    DJANGO SERVER (Backend)                        │
│                                                                   │
│  ┌────────────────┐    ┌──────────────────┐                       │
│  │  accounts app  │    │    jobs app      │                       │
│  │                │    │                  │                       │
│  │  • register    │    │  • list jobs     │                       │
│  │  • login       │    │  • create job    │                       │
│  │  • JWT tokens  │    │  • apply to job  │                       │
│  │  • role field  │    │  • view apps     │                       │
│  └───────┬────────┘    └────────┬─────────┘                       │
│          │                      │                                 │
│          │       ┌──────────────┘                                 │
│          │       │                                                │
│          ▼       ▼                                                │
│  ┌──────────────────────────┐   ┌──────────────────────────┐      │
│  │  utils/responses.py      │   │  DRF Serializers         │      │
│  │  (success / error resp)  │   │  (validate + convert)    │      │
│  └──────────────┬───────────┘   └──────────────┬───────────┘      │
│                 │                              │                  │
│                 └──────────────┬───────────────┘                  │
│                                ▼                                  │
│                    ┌──────────────────────┐                       │
│                    │   Django ORM         │                       │
│                    │   (Models)           │                       │
│                    └──────────┬───────────┘                       │
└───────────────────────────────┼───────────────────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   SQLite Database     │
                    │   (db.sqlite3)        │
                    │                       │
                    │   Tables:             │
                    │   • accounts_user     │
                    │   • jobs_job          │
                    │   • jobs_application  │
                    └───────────────────────┘

                    ┌───────────────────────┐
                    │   media/resumes/      │
                    │   (uploaded PDFs)     │
                    └───────────────────────┘
```

### 🔁 Typical Request Flow

```
1. User clicks "Apply Now"
        │
        ▼
2. Browser JS → fetch('/api/jobs/1/apply/', FormData, JWT)
        │
        ▼
3. Django routes → jobs.views.apply_to_job()
        │
        ▼
4. Permission check (is applicant?) → ✅
        │
        ▼
5. Serializer validates data → ✅
        │
        ▼
6. Model saves to DB (Application row + resume file to media/)
        │
        ▼
7. Response: { success: true, message: "..." }
        │
        ▼
8. Browser shows success message
```

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Backend | Django 5.x | Web framework |
| API | Django REST Framework | RESTful JSON APIs |
| Auth | Simple JWT | Token-based auth |
| Database | SQLite | Local development |
| Frontend | HTML, CSS, Bootstrap 5 | UI |
| Scripts | Vanilla JavaScript | API calls, DOM updates |
| File Uploads | Django FileField + MultiPartParser | Resume uploads |
| Env Config | python-decouple | `.env` handling |

---

## 📁 Project Structure

```
job_board_api/
│
├── manage.py                       # Django management script
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .env                            # Secret key + DEBUG flag
├── .gitignore                      # Files to ignore in Git
├── db.sqlite3                      # Local SQLite database
│
├── job_board_api/                  # Main project configuration
│   ├── __init__.py
│   ├── settings.py                 # Project settings
│   ├── urls.py                     # Root URL router
│   ├── wsgi.py                     # Deployment entry
│   └── asgi.py
│
├── accounts/                       # App 1: User authentication
│   ├── models.py                   # Custom User with role
│   ├── admin.py                    # Admin registration
│   ├── serializers.py              # Register + Login validators
│   ├── views.py                    # register_user, login_user
│   ├── urls.py                     # /api/register/, /api/login/
│   └── migrations/
│
├── jobs/                           # App 2: Jobs + Applications
│   ├── models.py                   # Job, Application
│   ├── admin.py                    # Admin registration
│   ├── serializers.py              # JobSerializer, ApplicationSerializer
│   ├── views.py                    # All job + application views
│   ├── urls.py                     # /api/jobs/...
│   └── migrations/
│
├── utils/                          # App 3: Helpers
│   ├── __init__.py
│   └── responses.py                # success_response, error_response
│
├── templates/                      # HTML pages
│   ├── base.html                   # Layout + navbar
│   ├── login.html                  # Login page
│   ├── register.html               # Register page
│   ├── jobs.html                   # Jobs listing + apply modal
│   ├── recruiter.html              # Recruiter dashboard
│   └── my_applications.html        # Applicant's applications
│
├── static/
│   └── css/
│       └── style.css               # Custom styles
│
└── media/                          # Uploaded files (auto-created)
    └── resumes/                    # Uploaded resumes
```

---

## 📂 File-by-File Explanation

### 🔹 `job_board_api/settings.py`
Central configuration. Contains:
- `INSTALLED_APPS` — registers Django apps + DRF + JWT
- `AUTH_USER_MODEL = 'accounts.User'` — uses our custom User
- `REST_FRAMEWORK` — configures JWT auth for all APIs
- `SIMPLE_JWT` — token lifetimes
- `TEMPLATES` — points to `templates/` folder
- `STATIC_URL` + `STATICFILES_DIRS` — CSS serving
- `MEDIA_URL` + `MEDIA_ROOT` — resume uploads

### 🔹 `job_board_api/urls.py`
Root router. Includes:
- `/admin/` — Django admin
- `/api/` — accounts + jobs APIs
- `/login/`, `/register/`, `/jobs/`, `/recruiter/`, `/my-applications/` — frontend pages
- Serves media files in development

### 🔹 `accounts/models.py`
Defines **`User`** extending `AbstractUser`:
- Adds `role` field: `recruiter` or `applicant`
- Helper methods: `is_recruiter()`, `is_applicant()`

### 🔹 `accounts/serializers.py`
- **`RegisterSerializer`** — validates username, email, password, role
- **`LoginSerializer`** — authenticates username + password

### 🔹 `accounts/views.py`
- **`register_user()`** — creates user + returns JWT
- **`login_user()`** — validates credentials + returns JWT
- **`get_tokens_for_user()`** — helper to generate tokens

### 🔹 `jobs/models.py`
- **`Job`** — posted by recruiter (title, company, location, etc.)
- **`Application`** — applicant's submission (all details + resume + status)

### 🔹 `jobs/serializers.py`
- **`JobSerializer`** — converts Job ↔ JSON
- **`ApplicationSerializer`** — converts Application ↔ JSON with validations

### 🔹 `jobs/views.py`
All API logic — 14 functions (see [Function Reference](#-function-reference))

### 🔹 `utils/responses.py`
Standard response helpers so every endpoint returns the same JSON shape.

### 🔹 `templates/base.html`
Master layout. Navbar is role-aware (shows different links per role). Shared `logout()` function.

### 🔹 `templates/jobs.html`
Shows all jobs + **Apply modal** with full form.

### 🔹 `templates/recruiter.html`
Recruiter dashboard: post jobs + view applications + shortlist/reject.

### 🔹 `templates/my_applications.html`
Applicant's list of own applications + status badges + resume link.

---

## 🗄 Database Models

### `User` (accounts)
| Field | Type | Notes |
|-------|------|-------|
| `username` | CharField | From AbstractUser |
| `email` | EmailField | From AbstractUser |
| `password` | CharField | Hashed |
| `role` | CharField | `recruiter` / `applicant` |

### `Job` (jobs)
| Field | Type | Notes |
|-------|------|-------|
| `recruiter` | ForeignKey(User) | Who posted |
| `title` | CharField | Job title |
| `company` | CharField | Company name |
| `location` | CharField | Job location |
| `description` | TextField | Full description |
| `salary` | CharField | Optional |
| `created_at` | DateTimeField | Auto |

### `Application` (jobs)
| Field | Type | Notes |
|-------|------|-------|
| `job` | ForeignKey(Job) | Which job |
| `applicant` | ForeignKey(User) | Who applied |
| `full_name` | CharField | Captured at apply time |
| `email` | EmailField | Contact |
| `phone` | CharField | Contact |
| `location` | CharField | Current city |
| `experience_years` | PositiveInteger | Years |
| `skills` | CharField | Comma-separated |
| `cover_letter` | TextField | Message |
| `resume` | FileField | PDF/DOC |
| `status` | CharField | pending / shortlisted / rejected |
| `applied_at` | DateTimeField | Auto |

**Constraint:** `unique_together = ('job', 'applicant')` — prevents duplicate applications.

---

## 🌐 REST API Endpoints

### 🔐 Authentication

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| POST | `/api/register/` | Public | Register (with role) |
| POST | `/api/login/` | Public | Login → JWT tokens |

### 💼 Jobs

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| GET | `/api/jobs/` | Public | List all jobs |
| POST | `/api/jobs/create/` | Recruiter | Create job |
| GET | `/api/jobs/<id>/` | Public | Single job detail |
| PUT | `/api/jobs/<id>/update/` | Owner | Update job |
| DELETE | `/api/jobs/<id>/delete/` | Owner | Delete job |

### 📄 Applications

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| POST | `/api/jobs/<id>/apply/` | Applicant | Apply to a job |
| GET | `/api/my-applications/` | Applicant | Own applications |
| GET | `/api/jobs/<id>/applications/` | Owner | Applications per job |
| PUT | `/api/applications/<id>/status/` | Owner | Update status |

### 📥 Example Request — Apply to Job

**POST** `/api/jobs/1/apply/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Body (form-data):**
```
full_name        = "Ravi Varma"
email            = "ravi@test.com"
phone            = "9876543210"
location         = "Hyderabad"
experience_years = "2"
skills           = "Python, Django, SQL"
cover_letter     = "I'm excited to apply..."
resume           = <file>
```

**Response (201):**
```json
{
    "success": true,
    "message": "Application submitted successfully.",
    "data": {
        "id": 1,
        "job_title": "Backend Developer",
        "full_name": "Ravi Varma",
        "status": "pending",
        "resume_url": "http://127.0.0.1:8000/media/resumes/ravi.pdf",
        ...
    }
}
```

### 📤 Standard Response Format

**Success:**
```json
{
    "success": true,
    "message": "Success message",
    "data": { ... }
}
```

**Error:**
```json
{
    "success": false,
    "message": "Error message",
    "errors": { "field": ["error detail"] }
}
```

---

## 🧩 Function Reference

### 🔹 `accounts/views.py`

#### `get_tokens_for_user(user)`
Generates JWT access + refresh tokens.
- **Input:** User instance
- **Returns:** `{ refresh, access }`

#### `register_user(request)`
Handles `POST /api/register/`.
- Validates data via `RegisterSerializer`
- Creates user with hashed password
- Returns user + JWT tokens

#### `login_user(request)`
Handles `POST /api/login/`.
- Validates via `LoginSerializer`
- Returns user + JWT tokens

### 🔹 `jobs/views.py`

#### `list_jobs(request)`
- **URL:** `GET /api/jobs/`
- **Auth:** Public
- **Returns:** All jobs (newest first)

#### `create_job(request)`
- **URL:** `POST /api/jobs/create/`
- **Auth:** Recruiter only
- **Logic:** Sets `recruiter = request.user`

#### `job_detail(request, job_id)`
- **URL:** `GET /api/jobs/<id>/`
- **Auth:** Public

#### `update_job(request, job_id)`
- **URL:** `PUT /api/jobs/<id>/update/`
- **Auth:** Owner recruiter only

#### `delete_job(request, job_id)`
- **URL:** `DELETE /api/jobs/<id>/delete/`
- **Auth:** Owner recruiter only

#### `apply_to_job(request, job_id)`
- **URL:** `POST /api/jobs/<id>/apply/`
- **Auth:** Applicant only
- **Parsers:** MultiPartParser (for resume)
- **Logic:** Blocks duplicate, sets `applicant = request.user`

#### `my_applications(request)`
- **URL:** `GET /api/my-applications/`
- **Auth:** Applicant only

#### `view_applications(request, job_id)`
- **URL:** `GET /api/jobs/<id>/applications/`
- **Auth:** Owner recruiter only

#### `update_application_status(request, app_id)`
- **URL:** `PUT /api/applications/<id>/status/`
- **Auth:** Owner recruiter only
- **Body:** `{ "status": "shortlisted" }`

### 🔹 Page Views
- `page_login`, `page_register`, `page_jobs`, `page_recruiter`, `page_my_applications` — render HTML templates.

### 🔹 `utils/responses.py`

#### `success_response(data, message, status)`
Standard success JSON.

#### `error_response(message, status, errors)`
Standard error JSON.

### 🔹 `jobs/serializers.py`

#### `ApplicationSerializer.get_resume_url(obj)`
Returns full URL for uploaded resume.

#### `ApplicationSerializer.validate_experience_years(value)`
Ensures 0 ≤ value ≤ 60.

#### `ApplicationSerializer.validate_phone(value)`
Ensures at least 10 digits.

---

## 🖥 Frontend Pages

| Page | URL | Who | Purpose |
|------|-----|-----|---------|
| Login | `/login/` | Public | Login form |
| Register | `/register/` | Public | Register with role |
| Jobs | `/jobs/` | Public | List jobs + Apply modal |
| Recruiter Dashboard | `/recruiter/` | Recruiter | Post jobs + manage apps |
| My Applications | `/my-applications/` | Applicant | Own applications + status |
| Django Admin | `/admin/` | Superuser | Developer view |

---

## 🚀 How to Run Locally

```bash
# 1. Clone project
git clone <your-repo-url>
cd job_board_api

# 2. Create virtual environment
python -m venv env

# 3. Activate
# Windows:
env\Scripts\activate
# Mac/Linux:
source env/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
echo "SECRET_KEY=your-secret-key" > .env
echo "DEBUG=True" >> .env

# 6. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 7. Create superuser
python manage.py createsuperuser

# 8. Run server
python manage.py runserver
```

Open **http://127.0.0.1:8000/**

---

## 🎮 How to Use the App

### 🧑‍💼 As a Recruiter
1. Register with role = **Recruiter**
2. Login → navbar shows **Dashboard**
3. Click **Dashboard** → post a new job
4. See your jobs listed
5. Click **Applications** on a job to review applicants
6. Click **Shortlist** or **Reject**

### 👤 As an Applicant
1. Register with role = **Applicant**
2. Login → navbar shows **My Applications**
3. Click **Jobs** → browse jobs
4. Click **Apply Now** → fill form (name, contact, experience, skills, cover letter, resume) → submit
5. Click **My Applications** → see pending/shortlisted/rejected badge
6. Click **View My Resume** to confirm upload

---

## 🐛 Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `AUTH_USER_MODEL refers to model 'accounts.User' that has not been installed` | User model missing when `AUTH_USER_MODEL` set | Create model first, then migrate |
| `401 Unauthorized` | Missing/invalid token | Check `Authorization: Bearer <token>` header |
| `403 Only recruiters can post jobs` | Logged in as applicant | Login as recruiter |
| `400 Invalid application data` | Missing required fields | Fill all fields in modal |
| `Media files not loading` | `MEDIA_URL`/`MEDIA_ROOT` not configured | Add to `settings.py` + `urls.py` |
| `No such table` | Migrations not applied | Run `python manage.py migrate` |
| `CORS error` | Frontend on different origin | Use same origin or add CORS headers |

---

## 🎓 What I Learned

- Designing a **multi-app Django project** with clean separation
- Creating a **custom User model** with a `role` field
- Implementing **JWT authentication** with Simple JWT
- Writing **function-based views** with clear docstrings
- Building **RESTful APIs** with Django REST Framework
- Handling **file uploads** with `FileField` + `MultiPartParser`
- Writing **custom serializer validations**
- Building a **role-aware frontend** using Bootstrap + vanilla JS
- Storing JWT in `localStorage` and attaching it to `fetch()` calls
- Enforcing **role-based permissions** at API level
- Preventing **duplicate applications** via `unique_together`
- Serving **media files** in development
- Using a **standard response format** across all endpoints

---

## 🧠 Interview Talking Points

1. **Why a custom User model?** → Needed a `role` field to distinguish recruiters from applicants.
2. **Why JWT over sessions?** → Stateless, works well with SPAs and mobile.
3. **How do you prevent duplicate applications?** → `unique_together` + explicit existence check in the view.
4. **Why function-based views?** → Simpler for small APIs, easier to read and explain.
5. **How do you handle file uploads?** → `FileField` + `MEDIA_ROOT` + DRF's `MultiPartParser`, and `FormData` on the frontend.
6. **How is your API structured?** → Apps by domain (`accounts`, `jobs`), with shared helpers in `utils`.
7. **How do you enforce permissions?** → Role checks at the top of each view + ownership checks before update/delete.

---

## 📜 License

MIT — free to use, modify, and learn from.

---

---

**Author:** RaviVarma  
**Project:** JobBoard API — Django + DRF + Bootstrap  
**Year:** 2026

---

## 🙌 Credits

Built as a **fresher portfolio project** to demonstrate:
- Django + DRF backend skills
- Authentication with JWT
- RESTful API design
- Bootstrap frontend integration
- File upload handling
- Clean code with docstrings