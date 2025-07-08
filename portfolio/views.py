from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .models import Profile, Skill, Project, Resume, ContactMessage
from .forms import ProfileForm, SkillForm, ProjectForm, ResumeForm, ContactForm

def index(request):
    profile = Profile.objects.filter(user__is_active=True).first()
    skills = Skill.objects.filter(user__is_active=True)[:6]
    projects = Project.objects.filter(user__is_active=True)[:3]
    resume = Resume.objects.filter(user__is_active=True).first()
    return render(request, 'index.html', {
        'profile': profile,
        'skills': skills,
        'projects': projects,
        'resume': resume,
    })

def about(request):
    profile = Profile.objects.filter(user__is_active=True).first()
    return render(request, 'about.html', {'profile': profile})

def skills(request):
    skills = Skill.objects.filter(user__is_active=True)
    return render(request, 'skills.html', {'skills': skills})

def projects(request):
    projects = Project.objects.filter(user__is_active=True)
    return render(request, 'projects.html', {'projects': projects})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = ContactMessage(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            contact_message.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

@login_required
def dashboard(request):
    profile = get_object_or_404(Profile, user=request.user)
    skills = Skill.objects.filter(user=request.user)
    projects = Project.objects.filter(user=request.user)
    resume = Resume.objects.filter(user=request.user).first()
    contact_messages = ContactMessage.objects.all()

    # Initialize forms
    profile_form = ProfileForm(instance=profile)
    skill_form = SkillForm()
    project_form = ProjectForm()
    resume_form = ResumeForm(instance=resume)

    if request.method == 'POST':
        if 'profile_form' in request.POST:
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Error updating profile. Please check the form.')
        elif 'skill_form' in request.POST:
            skill_form = SkillForm(request.POST)
            if skill_form.is_valid():
                skill = skill_form.save(commit=False)
                skill.user = request.user
                skill.save()
                messages.success(request, 'Skill added successfully!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Error adding skill. Please check the form.')
        elif 'project_form' in request.POST:
            project_form = ProjectForm(request.POST, request.FILES)
            if project_form.is_valid():
                project = project_form.save(commit=False)
                project.user = request.user
                project.save()
                messages.success(request, 'Project added successfully!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Error adding project. Please check the form.')
        elif 'resume_form' in request.POST:
            resume_form = ResumeForm(request.POST, request.FILES, instance=resume)
            if resume_form.is_valid():
                resume = resume_form.save(commit=False)
                resume.user = request.user
                resume.save()
                messages.success(request, 'Resume uploaded successfully!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Error uploading resume. Please check the form.')
        elif 'delete_skill' in request.POST:
            skill_id = request.POST.get('delete_skill')
            skill = get_object_or_404(Skill, id=skill_id, user=request.user)
            skill.delete()
            messages.success(request, 'Skill deleted successfully!')
            return redirect('dashboard')
        elif 'delete_project' in request.POST:
            project_id = request.POST.get('delete_project')
            project = get_object_or_404(Project, id=project_id, user=request.user)
            project.delete()
            messages.success(request, 'Project deleted successfully!')
            return redirect('dashboard')
        elif 'delete_resume' in request.POST:
            resume_id = request.POST.get('delete_resume')
            resume = get_object_or_404(Resume, id=resume_id, user=request.user)
            resume.delete()
            messages.success(request, 'Resume deleted successfully!')
            return redirect('dashboard')
        elif 'delete_message' in request.POST:
            message_id = request.POST.get('delete_message')
            message = get_object_or_404(ContactMessage, id=message_id)
            message.delete()
            messages.success(request, 'Message deleted successfully!')
            return redirect('dashboard')

    return render(request, 'dashboard.html', {
        'profile': profile,
        'skills': skills,
        'projects': projects,
        'resume': resume,
        'contact_messages': contact_messages,
        'profile_form': profile_form,
        'skill_form': skill_form,
        'project_form': project_form,
        'resume_form': resume_form,
    })

def download_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    response = HttpResponse(resume.file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{resume.file.name}"'
    return response