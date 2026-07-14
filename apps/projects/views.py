from django.shortcuts import render, get_object_or_404
from .models import Project

def project_list(request):
    projects = Project.objects.all()
    
    # Extract unique technologies for styling filter pills
    all_techs = set()
    for project in projects:
        for tech in project.get_tech_list():
            all_techs.add(tech)
            
    context = {
        'projects': projects,
        'all_techs': sorted(list(all_techs)),
    }
    return render(request, 'projects.html', context)

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    context = {
        'project': project,
    }
    return render(request, 'project_detail.html', context)
