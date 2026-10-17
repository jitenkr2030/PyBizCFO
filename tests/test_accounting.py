from decimal import Decimal
import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from apps.organizations.models import Organization
from apps.accounting.models import Account, JournalEntry, JournalLine

@pytest.mark.django_db
def test_demo_seed_is_idempotent():
    call_command("seed_demo")
    call_command("seed_demo")
    assert Organization.objects.filter(name="Aarav Components (Demo)").count() == 1

@pytest.mark.django_db
def test_demo_journal_balances():
    call_command("seed_demo")
    entry=JournalEntry.objects.get(reference="DEMO-JE-001")
    assert entry.debit_total == Decimal("25000.00")
    assert entry.credit_total == Decimal("25000.00")
    assert entry.is_balanced

@pytest.mark.django_db
def test_user_has_demo_org_membership():
    call_command("seed_demo")
    user=get_user_model().objects.get(username="demo-owner")
    assert user.organization_memberships.filter(organization__name="Aarav Components (Demo)").exists()
