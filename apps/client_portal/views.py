from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.organizations.models import Organization
from apps.sales.models import Invoice
from apps.compliance.models import ComplianceTask
@login_required
def portal_home(request):
    orgs=Organization.objects.filter(members=request.user,is_active=True)
    if request.user.is_superuser: orgs=Organization.objects.filter(is_active=True)
    return render(request,"portal/home.html",{"organizations":orgs,"invoices":Invoice.objects.filter(organization__in=orgs)[:10],"tasks":ComplianceTask.objects.filter(organization__in=orgs)[:10]})
