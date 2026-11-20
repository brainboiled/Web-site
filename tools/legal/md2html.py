"""Convertit une politique de confidentialité Markdown en fragment HTML pour tools/legal/<appli>/.

Usage : python3 tools/legal/md2html.py source.md tools/legal/<appli>/privacy.<langue>.html
"""
import html, re, sys


def md2html(t):
    out, para, lst = [], [], []

    def inl(s):
        s = html.escape(s, quote=False)
        s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
        s = re.sub(r'\[(.+?)\]\((https?://[^)]+)\)', r'<a href="\2">\1</a>', s)
        s = re.sub(r'(?<![">])(https?://[^\s<)]+)', r'<a href="\1">\1</a>', s)
        return re.sub(r'([\w.]+@brainboiled\.com)', r'<a href="mailto:\1">\1</a>', s)

    def flush():
        if para:
            out.append('<p>' + ' '.join(para) + '</p>')
            para.clear()
        if lst:
            out.append('<ul>\n' + '\n'.join('  <li>' + x + '</li>' for x in lst) + '\n</ul>')
            lst.clear()

    for line in t.splitlines():
        if line.startswith('# '):
            flush(); out.append('<h1>' + inl(line[2:]) + '</h1>')
        elif line.startswith('## '):
            flush(); out.append('<h2>' + inl(line[3:]) + '</h2>')
        elif re.match(r'^(Last updated|Dernière mise à jour|Última actualización|Última atualização|Zuletzt aktualisiert|Ultimo aggiornamento|最終更新日|Ostatnia aktualizacja|Laatst bijgewerkt)', line):
            flush(); out.append('<div class="updated">' + inl(line) + '</div>')
        elif line.startswith('- '):
            if para:
                out.append('<p>' + ' '.join(para) + '</p>'); para.clear()
            lst.append(inl(line[2:]))
        elif not line.strip():
            flush()
        else:
            para.append(inl(line))
    flush()
    return '\n\n'.join(out) + '\n'


if __name__ == '__main__':
    open(sys.argv[2], 'w', encoding='utf-8').write(md2html(open(sys.argv[1], encoding='utf-8').read()))
