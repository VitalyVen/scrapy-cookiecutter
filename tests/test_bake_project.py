import datetime
import os
import shlex
import subprocess

from tests.utils import bake_in_temp_dir, inside_dir, run_inside_dir


def check_output_inside_dir(command, dirpath):
    "Run a command from inside a given directory, returning the command output"
    with inside_dir(dirpath):
        return subprocess.check_output(shlex.split(command))


def test_year_compute_in_license_file(cookies):
    with bake_in_temp_dir(cookies) as result:
        license_file_path = result.project.join("LICENSE")
        now = datetime.datetime.now()
        assert str(now.year) in license_file_path.read()


def project_info(result):
    """Get toplevel dir, project_slug, and project dir from baked cookies"""
    project_path = str(result.project)
    project_slug = os.path.split(project_path)[-1]
    project_dir = os.path.join(project_path, project_slug)
    return project_path, project_slug, project_dir


def test_bake_with_defaults(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert "scrapy.cfg" in found_toplevel_files


def test_bake_and_run_spider(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        run_inside_dir("./dev.sh", str(result.project)) == 0
        run_inside_dir("docker-compose up -d", str(result.project)) == 0
        try:
            run_inside_dir(
                "docker-compose run -w /app/crawler/spiders/ scrapy python3 spider.py",
                str(result.project),
            ) == 0
            run_inside_dir(
                f"docker-compose run -w / -v {str(result.project)}:/app: scrapy rm /app/crawler/ -rf",
                str(result.project),
            ) == 0
            run_inside_dir(
                f"docker-compose run -w / -v {str(result.project)}:/app: scrapy rm /app/dbs/ -rf",
                str(result.project),
            ) == 0
        finally:
            run_inside_dir("docker-compose down", str(result.project)) == 0


def test_pre_commit(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        run_inside_dir("./dev.sh", str(result.project)) == 0
        run_inside_dir("git add .", str(result.project)) == 0
        run_inside_dir('git commit -am "hello"', str(result.project)) == 0


def test_bake_selecting_license(cookies):
    license_strings = {
        "MIT license": "MIT ",
        "BSD license": "Redistributions of source code must retain the "
        + "above copyright notice, this",
        "ISC license": "ISC License",
        "Apache Software License 2.0": "Licensed under the Apache License, Version 2.0",
        "GNU General Public License v3": "GNU GENERAL PUBLIC LICENSE",
    }
    for license, target_string in license_strings.items():
        with bake_in_temp_dir(cookies, extra_context={"license": license}) as result:
            assert target_string in result.project.join("LICENSE").read()
            # assert license in result.project.join('setup.py').read() #TODO:


def test_bake_not_open_source(cookies):
    with bake_in_temp_dir(
        cookies, extra_context={"license": "Not open source"}
    ) as result:
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert "LICENSE" not in found_toplevel_files
        assert "License" not in result.project.join("README.rst").read()
