from django.core.mail import EmailMessage, BadHeaderError


def send_email_message(to_email, subject, message, from_email="support@test.com"):
    try:
        if subject and message and from_email and to_email:
            try:
                send_email = EmailMessage(subject, message, from_email, to=[to_email])
                send_email.content_subtype = "html"
                send_email.send()
                response_data = {"message": "Email sent successfully"}
            except BadHeaderError:
                response_data = {"error": "Invalid header found"}
            except Exception as e:
                response_data = {
                    "error": f"An error occurred while sending the email: {str(e)}"
                }
        else:
            response_data = {"error": "Incomplete email data"}
    except Exception as e:
        response_data = {"error": f"An error occurred: {str(e)}"}

    return response_data
