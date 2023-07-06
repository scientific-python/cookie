from __future__ import annotations

import dataclasses
import json
from pathlib import Path


@dataclasses.dataclass(frozen=True)
class Option:
    name: str
    default: str
    prompt: str
    type: str

    def yaml(self) -> str:
        type_str = f"  type: {self.type}\n" if self.type else ""
        return f"{self.name}:\n{type_str}  help: {self.prompt}"


class CC:
    def __init__(self, filename: str):
        with Path(filename).open(encoding="utf-8") as f:
            data = json.load(f)

        for name, value in data.items():
            if name.startswith("_"):
                continue

            setattr(
                self,
                name,
                Option(
                    name,
                    value,
                    data.get("__prompts__", {}).get(name, name),
                    "str" if isinstance(value, str) else "",
                ),
            )
