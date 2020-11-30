import reportlab.rl_config
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus.flowables import DocAssign, PageBreak

def generate_pdf_from_list(thesis_title, limericks, monorhymes):
    reportlab.rl_config.warnOnMissingFontGlyphs = 0

    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
    pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))

    registerFontFamily('Vera', normal='Vera', bold='VeraBd', italic='VeraIt', boldItalic='VeraBI')

    normal = ParagraphStyle(name="Normal", fontName="Helvetica", fontSize=12, leading=11, )
    title = ParagraphStyle(name="Title", fontName="Helvetica", fontSize=42, leftIndent=50, leading=42)
    chapter_title = ParagraphStyle(name="Title", fontName="Helvetica", fontSize=42, leftIndent=50)
    header = ParagraphStyle(name='Header', fontName="Helvetica", fontSize=18, leading=11)

    story = [
        DocAssign("currentFrame", "doc.frame.id"),
        DocAssign("currentPageTemplate", "doc.pageTemplate.id"),
        DocAssign("aW", "availableWidth"),
        DocAssign("aH", "availableHeight"),
        DocAssign("aWH", "availableWidth,availableHeight")
    ]

    # frontpage
    paragraph = Paragraph(2*'<br/>' + "<b>" + thesis_title + "</b>" + 15 * '<br/>', title)
    story.append(paragraph)

    paragraph = Paragraph("<b>NaNoGenMo 2020 submission</b>", normal)
    story.append(paragraph)

    # make page for limericks
    story.append(PageBreak())
    paragraph = Paragraph(15 * '<br/>' + "<b>I. Limericks</b>" + 15 * '<br/>', chapter_title)
    story.append(paragraph)

    for limerick in limericks:
        story.append(Spacer(1, 0.25 * inch))
        story.append(Paragraph("*"))
        for sentence in limerick:
            story.append(Paragraph(sentence, normal))
        story.append(Spacer(1, 0.25 * inch))

    # make page for monorhyme
    story.append(PageBreak())
    paragraph = Paragraph(15 * '<br/>' + "<b>II. Monorhymes</b>" + 15 * '<br/>', chapter_title)
    story.append(paragraph)

    for monorhyme in monorhymes:
        story.append(Spacer(1, 0.25 * inch))
        story.append(Paragraph("*"))
        for sentence in monorhyme:
            story.append(Paragraph(sentence, normal))
        story.append(Spacer(1, 0.25 * inch))

    doc = SimpleDocTemplate(thesis_title + "rhymes.pdf")
    doc.build(story)