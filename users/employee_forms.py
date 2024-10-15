from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from .models import Employee


class EmployeeLoginForm(forms.Form):
    """
    A form for handling employee login using cell number and password.

    Fields:
        - cell_number: A CharField to input the employee's mobile number with a maximum length of 13 characters.
        - password: A CharField to input the employee's password with a maximum length of 50 characters.

    Widgets:
        - cell_number: Uses TextInput with Bootstrap classes for styling and a placeholder for formatting.
        - password: Uses PasswordInput with Bootstrap classes for styling and a placeholder for password entry.
    """
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


class EmployeeRegistrationForm(forms.ModelForm):
    """
    A form for employee registration, extending Django's ModelForm.

    Fields:
        - cell_number: Employee's mobile number, used as a unique identifier.
        - first_name: Employee's first name.
        - last_name: Employee's last name.
        - admission_group: The employee's level of electrical safety clearance, chosen from predefined options.
        - password: The employee's password for account authentication.
        - confirm_password: A confirmation field to ensure the password is entered correctly.

    Widgets:
        - password: Uses PasswordInput widget to obscure the password input.
        - confirm_password: Uses PasswordInput widget to obscure the confirm password input.

    Meta:
        - model: The form is linked to the `Employee` model.
        - fields: Specifies the fields included in the form, including custom `password` and `confirm_password` fields.
    """
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Підтвердити пароль', widget=forms.PasswordInput)


    class Meta:
        model = Employee
        fields = ['cell_number', 'first_name', 'last_name', 'admission_group', 'password']

    def __init__(self, *args, **kwargs):
        super(EmployeeRegistrationForm, self).__init__(*args, **kwargs)
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
        


class EmployeeCellUpdateForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 
                                                                 'placeholder': 'Введіть Ваш пароль'}
                                                        )
                               )

    class Meta:
        model = Employee
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
        user = authenticate(
            username=self.instance.cell_number, 
            password=password,
            )
        if not user:
            raise forms.ValidationError('Невірний пароль.')
        return cleaned_data


class EmployeePasswordChangeForm(PasswordChangeForm):
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


class EmployeePasswordCheckForm(forms.Form):
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
