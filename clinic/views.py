from django.shortcuts import render, redirect     
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

from .models import Patient, Blog
from .forms import CustomUserCreationForm, ContactForm  # 👈 Added ContactForm import

# ✅ Home View
def home(request):
    return render(request, 'clinic/home.html')

# ✅ About Page
def about(request):
    return render(request, 'clinic/about.html')

# ✅ Contact Page - Updated with Form Submission Logic
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            full_message = f"From: {name} <{email}>\n\n{message}"

            send_mail(
                subject,
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                ['tc3352180@gmail.com'],  # 🔁 Replace with your email
                fail_silently=False,
            )

            return redirect('home')  # 👈 Make sure this route exists
    else:
        form = ContactForm()
    return render(request, 'clinic/contact.html', {'form': form})

# ✅ Success Page View (Optional)
def success_view(request):
    return render(request, 'clinic/success.html')

# ✅ Dashboard (Requires Login)
@login_required
def dashboard(request):
    total_patients = Patient.objects.count()
    upcoming_appointments = 5
    total_invoices = 12

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
    appointments_data = [5, 7, 3, 8, 6]

    context = {
        'total_patients': total_patients,
        'upcoming_appointments': upcoming_appointments,
        'total_invoices': total_invoices,
        'months': months,
        'appointments_data': appointments_data,
    }
    return render(request, 'clinic/dashboard.html', context)

# ✅ Get a Quote Form Submission
def get_quote(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        print(f"Quote Request: {name}, {email}, {phone}, {message}")
        return redirect('home')
    return HttpResponse("Invalid Request", status=400)

# ✅ Patient List with Search
@login_required
def patient_list(request):
    query = request.GET.get('search', '')
    patients = Patient.objects.filter(
        Q(name__icontains=query) | Q(email__icontains=query)
    ) if query else Patient.objects.all()
    
    return render(request, 'clinic/patient_list.html', {'patients': patients, 'query': query})

# ✅ User Login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    
    return render(request, 'clinic/login.html', {'form': form})

# ✅ User Registration (Updated with Custom Form)
def user_register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'clinic/register.html', {'form': form})

# ✅ User Logout
def user_logout(request):
    logout(request)
    return redirect('login')

# ✅ Blog List View
def blog_list(request):   
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'clinic/blog.html', {'blogs': blogs})


# ✅ Blog Detail View
def blog_detail(request, id):
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        return HttpResponse("Blog post not found", status=404)
    return render(request, 'clinic/blog_detail.html', {'blog': blog})

# ✅ Services View with Dummy Data
def services(request):
    services = [
        {'icon': 'flaticon-tooth', 'title': 'Dental Care', 'description': 'High quality dental care for all ages'},
        {'icon': 'flaticon-dental-care', 'title': 'Cosmetic Dentistry', 'description': 'Get the smile you deserve'},
        {'icon': 'flaticon-dentist', 'title': 'Oral Surgery', 'description': 'Expert surgical dental solutions'},
        {'icon': 'flaticon-toothbrush', 'title': 'Teeth Cleaning', 'description': 'Professional hygiene treatments'},
    ]

    stats = [
        {'number': 500, 'label': 'Happy Clients'},
        {'number': 120, 'label': 'Qualified Staff'},
        {'number': 300, 'label': 'Dental Procedures'},
        {'number': 15, 'label': 'Years of Experience'},
    ]

    pricing = [
        {'name': 'Basic', 'price': '$50', 'features': ['Consultation', 'Basic Cleaning'], 'featured': False},
        {'name': 'Standard', 'price': '$100', 'features': ['Consultation', 'Teeth Whitening', 'X-Rays'], 'featured': True},
        {'name': 'Premium', 'price': '$200', 'features': ['Full Checkup', 'Deep Cleaning', 'Whitening', 'Oral Surgery Discount'], 'featured': False},
        {'name': 'Family', 'price': '$300', 'features': ['4 Members', 'Annual Checkups', 'Priority Support'], 'featured': False},
    ]

    return render(request, 'clinic/services.html', {
        'services': services,
        'stats': stats,
        'pricing': pricing
    })
