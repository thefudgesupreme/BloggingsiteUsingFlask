import os, secrets
from email.message import EmailMessage

from PIL import Image
from flask import url_for,current_app

from FlaskBlog import mail,fromEmail,emailPassword



def save_pic(form_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    pic_filename = random_hex + f_ext
    pic_path = os.path.join(current_app.root_path, 'static/profiles', pic_filename)
    form_pic.save(pic_path)

    output_size = (125, 125)
    i = Image.open(form_pic)
    i.thumbnail(output_size)
    i.save(pic_path)
    return pic_filename


def sendResetEmail(user):
    token = user.getResetToken()
    msg = EmailMessage()
    msg.set_content(f'''To reset your password,visit following link:
        {url_for('users.resetToken', token=token, _external=True)}
If you don't want to change password then don't do anything & password won't be changed
                     ''')

    toEmail = user.email

    msg['Subject'] = "Password Reset Request"
    msg['From'] = fromEmail
    msg['To'] = toEmail
    mail.starttls()
    mail.login(fromEmail, emailPassword)
    mail.send_message(msg)
    mail.quit()
