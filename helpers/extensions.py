import datetime
from collections.abc import Mapping

from copier_templates_extensions import ContextHook


class SmartDict(Mapping):
    def __init_subclass__(cls):
        cls._computed_keys = {}

    def __init__(self, init):
        self._init = init

    @classmethod
    def register(cls, func):
        cls._computed_keys[func.__name__] = func
        return func

    def __getitem__(self, item):
        if item in self._computed_keys:
            return self._computed_keys[item](self._init)

        return self._init[item]

    def __contains__(self, item):
        return item in self._init or item in self._computed_keys

    def __iter__(self):
        yield from self._init
        yield from self._computed_keys

    def __len__(self):
        return len(self._computed_keys) + len(self._init)


class CookiecutterContext(SmartDict):
    pass


@CookiecutterContext.register
def __year(_):
    return str(datetime.datetime.today().year)


@CookiecutterContext.register
def __ci(context):
    return "github" if "github.com" in context["url"] else "gitlab"


@CookiecutterContext.register
def __project_slug(context):
    return context["project_name"].lower().replace("-", "_").replace(".", "_")


@CookiecutterContext.register
def __type(context):
    return (
        "compiled"
        if context["backend"] in {"pybind11", "skbuild", "mesonpy", "maturin"}
        else "pure"
    )


@CookiecutterContext.register
def __answers(context):
    return context["_copier_conf"]["answers_file"]


class CookiecutterNamespace(ContextHook):
    def hook(self, context):
        return {"cookiecutter": CookiecutterContext(context)}
