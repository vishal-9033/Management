from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

class EmailSender:

    def send_email_custom(self, from_email, to_email, variable_dict):
        html_content = render_to_string("admin_template/mails/email.html", variable_dict)
        email = EmailMultiAlternatives(self, html_content, from_email, to_email)
        email.send()
        
class ReminderEmailSender:
    def send_email_custom(self,subject,from_email, to_email, variable_dic):
        html_content = render_to_string("admin_template/mails/email_remind.html", variable_dic)
        email = EmailMultiAlternatives(subject, html_content, from_email, to_email)
        email.send()