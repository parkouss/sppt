import os
import sys
import argparse

from jinja2 import Environment, FileSystemLoader
from configobj import ConfigObj

from sppt import variables


class SpptError(Exception):
    """Specific error class for sppt"""


def filter_rst_title(name, char="="):
    return "{}\n{}".format(name, char * len(name))


def create_template_env(template_path=None):
    """
    Create the Jinja2 template environment.
    """
    if template_path is None:
        template_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "templates"
        )
    env = Environment(
        loader=FileSystemLoader(template_path),
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=False,
    )
    env.filters['repr'] = repr
    env.filters['rst_title'] = filter_rst_title
    return env


def generate_dirs(ui, opts):
    if os.path.isdir(opts.output_dir):
        if os.listdir(opts.output_dir):
            raise SpptError("Output dir {} is not empty.")
    else:
        os.makedirs(opts.output_dir)

    os.mkdir(os.path.join(opts.output_dir, ui['project_name']))


def generate_project_template(ui, opts):
    generate_dirs(ui, opts)
    prj_dir = os.path.join(opts.output_dir, ui['project_name'])
    env = create_template_env()

    with open(os.path.join(opts.output_dir, "setup.py"), "w") as f:
        f.write(env.get_template("setup.py.tpl").render(**ui))

    with open(os.path.join(prj_dir, "__init__.py"), "w") as f:
        f.write(env.get_template("__init__.py.tpl").render(**ui))

    with open(os.path.join(opts.output_dir, "README.rst"), "w") as f:
        f.write(env.get_template("README.rst.tpl").render(**ui))

    if ui["executable"]:
        with open(os.path.join(prj_dir, "main.py"), "w") as f:
            f.write(env.get_template("main.py.tpl").render(**ui))


def get_defaults():
    defaults = {}
    config = ConfigObj(os.path.expanduser("~/.gitconfig"))
    try:
        defaults["author"] = config["user"]["name"]
    except KeyError:
        pass
    try:
        defaults["author_email"] = config["user"]["email"]
    except KeyError:
        pass
    return defaults


def parse_args(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output-dir",
                        help="Output dir")
    return parser.parse_args()


def main(argv=None):
    opts = parse_args(argv=argv)

    try:
        ui = variables.vars_to_dict(defaults=get_defaults())

        if opts.output_dir is None:
            opts.output_dir = ui["project_name"]
        generate_project_template(ui, opts)
    except SpptError as exc:
        sys.exit("Error: {}".format(exc))
    except (EOFError, KeyboardInterrupt):
        sys.exit("\nInterrupted.")
