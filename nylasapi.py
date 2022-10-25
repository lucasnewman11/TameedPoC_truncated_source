from nylas import APIClient

CLIENT_ID = '40svmc7wglkd21uvtadigklqa'
CLIENT_SECRET = 'bwpi53a6jcfttfl9h8sqeanh2'
ACCESS_TOKEN = 'lrkVn0Lk0kAVRVUH4Ayr2II1QaETmg'

nylas = APIClient(
    CLIENT_ID,
    CLIENT_SECRET,
    ACCESS_TOKEN
)

def send_email(recipient, subject, body):
    draft = nylas.drafts.create()
    draft.subject = subject
    draft.body = body
    draft.to = [{'name': 'New Message', 'email': recipient}]
    draft.send()



    


