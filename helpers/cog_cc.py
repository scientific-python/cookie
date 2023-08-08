from __future__ import annotations

import dataclasses
import json
from pathlib import Path


@dataclasses.dataclass
class Choice:
    name: str
    description: str = ""


@dataclasses.dataclass(frozen=True)
class Option:
    name: str
    default: str
    prompt: str
    type: str
    choices: list[Choice]

    def yaml(self) -> str:
        result = [f"{self.name}:"]
        if self.type:
            result.append(f"  type: {self.type}")
        result.append(f"  help: {self.prompt}")
        if self.choices:
            result.append("  choices:")
            for choice in self.choices:
                result.append(
                    f'    "{choice.description}": {choice.name}'
                    if choice.description
                    else f"    - {choice.name}"
                )
        return "\n".join(result)


class CC:
    def __init__(self, filename: str):
        with Path(filename).open(encoding="utf-8") as f:
            data = json.load(f)

        for name, value in data.items():
            if name.startswith("_"):
                continue
            prompts = data.get("__prompts__", {}).get(name, name)
            if isinstance(prompts, dict):
                prompt = prompts.pop("__prompt__")
                choices = [Choice(k, v) for k, v in prompts.items()]
                # Hack to enable " thing - thing" alignment:
                for choice in choices[9:]:
                    choice.description = choice.description.replace(" - ", "  - ")

            elif isinstance(value, list):
                prompt = prompts
                choices = [Choice(v) for v in value]
            else:
                prompt = prompts
                choices = []

            setattr(
                self,
                name,
                Option(
                    name,
                    value,
                    prompt,
                    "str"
                    if isinstance(value, str)
                    else "bool"
                    if isinstance(value, bool)
                    else "",
                    choices=choices,
                ),
            )
