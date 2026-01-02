from django import forms
from django.contrib.auth.models import User

class CadastroForm(forms.ModelForm):
    nome = forms.CharField(
        label="Nome Completo", 
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu nome'})
    )
    telefone = forms.CharField(
        label="Telefone", 
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '(00) 00000-0000'})
    )
    # Usei 'email' explicitamente para garantir que ele seja o foco
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={'placeholder': 'seu@email.com'})
    )
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'placeholder': 'Crie uma senha'})
    )
    confirmar_senha = forms.CharField(
        label="Confirme a Senha",
        widget=forms.PasswordInput(attrs={'placeholder': 'Repita a senha'})
    )

    class Meta:
        model = User
        # REMOVA o 'username' daqui. Deixe apenas o 'email'.
        # Isso diz ao Django para não exigir o preenchimento do username no HTML.
        fields = ['email']

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirmar_senha = cleaned_data.get("confirmar_senha")

        if senha != confirmar_senha:
            # Erro específico para o campo de confirmação
            self.add_error('confirmar_senha', "As senhas não conferem!")
        
        return cleaned_data