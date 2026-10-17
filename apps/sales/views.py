from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.organizations.models import Organization
from .models import Invoice, Customer
@login_required
def sales_home(request):
    orgs=Organization.objects.filter(members=request.user,is_active=True)
    if request.user.is_superuser: orgs=Organization.objects.filter(is_active=True)
    invoices=Invoice.objects.filter(organization__in=orgs).select_related("organization","customer")
    return render(request,"sales/home.html",{"invoices":invoices,"customers":Customer.objects.filter(organization__in=orgs)})
