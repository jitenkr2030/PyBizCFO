from datetime import date, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from apps.organizations.models import Organization, Membership
from apps.accounting.models import Account, JournalEntry, JournalLine
from apps.sales.models import Customer, Invoice, InvoiceLine
from apps.compliance.models import ComplianceTask

class Command(BaseCommand):
    help = "Create safe, clearly fictional BizCFO demonstration data."
    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        admin, created = User.objects.get_or_create(username="demo-admin", defaults={"email":"admin@example.test", "is_staff":True, "is_superuser":True})
        if created: admin.set_password("DemoAdmin-ChangeMe123!"); admin.save()
        owner, created = User.objects.get_or_create(username="demo-owner", defaults={"email":"owner@example.test"})
        if created: owner.set_password("DemoOwner-ChangeMe123!"); owner.save()
        accountant, created = User.objects.get_or_create(username="demo-accountant", defaults={"email":"accountant@example.test"})
        if created: accountant.set_password("DemoAccountant-ChangeMe123!"); accountant.save()
        org, _ = Organization.objects.get_or_create(name="Aarav Components (Demo)", defaults={"legal_name":"Aarav Components Private Limited (Demo)","industry":"Manufacturing","financial_year_start_month":4,"currency":"INR","gstin":"DEMO-GSTIN-NOT-REAL","pan":"DEMO-PAN-NOT-REAL"})
        for user, role in [(owner,"owner"),(accountant,"accountant"),(admin,"admin")]:
            Membership.objects.get_or_create(organization=org,user=user,defaults={"role":role})
        chart = [
            ("1000","Operating Bank","asset"),("1100","Accounts Receivable","asset"),("1500","Equipment","asset"),
            ("2000","Accounts Payable","liability"),("2100","GST Payable (demo)","liability"),
            ("3000","Owner Equity","equity"),("4000","Service Revenue","income"),("5000","Operating Expenses","expense"),
        ]
        accounts={}
        for code,name,typ in chart:
            accounts[code],_ = Account.objects.get_or_create(organization=org,code=code,defaults={"name":name,"account_type":typ})
        customer,_ = Customer.objects.get_or_create(organization=org,name="Northstar Retail (Demo)",defaults={"email":"finance@example.test","phone":"+91-00000-00000"})
        today=date.today()
        invoice,_ = Invoice.objects.get_or_create(organization=org,invoice_number="DEMO-INV-001",defaults={"customer":customer,"issue_date":today-timedelta(days=7),"due_date":today+timedelta(days=23),"status":"sent","notes":"Fictional sample invoice; not a tax invoice."})
        InvoiceLine.objects.get_or_create(invoice=invoice,description="Monthly finance operations support",defaults={"quantity":Decimal("1"),"unit_price":Decimal("25000.00"),"tax_rate":Decimal("0.00")})
        entry,_ = JournalEntry.objects.get_or_create(organization=org,reference="DEMO-JE-001",defaults={"entry_date":today-timedelta(days=5),"memo":"Fictional opening demo revenue transaction","status":"posted","created_by":admin})
        if not entry.lines.exists():
            JournalLine.objects.create(entry=entry,account=accounts["1000"],description="Demo receipt",debit=Decimal("25000"),credit=Decimal("0"))
            JournalLine.objects.create(entry=entry,account=accounts["4000"],description="Demo service revenue",debit=Decimal("0"),credit=Decimal("25000"))
        for i, title in enumerate(["Review monthly bank statement","Prepare GST workpaper (demo only)","Review monthly management report"]):
            ComplianceTask.objects.get_or_create(organization=org,title=title,due_date=today+timedelta(days=5+i*4),defaults={"status":"pending","assigned_to":accountant,"description":"Demonstration workflow only. Confirm applicability and deadlines with a qualified professional."})
        self.stdout.write(self.style.SUCCESS("Demo data ready. Logins: demo-admin / DemoAdmin-ChangeMe123!, demo-owner / DemoOwner-ChangeMe123!, demo-accountant / DemoAccountant-ChangeMe123!"))
