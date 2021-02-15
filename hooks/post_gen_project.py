"""
NOTE:
    the below code is to be maintained Python 2.x-compatible
    as the whole Cookiecutter Django project initialization
    can potentially be run in Python 2.x environment
    (at least so we presume in `pre_gen_project.py`).
"""
from __future__ import print_function

import os
import random
import shutil
import string

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

try:
    # Inspired by
    # https://github.com/django/django/blob/master/django/utils/crypto.py
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

DEBUG_VALUE = "debug"


def remove_dotgitlabciyml_file():
    os.remove(".gitlab-ci.yml")


def generate_random_string(
    length, using_digits=False, using_ascii_letters=False, using_punctuation=False
):
    """
    Example:
        opting out for 50 symbol-long, [a-z][A-Z][0-9] string
        would yield log_2((26+26+50)^50) ~= 334 bit strength.
    """
    if not using_sysrandom:
        return None

    symbols = []
    if using_digits:
        symbols += string.digits
    if using_ascii_letters:
        symbols += string.ascii_letters
    if using_punctuation:
        all_punctuation = set(string.punctuation)
        # These symbols can cause issues in environment variables
        unsuitable = {"'", '"', "\\", "$"}
        suitable = all_punctuation.difference(unsuitable)
        symbols += "".join(suitable)
    return "".join([random.choice(symbols) for _ in range(length)])


def set_flag(file_path, flag, value=None, formatted=None, *args, **kwargs):
    if value is None:
        random_string = generate_random_string(*args, **kwargs)
        if random_string is None:
            print(
                "We couldn't find a secure pseudo-random number generator on your system. "
                "Please, make sure to manually {} later.".format(flag)
            )
            random_string = flag
        if formatted is not None:
            random_string = formatted.format(random_string)
        value = random_string

    with open(file_path, "r+") as f:
        file_contents = f.read().replace(flag, value)
        f.seek(0)
        f.write(file_contents)
        f.truncate()

    return value


def remove_celery_files():
    file_names = [
        os.path.join("{{ cookiecutter.project_slug }}", "celery", "app.py"),
        os.path.join("{{ cookiecutter.project_slug }}", "pipelines", "celery.py"),
    ]
    for file_name in file_names:
        os.remove(file_name)


def remove_dir(dir_relpath):
    shutil.rmtree(os.path.join("{{ cookiecutter.project_slug }}", dir_relpath))


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def main():

    if "{{ cookiecutter.use_celery_pipeline }}".lower() == "n":
        remove_celery_files()
        remove_dir("celery")
    if "{{ cookiecutter.scheduler }}".lower() != "cron":
        remove_file("compose/production/scrapyd/cronjob.sh")
    if "{{ cookiecutter.license }}" == "Not open source":
        remove_file("LICENSE")
    if "{{ cookiecutter.db_driver }}" != "sqlachemy(sync)":
        remove_file(os.path.join("{{ cookiecutter.project_slug }}", "models", "sessions.py"))
    if "{{ cookiecutter.scheduler }}" != "scrapydweb":
        remove_dir(os.path.join("compose", "production", "scrapydweb"))


if __name__ == "__main__":
    main()
