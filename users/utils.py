from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProfiles(request, profiles, num_results):
    page = request.GET.get('page')
    paginator = Paginator(profiles, num_results)

    try:
        # Get the first page of the results
        profiles = paginator.page(page)
    except PageNotAnInteger:
        # set page number to 1 by default if page is not passed
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = (int(page)-4)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page)+5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)
    return custom_range, profiles

def searchProfiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    #skills = Skill.objects.filter(name__iexact=search_query)
    skills = Skill.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(intro__contains=search_query) |
        Q(skill__in=skills)
    )

    return profiles, search_query
