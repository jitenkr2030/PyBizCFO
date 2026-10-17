from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum

class Account(models.Model):
    TYPES=[("asset","Asset"),("liability","Liability"),("equity","Equity"),("income","Income"),("expense","Expense")]
    organization=models.ForeignKey("organizations.Organization",on_delete=models.CASCADE,related_name="accounts")
    code=models.CharField(max_length=20)
    name=models.CharField(max_length=160)
    account_type=models.CharField(max_length=12,choices=TYPES)
    is_active=models.BooleanField(default=True)
    class Meta:
        ordering=["code"]
        constraints=[models.UniqueConstraint(fields=["organization","code"],name="uniq_org_account_code")]
    def __str__(self): return f"{self.code} — {self.name}"

class JournalEntry(models.Model):
    STATUSES=[("draft","Draft"),("posted","Posted"),("reversed","Reversed")]
    organization=models.ForeignKey("organizations.Organization",on_delete=models.CASCADE,related_name="journal_entries")
    reference=models.CharField(max_length=40)
    entry_date=models.DateField()
    memo=models.CharField(max_length=255)
    status=models.CharField(max_length=10,choices=STATUSES,default="draft")
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="created_journal_entries")
    created_at=models.DateTimeField(auto_now_add=True)
    posted_at=models.DateTimeField(null=True,blank=True)
    class Meta:
        ordering=["-entry_date","-id"]
        constraints=[models.UniqueConstraint(fields=["organization","reference"],name="uniq_org_journal_ref")]
    def clean(self):
        if self.pk and self.status == "posted":
            prior=JournalEntry.objects.filter(pk=self.pk).first()
            if prior and prior.status=="posted" and any(k in self.__dict__ for k in []):
                raise ValidationError("Posted entries must be corrected using a reversal/adjustment workflow.")
    @property
    def debit_total(self): return self.lines.aggregate(v=Sum("debit"))["v"] or Decimal("0")
    @property
    def credit_total(self): return self.lines.aggregate(v=Sum("credit"))["v"] or Decimal("0")
    @property
    def is_balanced(self): return self.debit_total == self.credit_total and self.debit_total > 0
    def __str__(self): return self.reference

class JournalLine(models.Model):
    entry=models.ForeignKey(JournalEntry,on_delete=models.CASCADE,related_name="lines")
    account=models.ForeignKey(Account,on_delete=models.PROTECT,related_name="journal_lines")
    description=models.CharField(max_length=180,blank=True)
    debit=models.DecimalField(max_digits=14,decimal_places=2,default=Decimal("0"))
    credit=models.DecimalField(max_digits=14,decimal_places=2,default=Decimal("0"))
    class Meta: ordering=["id"]
    def clean(self):
        if self.debit < 0 or self.credit < 0: raise ValidationError("Debit and credit must not be negative.")
        if self.debit and self.credit: raise ValidationError("A line cannot have both debit and credit.")
        if self.entry_id and self.account_id and self.entry.organization_id != self.account.organization_id:
            raise ValidationError("Journal account must belong to the same organization.")
