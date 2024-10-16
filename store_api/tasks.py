import time

from celery import shared_task


@shared_task
def send_confirmation_email(user_name, order_id):
    print(f'Sending confirmation email to {user_name} for order {order_id}...')
    time.sleep(5)
    print('Email sent successfully!')
    return f'Email sent to {user_name}'
