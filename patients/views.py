from django.shortcuts import render

# Create a simple home view
def home(request):
    return render(request, 'patients/home.html')
