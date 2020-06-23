from celery import task

from django.core.mail import send_mail

from shopping.shop.models import Order


@task
def order_created(order_id):
    """
    a task to send email notification when successfully created an order
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f" Dear {order.name},  Order successfully placed.  Your order id is {order.id}"
    mail_sent = send_mail(subject,
                          message,
                          'admin@shopping.com',
                          [order.email]
                          )
    return mail_sent
