#!/usr/bin/env python3
"""Verify the static release artifact using only the Python standard library."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib, json

EXPECTED = 'd96d87fea85aa2349e2ed3c2d6258f446c664fc50a3d6420d72486c5c69a2919'
ROOT = Path(__file__).resolve().parent
class Document(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.meta={}; self.titles=[]; self.in_title=False
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag in ('a','iframe') and (a.get('href') or a.get('src')):
            self.links.append(a.get('href') or a.get('src'))
        if tag=='meta': self.meta[a.get('name','')]=a.get('content','')
        if tag=='title': self.in_title=True
    def handle_endtag(self,tag):
        if tag=='title': self.in_title=False
    def handle_data(self,data):
        if self.in_title:self.titles.append(data)

def verify():
    checks=[]
    def check(name,condition):
        checks.append({'check':name,'pass':bool(condition)})
    pdfs=list(ROOT.glob('*.pdf'))
    check('all six compatibility PDF aliases retained',len(pdfs)==6)
    for pdf in pdfs:
        check(pdf.name+' exact approved bytes',hashlib.sha256(pdf.read_bytes()).hexdigest()==EXPECTED)
        check(pdf.name+' PDF header',pdf.read_bytes().startswith(b'%PDF-'))
    for name in ['index.html','deck-e10.html']:
        d=Document();d.feed((ROOT/name).read_text())
        check(name+' current version label','E10.1' in ''.join(d.titles))
        check(name+' responsive viewport','width=device-width' in d.meta.get('viewport',''))
        check(name+' noindex','noindex' in d.meta.get('robots',''))
        check(name+' canonical embedded PDF','WisdomTwin-Investor-Deck.pdf' in d.links)
        for link in d.links:
            path=urlsplit(link).path
            if not path or urlsplit(link).scheme:continue
            target=(ROOT/unquote(path).lstrip('/')).resolve()
            check(name+' valid internal link '+link,target.is_relative_to(ROOT) and target.exists())
    page=(ROOT/'invest/index.html').read_text()
    check('investor download label current','Download the approved investor deck (E10.1)' in page)
    check('stale verified-E9 label removed','E9, verified' not in page)
    for line in (ROOT/'_redirects').read_text().splitlines():
        if not line.strip() or line.startswith('#'):continue
        source,target,status=line.split()
        check('redirect target exists '+source,(ROOT/target.lstrip('/')).exists())
        check('no self rewrite '+source,source!=target)
    return checks

if __name__=='__main__':
    checks=verify()
    result={'checks':checks,'passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks),'production_deployment_verified':False}
    print(json.dumps(result,indent=2))
    raise SystemExit(1 if result['failed'] else 0)
