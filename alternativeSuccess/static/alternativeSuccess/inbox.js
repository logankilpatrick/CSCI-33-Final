document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);
    document.querySelector('#compose-form').addEventListener('submit', sendemail);
  
    // By default, load the inbox
    load_mailbox('inbox');
  });
  
  // Generates the form that users use to send an email
  function compose_email() {
  
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#email-page').style.display = 'none';
  
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  
  }
  
  // Reply function called when a user clicks the reply button in an email view
  // pre-loads the info from the email that is being replied to. 
  function reply_email(email) {
  
    // Show Reply view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-page').innerHTML = '';
    document.querySelector('#compose-view').style.display = 'block';
  
    // Pre-Fill composition fields
    document.querySelector('#compose-recipients').value = email.sender;
  
    if ((email.subject.includes("Re:")) == false) {
      document.querySelector('#compose-subject').value = "Re:" + email.subject;
    } else {
      document.querySelector('#compose-subject').value = email.subject
    }
    document.querySelector('#compose-body').value = "On " + email.timestamp +
     " " + email.sender +  "  Wrote: " + email.body + "\n\n";
  }
  
  // Backend load that gets all data from the database and passes it along
  function load_mailbox(mailbox) {
  
    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-page').style.display = 'none';
    
    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
    // Get emails from API
    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
        // Log emails
        console.log(emails);
  
        // Loop through and display all emails. 
        emails.forEach(element => {
          if (mailbox == 'inbox' && element.archived == false) {
            showemail_inbox(element);
          } else if (mailbox == 'archive') {
            showemail_inbox(element);
          } else if (mailbox == 'sent' 
          && document.querySelector('#emailaddress').innerText == element.sender) {
            showemail_inbox(element);
          }
  
        });
  
    });
  }
  
  // Renders all emails in the inbox 
  function showemail_inbox(email){
    const element = document.createElement('div');
    element.innerHTML = email.sender + "  " + email.subject + "    " + email.timestamp;
  
    if (email.read == false) {
      element.style = "border:1px solid black; background-color:white;";
    } 
    else {
      element.style = "border:1px solid black; background-color:lightgrey;";
    }
  
    // Adds listener for each email in case it get's clicked. 
    element.addEventListener('click', () => viewemail(email));
    document.querySelector('#emails-view').appendChild(element);
  }
  
  // Renders all info and buttons for a single email
  function viewemail(email) {
  
    // Clear out other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-page').innerHTML = '';
    document.querySelector('#email-page').style.display = 'block';
  
    // Update email to be read. 
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    });
  
    // From field
    const from = document.createElement('div');
    from.innerHTML = "From: " + email.sender;
    document.querySelector('#email-page').appendChild(from);
  
    // TO field
    const recipients = document.createElement('div');
    recipients.innerHTML = "To: " + email.recipients;
    document.querySelector('#email-page').appendChild(recipients);
  
    // Subject
    const subject = document.createElement('div');
    subject.innerHTML = "Subject: " + email.subject;
    document.querySelector('#email-page').appendChild(subject);
  
    // Time Stamp
    const timestamp = document.createElement('div');
    timestamp.innerHTML = "Time Stamp: " + email.timestamp;
    document.querySelector('#email-page').appendChild(timestamp);
  
    // Reply Button 
    const reply = document.createElement('button');
    reply.class = "btn btn-sm btn-outline-primary";
    reply.id = "compose";
    reply.innerText = "Reply";
    //reply.onclick = compose_email;
  
    reply.addEventListener('click', function() {
      console.log('Reply to email has been clicked!');
      reply_email(email);
  
    });
    
    document.querySelector('#email-page').appendChild(reply);
  
    if (email.archived == false) {
      // Archive Button 
      const archive = document.createElement('button');
      archive.class = "btn btn-sm btn-outline-primary";
      archive.id = "archive";
      archive.innerText = "Archive";
  
      archive.addEventListener('click', function() {
  
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: true
          })
        });
        console.log('Email Archived.');
        load_mailbox('inbox');
      
      });
      
      document.querySelector('#email-page').appendChild(archive);
  
    } else {
        // Un-Archive Button 
        const unarchive = document.createElement('button');
        unarchive.class = "btn btn-sm btn-outline-primary";
        unarchive.id = "archive";
        unarchive.innerText = "Un-Archive";
    
        unarchive.addEventListener('click', function() {
    
          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived: false
            })
          });
          console.log('Email Un-Archived.');
          load_mailbox('inbox');
        
        });
        
        document.querySelector('#email-page').appendChild(unarchive);
  
    }
  
    // Create body view. 
    const body = document.createElement('p');
    body.innerHTML = email.body;
    body.style = "display: block; margin-top: 1em;";
    document.querySelector('#email-page').appendChild(body);
  
  
  }
  
  // Sends data from compose form to database. 
  function sendemail() {
  
    // Post emails to the API and then to database. 
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value,
      })
    })
    .then(response => response.json())
    .then(result => {
        // Log results
        console.log(result);     
    });
    load_mailbox('sent');
  
  }