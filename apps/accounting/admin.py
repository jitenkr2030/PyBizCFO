from django.contrib import admin
from .models import Account, JournalEntry, JournalLine
admin.site.register(Account)
class JournalLineInline(admin.TabularInline): model=JournalLine; extra=0
@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin): list_display=('reference','organization','entry_date','status'); inlines=[JournalLineInline]
