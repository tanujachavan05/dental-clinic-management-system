from django.urls import path
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

from . import views

# Optional: Redirect root URL to /home/
def root_redirect(request):
    return redirect('home')

urlpatterns = [
    path('', root_redirect),  # Redirect root (/) to /home/
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('patients/', views.patient_list, name='patient_list'),
    path('get-quote/', views.get_quote, name='get_quote'),

    # Blog URLs
    path('blog/', views.blog_list, name='blog_list'),  # List of blogs
    path('blog/<int:id>/', views.blog_detail, name='blog_detail'),  # Blog Detail by ID
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
