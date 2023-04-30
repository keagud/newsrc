"""Main module."""


import jinja2

from pathlib import Path
from typing import Final

import datetime
import sys

from os import environ

from subprocess import run, CalledProcessError
from pprint import pprint


TEMPLATE_DIR: Final = Path("~/.local/templates/newsrc").expanduser()


def main():
    target_filename = sys.argv[1]

    target_path = Path.joinpath(Path.cwd(), Path(target_filename))

    if target_path.exists():
        print(f"{target_filename} already exists")
        sys.exit(2)

    ext = target_path.suffix
    file_basename = target_path.stem

    print(ext)

    try:
        template_matches = list(TEMPLATE_DIR.glob(f"*{ext}"))
        template_match = template_matches[0]

    except IndexError:
        raise FileNotFoundError(f"No template file with the extension ")

    with open(template_match) as template_handle:
        loaded_template = jinja2.Template(template_handle.read())

    username_call = run(
        "git config --global --get user.name", shell=True, capture_output=True
    )
    user_email_call = run(
        "git config --global --get user.email", shell=True, capture_output=True
    )

    try:
        username_call.check_returncode()
        username = username_call.stdout.decode().strip()
    except CalledProcessError:
        username = None

    try:
        user_email_call.check_returncode()
        user_email = user_email_call.stdout.decode().strip()

    except CalledProcessError:
        user_email = None

    template_opts = {
        "name": file_basename,
        "date": datetime.date.today(),
        "username": username,
        "user_email": user_email,
    }

    content = loaded_template.render(**template_opts)

    with open(target_path, "w") as outfile:
        outfile.write(content)

    if "EDITOR" in environ:
        run([environ["EDITOR"], target_filename])


if __name__ == "__main__":
    main()
