from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Program, School
import time

# Returns all posts in order of when they were created. 
def index(request):
    schools = School.objects.order_by("-name").all()
    programs = Program.objects.all()

    return render(request, "network/index.html", {
        "schools": schools, 
        "programs": programs,
    })
    #TODO: Still need to do paignation

# Shows the "following" page where only made by a user that you are following will show.
def following(request):

    posts = Post.objects.order_by("-creation_time").all()
    users = User.objects.all()
    
    followed_posts = []

    # Logic to get only posts that are of users the current user is following 
    for post in posts.all():
        if post.author in request.user.following.all():
            followed_posts.append(post)


    return render(request, "network/following.html", {
        "posts": followed_posts
    })

# Shows the Schools profile when their profile name is clicked on
# Renders followers, following, and unfollow button logic. 
def profile(request, schoolID):
    schools = School.objects.order_by("-name").all()
    programs = Program.objects.all()

    schoolName = schools[schoolID].name

    # TODO: Pre-compute number of followers who follow said school. Use old code. 

    

    return render(request, "network/profile.html", {
        "schools": schools, 
        "programs": programs,
        "SchoolID":schoolID,
        "schoolName": schoolName
    })

# Creates a new School object and then returns us to the index page. 
@login_required
def newschool(request):
    if request.method == "POST":
        name = request.POST["body"]        
        schoolName = School.objects.filter(name = name).exists()
        
        # If the school name already exists, take them back to the main page. 
        if schoolName:
            # TODO: Go to 404 page instead or stay on the same page. 
            return render(request, "network/index.html")


        school = School(name=name)
        school.save()

        return render(request, "network/index.html")


# Creates a new Program object and then returns us to the index page. 
@login_required
def newprogram(request):
    if request.method == "POST":
        programname = request.POST["programname"]
        schoolname = request.POST["schooloptions"]

        schoolobj = School.objects.get(name=schoolname)

        school = Program(school=schoolobj, name=programname)
        school.save()

        return render(request, "network/index.html")


@login_required
def editpost(request, post_id):
    if request.method == "POST":

        # Attempt to sign user in
        body = request.POST["body"]
        
        post = Post(content=body, author=request.user)
        post.save()

    return render(request, "network/index.html")

# This will follow a user that is not being followed right now
@login_required
def follow(request, schoolName):
    if request.method == "POST":

        for user in User.objects.all():
            if user.id == author_id: 
                # TODO: This does not work.
                user.following.filter(id=user.id)
                user.save()

    # Return to the index page after a unfollow. 
    # TODO: Should stay on the same page. 
    posts = Post.objects.order_by("-creation_time").all()

    return render(request, "network/index.html", {
        "posts": posts
    })


# This will unfollow a user that is being followed right now
@login_required
def unfollow(request, schoolName):
    if request.method == "POST":
        for user in User.objects.all():
            if user.id == author_id: 
                user.following.filter(id=user.id).delete()
                user.save()

    # Return to the index page after a unfollow. 
    # TODO: Should stay on the same page. 
    posts = Post.objects.order_by("-creation_time").all()

    return render(request, "network/index.html", {
        "posts": posts
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    programs = Program.objects.all()
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        programName = request.POST["programoptions"]        
        programobj = Program.objects.get(name=programName)

        try:
            request.POST["ismentor"] 
            isMentor = True
        except:
            # If it errors out it means the box was not checked. 
            isMentor = False

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, program=programobj, isMentor=isMentor)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html", {
            "programs": programs,
        })
