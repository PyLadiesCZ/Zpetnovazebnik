from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<course_name>/', views.session_list, name='session_list'),
    path('<course_name>/<pk>/', views.session_detail, name='session_detail'),
    path('<course_name>/<pk>/<password>/', views.add_comment_to_session, name='add_comment_to_session'),
]
