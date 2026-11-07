import json, sys, html
OUT = sys.argv[1]
L = json.load(open('labels.json'))

# ---------------- 4. Reading handout PDF (reportlab) ----------------
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.enums import TA_LEFT

INK=HexColor('#18171c'); GREY=HexColor('#55555c'); RED=HexColor('#cc0605')
sH = ParagraphStyle('h', fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=INK, spaceAfter=6)
sH2 = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=12.5, leading=16, textColor=INK, spaceBefore=12, spaceAfter=4)
sB = ParagraphStyle('b', fontName='Times-Roman', fontSize=11, leading=15, textColor=INK, spaceAfter=7)
sS = ParagraphStyle('s', fontName='Times-Roman', fontSize=10.5, leading=14, textColor=GREY, spaceAfter=7)
sCallH = ParagraphStyle('ch', fontName='Helvetica-Bold', fontSize=11, leading=14)
sCall = ParagraphStyle('c', fontName='Helvetica', fontSize=9.5, leading=12.5, spaceAfter=3)
sCallK = ParagraphStyle('ck', fontName='Helvetica', fontSize=8, leading=10, textColor=GREY)
sLab1 = ParagraphStyle('l1', fontName='Helvetica-Bold', fontSize=10.5, leading=13)
sLab2 = ParagraphStyle('l2', fontName='Times-Roman', fontSize=10, leading=13)
sLab3 = ParagraphStyle('l3', fontName='Courier', fontSize=7, leading=8.6, textColor=GREY)

d = L['course']
footer_text = d['footer']
def on_page(canvas, doc):
    canvas.saveState(); canvas.setFont('Helvetica', 7); canvas.setFillColor(GREY)
    # wrap footer into two lines max
    words = footer_text.split(' '); lines=[]; cur=''
    for w in words:
        if canvas.stringWidth((cur+' '+w).strip(),'Helvetica',7) > 6.3*inch: lines.append(cur); cur=w
        else: cur=(cur+' '+w).strip()
    lines.append(cur)
    y = 0.62*inch
    canvas.setStrokeColor(INK); canvas.setLineWidth(0.5); canvas.line(1*inch, y+ (len(lines))*9 + 3, 7.5*inch, y + len(lines)*9 + 3)
    for i,ln in enumerate(lines): canvas.drawString(1*inch, y + (len(lines)-1-i)*9, ln)
    canvas.drawRightString(7.5*inch, 0.4*inch, f'Page {doc.page}'); canvas.restoreState()

def callout_pdf(title, lines, fill='#FFF4C2', border='#B8860B'):
    rows=[[Paragraph('INSTRUCTIONS FOR FACULTY (delete this box before you share the document)', sCallK)],[Paragraph(title, sCallH)]]+[[Paragraph('• '+html.escape(x), sCall)] for x in lines]
    t=Table(rows, colWidths=[6.5*inch]); t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),HexColor(fill)),('BOX',(0,0),(-1,-1),1.2,HexColor(border)),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)])); return t

def label_pdf(key):
    d=L[key]; u=d['universal'].split('\n')
    rows=[[Image(f'badge-{key}.png', width=3.8*inch, height=3.8*inch*317/880)],[Paragraph(html.escape(u[0]), sLab1)],[Paragraph(html.escape(u[1]), sLab2)],[Paragraph(html.escape(u[2]).replace('  ·  ','<br/>'), ParagraphStyle('l2b',parent=sLab2,fontSize=8.5,textColor=GREY))]]
    rows += [[Paragraph(html.escape(ln), sLab3)] for ln in d['short'].split('\n')]
    t=Table(rows, colWidths=[6.5*inch]); t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),HexColor('#F7F7F8')),('BOX',(0,0),(-1,-1),1,INK),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2)])); return t

doc = SimpleDocTemplate(f'{OUT}/04-reading-handout-with-label.pdf', pagesize=letter, leftMargin=1*inch, rightMargin=1*inch, topMargin=0.9*inch, bottomMargin=1.1*inch, title='Reading packet: three op-eds (example with Campus Only Label)', author='Dr. Jane Doe', subject=d['code'])
story=[callout_pdf('Where the label goes on a handout or PDF', [
  'The footer of every page, in 7 to 9 point type (already set on this document). A student who photographs or uploads any single page carries the label with it.',
  'The full label block once, on page one, so the badge and the two sentences are seen before anyone reads.',
  'In Word: Insert > Footer, paste the one-line version. In Google Docs: Insert > Headers & footers. Then export to PDF; the footer survives.',
  'Keep the grey notice text as text. If you paste it as an image, AI tools cannot read it.']),
  Spacer(1,8), Paragraph('Reading packet: three op-eds', sH), Paragraph('WRIT 102 · Week 9 · Dr. Jane Doe', sS), label_pdf('course'), Spacer(1,10)]
pieces=[('1. "The Case for Four-Day Weeks"','The author argues that a shorter week raises productivity, citing Iceland and Microsoft Japan trials, and anticipates the objection that service industries cannot compress hours.'),
        ('2. "Why Your City Needs More Parking Minimums"','Argues from safety and small-business access; relies on anecdotes from a Memphis retail strip.'),
        ('3. "Let Teenagers Sleep"','Uses sleep-science data to argue for later school start times, then pivots to a cost argument about bus schedules.')]
filler='This paragraph stands in for the op-ed itself. In your packet, the full text of each reading goes here, with the label riding in the footer of every page so that a photographed or uploaded page carries it. '
for i,(t,s) in enumerate(pieces):
    if i: story.append(PageBreak())
    story += [Paragraph(t, sH2), Paragraph(s, sB)] + [Paragraph(filler*3, sB) for _ in range(4)]
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)

# ---------------- 5. Slides (python-pptx) ----------------
from pptx import Presentation
from pptx.util import Inches as PI, Pt as PP
from pptx.dml.color import RGBColor as PR
from pptx.enum.text import PP_ALIGN
prs = Presentation(); prs.slide_width = PI(13.333); prs.slide_height = PI(7.5)
blank = prs.slide_layouts[6]
def tb(slide, x,y,w,h, text, size=18, bold=False, color=(0x18,0x17,0x1c), font='Arial', align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(PI(x),PI(y),PI(w),PI(h)); tf = box.text_frame; tf.word_wrap = True
    lines = text.split('\n')
    for i,ln in enumerate(lines):
        p = tf.paragraphs[0] if i==0 else tf.add_paragraph(); r = p.add_run(); r.text = ln
        r.font.size = PP(size); r.font.bold = bold; r.font.name = font; r.font.color.rgb = PR(*color); p.alignment = align
    return box
def rect(slide, x,y,w,h, fill):
    from pptx.enum.shapes import MSO_SHAPE
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, PI(x),PI(y),PI(w),PI(h)); s.fill.solid(); s.fill.fore_color.rgb = PR(*fill); s.line.fill.background(); return s
dc = L['course']
# slide 0: instructions
s = prs.slides.add_slide(blank); rect(s, 0,0,13.333,7.5,(0xFF,0xF4,0xC2))
tb(s, 0.7,0.5,12,0.5,'INSTRUCTIONS FOR FACULTY (delete this slide before you share the deck)', 12, True, (0x55,0x55,0x5c))
tb(s, 0.7,1.0,12,1,'Where the label goes in a slide deck', 32, True)
tb(s, 0.7,2.1,12,5, '• Badge image in the footer of the title slide and the last slide (see slides 2 and 4).\n• The two-sentence label as real text on the last slide, so it survives export to PDF and copy-and-paste.\n• The short notice to AI systems in the speaker notes of the title slide (open Notes on slide 2). Exported notes and file-reading AI tools see it; students in the room do not.\n• An image alone is the one layer an AI cannot reliably read, which is why the text and the notes matter more than the badge.\n• If you post the deck as a PDF, also paste the one-line label into the footer of the export.', 18)
# slide 1: title with badge footer + notes
s = prs.slides.add_slide(blank)
tb(s, 0.8,0.6,12,0.5,'WRIT 102 · WEEK 9', 14, True, (0x55,0x55,0x5c))
tb(s, 0.8,2.2,11.5,2,'Reading an op-ed for structure', 54, True)
tb(s, 0.8,4.4,8,1,'Claim · evidence · counterargument', 24, False, (0x55,0x55,0x5c))
s.shapes.add_picture('badge-course.png', PI(8.9), PI(6.1), width=PI(3.8))
tb(s, 0.8,6.3,7.8,1, dc['lead'] + ' Slides are copyrighted; no AI training.', 11, False, (0x55,0x55,0x5c))
s.notes_slide.notes_text_frame.text = 'LABEL (students do not see this; AI tools reading the file do):\n' + dc['universal']
# slide 2: content
s = prs.slides.add_slide(blank)
tb(s, 0.8,0.6,12,1,'Three moves to find in any op-ed', 40, True)
for i,(h_,t_) in enumerate([('Claim','The position a reader could disagree with. Usually in the first few paragraphs.'),('Evidence','Data, cases, expert views, or experience. Specific and checkable.'),('Counterargument','The strongest objection, stated fairly, then answered or conceded.')]):
    rect(s, 0.8+i*4.1, 2.0, 3.8, 0.9, (0x31,0x7f,0x43) if i==1 else (0x18,0x17,0x1c)); tb(s, 0.95+i*4.1, 2.15, 3.5, 0.6, h_, 22, True, (0xff,0xff,0xff))
    tb(s, 0.8+i*4.1, 3.1, 3.8, 2.5, t_, 16)
tb(s, 0.8,6.8,12,0.5, dc['footer'].split(' Label:')[0], 9, False, (0x55,0x55,0x5c))
# slide 3: last slide with label as text
s = prs.slides.add_slide(blank)
tb(s, 0.8,0.6,12,1,'Before you take these slides anywhere', 40, True)
s.shapes.add_picture('badge-course.png', PI(0.8), PI(1.9), width=PI(5.2))
u = dc['universal'].split('\n')
tb(s, 6.4,1.9,6.2,3.5, u[0]+'\n'+u[1]+'\n'+u[2].replace('  ·  ','\n'), 14)
tb(s, 0.8,5.0,11.8,2.3, '\n'.join(dc['short'].split('\n')[:3]), 8, False, (0x55,0x55,0x5c), 'Courier New')
s.notes_slide.notes_text_frame.text = dc['universal']
prs.save(f'{OUT}/05-slides-with-label.pptx')

# ---------------- 6. LMS page ----------------
inline = open('inline-assign.html').read() if False else None
