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
    # TODO: Make creation time and not name. 

    programs = Program.objects.all()

    return render(request, "alternativeSuccess/index.html", {
        "schools": schools, 
        "programs": programs,
    })

# Shows the Schools profile when their profile name is clicked on
# Renders followers, following, and unfollow button logic. 
def profile(request, schoolID):
    schools = School.objects.get(id=schoolID)
    programs = Program.objects.all()

    schoolName = schools.name

    # TODO: Pre-compute number of followers who follow said school. Use old code. 
    followers = 0
    users = User.objects.all()
    if request.user.is_authenticated:
        for user in users:
            schoolsFollowed = request.user.following.all()
            for school in schoolsFollowed:
                if school.name == schoolName:
                    followers += 1


    followed = False

    if request.user.is_authenticated:
        for school in request.user.following.all():
            if schoolID == school.id:
                followed = True


    return render(request, "alternativeSuccess/profile.html", {
        "schools": schools, 
        "programs": programs,
        "SchoolID":schoolID,
        "schoolName": schoolName,
        "followed": followed,
        "followers": followers,
    })

# Shows the Programs profile when their profile name is clicked on
# Renders studnets in the program who are mentors. 
def program(request, schoolName, programName):
    school = School.objects.get(name=schoolName)
    program = Program.objects.get(school=school, name=programName)

    students = User.objects.filter(program=program)

    # TODO: I think we may want to pass in the User object itself. 

    return render(request, "alternativeSuccess/program.html", {
        "program": program,
        "SchoolName":schoolName,
        "programName": programName,
        "Students": students,
    })

# Naviagtes user to the profile of another user. 
@login_required
def userprofile(request, studentID):
    student = User.objects.get(id=studentID)

    return render(request, "alternativeSuccess/userprofile.html", {
        "studentID": student.id,
        "programschool": student.program.school.name,
        "programname": student.program.name,
        "studentname": student.username,
        "isMentor": student.isMentor,
    })

# Naviagtes user to the profile of another user. 
@login_required
def chat(request):
    pass

# Creates a new School object and then returns us to the index page. 
@login_required
def newschool(request):
    if request.method == "POST":
        name = request.POST["body"]        
        schoolName = School.objects.filter(name = name).exists()
        
        # If the school name already exists, take them back to the main page. 
        if schoolName:
            # TODO: Go to 404 page instead or stay on the same page. 
            return render(request, "alternativeSuccess/index.html")


        school = School(name=name)
        school.save()

        return HttpResponseRedirect(
            request.META.get("HTTP_REFERER", reverse("index"))
        )

# Creates a new Program object and then returns us to the index page. 
@login_required
def newprogram(request):
    if request.method == "POST":
        programname = request.POST["programname"]
        schoolname = request.POST["schooloptions"]

        schoolobj = School.objects.get(name=schoolname)

        school = Program(school=schoolobj, name=programname)
        school.save()

        return HttpResponseRedirect(
            request.META.get("HTTP_REFERER", reverse("index"))
        )


@login_required
def editpost(request, post_id):
    if request.method == "POST":

        # Attempt to sign user in
        body = request.POST["body"]
        
        post = Post(content=body, author=request.user)
        post.save()

    return render(request, "alternativeSuccess/index.html")

# Shows the "following" page where only schools you are following will show.
def following(request):
    schools = request.user.following.all()
    
    programs = []
    for school in schools:
        holder = Program.objects.filter(school=school)
        for program in holder:
            programs.append(program)
    
    return render(request, "alternativeSuccess/following.html", {
        "schools": schools,
        "programs": programs,
    })

# This will follow a user that is not being followed right now
@login_required
def follow(request, schoolName):

    if request.method == "POST":

        schoolobj = School.objects.get(name=schoolName)        
        request.user.following.add(schoolobj)
        request.user.save()

    return HttpResponseRedirect(reverse("profile", args=(schoolobj.id,)))


# This will unfollow a user that is being followed right now
@login_required
def unfollow(request, schoolName):

    if request.method == "POST":

        schoolobj = School.objects.get(name=schoolName)
        request.user.following.remove(schoolobj)        
        request.user.save()

    return HttpResponseRedirect(reverse("profile", args=(schoolobj.id,)))


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
            return render(request, "alternativeSuccess/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "alternativeSuccess/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    programs = Program.objects.all()
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        try:
            programName = request.POST["programoptions"]
            programobj = Program.objects.get(name=programName)
        except:
            programobj = None

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
            return render(request, "alternativeSuccess/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, program=programobj, isMentor=isMentor)
            user.save()
        except IntegrityError:
            return render(request, "alternativeSuccess/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "alternativeSuccess/register.html", {
            "programs": programs,
        })
