from django.urls import path
from . import views

urlpatterns = [
    path('',views.editor, name='editor'),
    path('<int:assignment_id>', views.editor, name='editor'),
]