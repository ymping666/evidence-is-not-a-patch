"""Build the release PDF from paper.md and local SVGs; no network or scorer.

Optional presentation dependencies are pinned in requirements-render.txt.
Statistical validation does not import this module or require those packages.
"""
from pathlib import Path
import argparse
import hashlib
import html
import importlib.util
import os
import re

ROOT=Path(__file__).resolve().parents[1]

def register_fonts():
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    font_dirs=[Path(os.environ.get('EINAP_FONT_DIR','/usr/share/fonts/truetype/dejavu'))]
    matplotlib_spec=importlib.util.find_spec('matplotlib')
    if matplotlib_spec is not None and matplotlib_spec.origin:
        font_dirs.append(Path(matplotlib_spec.origin).parent/'mpl-data/fonts/ttf')
    files={
        'PaperSerif':'DejaVuSerif.ttf',
        'PaperSerif-Bold':'DejaVuSerif-Bold.ttf',
        'PaperSerif-Italic':'DejaVuSerif-Italic.ttf',
        'PaperSerif-BoldItalic':'DejaVuSerif-BoldItalic.ttf',
        'PaperSans':'DejaVuSans.ttf',
        'PaperSans-Bold':'DejaVuSans-Bold.ttf',
        'PaperMono':'DejaVuSansMono.ttf',
    }
    resolved={name:next((base/filename for base in font_dirs if (base/filename).is_file()),None) for name,filename in files.items()}
    missing=[files[name] for name,path in resolved.items() if path is None]
    if missing:raise FileNotFoundError(f'DejaVu font files missing: {missing}; install complete DejaVu fonts or set EINAP_FONT_DIR (checked {font_dirs})')
    for name,path in resolved.items():pdfmetrics.registerFont(TTFont(name,str(path)))
    pdfmetrics.registerFontFamily('PaperSerif',normal='PaperSerif',bold='PaperSerif-Bold',italic='PaperSerif-Italic',boldItalic='PaperSerif-BoldItalic')
    pdfmetrics.registerFontFamily('PaperSans',normal='PaperSans',bold='PaperSans-Bold')

def ascii_punctuation(text):
    return text.translate(str.maketrans({'−':'-','–':'-','—':' - ','→':' to ','↓':' down ',
                                       '’':"'",'‘':"'",'“':'"','”':'"','≠':'!=','≤':'<=','≥':'>='}))

def markup(text):
    text=html.escape(ascii_punctuation(text))
    text=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',r'<link href="\2" color="#285f85">\1</link>',text)
    text=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',text)
    text=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<i>\1</i>',text)
    text=re.sub(r'`([^`]+)`',r'<font name="PaperMono">\1</font>',text)
    return text

def main():
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,KeepTogether,Flowable
    from reportlab.graphics import renderPDF
    from reportlab.graphics.shapes import String
    from svglib.svglib import svg2rlg
    register_fonts()

    class VectorFigure(Flowable):
        def __init__(self,path,width):
            Flowable.__init__(self);self.drawing=svg2rlg(str(path));self.width=width
            pending=[self.drawing]
            while pending:
                node=pending.pop()
                if isinstance(node,String):
                    node.fontName='PaperSans-Bold' if str(node.fontName).endswith('Bold') else 'PaperSans'
                pending.extend(getattr(node,'contents',()))
            self.height=self.drawing.height*width/self.drawing.width
        def draw(self):
            factor=self.width/self.drawing.width
            self.canv.saveState();self.canv.scale(factor,factor)
            renderPDF.draw(self.drawing,self.canv,0,0);self.canv.restoreState()

    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'paper/paper.pdf');args=parser.parse_args()
    source=ROOT/'paper/paper.md';text=source.read_text()
    width=A4[0]-34*mm
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='PaperTitle',fontName='PaperSerif-Bold',fontSize=18,leading=22,spaceAfter=9,textColor=colors.HexColor('#182b3a')))
    styles.add(ParagraphStyle(name='PaperSubtitle',fontName='PaperSerif-Italic',fontSize=10,leading=13,spaceAfter=11))
    styles.add(ParagraphStyle(name='PaperArtifact',fontName='PaperSans',fontSize=8.5,leading=12,spaceAfter=10,textColor=colors.HexColor('#285f85')))
    styles.add(ParagraphStyle(name='PaperBody',fontName='PaperSerif',fontSize=9.5,leading=12.5,spaceAfter=5.5))
    styles.add(ParagraphStyle(name='PaperH2',fontName='PaperSerif-Bold',fontSize=11.6,leading=15,spaceBefore=10,spaceAfter=6,keepWithNext=True,textColor=colors.HexColor('#182b3a')))
    styles.add(ParagraphStyle(name='PaperCaption',fontName='PaperSerif',fontSize=8.4,leading=11,spaceBefore=4,spaceAfter=8))
    styles.add(ParagraphStyle(name='PaperReference',fontName='PaperSerif',fontSize=8.4,leading=11.5,spaceAfter=4))
    styles.add(ParagraphStyle(name='PaperTable',fontName='PaperSerif',fontSize=7.5,leading=9.7))
    styles.add(ParagraphStyle(name='PaperTableHeader',fontName='PaperSerif-Bold',fontSize=7.5,leading=9.7,textColor=colors.HexColor('#182b3a')))
    blocks=re.split(r'\n\s*\n',text.strip());story=[];references=False;i=0
    while i<len(blocks):
        block=blocks[i].strip()
        if block.startswith('# '):story.append(Paragraph(markup(block[2:]),styles['PaperTitle']))
        elif block.startswith('**Subtitle:**'):story.append(Paragraph(markup(block.replace('**Subtitle:**','').strip()),styles['PaperSubtitle']))
        elif block.startswith('**Artifact repository:**'):story.append(Paragraph(markup(block),styles['PaperArtifact']))
        elif block.startswith('## '):
            references=block=='## References';story.append(Paragraph(markup(block[3:]),styles['PaperH2']))
        elif block.startswith('!['):
            match=re.fullmatch(r'!\[[^\]]*\]\(([^)]+)\)',block);assert match,block
            image=(source.parent/match[1]).resolve();assert image.is_relative_to(source.parent.resolve()) and image.suffix=='.svg'
            figure=VectorFigure(image,width)
            if i+1<len(blocks)and blocks[i+1].strip().startswith('**Figure '):
                story.append(KeepTogether([Spacer(1,5),figure,Paragraph(markup(blocks[i+1].replace('\n',' ')),styles['PaperCaption'])]));i+=1
            else:story.append(figure)
        elif block.startswith('|'):
            lines=[l.strip()for l in block.splitlines()if l.strip()]
            rows=[[c.strip()for c in line.strip('|').split('|')]for line in lines if not re.fullmatch(r'\|[\s|:\-]+\|',line)]
            n=len(rows[0]);assert all(len(r)==n for r in rows)
            if n==3:ratios=[.31,.36,.33]
            elif n==5:ratios=[.10,.24,.22,.16,.28]
            else:ratios=[1/n]*n
            cells=[[Paragraph(markup(c),styles['PaperTableHeader'if r==0 else 'PaperTable'])for c in row]for r,row in enumerate(rows)]
            table=Table(cells,colWidths=[width*x for x in ratios],repeatRows=1,hAlign='LEFT')
            table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eaf1f5')),('LINEABOVE',(0,0),(-1,0),.65,colors.HexColor('#396b8f')),('LINEBELOW',(0,0),(-1,0),.35,colors.HexColor('#9bb2c2')),('LINEBELOW',(0,-1),(-1,-1),.5,colors.HexColor('#9bb2c2')),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
            if i+1<len(blocks) and blocks[i+1].strip().startswith('**Table '):
                caption=Paragraph(markup(blocks[i+1].replace('\n',' ')),styles['PaperCaption'])
                story.append(KeepTogether([Spacer(1,5),table,caption,Spacer(1,3)]))
                i+=1
            else:
                story.extend([Spacer(1,5),table,Spacer(1,3)])
        elif references:
            for line in block.splitlines():story.append(Paragraph(markup(line),styles['PaperReference']))
        elif block.startswith('**Figure ')or block.startswith('**Table '):story.append(Paragraph(markup(block.replace('\n',' ')),styles['PaperCaption']))
        else:story.append(Paragraph(markup(block.replace('\n',' ')),styles['PaperBody']))
        i+=1

    def page(canvas,doc):
        canvas.saveState();canvas.setFont('PaperSans',7.5);canvas.setFillColor(colors.HexColor('#526473'))
        canvas.drawString(17*mm,12*mm,'evidence-is-not-a-patch | 2026-11-09')
        canvas.drawRightString(A4[0]-17*mm,12*mm,str(doc.page));canvas.restoreState()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    doc=SimpleDocTemplate(str(args.output),pagesize=A4,rightMargin=17*mm,leftMargin=17*mm,topMargin=16*mm,bottomMargin=19*mm,
          title='From Local Improvement to Verified Repair: A Cross-Intervention Delivery Audit',author='Project contributors',
          subject='Public research release; source-state audit and exploratory prompt-only SEAL intervention',creator='ReportLab; local Markdown/SVG build',invariant=1)
    doc.build(story,onFirstPage=page,onLaterPages=page)
    print('Built PDF from released Markdown and editable SVGs: '+hashlib.sha256(args.output.read_bytes()).hexdigest())

if __name__=='__main__':main()
