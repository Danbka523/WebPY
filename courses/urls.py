from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('<int:course_id>/edit', views.edit_course, name='edit_course'),
    path('create/', views.create_course, name='create_course'),
    path('<int:course_id>/add_assignment/', views.add_assignment, name='add_assignment'),
    path('<int:course_id>/assignment/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('<int:course_id>/assignment/<int:assignment_id>/edit/', views.edit_assignment, name='edit_assignment'),
]
