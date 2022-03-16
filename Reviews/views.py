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

from .models import User, Info, Review

# Create your views here.
@login_required(login_url='/login')
@csrf_exempt
def index(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        try:
            info = Info.objects.get(user=request.user)
            return render(request, 'reviews/index.html', {"info": info, "reviews": reviews})
        except ObjectDoesNotExist:
            return render(request, 'reviews/index.html', {"reviews": reviews})
            
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

# Add/Edit position or location
@login_required(login_url='/login')
@csrf_exempt
def add(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        all_info = Info.objects.filter(user=request.user)
        if not all_info:
            info = Info()
            if data.get('position'):
                info.position = data.get('position')
            else:
                info.location = data.get('location')
            info.user = request.user
            info.save()
        else: 
            get_info = Info.objects.get(user=request.user)
            if data.get('position'):
                get_info.position = data.get('position')
            else:
                get_info.location = data.get('location')
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
        all_reviews = Review.objects.filter(name=restaurant)
        four_day_week = Review.objects.filter(name=restaurant, days=4)
        server_total_pay, bar_total_pay, buss_total_pay, run_total_pay, back_total_pay, envo, mngmt = [], [], [], [], [], [], []

        for review in four_day_week:
            if review.position == 'SERVER':
                server_total_pay.append(review.pay)
            elif review.position == 'BARTENDER':
                bar_total_pay.append(review.pay)
            elif review.position == 'BUSSER':
                buss_total_pay.append(review.pay)
            elif review.position == 'RUNNER':
                run_total_pay.append(review.pay)
            elif review.position == 'BARBACK':
                back_total_pay.append(review.pay)
            
        for review in all_reviews:
            envo.append(review.envo)
            mngmt.append(review.mngmt)

        server_average_pay, bar_average_pay, buss_average_pay, run_average_pay, back_average_pay = 0, 0, 0, 0, 0

        if server_total_pay:
            server_average_pay = mean(server_total_pay)
            print(server_average_pay)
        if bar_total_pay:
            bar_average_pay = mean(bar_total_pay)
        if buss_total_pay:
            buss_average_pay = mean(buss_total_pay)
        if run_total_pay:
            run_average_pay = mean(run_total_pay)
        if back_total_pay:
            back_average_pay = mean(back_total_pay)

        
        all_averages = {
            "server_average_pay": server_average_pay,
            "bar_average_pay":  bar_average_pay,
            "buss_average_pay": buss_average_pay,
            "run_average_pay": run_average_pay,
            "back_average_pay": back_average_pay,
            "average_envo": mean(envo),
            "average_mngmt": mean(mngmt)
        }

        return render(request, 'reviews/restaurant.html', {"restaurant": restaurant, "averages": all_averages})

