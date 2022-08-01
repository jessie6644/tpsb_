from django.contrib import admin
from django.utils.html import format_html
from meetings.models import *
from meetings.create_pdf import *
import meetings.create_pdf as create_pdf

class AgendaItemInline(admin.StackedInline):
    model = AgendaItem
    extra = 0


class MinuteItemInLine(admin.StackedInline):
    model = MinuteItem
    extra = 0


class AgendaAdmin(admin.ModelAdmin):
    inlines = [AgendaItemInline]
    list_display = ('meeting_title', 'meeting_date', 'meeting_type', 'view_pdf', 'generate_pdf')
    search_fields = ('meeting',)

    def meeting_title(self, obj):
        return obj.meeting.title

    def meeting_date(self, obj):
        return obj.meeting.date

    def meeting_type(self, obj):
        return dict(MEETING_TYPES)[obj.meeting.meeting_type]

    def view_pdf(self, obj):
        if (obj.generated_pdf == True):
            return mark_safe(f'<a class="button" href="{f"/uploads/{obj.pk}.pdf"}">View PDF</a>')
        else : 
            return "Please generate the PDF first."
    
    def generate_pdf(self, obj):
        import meetings.create_pdf as create_pdf 
        obj.generated_pdf = True
        obj.save(update_fields=['generated_pdf'])
        create_pdf.generate_agenda_pdf(obj, os.path.join(settings.BASE_DIR, f"uploads/{obj.pk}.pdf"))
        return mark_safe(f'<a class="button" href="{f"/uploads/{obj.pk}.pdf"}">Generate PDF</a>')

class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'meeting_type')
    list_filter = ('date', 'meeting_type')
    search_fields = ('title',)


class MinuteAdmin(admin.ModelAdmin):
    inlines = [MinuteItemInLine]
    list_display = ('meeting_title', 'meeting_date', 'meeting_type')
    search_fields = ('meeting',)

    def meeting_title(self, obj):
        return obj.meeting.title

    def meeting_date(self, obj):
        return obj.meeting.date

    def meeting_type(self, obj):
        return dict(MEETING_TYPES)[obj.meeting.meeting_type]


# Register your models here.
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Minute, MinuteAdmin)
admin.site.register(Agenda, AgendaAdmin)
admin.site.register(AgendaTemplate)
