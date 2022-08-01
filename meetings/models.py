from datetime import datetime
from django.db import models
from singleton_model import SingletonModel
import os
from pytz import timezone
import singleton_model
import tpsb.settings as settings
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.deletion import CASCADE
from django.utils.html import mark_safe

# Create your models here.

MEETING_TYPES = [('PUB', 'Public'), ('SPEC', 'Special'), ('CONF', 'Confidential')]


class Meeting(models.Model):
    title = models.CharField('Meeting Title', max_length=120)
    date = models.DateTimeField('Meeting Date')
    recording_link = models.URLField('YouTube Link', default="", blank=True)
    description = RichTextUploadingField('Description')

    meeting_type = models.CharField('Meeting Type', choices=MEETING_TYPES, max_length=4, default='PUB')

    class Meta:
        verbose_name = " Meeting"  # the space in front makes Meetings appear first

    def __str__(self) -> str:
        tz = timezone(settings.TIME_ZONE)
        time = self.date.astimezone(tz)
        return f'[{time.strftime("%B %d, %Y %I:%M %p")}] {self.title}'

class Agenda(models.Model):
    meeting = models.OneToOneField(Meeting, on_delete=CASCADE)

    def __str__(self) -> str:
        return f'{self.meeting.title} Agenda'

    def generate_pdf(self) :
        import meetings.create_pdf as create_pdf
        create_pdf.generate_agenda_pdf(self, os.path.join(settings.BASE_DIR, f"uploads/{self.pk}.pdf"))
        return mark_safe(f'<a class="button" href="{f"/uploads/{self.pk}.pdf"}">Generate PDF</a>')


class AgendaItem(models.Model):
    agenda = models.ForeignKey(Agenda, on_delete=CASCADE)
    number = models.FloatField('Agenda Item Number')
    title = models.CharField('Title (optional)', max_length=120, blank=True)
    description = RichTextUploadingField('Description')

    POSSIBLE_DECISIONS = [('TBC', 'To be considered'), ('CUC', 'Currently under consideration'), ('A', 'Approved'),
                          ('AWM', 'Approved with motion'), ('R', 'Rejected')]

    result = models.CharField('Result', choices=POSSIBLE_DECISIONS, max_length=3, default='TBC')

    motion = RichTextUploadingField('Motion (if applicable)', default="", blank=True)
    file = models.FileField('Attachment', upload_to="uploads", blank=True)  # temporary

    def __str__(self) -> str:
        return f'[{self.result}] {self.number}. {self.title}'


class Attachment(models.Model):
    agenda_item = models.ForeignKey(AgendaItem, on_delete=CASCADE)
    attachment = models.FileField('File', upload_to="uploads")
    name = models.CharField('Name (optional)', max_length=255, blank=True, default="Untitled File")

    def __str__(self) -> str:
        return f'{self.name} ({os.path.basename(self.attachment.__str__())})'


class Minute(models.Model):
    meeting = models.OneToOneField(Meeting, on_delete=CASCADE)
    minute_type = models.CharField('Minute Type',
                                    choices=MEETING_TYPES,
                                    max_length=4,
                                    default='PUB')
    minute_date = models.DateField('Minute Date')
    attendants =  models.TextField('Attendants', help_text="Separate Attendees by Commas")

    def __str__(self) -> str:
        return f'{self.meeting.title} Minute'

    class Meta:
        verbose_name_plural = "Minutes"


class MinuteItem(models.Model):
    minute = models.ForeignKey(Minute, on_delete=CASCADE)
    subitem_number = models.FloatField('Minute Subitem')
    title = models.CharField('Title', max_length=200)
    notes = RichTextUploadingField('Notes', blank=True)
    recommendation = RichTextUploadingField('Recommendations', blank=True)
    mover = models.CharField('Mover', max_length=120)
    seconder = models.CharField('Seconder', max_length=120)

    def __str__(self) -> str:
        return f'[{self.mover}] {self.subitem_number}. {self.title}'


class AgendaTemplate(SingletonModel):
    title_page = RichTextUploadingField()
    contents_header = RichTextUploadingField()
    contents_item = RichTextUploadingField()

    def __str__(self) -> str:
        return "Agenda Template"

    class Meta:
        verbose_name_plural = "Agenda Template"
