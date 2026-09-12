from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Order


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(
        label="Nome de Usuário",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-surface-container-lowest border border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary rounded px-4 py-2.5 text-on-surface text-sm placeholder-on-surface-variant/50 transition-colors',
            'placeholder': 'ex: tech_master'
        })
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={
            'class': 'w-full bg-surface-container-lowest border border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary rounded px-4 py-2.5 text-on-surface text-sm placeholder-on-surface-variant/50 transition-colors',
            'placeholder': 'seu.email@exemplo.com'
        })
    )
    first_name = forms.CharField(
        label="Nome Completo",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-surface-container-lowest border border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary rounded px-4 py-2.5 text-on-surface text-sm placeholder-on-surface-variant/50 transition-colors',
            'placeholder': 'Nome e Sobrenome'
        })
    )
    password = forms.CharField(
        label="Senha de Acesso",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-surface-container-lowest border border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary rounded px-4 py-2.5 text-on-surface text-sm placeholder-on-surface-variant/50 transition-colors',
            'placeholder': '••••••••••••'
        })
    )
    password_confirm = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-surface-container-lowest border border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary rounded px-4 py-2.5 text-on-surface text-sm placeholder-on-surface-variant/50 transition-colors',
            'placeholder': '••••••••••••'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado no sistema Nexus.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "As senhas digitadas não coincidem.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuário ou E-mail",
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-surface-container-lowest border border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary rounded px-4 py-2.5 text-on-surface text-sm placeholder-on-surface-variant/50 transition-colors',
            'placeholder': 'Usuário cadastrado'
        })
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-surface-container-lowest border border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary rounded px-4 py-2.5 text-on-surface text-sm placeholder-on-surface-variant/50 transition-colors',
            'placeholder': '••••••••••••'
        })
    )


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'full_name', 'email', 'phone', 'cpf',
            'cep', 'address', 'number', 'complement', 'neighborhood', 'city', 'state',
            'payment_method'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full bg-surface-container-lowest border border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary rounded px-4 py-2.5 text-on-surface text-sm',
                'placeholder': 'Nome completo do destinatário'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full bg-surface-container-lowest border border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary rounded px-4 py-2.5 text-on-surface text-sm',
                'placeholder': 'seu@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full bg-surface-container-lowest border border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary rounded px-4 py-2.5 text-on-surface text-sm',
                'placeholder': '(11) 99999-9999'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'w-full bg-surface-container-lowest border border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary rounded px-4 py-2.5 text-on-surface text-sm',
                'placeholder': '000.000.000-00'
            }),
            'cep': forms.TextInput(attrs={
                'class': 'w-full bg-surface-container-lowest border border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary rounded px-4 py-2.5 text-on-surface text-sm font-mono',
                'placeholder': '00000-000'
            }),
            'address': forms.TextInput(attrs={
                'class': 'w-full bg-surface-container-lowest border border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary rounded px-4 py-2.5 text-on-surface text-sm',
                'placeholder': 'Rua, Avenida, Alameda...'
            }),
            'number': forms.TextInput(attrs={
                'class': 'w-full bg-surface-container-lowest border border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary rounded px-4 py-2.5 text-on-surface text-sm',
                'placeholder': '123'
            }),
            'complement': forms.TextInput(attrs={
                'class': 'w-full bg-surface-container-lowest border border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary rounded px-4 py-2.5 text-on-surface text-sm',
                'placeholder': 'Apto, Bloco, Sala (Opcional)'
            }),
            'neighborhood': forms.TextInput(attrs={
                'class': 'w-full bg-surface-container-lowest border border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary rounded px-4 py-2.5 text-on-surface text-sm',
                'placeholder': 'Bairro'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full bg-surface-container-lowest border border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary rounded px-4 py-2.5 text-on-surface text-sm',
                'placeholder': 'Cidade'
            }),
            'state': forms.TextInput(attrs={
                'class': 'w-full bg-surface-container-lowest border border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary rounded px-4 py-2.5 text-on-surface text-sm uppercase font-mono',
                'placeholder': 'UF (ex: SP)'
            }),
            'payment_method': forms.RadioSelect(attrs={
                'class': 'text-primary focus:ring-primary'
            }),
        }


class CouponApplyForm(forms.Form):
    code = forms.CharField(
        label="Cupom de Desconto",
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-surface-container-lowest border border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary rounded px-3 py-2 text-on-surface text-sm font-mono uppercase tracking-wider',
            'placeholder': 'DIGITE SEU CUPOM'
        })
    )


class ShippingSimulationForm(forms.Form):
    cep = forms.CharField(
        label="Calcular Frete",
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-surface-container-lowest border border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary rounded px-3 py-2 text-on-surface text-sm font-mono',
            'placeholder': '00000-000'
        })
    )
