from jinja2 import Template
from html.parser import HTMLParser
from pathlib import Path


class HrefParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []
        
    def handle_starttag(self, tag, attrs):
        if tag=='a':
            for v in (v for k,v in attrs if k=='href'):
                self.targets.append(v)


def get_file_names():
    p = Path('_navbar.html')
    h = HrefParser()
    h.feed(p.read_text())
    return h.targets


def main():
    t = Template(Path('full_content_template.html').read_text())

    for href in (Path(f) for f in get_file_names()):
        href.write_text(t.render(title=href.stem.replace('_', ' ')))


if __name__ == '__main__':
    main()