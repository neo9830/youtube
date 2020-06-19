def sendmail(sender, receiver, subject, body_content, smpt_server, dir_path):

    import smtplib
    import os
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart
    #from smtplib import SMTPExecption
    import configparser

    #Reading config file
    config = configparser.ConfigParser()
    config.read("Path for the configuration file to store the username and password for the sender email")
    #make sure to match the following section or you can edit your own section
    username = config['credentials']['username'] 
    password = config['credentials']['password']

    msg = MIMEMultipart()
    msg['To'] = receiver
    msg['From'] = sender
    msg['Subject'] = subject

    body = MIMEText(body_content, 'html', 'utf-8')
    msg.attach(body)

    files = []
    for r, d, f in os.walk(dir_path):
        for file in f:
            files.append(os.path.join(r, file))
    if dir_path is not None:
        for file_path in files:
            attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
            attachment.add_header('Content-Disposition', 'attachment', filename = file_path)
            msg.attach(attachment)
    try: 
        server = smtplib.SMTP(smpt_server)
        server.starttls()
        server.login(username, password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.close()
        return "Success"
    except SMTPException:
        return "Connection failed"
    except TimeoutError:
        return "Connection time exceeded"


