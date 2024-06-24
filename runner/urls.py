from django.urls import path
from . import views

urlpatterns = [
    path('run_code/', views.interpreter, name='interpreter'),
    path('check_code/', views.checker, name='checker'),
]