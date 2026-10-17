from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.organizations.models import Organization
from .models import BankAccount, BankTransaction
@login_required
def banking_home(request):
    orgs=Organization.objects.filter(members=request.user,is_active=True)
    if request.user.is_superuser: orgs=Organization.objects.filter(is_active=True)
    accounts=BankAccount.objects.filter(organization__in=orgs)
    return render(request,"banking/home.html",{"accounts":accounts,"transactions":BankTransaction.objects.filter(bank_account__in=accounts).select_related("bank_account")[:50]})
