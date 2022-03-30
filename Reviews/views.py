from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from statistics import mean
from django.core.paginator import Paginator

from .models import User, Info, Review

# Create your views here.
@login_required(login_url='/login')
@csrf_exempt
def index(request):
    if request.method == 'GET':
        user_reviews = Review.objects.filter(user=request.user)
        reviews = Review.objects.all().order_by('-id')
        paginator = Paginator(reviews, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        try:
            info = Info.objects.get(user=request.user)
            return render(request, 'reviews/index.html', {"info": info, "reviews": reviews, "page_obj": page_obj, "user_reviews": user_reviews})
        except ObjectDoesNotExist:
            return render(request, 'reviews/index.html', {"reviews": reviews, "page_obj": page_obj, "user_reviews": user_reviews})
            
# Try to log user in
@csrf_exempt
def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        if not username:
            return render(request, "reviews/login.html", {
                "message": "Invalid username and/or password."
            })
        password = request.POST["password"]
        if not password:
            return render(request, "reviews/login.html", {
                "message": "Invalid username and/or password."
            })

        # Check if inputs match database
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "reviews/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "reviews/login.html")

# Register new users
@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        if not username:
            return render(request, "reviews/register.html", {
                "message": "Please choose a username."
            })
        email = request.POST["email"]

        # Error check that password matches
        password = request.POST["password"]
        if not password:
            return render(request, "reviews/register.html", {
                "message": "Please choose a password."
            })
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "reviews/register.html", {
                "message": "Passwords must match."
            })

        # Error check if username already taken
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "reviews/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "reviews/register.html")

# Log users out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# Show review selected from my reviews
@login_required(login_url='/login')
def show(request, review_id):
    if request.method == "GET":
        data = Review.objects.filter(id=review_id).values()

        return JsonResponse({"review": list(data)})

# Delete Review
@login_required(login_url='/login')
@csrf_exempt
def delete(request, review_id):
    if request.method == "GET":
        review = Review.objects.filter(id=review_id).values()

        return JsonResponse({"review": list(review)})

    if request.method == "DELETE":
        Review.objects.filter(id=review_id).delete()

        return JsonResponse({"message": "Deleted successfuly"}, status=201)



# Add/Edit position or location
@login_required(login_url='/login')
@csrf_exempt
def add(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        all_info = Info.objects.filter(user=request.user)
        if not all_info:
            info = Info()
            info.position = data.get('position').upper()
            info.user = request.user
            info.save()
        else: 
            get_info = Info.objects.get(user=request.user)
            get_info.position = data.get('position').upper()
            get_info.save()

        return JsonResponse({"message": "Updated successfuly"}, status=201)

@login_required(login_url='/login')
@csrf_exempt
def review(request):
    if request.method == "GET":
        return render(request, "reviews/review.html")

    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        review = Review()
        review.user = request.user
        review.name = data.get('name').upper()
        review.position = data.get('position').upper()
        review.days = data.get('days')
        review.hours = data.get('hours')
        review.pay = data.get('pay')
        review.slow = data.get('slow')
        review.busy = data.get('busy')
        review.envo = data.get('envo')
        review.mngmt = data.get('mngmt')
        review.comments = data.get('comments')
        review.rating = data.get('rating')

        review.save()

        return JsonResponse({"message": "Updated successfuly"}, status=201)

@login_required(login_url='/login')
@csrf_exempt
def restaurant(request, restaurant):
    if request.method == "GET":
        all_reviews = Review.objects.filter(name=restaurant).order_by('-id')
        paginator = Paginator(all_reviews, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        server_pay, bar_pay, busser_pay, runner_pay, back_pay = 0, 0, 0, 0, 0
        server_days, bar_days, busser_days, runner_days, back_days = 0, 0, 0, 0, 0
        envo, mngmt, hours, rating = [], [], [], []
            
        for review in all_reviews:
            if review.position == 'SERVER':
                server_pay += review.pay
                server_days += review.days
            elif review.position == 'BARTENDER':
                bar_pay += review.pay
                bar_days += review.days
            elif review.position == 'BUSSER':
                busser_pay += review.pay
                busser_days += review.days
            elif review.position == 'RUNNER':
                runner_pay += review.pay
                runner_days += review.days
            elif review.position == 'BARBACK':
                back_pay += review.pay
                back_days += review.days

            envo.append(review.envo)
            mngmt.append(review.mngmt)
            rating.append(review.rating)
            hours.append(review.hours)

        try:
            serv_four_day = round(server_pay/server_days * 4)
        except ZeroDivisionError:
            serv_four_day = 0
        try:
            bar_four_day = round(bar_pay/bar_days * 4)
        except ZeroDivisionError:
            bar_four_day = 0
        try:
            busser_four_day = round(busser_pay/busser_days * 4)
        except ZeroDivisionError:
            busser_four_day = 0
        try:
            runner_four_day = round(runner_pay/runner_days * 4)
        except ZeroDivisionError:
            runner_four_day = 0
        try:
            back_four_day = round(back_pay/back_days * 4)
        except ZeroDivisionError:
            back_four_day = 0

        all_averages = {
            "serv_four_day": serv_four_day,
            "bar_four_day": bar_four_day,
            "busser_four_day": busser_four_day,
            "runner_four_day": runner_four_day,
            "back_four_day": back_four_day,
            "average_envo": mean(envo),
            "average_mngmt": mean(mngmt),
            "average_hours": mean(hours),
            "average_rating": mean(rating)
        }

        return render(request, 'reviews/restaurant.html', {"restaurant": restaurant, "averages": all_averages, "page_obj": page_obj})

