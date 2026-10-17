from decimal import Decimal
from django.db import models
class Customer(models.Model):
    organization=models.ForeignKey("organizations.Organization",on_delete=models.CASCADE,related_name="customers")
    name=models.CharField(max_length=180)
    email=models.EmailField(blank=True)
    phone=models.CharField(max_length=30,blank=True)
    gstin=models.CharField(max_length=20,blank=True)
    is_active=models.BooleanField(default=True)
    def __str__(self): return self.name
class Invoice(models.Model):
    STATUSES=[("draft","Draft"),("sent","Sent"),("part_paid","Part paid"),("paid","Paid"),("overdue","Overdue"),("void","Void")]
    organization=models.ForeignKey("organizations.Organization",on_delete=models.CASCADE,related_name="invoices")
    customer=models.ForeignKey(Customer,on_delete=models.PROTECT,related_name="invoices")
    invoice_number=models.CharField(max_length=40)
    issue_date=models.DateField()
    due_date=models.DateField()
    status=models.CharField(max_length=12,choices=STATUSES,default="draft")
    notes=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=["-issue_date"]
        constraints=[models.UniqueConstraint(fields=["organization","invoice_number"],name="uniq_org_invoice_no")]
    @property
    def subtotal(self): return sum((x.quantity*x.unit_price for x in self.lines.all()),Decimal("0"))
    @property
    def tax_total(self): return sum((x.quantity*x.unit_price*x.tax_rate/100 for x in self.lines.all()),Decimal("0"))
    @property
    def total(self): return self.subtotal+self.tax_total
    def __str__(self): return self.invoice_number
class InvoiceLine(models.Model):
    invoice=models.ForeignKey(Invoice,on_delete=models.CASCADE,related_name="lines")
    description=models.CharField(max_length=200)
    quantity=models.DecimalField(max_digits=10,decimal_places=2,default=1)
    unit_price=models.DecimalField(max_digits=12,decimal_places=2)
    tax_rate=models.DecimalField(max_digits=5,decimal_places=2,default=0)
