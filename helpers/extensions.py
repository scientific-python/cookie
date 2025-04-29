import datetime

from copier_templates_extensions import ContextHook


class SmartDict(dict):
    def __getitem__(self, item):
        if item == "__ci":
            return "github" if "github.com" in self["url"] else "gitlab"
        if item == "__project_slug":
            return self["project_name"].lower().replace("-", "_").replace(".", "_")
        if item == "__type":
            return (
                "compiled"
                if self["backend"] in ["pybind11", "skbuild", "mesonpy", "maturin"]
                else "pure"
            )
        if item == "__answers":
            return self["_copier_conf"]["answers_file"]

        return super(item)


class CookiecutterNamespace(ContextHook):
    def hook(self, context):
        if context.get("_copier_phase", "") == "prompt":
            return {}
        context["__year"] = str(datetime.datetime.today().year)
        return {"cookiecutter": SmartDict(context)}
