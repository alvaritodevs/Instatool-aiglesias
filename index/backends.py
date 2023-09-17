from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        print("hola ma g")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
            
        else:
            if user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
class UserManager:
    def create_user(self, email, password):
        user = User(email, password)  # Assuming User is a class representing a user
        # Code to store the user in a database or perform any other necessary operations
        # ...
        return user