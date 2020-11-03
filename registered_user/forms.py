from django.forms import ModelForm
from registered_user.models import Parents_Details, User_Details, Image

class MakeForm(ModelForm):
    class Meta:
        model = Parents_Details
        fields = '__all__'
class UserForm(ModelForm):
    class Meta:
        model = User_Details
        exclude = ('user','profile_pic')
        fields = '__all__'

class ImageForm(ModelForm):
    class Meta:
        model= Image
        exclude = ('user',)
        fields= ["name", "imagefile"]