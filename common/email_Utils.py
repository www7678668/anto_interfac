#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/7/25 17:05
# @Author  : zhangwen
# @File    : email_Utils.py
# @Software: PyCharm

import smtplib
import unittest
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from common.setting_path import *
from common import HTMLTestReportCN
from common.localconfig_utils import local_config

class EmailUtils():
    def __init__(self,smtp_body,smtp_attch_path=None):
       self.smtp_server = local_config.SMTP_SERVER
       self.smtp_sender = local_config.SMTP_SENDER
       self.smtp_password = local_config.SMTP_PASSWORD
       self.smtp_receiver = local_config.SMTP_RECEIVER
       self.smtp_cc = local_config.SMTP_CC
       self.smtp_subject = local_config.SMTP_SUBJECT
       self.smtp_body = smtp_body
       self.smtp_attch = smtp_attch_path

    def mail_message_body(self):
        message = MIMEMultipart()
        message['from'] = self.smtp_sender
        message['to'] = self.smtp_receiver
        message['Cc'] = self.smtp_cc
        message['subject'] = self.smtp_subject
        message.attach( MIMEText(self.smtp_body,'html','utf-8') )
        if self.smtp_attch:
            attach_file = MIMEText(open(self.smtp_attch, 'rb').read(), 'base64', 'utf-8')
            attach_file['Content-Type'] = 'application/octet-stream'
            attach_file.add_header('Content-Disposition', 'attachment', filename=('gbk', '', os.path.basename(self.smtp_attch)))
            message.attach(attach_file)
        return message

    def send_mail(self):
        smtp = smtplib.SMTP()
        smtp.connect(self.smtp_server)
        smtp.login(user=self.smtp_sender, password=self.smtp_password)
        smtp.sendmail(self.smtp_sender,self.smtp_receiver.split(",")+ self.smtp_cc.split(","), self.mail_message_body().as_string())

if __name__=='__main__':
    test_report_path_new = os.path.join(test_report_path, 'P1P2接口自动化测试报告V1.5')
    html_path = os.path.join(test_report_path_new , 'P1P2接口自动化测试报告V1.5.html')
    print(html_path)
    EmailUtils('<h3 align="center">自动化测试报告</h3>',html_path).send_mail()