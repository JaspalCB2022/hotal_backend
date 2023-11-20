from .models import User
def setPasswordForUser():
    print("start call")
    u = User.objects.get(email="jesse63@okeefe.com")
    print("start call >> u", u)
    u.set_password("testing321")
    u.save()

