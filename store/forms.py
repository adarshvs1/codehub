from django import forms

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from store.models import UserProfile,Project,Reviews





class SignUpForm(UserCreationForm):

    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    password2=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:

        model=User

        fields=['username','email','password1','password2']

        widgets={

            'username':forms.TextInput(attrs={'class':'form-control'}),

            'email':forms.EmailInput(attrs={'class':'form-control'})


        }

class SignInForm(forms.Form):

    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    

#Userprofile

class UserprofileForm(forms.ModelForm):

    class Meta:

        model=UserProfile

        fields=['bio','profile_pic']

        widgets={

            'bio':forms.TextInput(attrs={'class':'w-full border p-2 my-3'}),

            'profile_pic':forms.FileInput(attrs={'class':'w-full border p-2 my-3'})
        }

        
class ProjectForm(forms.ModelForm):

    class Meta:

        model=Project

        exclude={'owner','created_date','updated_date','is_active'} #do not wanted fields
       
        widgets={
            'title':forms.TextInput(attrs={'class':'w-full border p-2 mb-3'}),

            'description':forms.Textarea(attrs={'class':'w-full border p-2 mb-3','rows':5}),

            'thumbnail':forms.TextInput(attrs={'class':'w-full border p-2 mb-3 mt-3'}),

            'price':forms.NumberInput(attrs={'class':'w-full p-3 border mb-3'}),

            'files':forms.FileInput(attrs={'class':'w-full p-3 border mb-3'}),

            'tag_objects':forms.SelectMultiple(attrs={'class':'w-full p-3 border mb-3 mt-4'})

        }


#review form

class ReviewForm(forms.ModelForm):

    class Meta:

        model= Reviews

        fields= ['comment','rating']