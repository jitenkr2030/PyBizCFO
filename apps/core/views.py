from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.shortcuts import render
from apps.organizations.models import Organization
from apps.accounting.models import JournalEntry, JournalLine, Account
from apps.sales.models import Invoice
from apps.compliance.models import ComplianceTask

@login_required
def dashboard(request):
    # Non-superusers see only organizations they belong to. Demo users are assigned explicitly.
    orgs = Organization.objects.filter(members=request.user, is_active=True)
    if request.user.is_superuser:
        orgs = Organization.objects.filter(is_active=True)
    org_ids = list(orgs.values_list("id", flat=True))
    invoices = Invoice.objects.filter(organization_id__in=org_ids)
    tasks = ComplianceTask.objects.filter(organization_id__in=org_ids, status__in=["pending", "in_progress", "review"])
    revenue = JournalLine.objects.filter(entry__organization_id__in=org_ids, entry__status="posted", account__account_type="income").aggregate(v=Sum("credit"))["v"] or Decimal("0")
    expenses = JournalLine.objects.filter(entry__organization_id__in=org_ids, entry__status="posted", account__account_type="expense").aggregate(v=Sum("debit"))["v"] or Decimal("0")
    context = {
        "organizations": orgs,
        "organization_count": orgs.count(),
        "invoice_count": invoices.count(),
        "open_tasks": tasks.count(),
        "revenue": revenue,
        "expenses": expenses,
        "net_result": revenue - expenses,
        "recent_invoices": invoices.select_related("organization").order_by("-issue_date")[:6],
        "upcoming_tasks": tasks.select_related("organization").order_by("due_date")[:6],
    }
    return render(request, "dashboard.html", context)
