document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_message);
    document.querySelector('#compose-form').addEventListener('submit', sendmessage);
  
    // By default, load the inbox
    load_mailbox('inbox');
  });
  
  // Generates the form that users use to send an message
  function compose_message() {
  
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#email-page').style.display = 'none';
  
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-body').value = '';
  
  }
  
  // Reply function called when a user clicks the reply button in an message view
  // pre-loads the info from the message that is being replied to. 
  function reply_message(message) {
  
    // Show Reply view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-page').innerHTML = '';
    document.querySelector('#compose-view').style.display = 'block';
  
    // Pre-Fill composition fields
    document.querySelector('#compose-recipients').value = message.sender;
  
    document.querySelector('#compose-body').value = "On " + message.timestamp +
     " " + message.sender +  "  Wrote: " + message.body + "\n\n";
  }
  
  // Backend load that gets all data from the database and passes it along
  function load_mailbox(mailbox) {
    
    console.log("mailbox loaded");
    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-page').style.display = 'none';
    
    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
    // Get messages from API
    fetch(`/chatinbox/messages/${mailbox}`)
    .then(response => response.json())
    .then(messages => {
        // Log messages
        console.log(messages);
  
        // Loop through and display all emails. 
        messages.forEach(element => {
          if (mailbox == 'inbox') {
            showmessages_inbox(element);
          } else if (mailbox == 'sent' 
          && document.querySelector('#emailaddress').innerText == element.sender) {
            showmessages_inbox(element);
          }
  
        });
  
    });
  }
  
  // Renders all messages in the inbox 
  function showmessages_inbox(message){
    const element = document.createElement('div');
    element.innerHTML = message.sender + "  " + message.timestamp;
  
    if (message.read == false) {
      element.style = "border:1px solid black; background-color:white;";
    } 
    else {
      element.style = "border:1px solid black; background-color:lightgrey;";
    }
  
    // Adds listener for each message in case it get's clicked. 
    element.addEventListener('click', () => viewmessage(message));
    document.querySelector('#emails-view').appendChild(element);
  }
  
  // Renders all info and buttons for a single message
  function viewmessage(message) {
  
    // Clear out other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-page').innerHTML = '';
    document.querySelector('#email-page').style.display = 'block';
  
    // Update messsages to be read. 
    fetch(`/chatinbox/messages/${message.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    });
  
    // From field
    const from = document.createElement('div');
    from.innerHTML = "From: " + message.sender;
    document.querySelector('#email-page').appendChild(from);
  
    // TO field
    const recipients = document.createElement('div');
    recipients.innerHTML = "To: " + message.recipients;
    document.querySelector('#email-page').appendChild(recipients);
  
    // Time Stamp
    const timestamp = document.createElement('div');
    timestamp.innerHTML = "Time Stamp: " + message.timestamp;
    document.querySelector('#email-page').appendChild(timestamp);
  
    // Reply Button 
    const reply = document.createElement('button');
    reply.class = "btn btn-sm btn-outline-primary";
    reply.id = "compose";
    reply.innerText = "Reply";
  
    reply.addEventListener('click', function() {
      console.log('Reply to message has been clicked!');
      reply_message(message);
  
    });
    
    document.querySelector('#email-page').appendChild(reply);
  
    // Create body view. 
    const body = document.createElement('p');
    body.innerHTML = message.body;
    body.style = "display: block; margin-top: 1em;";
    document.querySelector('#email-page').appendChild(body);
  
  
  }
  
  // Sends data from compose form to database. 
  function sendmessage() {
  
    // Post emails to the API and then to database. 
    fetch('/chatinbox/messages', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
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