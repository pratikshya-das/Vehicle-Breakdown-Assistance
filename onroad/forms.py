from django import forms
import hashlib
from hashlib import md5
from .models import  UserReg,User,Feedback,PasswordReset,Payment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth import get_user_model
from .models import Business

User = get_user_model()

class DateInput(forms.DateInput):
    input_type = 'date'


class BusinessCreate(forms.ModelForm):
        
    class Meta:
             
           model = Business
           
           fields = ('business','mechanic', 'service', 'available','address','mobile','locality','city','loggeduser')
           
           widgets = {'loggeduser': forms.HiddenInput(), 'latitude': forms.HiddenInput(),'longitude': forms.HiddenInput(),'status': forms.HiddenInput()}
class MapCreate(forms.ModelForm):
        
    class Meta:
             
           model = Business
           
           fields = ('latitude','longitude')
         
            
class FeedbackCreate(forms.ModelForm):
     loggeduser = forms.CharField(widget=forms.HiddenInput()) 
     feedcreateuser = forms.CharField(widget=forms.HiddenInput()) 
     class Meta:
             
            model = Feedback
            fields = ('name','feedback','loggeduser','feedcreateuser')

           
class PayCreate(forms.ModelForm):
     
     class Meta:
             
            model = Payment
            fields = ('Name','Cardno','Expirydate','CCV','Amount','loggeduser','payuser','created_at')
            widgets = {'loggeduser': forms.HiddenInput(), 'payuser': forms.HiddenInput(),'Expirydate': DateInput()}

    
 
class ShopSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','first_name', 'last_name', 'email','answer1')
     

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_mechanic = True
        if commit:
            user.save()
        return user

class UserForm(forms.ModelForm):

     class Meta: 
            model = User
            fields = ('username','first_name', 'last_name', 'email')
class ForgetpasswordForm(UserCreationForm):

     class Meta(UserCreationForm.Meta): 
            model = User
            field = ('answer1')
class ResetpasswordForm(forms.ModelForm):
    
    answer1 = forms.CharField(widget=forms.HiddenInput()) 
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta: 
            model = User
            fields=('answer1','password')
            
          

class UserSignUpForm(UserCreationForm):
   

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','first_name', 'last_name', 'email','answer1')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_user = True
        if commit:
           user.save()
           userreg = UserReg.objects.create(user=user)
      
        return user
