from django.core.mail import send_mail

import base64
import uuid
from django.core.files.base import ContentFile

def send_email(first_name, last_name, recipient, role):
    send_mail(
       'Peek-a-Baby App Invitation',
       ('This is an automated email. Please do not reply.\nYou have been invited to become a {} by {} {} to be part of their household.\n Please download the app and sign up with your email to join.'
        .format(role, first_name, last_name)) ,
       'bookcare8982@gmail.com',
       recipient,
       fail_silently=False,
    )


def decode_base64(encoding):
	extension = ""
	result={}
	if 'data:' in encoding and ';base64,' in encoding:
		extension, encoding = encoding.split(';base64,')
	try:
		result = base64.standard_b64decode(encoding)
	except TypeError:
		print("error:", TypeError)
	if extension:
		trash, extension = extension.split('/')
	else:
		extension = "png"
	name = (str(uuid.uuid4())[:12])
	file_name = "%s.%s" % (name, extension)
	data = ContentFile(result, name=file_name)
	return data