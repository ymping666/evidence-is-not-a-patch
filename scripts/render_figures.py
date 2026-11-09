"""Regenerate three editable SVGs using only stdlib and released statistics."""
from pathlib import Path
import argparse
import html
import json
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
INK='#182b3a'; MUTED='#526473'; BLUE='#396b8f'; LIGHT='#cbdce9'; GREEN='#25736d'; GOLD='#b67b28'; RED='#a84343'

class SVG:
    def __init__(self,w,h,title,description):
        self.w=w;self.h=h
        self.parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',f'<title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(description)}</desc>', '<rect width="100%" height="100%" fill="white"/>']
    def rect(self,x,y,w,h,color,stroke=None,rounding=0):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rounding}" fill="{color}"'+(f' stroke="{stroke}"'if stroke else '')+'/>')
    def text(self,x,y,text,size=20,color=INK,weight='normal',anchor='start'):
        self.parts.append(f'<text x="{x}" y="{y}" font-family="Helvetica, Arial, sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{color}">{html.escape(str(text))}</text>')
    def lines(self,x,y,lines,size=19,color=INK,leading=26):
        for i,line in enumerate(lines):self.text(x,y+i*leading,line,size,color)
    def arrow(self,x1,y,x2,color=MUTED):
        self.parts.append(f'<line x1="{x1}" y1="{y}" x2="{x2-8}" y2="{y}" stroke="{color}" stroke-width="2"/><polygon points="{x2},{y} {x2-9},{y-5} {x2-9},{y+5}" fill="{color}"/>')
    def save(self,path):path.write_text('\n'.join(self.parts+['</svg>'])+'\n')

def figure1(out):
    s=SVG(1200,250,'Repair realization has multiple observable links','Conceptual audit map. No stage is asserted necessary for every task; supplied correct candidates may bypass new editing.')
    s.text(28,35,'Repair realization links',25,weight='bold')
    cards=[('Repair intent',['Concrete operation','and Issue behavior']),('Tool execution',['Accepted operation','and actual source diff']),('Local evidence',['Behavior coverage','and current source']),('Artifact commitment',['Retained patch','and submit timing']),('Independent result',['Returned artifact','passes fixed grading'])]
    for i,(title,lines)in enumerate(cards):
        x=28+i*235;s.rect(x,72,210,116,'#f2f6f9',LIGHT,8);s.text(x+14,103,title,21,weight='bold');s.lines(x+14,136,lines,18,MUTED)
        if i<4:s.arrow(x+213,129,x+232)
    s.text(28,231,'Descriptive, not causal.',17,MUTED)
    s.save(out/'figure1_repair_chain.svg')

def figure2(out,stats):
    s=SVG(1200,455,'Nested mechanical delivery subsets','Counts recomputed from anonymized frozen events. Source change, a zero-exit check after the last production edit, and independent PASS inside that checked subset. These are dependent descriptive subsets.')
    s.text(28,35,'Mechanical delivery subsets',25,weight='bold')
    colors=[LIGHT,BLUE,GREEN]; labels=['Actual source change','Post-last-edit zero-exit check','Independent PASS inside checked subset']
    for i,(c,label)in enumerate(zip(colors,labels)):
        x=[28,320,705][i];s.rect(x,58,16,16,c);s.text(x+24,72,label,17)
    keys=['source_changed','strict_post_last_change_zero','resolved_inside_strict']
    for row,panel in enumerate(('P5','P6.2','P8','P12')):
        values=stats['figure2'][panel];y=115+row*77
        s.text(28,y+20,panel,23,weight='bold')
        s.text(28,y+45,f"n={values['episode_total']}",16,MUTED)
        for j,key in enumerate(keys):
            n=values[key];yy=y+j*17
            s.rect(155,yy,n*17.5,13,colors[j]);s.text(165+n*17.5,yy+12,n,16,colors[j]if j else INK,weight='bold')
    s.text(28,441,'Descriptive subsets; shared tasks.',17,MUTED)
    s.save(out/'figure2_delivery_subsets.svg')

def figure3(out,abjad):
    s=SVG(1200,435,'Abjad: diagnosis, edits, and CPU patch ablation','Original agent C passed eight tests after two edits, with no post-edit check or explicit submission. Separate CPU code ablations: default-only eight pass; filter-only six pass and two fail. No prompt causal effect is established.')
    s.text(28,35,'Abjad: diagnosis, code changes, and limits',25,weight='bold')
    s.text(28,76,'Original C: actual tool order',19,weight='bold')
    timeline=abjad['timeline']
    cards=[(f"{timeline['C_diagnostic_tool']}: diagnose",['Real Quantizer output','shows second behavior']),
           (f"{timeline['C_first_source_edit_tool']}: default",['replace_rest flag','False to True']),
           (f"{timeline['C_second_source_edit_tool']}: filtering",['Replace remove loop','with list filtering']),
           ('Then: context stop',['No post-edit check','No explicit submit'])]
    for i,(title,lines)in enumerate(cards):
        x=28+i*294;s.rect(x,95,270,100,'#f2f6f9',LIGHT,6);s.text(x+12,123,title,20,weight='bold');s.lines(x+12,153,lines,18,MUTED,24)
        if i<3:s.arrow(x+274,145,x+292)
    s.text(28,233,'Recorded 8-test outcomes (distinct execution origins)',20,weight='bold')
    c=next(v for v in abjad['original_agent_results']if v['arm']=='C')
    assert timeline['checks_after_C_last_source_edit']==timeline['C_explicit_submits']==0
    variants={v['variant']:v for v in abjad['cpu_ablations']}
    rows=[('Full C patch','Original agent artifact',c['passed'],c['failed']),
          ('Default-only','Later CPU ablation',variants['DEFAULT_ONLY']['passed'],variants['DEFAULT_ONLY']['failed']),
          ('Filter-only','Later CPU ablation',variants['FILTER_ONLY']['passed'],variants['FILTER_ONLY']['failed'])]
    for i,(name,origin,p,f)in enumerate(rows):
        y=267+i*46;s.text(28,y,name,20,weight='bold');s.text(230,y,origin,17,MUTED);s.rect(500,y-18,p*60,24,GREEN)
        if f:s.rect(500+p*60,y-18,f*60,24,RED)
        s.text(1005,y,f'{p} PASS / {f} FAIL',18)
    s.text(28,421,'Code ablation, not prompt causality.',17,MUTED)
    # Validate chart constants against the released, source-bound receipts.
    assert sorted((v['passed'],v['failed'])for v in abjad['cpu_ablations'])==[(6,2),(8,0)]
    assert (c['passed'],c['failed'])==(8,0)
    s.save(out/'figure3_abjad_ablation.svg')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,default=ROOT/'paper/figures');args=parser.parse_args()
    args.output_dir.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='paper_statistics_')as tmp:
        path=Path(tmp)/'statistics.json'
        subprocess.run([sys.executable,'-B',str(ROOT/'scripts/verify_statistics.py'),'--output',str(path)],check=True,stdout=subprocess.PIPE,text=True)
        stats=json.loads(path.read_text())
    abjad=json.loads((ROOT/'data/abjad_results.json').read_text())
    figure1(args.output_dir);figure2(args.output_dir,stats);figure3(args.output_dir,abjad)
    print('Regenerated 3 editable SVG figures from released statistical data; no experiments executed.')

if __name__=='__main__':main()
