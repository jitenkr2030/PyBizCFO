from django import forms
from django.forms import inlineformset_factory
from .models import JournalEntry, JournalLine
class JournalEntryForm(forms.ModelForm):
    class Meta:
        model=JournalEntry
        fields=["organization","reference","entry_date","memo"]
        widgets={"entry_date":forms.DateInput(attrs={"type":"date"}),"memo":forms.TextInput(attrs={"placeholder":"Reason for this entry"})}
class JournalLineForm(forms.ModelForm):
    class Meta:
        model=JournalLine
        fields=["account","description","debit","credit"]
        widgets={"debit":forms.NumberInput(attrs={"step":"0.01","min":"0"}),"credit":forms.NumberInput(attrs={"step":"0.01","min":"0"})}
JournalLineFormSet=inlineformset_factory(JournalEntry,JournalLine,form=JournalLineForm,extra=2,can_delete=True)
