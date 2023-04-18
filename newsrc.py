"""Main module."""


import jinja2

from pathlib import Path
from typing import Final

import datetime
import sys

from os import environ
from subprocess import run
from pprint import pprint


TEMPLATE_DIR: Final = Path("~/.local/templates/newsrc").expanduser()


def main():
    target_filename = sys.argv[1]

    target_path = Path.joinpath(Path.cwd(), Path(target_filename))
    ext = target_path.suffix
    file_basename = target_path.stem

    print(ext)

    try:
        template_matchs = list(TEMPLATE_DIR.glob(f"*{ext}"))
        pprint(template_matchs)

        template_match = template_matchs[0]

    except IndexError:
        raise FileNotFoundError(f"No template file with the extension ")

    with open(template_match) as template_handle:
        loaded_template = jinja2.Template(template_handle.read())

    content = loaded_template.render(name=file_basename, date=datetime.date.today())

    with open(target_path, "w") as outfile:
        outfile.write(content)

    if "EDITOR" in environ:
        run([environ["EDITOR"], target_filename])


if __name__ == "__main__":
    main()
