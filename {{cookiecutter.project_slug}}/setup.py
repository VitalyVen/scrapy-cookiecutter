from setuptools import find_packages, setup

setup(
    name="{{cookiecutter.project_slug}}",
    version="0.0.1",
    packages=find_packages(),
    entry_points={"scrapy": ["settings = {{cookiecutter.project_slug}}.settings"]},
)
