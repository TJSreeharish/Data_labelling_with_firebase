from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import image_model,classes
from .img_upload import start
from .check import initialize
from datetime import timedelta
from firebase_admin import storage
import pyrebase


def index(request):
    return render(request,'index.html')

def services(request):
    return render(request, "service-details.html")

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)
        print(user)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Credentials Invalid')
            return redirect('login')
    else:
        return render(request,'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect("/")

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1'] 

        if password == password1:
            if User.objects.filter(email=email).exists():
                messages.info(request,'email already exists')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already exists')
                return redirect('register')
            else:
                User.objects.create_user(username = username,email = email,password = password)
                return redirect('login')
        else:
            messages.info(request,'password not the same')
            return redirect('register')
    else:
        return render(request,'register.html')
    
def image(request):
    if request.method == 'POST':
        images = request.FILES.getlist('files')
        for image in images:
            if image:
                img = image_model(image = image)
                img.save()
        start()
        return redirect('image')
    else:
        return render(request,'image.html')
    
def index1(request):
    return render(request,'index1.html')

def organization(request):
    return render(request,'organization.html')

def courses(request):
    return render(request,'courses.html')

def student(request):
    return render(request,'student.html')

def classess(request):
    if request.method == "POST":
        if 'classes' in request.POST:  # If the form was submitted with a new class
            form = request.POST['classes']
            new_form = classes(cat=form)
            new_form.save()
            messages.success(request, 'Class saved successfully!')
            return redirect('classes')
        elif 'clear_database' in request.POST:  # If the clear database button was clicked
            classes.objects.all().delete()  # Delete all entries
            messages.success(request, 'Database cleared successfully!')
            return redirect('classes')
    return render(request,'classes.html')

def list_images_in_firebase():
    """Retrieve all image file paths from Firebase storage."""
    bucket = storage.bucket()
    blobs = bucket.list_blobs(prefix="images/")
    return [blob.name for blob in blobs if blob.name.endswith(('.png', '.jpg', '.jpeg'))]

def get_image_url(file_path):
    """Retrieve a download URL for an image stored in Firebase."""
    bucket = storage.bucket()
    blob = bucket.blob(file_path)
    # Create a URL valid for 1 hour
    return blob.generate_signed_url(timedelta(hours=1))

def coursedetails(request):
    return request(request, "image_template.html")

def image_view(request):
    """Render template with a list of Firebase images and navigation."""
    initialize()  # Initialize Firebase

    # Get the list of all images in the Firebase storage
    image_files = list_images_in_firebase()

    # Get the current image index from the URL or session (default to 0)
    current_index = int(request.GET.get('index', 0))

    # Ensure the index is within bounds
    if current_index < 0:
        current_index = 0
    elif current_index >= len(image_files):
        current_index = len(image_files) - 1

    # Get the image path for the current index
    file_path = image_files[current_index] if image_files else None

    # Retrieve the signed URL for the current image
    image_url = None
    if file_path:
        try:
            image_url = get_image_url(file_path)
        except Exception as e:
            print(f"Error retrieving image URL: {e}")

    # Calculate the next image index, wrapping around if necessary
    next_index = (current_index + 1) % len(image_files)

    # Pass the image URL and index information to the template
    context = {
        'image_url': image_url,
        'next_index': next_index,
        'features': classes.objects.all(),  # Categories to display
    }

    return render(request, 'image_template.html', context)



'''def get_image_url(file_path):
    """Retrieve a download URL for an image stored in Firebase."""
    bucket = storage.bucket()
    blob = bucket.blob(file_path)
    # Create a URL valid for 1 hour
    return blob.generate_signed_url(timedelta(hours=1))

def image_view(request):
    """Render template with Firebase image URL."""
    initialize()  # Initialize Firebase
    file_path = "images/Screenshot_2024-01-16_191056.png"  # Path to your Firebase image

    features = classes.objects.all()

    try:
        image_url = get_image_url(file_path)  # Get signed URL
    except Exception as e:
        print(f"Error retrieving image URL: {e}")
        image_url = None  # Handle error gracefully

    return render(request, 'image_template.html', {'image_url': image_url,'features' : features})'''

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.conf import settings
from datetime import datetime

@csrf_exempt  # Disable CSRF for testing
def receive_json(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)

            # Generate a unique filename with a timestamp
            filename = f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            file_path = os.path.join(settings.MEDIA_ROOT, filename)

            # Save the JSON data to a file in the media/ directory
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

            return JsonResponse({'status': 'success', 'message': f'Data saved as {filename}'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)
