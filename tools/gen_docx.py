import json, sys
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = sys.argv[1]
L = json.load(open('labels.json'))
INK = RGBColor(0x18,0x17,0x1c); GREY = RGBColor(0x55,0x55,0x5c); RED = RGBColor(0xcc,0x06,0x05); GREEN = RGBColor(0x31,0x7f,0x43)

def shade(cell, hexfill):
    tcPr = cell._tc.get_or_add_tcPr(); shd = OxmlElement('w:shd')
    shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'),hexfill); tcPr.append(shd)

def borders(cell, color='18171c', sz='8'):
    tcPr = cell._tc.get_or_add_tcPr(); b = OxmlElement('w:tcBorders')
    for side in ('top','left','bottom','right'):
        e = OxmlElement('w:'+side); e.set(qn('w:val'),'single'); e.set(qn('w:sz'),sz); e.set(qn('w:color'),color); b.append(e)
    tcPr.append(b)

def base(doc):
    st = doc.styles['Normal']; st.font.name = 'Georgia'; st.font.size = Pt(11)
    for s in doc.sections:
        s.page_width = Inches(8.5); s.page_height = Inches(11)
        s.left_margin = s.right_margin = Inches(1); s.top_margin = Inches(0.9); s.bottom_margin = Inches(0.9)

def h(doc, text, size=16, color=INK, space_before=14):
    p = doc.add_paragraph(); r = p.add_run(text); r.bold = True; r.font.size = Pt(size); r.font.name = 'Arial'; r.font.color.rgb = color
    p.paragraph_format.space_before = Pt(space_before); p.paragraph_format.space_after = Pt(4); p.paragraph_format.keep_with_next = True
    return p

def para(doc, text, size=11, color=INK, italic=False, after=6):
    p = doc.add_paragraph(); r = p.add_run(text); r.font.size = Pt(size); r.font.color.rgb = color
    p.paragraph_format.space_after = Pt(after); return p

def callout(doc, title, lines, fill='FFF4C2', border='B8860B'):
    """Instruction box for faculty. Delete before distributing."""
    t = doc.add_table(rows=1, cols=1); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = t.cell(0,0); shade(c, fill); borders(c, border, '12')
    p = c.paragraphs[0]; r = p.add_run('INSTRUCTIONS FOR FACULTY (delete this box before you share the document)'); r.bold = True; r.font.size = Pt(8.5); r.font.name = 'Arial'; r.font.color.rgb = GREY
    p = c.add_paragraph(); r = p.add_run(title); r.bold = True; r.font.size = Pt(12); r.font.name = 'Arial'
    for ln in lines:
        p = c.add_paragraph(style=None); r = p.add_run('• ' + ln); r.font.size = Pt(10); r.font.name = 'Arial'
        p.paragraph_format.space_after = Pt(2)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def label_block(doc, key, badge=True):
    """The universal label as it should appear in the document: badge image, two sentences, quiet short notice."""
    d = L[key]
    t = doc.add_table(rows=1, cols=1); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = t.cell(0,0); shade(c, 'F7F7F8'); borders(c, '18171c', '10')
    if badge:
        p = c.paragraphs[0]; p.add_run().add_picture(f'badge-{key}.png', width=Inches(4.2)); p.paragraph_format.space_after = Pt(6)
        p = c.add_paragraph()
    else:
        p = c.paragraphs[0]
    r = p.add_run(d['universal'].split('\n')[0]); r.bold = True; r.font.name = 'Arial'; r.font.size = Pt(11)
    p = c.add_paragraph(); r = p.add_run(d['universal'].split('\n')[1]); r.font.size = Pt(10.5)
    p = c.add_paragraph(); r = p.add_run(d['universal'].split('\n')[2]); r.font.size = Pt(9); r.font.color.rgb = GREY
    p = c.add_paragraph(); p.paragraph_format.space_before = Pt(6)
    for i, ln in enumerate(d['short'].split('\n')):
        if i: p = c.add_paragraph()
        r = p.add_run(ln); r.font.size = Pt(7.5); r.font.name = 'Consolas'; r.font.color.rgb = GREY
        p.paragraph_format.space_after = Pt(0)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def footer_line(doc, key):
    for s in doc.sections:
        f = s.footer; f.is_linked_to_previous = False
        p = f.paragraphs[0]; p.text = ''
        r = p.add_run(L[key]['footer']); r.font.size = Pt(7.5); r.font.name = 'Arial'; r.font.color.rgb = GREY
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT

def skel(doc, n=3):
    for _ in range(n):
        para(doc, 'Lorem ipsum stands in for your own text here. The structure of the document is what matters: where the label sits relative to the content students read and the place they upload.', size=10.5, color=GREY)

# ---------------- 1. Syllabus ----------------
doc = Document(); base(doc)
callout(doc, 'Where the label goes on a syllabus', [
  'Once, under your AI policy heading, with scope set to the whole course (the "My course materials" choice on the Start page). Everything you hand out afterward inherits it.',
  'Put the one-line version in the page footer of this document (already done below). Students skim footers; AI tools read them.',
  'Keep the badge image and the small grey notice together. The image is for people; the grey text is what an AI reads.',
  'The "Ask your AI first" link is the most useful line for students. Say it out loud on day one.',
  'Make a separate No-AI label only for exams and student work; see example 03.'])
h(doc, 'WRIT 102: First-Year Writing II', 20, space_before=0)
para(doc, 'Spring 2026 · Dr. Jane Doe · University of Mississippi · MWF 10:00', 11, GREY)
h(doc, 'Course description'); skel(doc, 2)
h(doc, 'Required texts'); skel(doc, 1)
h(doc, 'AI use and course materials')
para(doc, 'Each assignment carries its own AI-use icons that say what you may do. The materials for this course carry the label below, which says where they may go.')
label_block(doc, 'course')
h(doc, 'Grading'); skel(doc, 2)
h(doc, 'Schedule'); skel(doc, 3)
footer_line(doc, 'course')
doc.save(f'{OUT}/01-syllabus-with-label.docx')

# ---------------- 2. Assignment sheet ----------------
doc = Document(); base(doc)
callout(doc, 'Where the label goes on an assignment sheet', [
  'After the directions and before the submission instructions, so it is the last thing a student reads before uploading anything.',
  'If your syllabus already carries the whole-course label, this one is optional. Include it when the assignment is distributed on its own (a PDF, an email) or when its rule differs.',
  'This example uses the assignment-scope label (S-A) from the Advanced builder; the Start page\'s course label works here too.',
  'Footer carries the one-line version so every printed or photographed page shows it.'])
h(doc, 'Essay 2: Rhetorical Analysis', 20, space_before=0)
para(doc, 'WRIT 102 · Due Friday 11:59 PM · 100 points', 11, GREY)
h(doc, 'The task')
para(doc, 'Choose one of the three op-eds in the reading packet and analyze how it builds its argument: what it claims, what evidence it uses, how it handles the strongest objection, and whether those moves work for its audience. 1,200 words, MLA format.')
h(doc, 'Requirements'); skel(doc, 2)
h(doc, 'Before you upload or paste this anywhere')
label_block(doc, 'assign')
h(doc, 'Submission')
para(doc, 'Submit a PDF through the Essay 2 link in Blackboard by the deadline.')
footer_line(doc, 'assign')
doc.save(f'{OUT}/02-assignment-sheet-with-label.docx')

# ---------------- 3. Exam ----------------
doc = Document(); base(doc)
callout(doc, 'Where the label goes on an exam or anything with student work', [
  'This is a separate No AI processing (L2) label: the "An exam, quiz or student work" choice on the Start page. Do not reuse the course label here.',
  'Top of page one, before the first question, and in the footer of every page. A photographed page carries the footer in the frame.',
  'Use the same L2 label on peer-review packets and discussion exports: other students\' work is theirs.',
  'In testing, every Claude model and one of three GPT configurations declined to answer an L2-labeled exam; the rest did not. The label is a record and a request, not a lock.'], fill='FDE2E1', border='CC0605')
h(doc, 'Midterm Exam', 20, space_before=0)
para(doc, 'WRIT 102 · Take-home · Due Monday 9:00 AM · Dr. Jane Doe', 11, GREY)
label_block(doc, 'exam')
h(doc, 'Instructions')
para(doc, 'Answer three of the four questions. Each answer should be about 300 words and cite specific moves from the op-eds in the reading packet.')
h(doc, 'Question 1'); skel(doc, 1)
h(doc, 'Question 2'); skel(doc, 1)
h(doc, 'Question 3')
para(doc, 'Compare how two of the op-eds in the packet handle counterarguments. Cite specific moves.')
h(doc, 'Question 4'); skel(doc, 1)
footer_line(doc, 'exam')
doc.save(f'{OUT}/03-exam-with-label.docx')
print('docx ok')
