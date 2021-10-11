from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, paginateProjects

'''
Filler Data
projectList = [
    {
        'id': '1',
        'title': 'Ecommerce website',
        'description': 'Fully functional ecommerce website'
    },
    {
        'id': '2',
        'title': 'Portfolio website',
        'description': 'A project highlighting my portfolio'
    },
    {
        'id': '3',
        'title': 'Social Network',
        'description': 'Awesome ongoing open source project'
    },
]
'''

def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)
    context = {'projects': projects, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)

# Read of CRUD
def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        # commit=False is used to get the instance (review in this case) before saving
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        # update project vote count
        projectObj.updateVote()

        messages.success(request, 'Your review was successfully submitted')
        return redirect('project', pk=projectObj.id)

    context = {'project': projectObj, 'form': form}
    return render(request, 'projects/single_project.html', context)

@login_required(login_url="login")
# Create of CRUD
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('projects')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login")
# Update of CRUD
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('projects')
    context = {'form': form, 'project': project}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login")
# Delete of CRUD
def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'delete.html', context)
