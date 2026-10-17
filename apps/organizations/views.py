from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Organization
@login_required
def organization_list(request):
    qs=Organization.objects.filter(members=request.user,is_active=True)
    if request.user.is_superuser: qs=Organization.objects.filter(is_active=True)
    return render(request,"organizations/list.html",{"organizations":qs})
