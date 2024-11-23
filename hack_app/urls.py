from django.urls import path
from . import views
from django.http.response import HttpResponse

urlpatterns = [
    path('',views.index,name = 'index'),
    path('login',views.login,name = 'login'),
    path('register',views.register,name = 'register'),
    path('image',views.image,name = 'image'),
    path('logout',views.logout,name = 'logout'),
    path('index1',views.index1,name = 'index1'),
    path('organization',views.organization,name = 'organization'),
    path('courses',views.courses,name = 'courses'),
    path('student',views.student,name = 'student'),
    path('servicedetails',views.services,name = 'sd'),
    path('classes',views.classess,name = 'classes'),
    path('firebase-image/', views.image_view, name='firebase_image'),
    path('course-details',views.coursedetails,name = 'cd'),
    path('receive-json/', views.receive_json, name='receive_json'),
]