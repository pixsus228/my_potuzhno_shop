from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=False, label="Електронна пошта", widget=forms.EmailInput(attrs={'class': 'w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white focus:border-amber-400 focus:outline-none transition'}))

    class Meta:
        model = Profile
        fields = ['phone', 'address', 'photo', 'email']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white focus:border-amber-400 focus:outline-none transition'}),
            'address': forms.Textarea(attrs={'rows': 2, 'id': 'np-address-input', 'class': 'w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white focus:border-amber-400 focus:outline-none transition'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white focus:border-amber-400 focus:outline-none transition file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-amber-500 file:text-slate-950 hover:file:bg-amber-600'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.email = self.cleaned_data.get('email', '')
        if commit:
            user.save()
            profile.save()
        return profile
