from jinja2 import Template
from html.parser import HTMLParser
import os
from pathlib import Path


def get_file_names():
    class HrefParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.targets = []
            
        def handle_starttag(self, tag, attrs):
            if tag=='a':
                for v in (v for k,v in attrs if k=='href'):
                    self.targets.append(v)

    p = Path('_navbar.html')
    h = HrefParser()
    h.feed(p.read_text())
    return h.targets


def main():
    t = Template(Path('full_content_template.html').read_text())

    for href in (Path(f) for f in get_file_names()):
        href.parent.mkdir(parents=True,exist_ok=True)
        root_rel = os.path.relpath('.', href.parent)
        print(f"Writing {href}. Root rel: {root_rel}")
        href.write_text(t.render(
            title=href.stem.replace('_', ' '),
            root_rel=root_rel,
        ))


if __name__ == '__main__':
    main()