# Ethel Sakyi
# CSCI 466 - Simple Mail Transfer Protocol Lab
from socket import *
import sys

# Configuration
MAILSERVER ="list.winthrop.edu" #server 
PORT = 25 # port 
SENDER = "sakyie2@winthrop.edu" # sender email
RECIPIENT = "atiasea2@winthrop.edu" # recipient email
SUBJECT = "SMTP Mail Client Test"  # email subject
BODY = "This is a test email message for the Project." # email body

# Helper function to send a command and receive a reply
def send_and_recv(sock, line: str, expect: str | None = None): 
    if not line.endswith("\r\n"):
        line += "\r\n"
    sock.sendall(line.encode("ascii")) # send the command to the server
    reply = sock.recv(4096).decode("ascii", errors="replace") #then read the servers reply
    print(reply, end="") # print the reply to the terminal
     # check if the reply starts with the expected code
    if expect and not reply.startswith(expect):
        print("Did not receive expected reply from server.")
        sys.exit(1)
    return reply


client = socket(AF_INET, SOCK_STREAM) # creating a TCP socket 
client.connect((MAILSERVER, PORT)) # connecting to the mail server on port 25

banner = client.recv(4096).decode("ascii", errors="replace") # initial 220 banner from the server
print(banner, end='') # transcript

send_and_recv(client, "HELO winthrop.edu", "250") # send HELO command and expect 250 reply
send_and_recv(client, f"MAIL FROM:<{SENDER}>", "250") # send MAIL FROM command and expect 250 reply
send_and_recv(client, f"RCPT TO:<{RECIPIENT}>", "250") # send RCPT TO command and expect 250 reply
send_and_recv(client, "DATA", "354") # send DATA command and expect 354 reply

lines = [ # email headers and body
    f"From: {SENDER}", 
    f"To: {RECIPIENT}", 
    f"Subject: {SUBJECT}",
    "",
    BODY,
] # lines of the email message
for ln in lines: 
   if ln.startswith('.'):
       ln = '.' + ln
   client.sendall((ln + '\r\n').encode("ascii")) # send each line of the email with CRLF

send_and_recv(client, ".", "250")
send_and_recv(client, "QUIT", "221")
client.close()
