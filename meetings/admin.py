from django.contrib import admin
from django.utils.html import format_html
from meetings.models import *
from meetings.create_pdf import *

class AgendaItemInline(admin.StackedInline):
    model = AgendaItem
    extra = 0


class MinuteItemInLine(admin.StackedInline):
    model = MinuteItem
    extra = 0


class AgendaAdmin(admin.ModelAdmin):
    inlines = [AgendaItemInline]
    list_display = ('meeting_title', 'meeting_date', 'meeting_type', 'generate_pdf')
    search_fields = ('meeting',)

    def meeting_title(self, obj):
        return obj.meeting.title

    def meeting_date(self, obj):
        return obj.meeting.date

    def meeting_type(self, obj):
        return dict(MEETING_TYPES)[obj.meeting.meeting_type]


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
