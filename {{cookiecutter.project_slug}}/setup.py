import pkg_resources
import six
from pkg_resources import parse_requirements
from setuptools import find_packages, setup


def removeprefix(self: str, prefix: str, /) -> str:
    if self.startswith(prefix):
        # fmt: off
        return self[len(prefix):]
        # fmt: on
    else:
        return self[:]


def yield_lines(strs):
    """Yield non-empty/non-comment lines of a string or sequence,
    the only difference with yield_lines from pkg_resources
    is yielding requirements from base requirement like -r requests.txt as well"""
    if isinstance(strs, six.string_types):
        for s in strs.splitlines():
            s = s.strip()
            if s.startswith("-r "):
                if " #" in s:
                    s = s[: s.find(" #")]
                fname = removeprefix(s, "-r").lstrip()
                with open(fname, "r", encoding="utf-8") as fp:
                    yield from yield_lines(fp.read())
            # skip blank lines/comments
            elif s and not s.startswith("#"):  # the only difference
                yield s
    else:
        for ss in strs:
            for s in yield_lines(ss):
                yield s


pkg_resources.yield_lines = (
    yield_lines  # monkeypatch with handling of -r requirements.txt
)


def load_requirements(fname: str) -> list:
    requirements = []
    with open(fname, "r", encoding="utf-8") as fp:
        for req in parse_requirements(fp.read()):
            extras = "[{}]".format(",".join(req.extras)) if req.extras else ""
            requirements.append("{}{}{}".format(req.name, extras, req.specifier))
    return requirements


setup(
    name="{{cookiecutter.project_slug}}",
    version="0.0.1",
    python_requires=">=3.9",  # TODO: tox for test other versions
    packages=find_packages(),
    # packages=find_packages(exclude=["tests"]), # TODO: after tests will be added
    install_requires=load_requirements("requirements.txt"),
    extras_require={"dev": load_requirements("requirements_dev.txt")},
    entry_points={"scrapy": ["settings = {{cookiecutter.project_slug}}.settings"]},
)
