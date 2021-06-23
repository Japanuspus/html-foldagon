from jinja2 import Template
from html.parser import HTMLParser
import os
import posixpath
from pathlib import Path, PurePosixPath


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

    for file_path in (Path(f) for f in get_file_names()):
        file_path.parent.mkdir(parents=True,exist_ok=True)
        posix_path = PurePosixPath(file_path)
        root_rel = posixpath.relpath('.', posix_path.parent)
        print(f"Writing {file_path}. Root rel: {root_rel}")
        file_path.write_text(t.render(
            title=file_path.stem.replace('_', ' '),
            root_rel=root_rel,
            page_href=posix_path,
        ))


if __name__ == '__main__':
    main()