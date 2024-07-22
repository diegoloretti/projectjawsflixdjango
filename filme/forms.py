from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django import forms

class FormHomepage(forms.Form):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu e-mail'}))


class CriarContaForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Informe um e-mail válido.')

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Nome de usuário',
            'password1': 'Senha',
            'password2': 'Confirmação de senha',
        }
        help_texts = {
            'username': None,
        }
        error_messages = {
            'password_mismatch': 'As senhas não coincidem.',
        }
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está cadastrado.')
        return email