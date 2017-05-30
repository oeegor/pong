import logging

from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template


log = logging.getLogger('mail')


def send_templated_mail(
    subject,
    template_name,
    recipients,
    context=None,
    sender=None,
    bcc=None,
    cc=None,
    files=None,
    fail_silently=False
):
    # remove duplicates from bcc
    if not bcc:
        bcc = []
    if cc:
        bcc = set(bcc) - set(cc)
    bcc = list(set(bcc) - set(recipients))

    context = context or {}
    files = files or []

    text = get_template(template_name).render(Context(context))
    msg = EmailMultiAlternatives(
        subject,
        text,
        sender,
        list(recipients),
        bcc=bcc,
        cc=cc,
    )
    msg.attach_alternative(text, 'text/html')

    for file_data in files:
        msg.attach(*file_data)

    log.info('sending {} to {} bcc {}'.format(template_name, recipients, bcc))
    msg.send(fail_silently=fail_silently)
