import smtplib


def Email_it(email_to, subject, msg1, msg2=None, code=None):
    my_gmail = "testaksmtp@gmail.com"
    password = "rtnyvzjslbfbbwtv"   
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_gmail, password=password)
        connection.sendmail(from_addr=my_gmail,
                            to_addrs=email_to,
                            msg=f"Subject:{subject}\n\n{msg1} {code} {msg2}")