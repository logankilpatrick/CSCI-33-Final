from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json


from .models import User, Program, School, Message
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

def chatindex(request):
    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "alternativesuccess/inbox.html")

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

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
            schoolsFollowed = user.following.all()
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

    programschool = None

    try:
        programschool = student.program.school.name
    except:
        pass
    
    programname = None

    try:
        programname = student.program.name
    except:
        pass

    return render(request, "alternativeSuccess/userprofile.html", {
        "studentID": student.id,
        "programschool": programschool,
        "programname": programname,
        "studentname": student.username,
        "isMentor": student.isMentor,
        "studentemail": student.email,
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

# TODO: This needs to be updated. Likely won't have time. 
# Should allow a mentor to edit the info about a school/program.
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

# This will follow a mentor so assign themself as the mentor of a student
@login_required
def addMentee(request, username):

    if request.method == "POST":
        menteeName = request.POST["menteeName"]
        try:
            mentor = User.objects.get(username=username)
            User.objects.get(username=menteeName).studentsmentor.update(mentor=mentor)
        except:
            # This catches if there is no username.
            return render(request, "alternativeSuccess/error.html")

        return render(request, "alternativeSuccess/success.html")

    return HttpResponseRedirect(reverse("userprofile", args=(request.user.id,)))

## Follow/Unfollow functions:

# This will follow a user that is not being followed right now
@login_required
def follow(request, schoolName):

    if request.method == "POST":
        user = User.objects.get(username=request.user.username)

        schoolobj = School.objects.get(name=schoolName)        
        user.following.add(schoolobj)

    return HttpResponseRedirect(reverse("profile", args=(schoolobj.id,)))


# This will unfollow a user that is being followed right now
@login_required
def unfollow(request, schoolName):

    if request.method == "POST":
        schoolobj = School.objects.get(name=schoolName)
        request.user.following.remove(schoolobj)        

    return HttpResponseRedirect(reverse("profile", args=(schoolobj.id,)))

# Used to send Messages
@csrf_exempt
@login_required
def compose(request):    
    # Composing a new message must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient emails
    data = json.loads(request.body)
    emails = [message.strip() for message in data.get("recipients").split(",")]
    if emails == [""]:
        return JsonResponse({
            "error": "At least one recipient required."
        }, status=400)

    # Convert email addresses to users
    recipients = []
    for email in emails:
        try:
            user = User.objects.get(email=email)
            recipients.append(user)
        except User.DoesNotExist:
            return JsonResponse({
                "error": f"User with email {email} does not exist."
            }, status=400)

    # Get contents of message
    body = data.get("body", "")

    # Create one message for each recipient, plus sender
    users = set()
    users.add(request.user)
    users.update(recipients)
    for user in users:
        message = Message(
            user=user,
            sender=request.user,
            body=body,
            read=user == request.user
        )
        message.save()
        for recipient in recipients:
            message.recipients.add(recipient)
        message.save()

    return JsonResponse({"message": "Message sent successfully."}, status=201)

# Mail boxes function. Routes us to the correct mailbox (sent, inbox, etc.)
@login_required
def chatbox(request, mailbox):
    # Filter emails returned based on mailbox
    if mailbox == "inbox":
        messages = Message.objects.filter(
            user=request.user, recipients=request.user
        )
    elif mailbox == "sent":
        messages = Message.objects.filter(
            user=request.user, sender=request.user
        )
    elif mailbox == "archive":
        messages = Message.objects.filter(
            user=request.user, recipients=request.user
        )
    else:
        return JsonResponse({"error": "Invalid mailbox."}, status=400)

    # Return messages in reverse chronologial order
    messages = messages.order_by("-timestamp").all()
    return JsonResponse([message.serialize() for message in messages], safe=False)


@csrf_exempt
@login_required
def message(request, message_id):

    # Query for requested email
    try:
        message = Message.objects.get(user=request.user, pk=message_id)
    except Message.DoesNotExist:
        return JsonResponse({"error": "Message not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(message.serialize())

    # Update whether email is read or should be archived
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("read") is not None:
            message.read = data["read"]
        message.save()
        return HttpResponse(status=204)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)




# Login, Logout, Register Functions:

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
