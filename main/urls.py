from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index_view"),
    path("discover/", views.discover_view, name="discover_view"),
    path("discover/<str:type>/", views.list_view, name="list_view"),
    path("3d_models/", views.view_3d, name="3d_view"),
    path('3d_models/<int:pk>/', views.viewer, name="viewer"),
    path("data/", views.data_view, name="data_view"),
    path("data/<int:pk>/", views.list_data_view, name="list_data_view"),
    path("contact/", views.contact_view, name="contact_view"),
    # path("login/", views.login_view, name="login_view"),
    # path("logout/", views.logout_view, name="logout_view"),
    # path("register/", views.register_view, name="register_view"),
    # path("model/", views.add_model),
]
