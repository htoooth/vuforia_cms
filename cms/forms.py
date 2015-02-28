from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate

# CustomFileInput用に。
from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_text
from django.forms.widgets import FileInput, Input, CheckboxInput

from cms.models import UserProfile, Content

PW_MIN_LENGTH = 8


class UserProfileForm(forms.ModelForm):
    error_css_class = 'error'
    class Meta:
        model = UserProfile
        fields = ('acc_type_id', 'enterprise', 'person', 'address',
                  'email','phone_number',)

class CreateUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('acc_type_id', 'enterprise', 'person', 'address',
                  'email','phone_number', 'password',)
        widgets = {'password': forms.PasswordInput(),}

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # At least PW_MIN_LENGTH long
        if len(password) < PW_MIN_LENGTH:
            raise forms.ValidationError(
                "The new password must be at least %d characters long." % PW_MIN_LENGTH)
        # At least one letter and one non-letter
        first_isalpha = password[0].isalpha()
        if all(c.isalpha() == first_isalpha for c in password):
            raise forms.ValidationError(
                "The new password must contain at least one letter and at least one digit or punctuation character.")
        return password


class ValidatingPasswordChangeForm(PasswordChangeForm):
    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        # At least PW_MIN_LENGTH long
        if len(password1) < PW_MIN_LENGTH:
            raise forms.ValidationError(
                "The new password must be at least %d characters long." % PW_MIN_LENGTH)
        # At least one letter and one non-letter
        first_isalpha = password1[0].isalpha()
        if all(c.isalpha() == first_isalpha for c in password1):
            raise forms.ValidationError(
                "The new password must contain at least one letter and at least one digit or punctuation character.")
        return password1


# 以下は、Contentモデルに関するフォーム
#class CustomClearableFileInput(ClearableFileInput):
class CustomFileInput(FileInput):
    """
    下の ContentFormクラスのためのウィジェット
    (画像編集の時の Djangoのデフォルトを修正するために)
    """
    def render(self, name, value, attrs=None):
        substitutions = {
            #uncomment to get 'Currently'
            'initial_text': "", # self.initial_text,
            #'input_text': self.input_text,
            'clear_template': '',
            #'clear_checkbox_label': self.clear_checkbox_label,
            }
        template = '%(input)s'
        substitutions['input'] = Input.render(self, name, value, attrs)

        if value and hasattr(value, "url"):
            #template = self.template_with_initial
            substitutions['initial'] = (
                        '<img src="%s" alt="%s" width="80" height="80"/>'
                                        % (escape(value.url),
                                           escape(force_text(value))))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(
                                                            checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(
                                                            checkbox_id)
                substitutions['clear'] = CheckboxInput().render(
                            checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = (self.template_with_clear
                                                        % substitutions)

        return mark_safe(template % substitutions)

class ContentForm(forms.ModelForm):
    image = forms.ImageField(label='マーカー', required=True,
                             widget=CustomFileInput(),
                             #allow_empty_file=True
                             )
    class Meta:
        model = Content
        fields = ('open_from', 'open_to', 'title', 'mapping_url', 'image',)
        widgets = {
            'open_from': forms.DateInput(
                                attrs={'data-datepicker':'datepicker'}),
            'open_to': forms.DateInput(
                                attrs={'data-datepicker':'datepicker'}),
        }

class ContractForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ('contracted_at',)


# 以下は、ログインに関するフォーム
class LoginForm(forms.Form):
    user_id = forms.IntegerField(label="ユーザーID", min_value=1)
    acc_type_id = forms.ChoiceField(label="アカウントタイプ",
                                  choices=UserProfile.ACC_TYPE_CHOICES)
    #identifier = forms.CharField(label="アカウント")
    password = forms.CharField(label="パスワード",
                               widget=forms.PasswordInput)

class Form_connection(forms.Form):
    username = forms.CharField(label="Login")
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(Form_connection, self).clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not authenticate(username=username, password=password):
            raise forms.ValidationError("Wrong login or password")
        return self.cleaned_data
