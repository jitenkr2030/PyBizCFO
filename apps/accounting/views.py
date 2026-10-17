from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.exceptions import ValidationError
from apps.organizations.models import Organization
from apps.audit.models import AuditEvent
from .models import Account, JournalEntry, JournalLine
from .forms import JournalEntryForm, JournalLineFormSet

def allowed_orgs(user):
    qs=Organization.objects.filter(members=user,is_active=True)
    return Organization.objects.filter(is_active=True) if user.is_superuser else qs

@login_required
def accounting_home(request):
    orgs=allowed_orgs(request.user)
    ids=orgs.values_list("id",flat=True)
    entries=JournalEntry.objects.filter(organization_id__in=ids).select_related("organization","created_by")
    return render(request,"accounting/home.html",{"organizations":orgs,"entries":entries[:30],"accounts":Account.objects.filter(organization_id__in=ids)})

@login_required
def journal_create(request):
    orgs=allowed_orgs(request.user)
    if request.method=="POST":
        form=JournalEntryForm(request.POST)
        form.fields["organization"].queryset=orgs
        if form.is_valid():
            with transaction.atomic():
                entry=form.save(commit=False); entry.created_by=request.user; entry.save()
                lines=JournalLineFormSet(request.POST,instance=entry)
                if lines.is_valid():
                    objects=lines.save(commit=False)
                    for obj in objects:
                        if obj.account.organization_id != entry.organization_id:
                            form.add_error(None,"All accounts must belong to the selected organization."); break
                    else:
                        for obj in objects: obj.entry=entry; obj.full_clean(); obj.save()
                        for obj in lines.deleted_objects: obj.delete()
                        entry.refresh_from_db()
                        if entry.lines.count()<2 or not entry.is_balanced:
                            messages.error(request,"Journal saved as draft. Add at least two lines and ensure total debits equal credits.")
                        AuditEvent.objects.create(actor=request.user,organization=entry.organization,event_type="journal.created",object_ref=entry.reference,details="Journal entry created as draft.")
                        return redirect("accounting_home")
            messages.error(request,"Please correct the form errors.")
    else:
        form=JournalEntryForm(initial={"entry_date":timezone.localdate()})
        form.fields["organization"].queryset=orgs
        lines=JournalLineFormSet()
        return render(request,"accounting/journal_form.html",{"form":form,"lines":lines})
    lines=JournalLineFormSet(request.POST)
    return render(request,"accounting/journal_form.html",{"form":form,"lines":lines})

@login_required
def journal_post(request, pk):
    if request.method!="POST": return redirect("accounting_home")
    entry=get_object_or_404(JournalEntry.objects.filter(organization__in=allowed_orgs(request.user)),pk=pk)
    if entry.status!="draft":
        messages.error(request,"Only draft journals can be posted.")
    elif entry.lines.count()<2 or not entry.is_balanced:
        messages.error(request,"Cannot post: journal must contain at least two lines and balance exactly.")
    elif entry.lines.exclude(account__organization=entry.organization).exists():
        messages.error(request,"Cannot post: cross-organization account detected.")
    else:
        entry.status="posted"; entry.posted_at=timezone.now(); entry.save(update_fields=["status","posted_at"])
        AuditEvent.objects.create(actor=request.user,organization=entry.organization,event_type="journal.posted",object_ref=entry.reference,details="Journal posted.")
        messages.success(request,"Journal posted.")
    return redirect("accounting_home")
