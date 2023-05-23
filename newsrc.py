"""Main module."""


import jinja2
import json

from pathlib import Path
from typing import Final

import datetime
import sys

from typing import NamedTuple

from os import environ

from subprocess import run, CalledProcessError
from pprint import pprint


TEMPLATE_DIR: Final = Path("~/.local/templates/newsrc").expanduser()


LanguageActions = dict[str, list[str]]


def read_actions() -> LanguageActions:
    actions_file = TEMPLATE_DIR.joinpath("actions.json")

    if not actions_file.exists():
        return {}

    with open(actions_file, "r") as infile:
        lang_actions = json.load(infile)

    return lang_actions


def main():
    target_filename = sys.argv[1]

    target_path = Path.joinpath(Path.cwd(), Path(target_filename))

    if target_path.exists():
        print(f"{target_filename} already exists")
        sys.exit(2)

    ext = target_path.suffix
    file_basename = target_path.stem

    #fetch the matching template for the given filetype
    try:
        template_matches = list(TEMPLATE_DIR.glob(f"*{ext}"))
        template_match = template_matches[0]

    except IndexError:
        raise FileNotFoundError(f"No template file with the extension ")

    with open(template_match) as template_handle:
        loaded_template = jinja2.Template(template_handle.read())

    # get data to fill the template fields
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
        "filename": target_filename,
        "filepath": target_path.resolve().as_posix(),
        "date": datetime.date.today(),
        "username": username,
        "user_email": user_email,
    }

    content = loaded_template.render(**template_opts)

    #write to file
    with open(target_path, "w") as outfile:
        outfile.write(content)

    # execute any post-generation actions
    action_env = jinja2.Environment()

    lang_actions = read_actions()
    if ext in lang_actions:
        actions = lang_actions[ext]

        for action in actions:
            action_template = action_env.from_string(action)
            template_result = action_template.render(**template_opts)

            print(f"Executing: {template_result}")
            run(template_result, shell=True)

    # open in editor if configured
    if "EDITOR" in environ:
        run([environ["EDITOR"], target_filename])


if __name__ == "__main__":
    main()
