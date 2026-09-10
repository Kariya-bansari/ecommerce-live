# ================================================================
# REQUIRED SETTINGS.PY ADDITIONS
# Add/verify these in your main project's settings.py
# ================================================================

# 1. INSTALLED APPS — make sure both apps are listed
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',          # ← Required for User model
    'django.contrib.contenttypes',
    'django.contrib.sessions',      # ← Required for session auth
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',                     # ← Your accounts app
    'store',                        # ← Your store app
]

# 2. MIDDLEWARE — sessions and auth middleware must be present
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',   # ← Required
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # ← Required
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 3. TEMPLATES — must have 'django.contrib.auth.context_processors.auth'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],   # ← Point to your templates folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # ← Required
                'django.contrib.auth.context_processors.auth', # ← Required
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 4. SESSION SETTINGS (recommended)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Store sessions in DB
SESSION_COOKIE_AGE = 86400 * 7   # Sessions last 7 days
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False     # Set True in production with HTTPS

# 5. AUTH REDIRECT SETTINGS
# Where @login_required redirects unauthenticated users:
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'     # After login, go to home

# ================================================================
# MAIN PROJECT urls.py  (your project's main urls.py, not app urls.py)
# ================================================================
# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('accounts.urls')),   # register, login, logout, home
#     path('product/', include('store.urls')), # store, cart, wishlist
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ================================================================
# MIGRATION STEPS — run these commands in order
# ================================================================
# 1. python manage.py makemigrations accounts
# 2. python manage.py makemigrations store
# 3. python manage.py migrate
# 4. python manage.py createsuperuser   (to create an admin account)
# 5. python manage.py runserver

# ================================================================
# HOW THE FIX WORKS (Summary)
# ================================================================
# BEFORE (broken):
#   - accounts/views.py used Register model + manual session: request.session["user_id"] = user.id
#   - store/views.py used Django's @login_required which checks request.user.is_authenticated
#   - These two systems did NOT talk to each other → cart/wishlist always said "login required"
#
# AFTER (fixed):
#   - register view: User.objects.create_user(username, email, password)  [hashed password, auth_user table]
#   - login view:    authenticate() + login(request, user)                 [sets request.user + session cookie]
#   - logout view:   logout(request)                                       [clears session]
#   - store views:   @login_required + request.user.is_authenticated       [now works correctly]
#   - AJAX views:    return 401 JSON (not redirect) for unauthenticated   [frontend handles redirect]
