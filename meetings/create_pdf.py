from typing import List, Iterable, Any

from PyPDF3 import PdfFileMerger, PdfFileReader, PdfFileWriter
from PyPDF3.generic import Destination
from .models import AgendaTemplate, Agenda, AgendaItem
from pytz import timezone
from tpsb.settings import TIME_ZONE, BASE_DIR
import pdfkit
from django.template import Template, Context
import re, os, sys
from pdfminer.high_level import extract_pages
import io

def generate_agenda_pdf(agenda, output_path):
    generate_agenda(AgendaTemplate.objects.all().get(), agenda, list(AgendaItem.objects.filter(agenda=agenda)), output_path)

def generate_agenda(template: AgendaTemplate,
                    agenda: Agenda,
                    agenda_items: List[AgendaItem],
                    output_path: str = os.path.join(BASE_DIR, "uploads/untitled_agenda.pdf")):
    """
    Generate an agenda PDF.

    :param template: the agenda template
    :param agenda: Agenda model
    :param agenda_items: AgendaItem models
    """
    wk_options = {
        'enable-local-file-access': None,
        'enable-internal-links': None,
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
    }

    os.makedirs(os.path.join(BASE_DIR, 'uploads'), exist_ok=True)

    agenda_items.sort(key=lambda x: x.number)

    output_dir = get_parent_dir(output_path)
    pdfs = convert_attachments_to_pdf(agenda_items, output_dir)

    title_page_template = preprocess_html(template.title_page)
    toc_template = preprocess_html(template.contents_header)
    contents_template = re.sub('</?ol>', '',
                               preprocess_html(template.contents_item))  # remove <ol> tags between list items

    agenda_context = Context({
        "title": str(agenda),
        "date": agenda.meeting.date.astimezone(timezone(TIME_ZONE)).strftime("%A %B %d, %Y at %I:%M %p"),
        "recording_link": agenda.meeting.recording_link,
        "description": agenda.meeting.description
    })

    title_page_html = Template(title_page_template).render(agenda_context)
    toc_header_html = Template(toc_template).render(agenda_context)
    contents_html = generate_table_of_contents(Template(contents_template), agenda_items)

    agenda_html = title_page_html + toc_header_html + contents_html

    temp_path = os.path.join(output_dir, 'toc.pdf')
    pdfkit.from_string(agenda_html, output_path=temp_path, options=wk_options, css='meetings/agenda.css')

    page_nums = {}
    merger = PdfFileMerger()
    merger.append(temp_path, import_bookmarks=False, bookmark="Table of Contents")
    for agenda_item in agenda_items:
        if agenda_item.id in pdfs:
            page_nums[agenda_item.id] = len(merger.pages)
            merger.append(pdfs[agenda_item.id], bookmark=os.path.basename(pdfs[agenda_item.id]))

  
    merger.write(output_path)
    
    merger.close()

    add_links(temp_path, output_path, agenda_items, pdfs, page_nums)

    os.remove(temp_path)


def add_links(toc_path, output_path, agenda_items, pdfs, page_nums):
    """Adds links to the attachment names in the output_path PDF, with pages specified by page_nums."""
    toc_data = extract_pages(toc_path)
    bboxes = get_text_lines(toc_data)

    reader = PdfFileReader(output_path)
    writer = PdfFileWriter()

    # should be writer.cloneDocumentFromReader(reader) but this bug exists https://github.com/mstamy2/PyPDF2/issues/219
    # thus PDF bookmarks aren't preserved
    writer.appendPagesFromReader(reader)

    for agenda_item in agenda_items:
        if agenda_item.id in pdfs:
            page_num = page_nums[agenda_item.id]
            writer.addLink(
                PdfFileReader(toc_path).getNumPages() - 1, page_num, bboxes[os.path.basename(agenda_item.file.name)])

    bookmarks = reader.getOutlines()

    add_bookmarks(writer, bookmarks)

    with open(output_path, 'wb') as toc:
        writer.write(toc)


def add_bookmarks(writer: PdfFileWriter, bookmarks: List[Destination], parent=None):
    """Recursive function which adds bookmarks to the document based on the nested list, bookmarks."""
    prev = None
    for i in range(len(bookmarks)):
        if isinstance(bookmarks[i], list):
            add_bookmarks(writer, bookmarks[i], prev)
        else:
            fit = bookmarks[i]['/Type']
            args = []
            for arg in ["/Left", "/Bottom", "/Right", "/Top", "/Zoom"]:
                if arg in bookmarks[i]:
                    args.append(bookmarks[i][arg])

            prev = writer.addBookmark(bookmarks[i]['/Title'], bookmarks[i]['/Page'], parent, None, False, False, fit,
                                      *args)


# https://stackoverflow.com/a/39327252/13176711
def newest_file(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    path = max(paths, key=os.path.getctime)
    return os.path.abspath(path)


def preprocess_html(template: str) -> str:
    """
    Preprocess the template by replacing some variables and other fixes for wkhtmltopdf.
    """
    template = re.sub('{{ ?logo ?}}', f'<img src=file://{newest_file("admin-interface/logo")}>', template)
    template = template.replace('<p><!-- pagebreak --></p>',
                                '<p style="page-break-after:always;"><!-- pagebreak --></p>')
    return template


def generate_table_of_contents(template: str, agenda_items: List[AgendaItem]):
    """
    Generates the table of contents list, including sub-items.
    Prerequisites: template is an HTML ordered list.
    """
    contents_html = "<ol>"

    in_subsection = False

    for item in agenda_items:
        # Indent and unindent sub-items correctly
        if item.number % 1 != 0 and not in_subsection:
            in_subsection = True
            contents_html = rreplace(contents_html, '</li>', '')
            contents_html += "<ol>"
        elif item.number % 1 == 0 and in_subsection:
            in_subsection = False
            contents_html += "</ol>"
            contents_html += "</li>"

        item_context = Context({
            "number": item.number,
            "title": item.title,
            "description": item.description,
            "attachment":
                os.path.basename(item.file.name)  # TODO: replace with attachment titles
        })
        item_html = template.render(item_context)
        if not item.file:
            item_html = item_html[:item_html.rfind("<u>Attachments")]
        contents_html += item_html

    contents_html += '</ol>'
    
    return contents_html


# https://stackoverflow.com/a/2556252/13176711
def rreplace(s, old, new):
    """Replace last occurence of old in s with new."""
    li = s.rsplit(old, 1)
    return new.join(li)


def find_libreoffice() -> str:
    """Returns the command on the system to run LibreOffice."""
    # Try system version (apt)
    if os.system("libreoffice --version 2> /dev/null") == 0:
        return "libreoffice"
    # Try flatpak version
    elif os.system("flatpak run org.libreoffice.LibreOffice --version 2> /dev/null") == 0:
        return "flatpak run org.libreoffice.LibreOffice"
    # Try snap version
    elif os.system("/snap/bin/libreoffice --version 2> /dev/null") == 0:
        return "/snap/bin/libreoffice"
    else:
        return ""


def strip_filename(path: str) -> str:
    """Returns the filename without the extension or path"""
    filename = os.path.basename(path)
    dot = filename.rindex(".")
    filename = filename[:dot]
    return filename


def get_parent_dir(path: str) -> str:
    """Returns the absolute path of the parent directory"""
    return os.path.abspath(os.path.join(path, os.pardir))


def convert_attachments_to_pdf(agenda_items: List[AgendaItem], output_dir: str):
    """
    Converts and saves AgendaItem attachments to PDF format.
    Returns a dict where the keys are the AgendaItem id and the value the file path of the pdf.
    """
    libreoffice_cmd = find_libreoffice()
    if libreoffice_cmd == "":
        print(f"Libreoffice was not found on your system.", file=sys.stderr)
        exit(1)

    pdfs = {}
    for agenda_item in agenda_items:
        if agenda_item.file:
            input_doc = os.path.abspath(agenda_item.file.name)

            assert os.system(
                f'{libreoffice_cmd} --convert-to pdf "{input_doc}" --outdir "{output_dir}" 2> /dev/null') == 0
            pdf = f"{output_dir}/{strip_filename(input_doc)}.pdf"
            pdfs[agenda_item.id] = pdf

    return pdfs


# This function and related ones are derived from https://stackoverflow.com/a/69151177/13176711
def get_text_lines(o: Any, depth=0, lines={}):
    """Get bounding boxes of text lines in the document."""
    # key=text, value=bbox

    if get_indented_name(o, depth) == 'LTTextLineHorizontal':
        lines[get_optional_text(o)] = get_optional_bbox(o)

    if isinstance(o, Iterable):
        for i in o:
            get_text_lines(i, depth=depth + 1, lines=lines)

    return lines


def get_indented_name(o: Any, depth: int) -> str:
    """Indented name of LTItem"""
    return o.__class__.__name__


def get_optional_bbox(o: Any) -> str:
    """Bounding box of LTItem if available, otherwise empty string"""
    if hasattr(o, 'bbox'):
        return o.bbox
    return []


def get_optional_text(o: Any) -> str:
    """Text of LTItem if available, otherwise empty string"""
    if hasattr(o, 'get_text'):
        return o.get_text().strip()
    return ''
