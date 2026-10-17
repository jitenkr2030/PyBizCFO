from django.contrib import admin
from .models import Customer,Invoice,InvoiceLine
admin.site.register(Customer)
class InvoiceLineInline(admin.TabularInline): model=InvoiceLine; extra=1
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin): list_display=('invoice_number','organization','customer','issue_date','due_date','status'); inlines=[InvoiceLineInline]
