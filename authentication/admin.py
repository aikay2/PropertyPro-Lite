# admin.py in your authentication app
from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Agent, Customer

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=[
        ('agent', 'Agent'),
        ('customer', 'Customer')
    ])
    
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'address', 'phoneNumber', 'user_type')

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
            user_type = self.cleaned_data['user_type']
            if user_type == 'agent':
                Agent.objects.create(user=user)
            else:
                Customer.objects.create(user=user)
        
        return user


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ('username', 'first_name', 'last_name', 'is_staff')

    # Specify fields for the admin
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'address', 'phoneNumber', 'is_active', 'is_staff')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'address', 'phoneNumber', 'password1', 'password2', 'user_type'),
        }),
    )
    
admin.site.register(CustomUser, CustomUserAdmin)
