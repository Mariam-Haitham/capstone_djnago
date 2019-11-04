from django.core.mail import send_mail

def send_email(first_name, last_name, recipient, role):
    send_mail(
       'Book Care Invitation',
       ('This is an automated email.\n You have been invited to become a {} by {} {}.'
        .format(role, first_name, last_name)) ,
       'bookcare8982@gmail.com',
       recipient,
       fail_silently=False,
    )