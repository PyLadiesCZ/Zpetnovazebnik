from django.urls import path
from . import views


urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<course_slug>/', views.session_list, name='session_list'),
    path('<course_slug>/<session_slug>/', views.session_detail, name='session_detail'),
    path('<course_slug>/<session_slug>/<password>/', views.add_comment_to_session, name='add_comment_to_session'),
]
