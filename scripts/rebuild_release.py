"""Update the public PDF build receipt and manifest after an audited manuscript change.
No task code, model, scoring environment, or network is invoked.
"""
from pathlib import Path
import hashlib, json, re, subprocess
R=Path(__file__).resolve().parents[1]
def sha(data):return hashlib.sha256(data).hexdigest()
def lex(t):return len(re.findall(r"[A-Za-z0-9]+(?:[-_'][A-Za-z0-9]+)*",t))
md=(R/'paper/paper.md').read_text(encoding='utf-8')
pdf_text=subprocess.check_output(['pdftotext','-layout',str(R/'paper/paper.pdf'),'-']).decode('utf-8')
info=subprocess.check_output(['pdfinfo',str(R/'paper/paper.pdf')]).decode('utf-8')
pages=int(re.search(r'^Pages:\s*(\d+)',info,re.M).group(1))
w={
 'markdown_whitespace_including_tables_captions_references':len(md.split()),
 'markdown_lexical_including_tables_captions_references':lex(md),
 'PDF_whitespace_including_figure_text_repeated_headers_footers_page_numbers_references':len(pdf_text.split()),
 'PDF_lexical_including_figure_text_repeated_headers_footers_page_numbers_references':lex(pdf_text),
 'cap':3000, 'reference_or_footer_exemption_used':False,
}
assert max(w[k] for k in w if 'lexical' in k)<3000, w
p=R/'paper/build_receipt.json'
receipt=json.loads(p.read_text())
receipt.update(public_markdown_sha256=sha(md.encode()),public_PDF_sha256=sha((R/'paper/paper.pdf').read_bytes()),PDF_pages=pages,word_counts=w)
receipt.setdefault('presentation_changes',[]).append('Cited seven additional verified first-party works across introduction and related work (17 references total), shortened repeated prose; experiments unchanged')
p.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
manifest_path=R/'release_manifest.json'
manifest=json.loads(manifest_path.read_text())
rows={x['path']:x for x in manifest['files']}
for rel,category in [('.github/workflows/rebuild-paper.yml','research_documentation_or_configuration'),('scripts/rebuild_release.py','new_statistical_or_presentation_utility')]:
 if rel not in rows:
  rows[rel]={'path':rel,'category':category,'rights_basis':'User-authorized public research reproducibility workflow; first-party code','public_release_authorized':True}
for rel,row in rows.items():
 content=(R/rel).read_bytes()
 row.update(bytes=len(content),sha256=sha(content))
manifest['files']=[rows[x] for x in sorted(rows)]
for k in ('file_count_excluding_manifest','file_count'):
 if k in manifest:manifest[k]=len(rows)
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'pages':pages,'counts':w,'files':len(rows),'status':'PASS'},indent=2))
