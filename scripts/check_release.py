"""Validate the selected public release (standard library; no network).

PDF text/attachments/fonts were inspected before release; its exact audited bytes
are bound by the manifest. This script does not pretend to be a PDF interpreter.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
RULES={
    'credential_token':rb'\b(?:KGAT_[A-Za-z0-9]{16,}|gh[pousr]_[A-Za-z0-9]{24,}|github_pat_[A-Za-z0-9_]{24,}|hf_[A-Za-z0-9]{24,}|sk-[A-Za-z0-9_-]{32,})',
    'private_key':rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    'private_host_path':rb'/(?:m[n]t[0-9]*|r[o]ot|home)/',
    'private_origin_url':rb'github[.]com/ymping666/gemma(?:[/\s"\x27]|$)',
    'machine_endpoint':rb'https?://(?:127[.]0[.]0[.]1|localhost|10[.]\d+[.]\d+[.]\d+|192[.]168[.]\d+[.]\d+)(?::\d+)?',
}
FORBIDDEN_DATA_KEYS={'problem_statement','hints_text','test_patch','reference_patch','gold_patch',
                     'command','arguments','stdout','stderr','messages','api_key','access_token'}

def inspect_json(value,path):
    if isinstance(value,dict):
        assert not (set(value)&FORBIDDEN_DATA_KEYS),'excluded raw field: '+str(path)
        for child in value.values():inspect_json(child,path)
    elif isinstance(value,list):
        for child in value:inspect_json(child,path)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=ROOT);args=parser.parse_args();root=args.root.resolve()
    manifest=json.loads((root/'release_manifest.json').read_bytes())
    expected={x['path']:x for x in manifest['files']};assert len(expected)==len(manifest['files'])
    assert all(x.get('public_release_authorized')is True and x.get('rights_basis')for x in expected.values())
    actual=set()
    for base,dirs,names in os.walk(root,followlinks=False):
        dirs[:]=[d for d in dirs if d not in ('.git','__pycache__')and not d.startswith('.venv')]
        for d in dirs:assert not (Path(base)/d).is_symlink(),'symlink directory excluded'
        for name in names:
            p=Path(base)/name
            if p.suffix in ('.pyc','.pyo'):continue
            assert not p.is_symlink(),'symlink file excluded'
            rel=str(p.relative_to(root))
            if rel=='release_manifest.json':continue
            actual.add(rel)
    assert actual==set(expected),'unmanifested or missing files: '+str(sorted(actual^set(expected)))
    namespace='{http://www.w3.org/2000/svg}'
    svg_count=0;patch_count=0;text_files=0
    for rel,row in expected.items():
        p=root/rel;assert p.resolve().is_relative_to(root)
        data=p.read_bytes();assert len(data)==row['bytes']and hashlib.sha256(data).hexdigest()==row['sha256'],'hash mismatch: '+rel
        assert p.suffix not in ('.zip','.tgz','.gz','.whl','.so','.bin','.safetensors','.pt','.pkl','.pem'),rel
        if p.suffix=='.pdf':
            assert rel=='paper/paper.pdf'and data.startswith(b'%PDF-'),rel
            continue
        text_files+=1;text=data.decode('utf-8')
        for rule,pattern in RULES.items():assert not re.search(pattern,data),rule+': '+rel
        if p.suffix=='.json'and(rel.startswith('data/')or rel.startswith('abjad/')):inspect_json(json.loads(text),rel)
        if p.suffix=='.svg':
            svg_count+=1;xml=ET.fromstring(text)
            assert xml.tag==namespace+'svg'
            assert len(list(xml.iter(namespace+'text')))>0,'SVG text converted to paths: '+rel
            forbidden={'image','script','foreignObject','use','iframe'}
            assert all(e.tag.split('}')[-1]not in forbidden for e in xml.iter())
            assert not re.search(r'(?:xlink:href|\bhref)\s*=|data:|<\!DOCTYPE',text,re.I),rel
        if p.suffix=='.patch':
            patch_count+=1;assert rel.startswith('abjad/patches/')and len(data)<4000
            paths=re.findall(r'^diff --git a/(\S+) b/(\S+)$',text,re.M)
            assert paths and all(a==b=='abjadext/nauert/gracehandlers.py'for a,b in paths),'non-allowlisted patch target'
    assert svg_count==3 and patch_count==3
    assert (root/'LICENSES/abjad-ext-nauert.txt').read_text().startswith('MIT License')
    print(json.dumps({'status':'PASS','manifested_files':len(expected),'manifest_control_file':1,
                      'text_files_scanned':text_files,'editable_SVGs':svg_count,'licensed_production_patches':patch_count,
                      'PDF_exact_audited_bytes_verified':True,'network_calls':0,'agent_generations':0,'scoring_executions':0},indent=2))

if __name__=='__main__':main()
