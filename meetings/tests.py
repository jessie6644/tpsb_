from django.test import TestCase
from meetings import create_pdf
from meetings.models import *
from datetime import datetime

# Temporary: should be in database using fixture
title_template = """
<br />
<br />
<br />
<h1 style="text-align: center;">{{ logo }}</h1>
<br />
<h1 style="text-align: center;">{{ title }}</h1>
<p></p>
<h2 style="text-align: center;">{{ date }}</h2>
<p><!-- pagebreak --></p>
"""

toc_template = """
<h2 style="text-align: center;">{{ title }}</h2>
<h2 style="text-align: center;">{{ date }}</h2>
<h3 style="text-align: center;">Livestream at: <a href="{{ recording_link }}">{{ recording_link }}</a></h3>
<hr />
<p>{{ description }}</p>
<hr />
<p>{{ table_of_contents }}</p>
"""

content_template = """
<ol>
<li value="{{ number }}. ">{{ title }}<br />{{ description }}<br /><u>Attachments:</u></li>
<ul>
<li><a href="#{{ attachment_page }}">{{ attachment }}</a></li>
</ul>
</ol>
"""


# Exclude this test from running in GH Actions
class PDFGenerationTestCase(TestCase):

    meeting = Meeting(title='TPSB Nov Test Meeting',
                      date=datetime.now(),
                      description='Test Description',
                      meeting_type='PUB',
                      recording_link='https://youtube.com/')

    agenda = Agenda(meeting=meeting)

    agenda_template = AgendaTemplate(title_page=title_template,
                                     contents_header=toc_template,
                                     contents_item=content_template)

    agenda_items = [
        AgendaItem(agenda=agenda, number=1, title='Agenda Item 1', description='Test Description 1', file="uploads/TPSB Board Meeting Management System specs doc.docx"),
        AgendaItem(agenda=agenda, number=1.1, title='Agenda Item 1.1', description='Test 1.1'),
        AgendaItem(agenda=agenda, number=2.2, title='Agenda Item 2.2', description=''),
        AgendaItem(agenda=agenda, number=2.1, title='Agenda Item 2.1', description='Test Description 2'),
        AgendaItem(agenda=agenda, number=2, title='Really Long Title ' * 8, description='Test Description 2', file="uploads/TPSB Board Meeting Management System specs doc.pdf"),
    ]

    # To run this case use python manage.py test meetings.tests.PDFGenerationTestCase.agenda_pdf_generation
    def agenda_pdf_generation(self):
        self.meeting.save()
        self.agenda.save()
        for agenda_item in self.agenda_items:
            agenda_item.save() 
        create_pdf.generate_agenda(self.agenda_template, self.agenda, self.agenda_items)