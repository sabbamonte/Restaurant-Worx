from django.urls import path
from . import views

urlpatterns = [
	path("", views.index, name="index" ),
	path("login", views.login_view, name="login"),
	path("logout", views.logout_view, name="logout"),
	path("register", views.register, name="register"),
	path("review", views.review, name="review" ),

	# API paths
	path("add", views.add, name="add"),
	path("review", views.review, name="review")
]

	
