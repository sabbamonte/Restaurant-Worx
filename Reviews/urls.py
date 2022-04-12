from django.urls import path
from . import views

urlpatterns = [
	path("", views.index, name="index" ),
	path("landing", views.landing, name="landing"),
	path("login", views.login_view, name="login"),
	path("logout", views.logout_view, name="logout"),
	path("register", views.register, name="register"),
	path("review", views.review, name="review" ),
	path("restaurant/<str:restaurant>", views.restaurant, name="restaurant"),
	path("search", views.search, name="search"),
	path("about", views.about, name="about"),

	# API paths
	path("add", views.add, name="add"),
	path("review", views.review, name="review"),
	path("show/<int:review_id>", views.show, name="show"),
	path("delete/<int:review_id>", views.delete, name="delete"),
	path("position/<str:position>", views.position, name="position")
]

	
