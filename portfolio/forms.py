from django import forms
from .models import Profile, Skill, Project, Resume

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Message', 'class': 'form-control', 'rows': 5}))

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'placeholder': 'Your Bio', 'class': 'form-control', 'rows': 5}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'proficiency']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Skill Name', 'class': 'form-control'}),
            'proficiency': forms.NumberInput(attrs={'placeholder': 'Proficiency (0-100)', 'class': 'form-control', 'min': 0, 'max': 100}),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'image', 'link']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Project Title', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Project Description', 'class': 'form-control', 'rows': 5}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'link': forms.URLInput(attrs={'placeholder': 'Project URL (optional)', 'class': 'form-control'}),
        }

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }