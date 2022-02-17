from django.core.mail import send_mail


def send_activation_code(email, activation_code):
    activation_url = f'http://localhost:8000/v1/api/account/activate/{activation_code}'
    message = f"""
        Thank you for signing up!
        Please, activate your account.
        Click on the link: {activation_url} to activate your account.
    """
    send_mail(
        'Activate your account',
        message,
        'AvtoDom@icloud.com',
        [email, ],
        fail_silently=False
    )