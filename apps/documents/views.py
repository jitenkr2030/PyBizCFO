from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.organizations.models import Organization
from .models import Document
@login_required
def documents_home(request):
    orgs=Organization.objects.filter(members=request.user,is_active=True)
    if request.user.is_superuser: orgs=Organization.objects.filter(is_active=True)
    return render(request,"documents/home.html",{"documents":Document.objects.filter(organization__in=orgs).select_related("organization","uploaded_by")})
