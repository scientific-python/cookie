import datetime

from copier_templates_extensions import ContextHook


class CookiecutterNamespace(ContextHook):
    def hook(self, context):
        context["__year"] = str(datetime.datetime.today().year)
        context["__project_slug"] = (
            context["project_name"].lower().replace("-", "_").replace(".", "_")
        )
        context["__type"] = (
            "compiled"
            if context["backend"] in ["pybind11", "skbuild", "mesonpy", "maturin"]
            else "pure"
        )
        context["__answers"] = context["_copier_conf"]["answers_file"]
        context["__ci"] = "github" if "github.com" in context["url"] else "gitlab"
        return {"cookiecutter": context}
