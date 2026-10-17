from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from apps.organizations.models import Organization
from apps.accounting.models import JournalLine
@login_required
def reports_home(request):
    orgs=Organization.objects.filter(members=request.user,is_active=True)
    if request.user.is_superuser: orgs=Organization.objects.filter(is_active=True)
    qs=JournalLine.objects.filter(entry__organization__in=orgs,entry__status="posted")
    totals={}
    for typ in ["asset","liability","equity","income","expense"]:
        totals[typ]=qs.filter(account__account_type=typ).aggregate(debit=Sum("debit"),credit=Sum("credit"))
    revenue=(totals["income"]["credit"] or Decimal("0"))-(totals["income"]["debit"] or Decimal("0"))
    expenses=(totals["expense"]["debit"] or Decimal("0"))-(totals["expense"]["credit"] or Decimal("0"))
    return render(request,"reports/home.html",{"totals":totals,"revenue":revenue,"expenses":expenses,"net_result":revenue-expenses})
