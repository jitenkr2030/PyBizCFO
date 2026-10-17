from django.conf import settings
from django.db import models
class BankAccount(models.Model):
    organization=models.ForeignKey("organizations.Organization",on_delete=models.CASCADE,related_name="bank_accounts")
    name=models.CharField(max_length=120)
    bank_name=models.CharField(max_length=120,blank=True)
    account_last4=models.CharField(max_length=4,blank=True)
    currency=models.CharField(max_length=3,default="INR")
    opening_balance=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    is_active=models.BooleanField(default=True)
    def __str__(self): return self.name
class BankTransaction(models.Model):
    STATUS=[("unmatched","Unmatched"),("matched","Matched"),("ignored","Ignored")]
    bank_account=models.ForeignKey(BankAccount,on_delete=models.CASCADE,related_name="transactions")
    transaction_date=models.DateField()
    description=models.CharField(max_length=255)
    amount=models.DecimalField(max_digits=14,decimal_places=2)
    external_reference=models.CharField(max_length=100,blank=True)
    status=models.CharField(max_length=12,choices=STATUS,default="unmatched")
    imported_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=["-transaction_date"]
