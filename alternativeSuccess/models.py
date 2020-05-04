from django.contrib.auth.models import AbstractUser
from django.db import models

# Overrides/extends default user class to include specifics for this website. 
class User(AbstractUser):
    following = models.ManyToManyField("School", related_name="schools_followed", default=None)
    # Each student can follow many schools. 

    program = models.ForeignKey("Program", default=None, null=True, on_delete=models.CASCADE, related_name="studentsprogram")
    isMentor = models.BooleanField(blank=True, default=False)
    mentor = models.ForeignKey("User", blank=True, default=None, null=True, on_delete=models.CASCADE, related_name="studentsmentor")

# Program class, used for a program within a school
class Program(models.Model):
    school = models.ForeignKey("School", blank=True, default=None, null=True, on_delete=models.CASCADE, related_name="schools")
    # Each program has a school associated with it. 
    name = models.TextField(blank=True)

# School class, is the parent of all programs
class School(models.Model):
    programs = models.ManyToManyField("Program", blank=True, default=None, related_name="schoolprograms")
    # Each school can have many programs. 

    name = models.TextField(blank=True)

# Message class, is the object created for each message composed. 
class Message(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey("User", on_delete=models.PROTECT, related_name="messages_sent")
    recipients = models.ManyToManyField("User", related_name="messages_received")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender.email,
            "recipients": [user.email for user in self.recipients.all()],
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "read": self.read,
        }

# Do not forget to run "python manage.py makemigrations" and then "python manage.py migrate"
# after any changes are made to this file. 

# "python manage.py createsuperuser" to create admin account. 