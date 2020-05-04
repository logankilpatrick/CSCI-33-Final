# CSCI-33-Final
Final Project for CSCI-33 Spring 2020

## File Breakdown:

| File Name        | What it does   |
| ------------- |:-------------:|
| about.html      | Landing page for user's that are not signed in. |
| error.html      | Landing page for any failed operations. Displays variable error message.      |
| following.html | Displays the schools a user is following.  | 
| inbox.html | Displays the different chat boxes (sent & inbox).      | 
| index.html | Displays available programs for each school if a user is logged in.      | 
| layout.html | Sets the basic format for all other pages. Every page extends this page.     | 
| login.html | Allows returning users to login.    | 
| profile.html | Displays info about a paticular school. (I could have added more details here but I wanted to focus on features)    | 
| program.html | Displays info about a paticular program. Again could be extended easily with more details like cost, students, etc.      | 
| register.html | Allows user to register, select if they are part of a paticular program, and if they are a mentor.    | 
| success.html | Generic page for displaying a success message following a successful database update.      | 
| userprofile.html | Displays info about a user. Has a shortcut to the messages section. Allows for adding/removing mentors/mentees.      | 
| inbox.js | Does most of the logic/rendering of info for the Messages/Chat feature.      | 
| admin.py | Declares models so the admin can manually alter them via the Admin portal.      | 
| models.py | Sets up the User, Program, School, and Message Classes.      | 
| urls.py | Creates the different URL paths for this application.      | 
| zebra stripes | are neat      | 
| zebra stripes | are neat      | 



## Outcomes

__In a sentence (or list of features), define a GOOD outcome for your final project. I.e., what WILL you accomplish no matter what?__

- [x] Ability for mentors/students to sign up
- [x] Breakdown of all the different schools for students
- [x] Chat feature for students/mentors (Using JavaScript)
- [x] Profile for mentors
- ~~Main public feed that shows successful mentored students~~ 
  - (Switched to have the main feed be newly added programs)

__In a sentence (or list of features), define a BETTER outcome for your final project. I.e., what do you THINK you can accomplish before the final project's deadline?__

- ~~Calendar integration so mentors and students can set up times to talk~~
  - Upon further investiagtion, the "Date Input" html attribute is not universally supported by browsers (like Safari) so I decided to remove this feature. 
- [ ] Better CSS to make the site more friendly and modern (this is a weak point for me as I am not very good at designing User Interfaces)

__In a paragraph or more, outline your next steps. What new skills will you need to acquire? What topics will you need to research?__

 I plan to start things off simply. I want to get the User Signup for Students and mentors set. Then I will create the ability for mentors to add Schools and subsequent programs at those schools. These will be visible to students. 

After that, I will add the mentor profiles which will allow me to set up a review process for the mentors so that after the student's connect, they can review said mentor. Once the profile is setup, I will then allow the student to actually contact a mentor for a particular school/program. This is when I will integrate the text based chat for the student/mentor. 

The "relationship" between the student and mentor will have three states: in progress, ended-bad, and ended-good. Ended-good state relationships will show up on the main public feed that is visible without signing in along with a required student testimonial. 

I think the biggest thing I will need to focus on is the user interfaces. I am not very good at (and truthfully not very passionate about) making the interfaces all pretty and refined so I am going to have to push myself to make it so this App does not look bland and boring. 
