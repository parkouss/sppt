from builtins import input

class Var:
    def __init__(self, name, default=None, should_input=True, prompt=None,
                 validator=str):
        self.name = name
        self.default = default
        self.should_input = should_input
        self.prompt = prompt
        self.validator = validator

    def title(self):
        if self.prompt:
            return self.prompt
        return ' '.join(p.title() for p in self.name.split('_'))

    def value(self, vs):
        if callable(self.default):
            default = self.default(vs)
        else:
            default = self.default
        if (callable(self.should_input) and not self.should_input(vs)) or \
           not self.should_input:
            return default
        if default is not None:
            prompt = "{} [{}]: ".format(self.title(), default)
        else:
            prompt = "{}: ".format(self.title())
        while 1:
            up = input(prompt)
            if not up and self.default is not None:
                return default
            try:
                return self.validator(up)
            except ValueError:
                continue


def validate_yN(value):
    if value in ('y', 'Y'):
        return True
    elif value in ('', 'n', 'N'):
        return False
    raise ValueError


def validate_require(value):
    if not value:
        raise ValueError
    return value


def default_vars():
    return [
        Var("project_name", validator=validate_require),
        Var("project_description", validator=validate_require),
        Var("project_version", default="0.1.0", validator=validate_require),
        Var("author", validator=validate_require),
        Var("author_email", validator=validate_require),
        Var("license", default="GPL", validator=validate_require),
        Var(
            "executable",
            prompt="Do you want a console executable? [y/N]",
            validator=validate_yN,
        ),
        Var(
            "executable_name",
            prompt="Name of the executable",
            default=lambda vs: vs["project_name"],
            should_input=lambda vs: vs["executable"],
            validator=validate_require,
        ),
        Var(
            "executable_entry_point",
            default=lambda vs: "{}.main:main".format(vs["project_name"]),
            should_input=False,
        )
    ]


def vars_to_dict(vs=None, defaults=None):
    vs = vs or default_vars()
    defaults = defaults or {}
    dct = {}
    for v in vs:
        if v.name in defaults:
            v.default = defaults[v.name]
        dct[v.name] = v.value(dct)
    return dct
