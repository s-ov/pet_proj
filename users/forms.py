from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, authenticate

CustomUser = get_user_model()


class UserLoginForm(forms.Form):
    cell_number = forms.CharField(
        max_length=13,
        label='Номер мобільного',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+380501234567'
        },
        )
    )
    password = forms.CharField(
        max_length=50,
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Введіть Ваш пароль'
            })
    )


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Підтвердити пароль', widget=forms.PasswordInput)


    class Meta:
        model = CustomUser
        fields = ['cell_number', 'first_name', 'last_name', 'admission_group', 'password']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            self.fields['cell_number'].label = 'Номер мобільного'
            self.fields['cell_number'].widget.attrs['placeholder'] = '+380501234567'
            self.fields['first_name'].label = 'Ім\'я'
            self.fields['last_name'].label = 'Прізвище'
            self.fields['admission_group'].label = 'Група допуску'

            self.fields['cell_number'].error_messages.update({
            'required': 'Номер мобільного обов’язково.',
            'invalid': 'Введіть правильний номер мобільного.',
            'unique': 'Цей номер вже зареєстровано.',
            })
            self.fields['password'].error_messages.update({
                'required': 'Пароль обов’язковий.',
            })

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Паролі не співпадають.')
        return cleaned_data
        


class UserCellUpdateForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 
                                                                 'placeholder': 'Введіть Ваш пароль'}
                                                        )
                               )

    class Meta:
        model = CustomUser
        fields = ['cell_number',]
        widgets = {
            'cell_number': forms.TextInput(attrs={'class': 'form-control'}),
            }
        labels = {
            'cell_number': 'Номер мобільного',  
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        user = authenticate(username=self.instance.cell_number, password=password)
        if not user:
            raise forms.ValidationError('Невірний пароль.')
        return cleaned_data


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Старий пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введіть старий пароль'}),
        error_messages = {
            'password_incorrect': 'Введіть правильний пароль.', 
            'required': 'Будь ласка, введіть старий пароль.'
            }
    )
    new_password1 = forms.CharField(
        max_length=50,
        min_length=8,
        label="Новий пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введіть новий пароль'}),
        error_messages={
            'required': 'Будь ласка, введіть новий пароль.',
            'max_length': 'Пароль занадто довгий: не більше 50 символів.',
            'min_length': 'Пароль занадто короткий: не менше 8 символів.',
        }
    )
    new_password2 = forms.CharField(
        label="Новий пароль (підтвердження)",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Підтвердіть новий пароль'}),
        error_messages={
            'required': 'Будь ласка, підтверджте новий пароль.',
            'password_mismatch': 'Новий пароль і підтвердження паролю не співпадають.',
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2:
            if new_password1 != new_password2:
                self.add_error('new_password2', 'Паролі не збігаються.')
        return cleaned_data


class UserPasswordCheckForm(forms.Form):
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={ 
                                        'class': 'form-control', 
                                        'placeholder': 'Введіть пароль'
                                        }
                                    ),
        strip=False,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not self.user.check_password(password):
            raise forms.ValidationError("Невірний пароль. Будь ласка, спробуйте ще раз.")
        return password
