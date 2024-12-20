from django import forms
from .models import Author, Category, Post, Profile
from django.contrib.auth.forms import PasswordChangeForm
from django.forms.widgets import DateInput
from datetime import datetime, date

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'birth_date']
        widgets = {
            'birth_date': DateInput(format='%d/%m/%Y', attrs={
                'type': 'text',  
                'placeholder': 'dd/mm/yyyy',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].input_formats = ['%d/%m/%Y']    

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')

        
        if isinstance(birth_date, date):
            birth_date = birth_date.strftime('%d/%m/%Y')

        try:
            
            datetime.strptime(birth_date, '%d/%m/%Y')
        except ValueError:
            raise forms.ValidationError('El formato de fecha debe ser DD/MM/YYYY.')
        
        return self.cleaned_data.get('birth_date')  

class CustomPasswordChangeForm(PasswordChangeForm):
    pass

