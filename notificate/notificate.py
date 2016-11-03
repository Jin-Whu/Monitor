#!usr/bin/env python
# coding:utf-8

import os
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def notificate(subject, message):
    """notificate.

    Args:
        subject:subject of email.
        message:message of email.
    """
    # read to_addr  and to_name from notificate.ini
    to_addr = None
    to_name = None
    with open(os.path.join(os.path.dirname(__file__), 'notificate.ini')) as f:
        for line in f:
            if line.startswith('email'):
                to_addr = line.split('=')[1].strip()
            if line.startswith('name'):
                to_name = line.split('=')[1].strip()
    if not to_addr:
        print 'Nont find to_addr'
        return
    if not to_name:
        print 'Not find to_name'
        return
    from_addr = '2654757322@qq.com'
    password = 'fzawrkqsgdzfecdd'
    smtp_server = 'smtp.qq.com'
    msg = MIMEText('%s' % message, 'plain', 'utf-8')
    msg['From'] = _format_addr('Jin Xueyuan <%s>' % from_addr)
    msg['To'] = _format_addr('%s <%s>' % (to_name, to_addr))
    msg['Subject'] = Header(subject, 'utf-8').encode()

    while True:
        try:
            server = smtplib.SMTP_SSL(smtp_server, 465)
            server.login(from_addr, password)
            server.sendmail(from_addr, [to_addr], msg.as_string())
            server.quit()
            print 'Send email successfully!'
        except:
            print 'Send email failed, try again...'
        else:
            break
