#!usr/bin/env python
# coding:utf-8

import os
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.utils import parseaddr, formataddr
from email import encoders
import smtplib
import datetime
import time


class Config(object):
    def __init__(self, addr, name):
        self.addr = addr
        self.name = name


def readconfig():
    """Read configure file.

    Return:
        config, type:Config.
    """
    configpath = os.path.join(os.path.dirname(__file__), 'notificate.ini')
    if not os.path.isfile(configpath):
        print('Not find notificate.ini\n')
        return None
    config = Config(list(), list())
    with open(configpath) as f:
        for line in f:
            if line.startswith('email'):
                email = line.split('=')[1].strip()
                if email:
                    config.addr.append(email)
            if line.startswith('name'):
                name = line.split('=')[1].strip()
                if name:
                    config.name.append(name)
    if not config.addr or not config.name:
        print('Not find valid email or name information\n')
        return None
    return config


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def notificate(subject, message=None, files=None):
    """notificate.

    Args:
        subject:subject of email.
        message:message of email.
        files:file attacment.
    """
    # read to_addr  and to_name from notificate.ini
    config = readconfig()
    if not config:
        print('Not valid configure\n')
        return

    from_addr = '2654757322@qq.com'
    password = 'ohpisdmsdtqkeabf'
    smtp_server = 'smtp.qq.com'
    msg = MIMEMultipart()
    msg['From'] = _format_addr('Jin Xueyuan <%s>' % from_addr)
    msg['To'] = ', '.join([
        _format_addr('%s <%s>' % (to_name, to_addr))
        for to_addr, to_name in zip(config.addr, config.name)
    ])
    msg['Subject'] = Header(subject, 'utf-8').encode()
    if message:
        msg.attach(MIMEText('%s' % message, 'plain', 'utf-8'))
    if files:
        for filepath in files:
            with open(filepath, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.add_header(
                    'Content-Disposition',
                    'attacment',
                    filename=os.path.basename(filepath))
                part.set_payload(f.read())
                encoders.encode_base64(part)
                msg.attach(part)

    while True:
        try:
            server = smtplib.SMTP_SSL(smtp_server, 465)
            server.login(from_addr, password)
            server.sendmail(from_addr, config.addr, msg.as_string())
            server.quit()
            now = str(datetime.datetime.now().replace(second=0, microsecond=0))
            for to_addr in config.addr:
                print('%s: Send email to %s successfully!\n' % (now, to_addr))
        except:
            time.sleep(300)
        else:
            break
