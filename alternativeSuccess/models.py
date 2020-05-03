from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("School", related_name="schools_followed", default=None)
    # Each student can follow many schools. 

    program = models.ForeignKey("Program", default=None, null=True, on_delete=models.CASCADE, related_name="studentsprogram")
    isMentor = models.BooleanField(blank=True, default=False)
    mentor = models.ForeignKey("User", blank=True, default=None, null=True, on_delete=models.CASCADE, related_name="studentsmentor")



class Program(models.Model):
    school = models.ForeignKey("School", blank=True, default=None, null=True, on_delete=models.CASCADE, related_name="schools")
    # Each program has a school associated with it. 
    name = models.TextField(blank=True)

class School(models.Model):
    programs = models.ManyToManyField("Program", blank=True, default=None, related_name="schoolprograms")
    # Each school can have many programs. 

    name = models.TextField(blank=True)


class Message(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="emails")
    sender = models.ForeignKey("User", on_delete=models.PROTECT, related_name="emails_sent")
    recipients = models.ManyToManyField("User", related_name="emails_received")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender.email,
            "recipients": [user.message for user in self.recipients.all()],
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "read": self.read,
        }

# Do not forget to run "python manage.py makemigrations" and then "python manage.py migrate"
# after any changes are made to this file. 

# "python manage.py createsuperuser" to create admin account. 