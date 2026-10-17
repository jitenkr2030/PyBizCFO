from django.contrib import admin
from .models import AuditEvent
@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin): list_display=('created_at','actor','organization','event_type','object_ref'); readonly_fields=[f.name for f in AuditEvent._meta.fields]
