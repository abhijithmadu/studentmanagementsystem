from django.contrib.auth.backends import ModelBackend, UserModel
from django.contrib.auth import get_user_model

class EmailBackEnd(ModelBackend):
    def authenticate(self,username= None, password= None, **kwargs):
        UserModele=get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None



        




        
