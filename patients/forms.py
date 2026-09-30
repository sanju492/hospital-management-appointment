from django import forms
from django.contrib.auth import get_user_model
from .models import Patient

User = get_user_model()


class PatientRegistrationForm(forms.ModelForm):

    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput
    )
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(
        max_length=150,
        required=False
    )

    class Meta:
        model = Patient
        fields = [
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'phone',
            'date_of_birth',
            'gender',
            'address',
        ]

        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'gender': forms.Select(),
            'address': forms.Textarea(
                attrs={'rows': 3}
            ),
        }

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'Username already exists.'
            )

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Email already exists.'
            )

        return email