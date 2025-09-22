from socket import *
import sys

MAILSERVER ="list.winthrop.edu"
PORT = 25
SENDER = "sakyie2@winthrop.edu"
RECIPIENT = "atiasea2@winthrop.edu"
SUBJECT = "SMTP Mail Client Test"
BODY = "This is a test email message for the Project."

def send_and_recv(sock, line: str, expect: str | None = None):
    if not line.endswith("\r\n"):
        line += "\r\n"
    sock.sendall(line.encode("ascii"))
    reply = sock.recv(4096).decode("ascii", errors="replace")
    print(reply, end="")
    if expect and not reply.startswith(expect):
        print("Did not receive expected reply from server.")
        sys.exit(1)
    return reply


client = socket(AF_INET, SOCK_STREAM)
client.connect((MAILSERVER, PORT))

banner = client.recv(4096).decode("ascii", errors="replace")
print(banner, end='')

send_and_recv(client, "HELO winthrop.edu", "250")
send_and_recv(client, f"MAIL FROM:<{SENDER}>", "250")
send_and_recv(client, f"RCPT TO:<{RECIPIENT}>", "250")
send_and_recv(client, "DATA", "354")

lines = [
    f"From: {SENDER}",
    f"To: {RECIPIENT}",
    f"Subject: {SUBJECT}",
    "",
    BODY,
]
for ln in lines: 
   if ln.startswith('.'):
       ln = '.' + ln
   client.sendall((ln + '\r\n').encode("ascii"))

send_and_recv(client, ".", "250")
send_and_recv(client, "QUIT", "221")
client.close()
