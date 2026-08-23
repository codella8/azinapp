from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator, EmailValidator
from .models import Contact, Profile


# ======================================== #
# 1. CONTACT FORM                          #
# ======================================== #

class ContactForm(forms.ModelForm):
    """Contact form for website visitors"""
    
    name = forms.CharField(
        label=_("Full Name"),
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your full name'),
            'id': 'contactName'
        }),
        error_messages={
            'required': _('Please enter your name.'),
            'max_length': _('Name cannot exceed 100 characters.'),
        }
    )
    
    email = forms.EmailField(
        label=_("Email Address"),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('example@email.com'),
            'id': 'contactEmail'
        }),
        error_messages={
            'required': _('Please enter your email address.'),
            'invalid': _('Please enter a valid email address.'),
        }
    )
    
    message = forms.CharField(
        label=_("Message"),
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': _('Enter your message here...'),
            'id': 'contactMessage'
        }),
        error_messages={
            'required': _('Please enter your message.'),
        }
    )
    
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
    
    def clean_email(self):
        """Validate email address"""
        email = self.cleaned_data.get('email')
        if email:
            validator = EmailValidator()
            try:
                validator(email)
            except forms.ValidationError:
                raise forms.ValidationError(_('Please enter a valid email address.'))
        return email


# ======================================== #
# 2. USER PROFILE FORMS                   #
# ======================================== #

class UpdateUserInfo(forms.ModelForm):
    """Form for updating user profile information"""
    
    phone = forms.CharField(
        label=_("Phone Number"),
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('e.g. 09123456789'),
            'dir': 'ltr'
        }),
        error_messages={
            'required': _('Please enter your phone number.'),
        }
    )
    
    address1 = forms.CharField(
        label=_("Address Line 1"),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your address')
        })
    )
    
    address2 = forms.CharField(
        label=_("Address Line 2"),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your address (optional)')
        })
    )
    
    city = forms.CharField(
        label=_("City"),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your city')
        })
    )
    
    country = forms.CharField(
        label=_("Country"),
        required=False,
        initial='Iran',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your country')
        })
    )
    
    class Meta:
        model = Profile
        fields = ['phone', 'address1', 'address2', 'city', 'country']
    
    def clean_phone(self):
        """Validate phone number"""
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove spaces and dashes
            phone = phone.replace(' ', '').replace('-', '')
            # Check if only digits
            if not phone.isdigit():
                raise forms.ValidationError(_('Phone number must contain only digits.'))
            if len(phone) < 10:
                raise forms.ValidationError(_('Phone number must be at least 10 digits.'))
        return phone


# ======================================== #
# 3. PASSWORD FORMS                       #
# ======================================== #

class UpdatePasswordForm(SetPasswordForm):
    """Form for changing user password"""
    
    new_password1 = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your new password'),
            'id': 'newPassword1',
            'autocomplete': 'new-password'
        }),
        error_messages={
            'required': _('Please enter your new password.'),
        }
    )
    
    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your new password again'),
            'id': 'newPassword2',
            'autocomplete': 'new-password'
        }),
        error_messages={
            'required': _('Please confirm your new password.'),
        }
    )
    
    def clean_new_password1(self):
        """Validate new password strength"""
        password = self.cleaned_data.get('new_password1')
        if password:
            if len(password) < 8:
                raise forms.ValidationError(_('Password must be at least 8 characters.'))
            if not any(char.isdigit() for char in password):
                raise forms.ValidationError(_('Password must contain at least one number.'))
            if not any(char.isalpha() for char in password):
                raise forms.ValidationError(_('Password must contain at least one letter.'))
        return password


# ======================================== #
# 4. USER UPDATE FORM                     #
# ======================================== #

class UserUpdateForm(UserChangeForm):
    """Form for updating user account information"""
    
    password = None  # Remove password field from form
    
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your first name')
        })
    )
    
    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your last name')
        })
    )
    
    email = forms.EmailField(
        label=_("Email Address"),
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('example@email.com')
        }),
        error_messages={
            'invalid': _('Please enter a valid email address.'),
        }
    )
    
    username = forms.CharField(
        label=_("Username"),
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your username')
        })
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
    
    def clean_username(self):
        """Validate username"""
        username = self.cleaned_data.get('username')
        if username:
            if len(username) < 3:
                raise forms.ValidationError(_('Username must be at least 3 characters.'))
            if not username.isalnum():
                raise forms.ValidationError(_('Username must contain only letters and numbers.'))
            # Check uniqueness
            if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
                raise forms.ValidationError(_('This username is already taken.'))
        return username
    
    def clean_email(self):
        """Validate email"""
        email = self.cleaned_data.get('email')
        if email:
            # Check uniqueness
            if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
                raise forms.ValidationError(_('This email is already registered.'))
        return email


# ======================================== #
# 5. SIGNUP FORM                          #
# ======================================== #

class SignUpForm(UserCreationForm):
    """Form for new user registration"""
    
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your first name'),
            'autofocus': True
        }),
        error_messages={
            'required': _('Please enter your first name.'),
        }
    )
    
    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your last name')
        }),
        error_messages={
            'required': _('Please enter your last name.'),
        }
    )
    
    email = forms.EmailField(
        label=_("Email Address"),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('example@email.com')
        }),
        error_messages={
            'required': _('Please enter your email address.'),
            'invalid': _('Please enter a valid email address.'),
        }
    )
    
    username = forms.CharField(
        label=_("Username"),
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your username')
        }),
        error_messages={
            'required': _('Please enter your username.'),
        },
        help_text=_('Minimum 3 characters, letters and numbers only.')
    )
    
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your password'),
            'autocomplete': 'new-password'
        }),
        error_messages={
            'required': _('Please enter your password.'),
        },
        help_text=_('Minimum 8 characters including letters and numbers.')
    )
    
    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your password again'),
            'autocomplete': 'new-password'
        }),
        error_messages={
            'required': _('Please confirm your password.'),
        }
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
    
    def clean_username(self):
        """Validate username"""
        username = self.cleaned_data.get('username')
        if username:
            if len(username) < 3:
                raise forms.ValidationError(_('Username must be at least 3 characters.'))
            if not username.isalnum():
                raise forms.ValidationError(_('Username must contain only letters and numbers.'))
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError(_('This username is already taken.'))
        return username
    
    def clean_email(self):
        """Validate email"""
        email = self.cleaned_data.get('email')
        if email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError(_('This email is already registered.'))
        return email
    
    def clean_password1(self):
        """Validate password strength"""
        password = self.cleaned_data.get('password1')
        if password:
            if len(password) < 8:
                raise forms.ValidationError(_('Password must be at least 8 characters.'))
            if not any(char.isdigit() for char in password):
                raise forms.ValidationError(_('Password must contain at least one number.'))
            if not any(char.isalpha() for char in password):
                raise forms.ValidationError(_('Password must contain at least one letter.'))
        return password
    
    def clean_password2(self):
        """Check if passwords match"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('Passwords do not match.'))
        
        return password2
    
    def save(self, commit=True):
        """Save user with email"""
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user


# ======================================== #
# 6. EXTRA FORMS (Optional)               #
# ======================================== #

class SearchForm(forms.Form):
    """Search form"""
    query = forms.CharField(
        label=_("Search"),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Search...'),
            'aria-label': _('Search')
        })
    )
    
    category = forms.ChoiceField(
        label=_("Category"),
        required=False,
        choices=[],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )


class NewsletterForm(forms.Form):
    """Newsletter subscription form"""
    email = forms.EmailField(
        label=_("Email Address"),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your email address'),
            'aria-label': _('Subscribe to newsletter')
        }),
        error_messages={
            'required': _('Please enter your email address.'),
            'invalid': _('Please enter a valid email address.'),
        }
    )