---
layout: page
title: "Static type checking"
permalink: /guides/mypy/
nav_order: 9
parent: Topical Guides
---

{% include toc.html %}

# Static type checking

## Basics

The most exciting thing happening right now in Python development is static
typing. Since Python 3.0, we've had function annotations, and since 3.6,
variable annotations. In 3.5, we got a "typing" library, which provides tools to
describe types. This is what static type hints look like:

```python
def f(x: int) -> int:
    return x * 5
```

This does nothing at runtime, except store the object. If you add
`from __future__ import annotations`, it doesn't even store the actual object,
just the string you type here, so then anything that can pass the Python parser
is allowed here.

It is not useless though! For one, it helps the reader. Knowing the types
expected really gives you a much better idea of what is going on and what you
can do and can't do.

But the key goal is: static type checking! There are a collection of static type
checkers, the most "official" and famous of which is MyPy. You can think of this
as the "compiler" for compiled languages like C++; it checks to make sure you
are not lying about the types. For example, passing in anything that is not an
int to `f` will fail a mypy check, _before you run or deploy any code_.

Your tests cannot test every possible branch, every line of code. MyPy can
(though it doesn't by default, due to gradual typing). You may have code that
runs rarely, that requires remote resources, that is slow, etc. All those can be
checked by MyPy. It also keeps you (too?) truthful in your types.

### Adding types

There are three ways to add types.

1. They can be inline as annotations. Best for Python 3 code, usually.
2. They can be in special "type comments". Originally designed for Python 2
   code, and still requires the proper imports.
3. They can be in a separate file with the same name but with a `.pyi`
   extension. This is important for type stubs or for cases where you don't want
   to add imports or touch the original code. You can annotate compiled files or
   libraries you don't control this way.

If you have a library you don't control, you can add "type stubs" for it, then
give MyPy your stubs directory. MyPy will pull the types from your stubs. If you
are writing code for a Raspberry Pi, for example, you could add the stubs for
the Pi libraries, and then validate your code, without ever even installing the
Pi-only libraries!

You do not have to add types for every object - most of the time, you just need
it for parameters and returns from functions. When running MyPy, you can use
`reveal_type(...)` to show the inferred type of any object, which is like a
print statement but at type-checking time, or `reveal_locals()` to see all local
types.

### Configuration

By default, MyPy does as little as possible, so that you can add it iteratively
to a code base. By default:

- All untyped variables and return values will be `Any`.
- Code inside untyped functions is not checked _at all_.

You can add configuration to `pyproject.toml` (and a little bit to the files
themselves), or you can go all the way and pass `--strict`, which will turn on
everything. Try to turn on as much as possible, and increase it until you can
run with full `strict` checking. See the [style page][] for configuration
suggestions.

[style page]: {% link pages/guides/style.md %}

For a library to support typing, it has to a) add types using any of the three
methods, and b) add a `py.typed` empty file to indicate that it's okay to look
for types inside it. MyPy also looks in `typeshed`, which is a library full of
type hints for (mostly) the standard library.

Third party libraries that are typed sometimes forget this last step, by the
way!

## Features

### Type narrowing

One of the key features of type checking is type narrowing. The type checker
monitors the types of a variable, and "narrows" it when something restricts it.
For example:

```python
x: Union[A, B]
if isinstance(x, A):
    reveal_type(x)
else:
    reveal_type(x)
```

This will print `A`, then `B`. It prints `A` because that's the only thing that
can exist in the first branch, and then the remaining types (`B`) must be the
type in the second branch. And it prints both because it's not actually running
the code, just type checking it, so both sides of the if are checked.

You can manually force type narrowing with assert:

```python
x: Union[A, B]
assert isinstance(x, A)
reveal_type(x)
```

This will print `A` because you removed B via the type narrowing using the
`assert`.

### Protocols

One of the best features of MyPy is support for structural subtyping via
Protocols - formalized duck-typing, basically. This allows cross library
interoperability, unlike traditional inheritance. Here’s how it works:

```python
from typing import Protocol


class Duck(Protocol):
    def quack() -> str:
        ...
```

Now any object that can "quack" (and return a string) is a Duck. We can even add
`@runtime_checkable` which will allow us to check this (minus the types) at
runtime in `isinstance`. So now we can design code like this:

```python
def pester_duck(a_duck: Duck) -> None:
    print(a_duck.quack())
    print(a_duck.quack())
```

And the type checker will ensure we only write code valid on all `Duck`s. And,
we can write a duck implementation and test it like this:

```python
class MyDuck:
    def quack() -> str:
        return "quack"
```

This will pass a check for being a `Duck`, for example something like this:

```python
import typing

if typing.TYPE_CHECKING:
    _: Duck = typing.cast(MyDuck, None)
```

Notice the complete lack of dependencies here. We don’t need `MyDuck` to write
`pester_duck`, or vice-versa. And, we don't even need `Duck` to write either one
at runtime! The dependence on `Duck` for `pester_duck` is entirely a
type-check-time dependence (unless we want to use a `runtime_checkable` powered
`isinstance`).

There are lots of built-in Protocols, most of which pre-date typing and are
available in an Abstract Base Class form. Most of them check for one or more
special methods, like `Iterable`, `Iterator`, etc.

### Other features

Static typing has some great features worth checking out:

- Unions (New syntax in Python 3.10)
- Generic Types (New syntax in Python 3.9)
- Literals
- TypedDict
- Nicer NamedTuple definition (very popular in Python 3 code)
- MyPy validates with the Python version you ask for, regardless of what version
  you are actually running.

## Complete example

### Runtime compatible types

Here's the classic syntax, which you need to use if you want to access the type
annotations at runtime and you need to support Python < 3.10:

```python
from typing import Union, List


# Generic types take bracket arguments
def f(x: int) -> List[int]:
    return list(range(x))


# Unions are a list of types that all could be allowed
def g(x: Union[str, int]) -> None:
    # Type narrowing - Unions get narrowed
    if isinstance(x, str):
        print("string", x.lower())
    else:
        print("int", x)

    # Calling x.lower() is invalid here!
```

### Types as strings

If you don't access the types at runtime, or if you use Python 3.10+ only, then
you can use a much nicer syntax. The `annotations` future feature causes the
annotations to be stored as strings and not evaluated, which allows you to write
things that are not yet valid, like `list[int]`!

```python
from __future__ import annotations


def f(x: int) -> list[int]:
    return list(range(x))


def g(x: str | int) -> None:
    if isinstance(x, str):
        print("string", x.lower())
    else:
        print("int", x)
```

Notice that there are no imports from typing! Note that you cannot use the "new"
syntax in non annotation locations (like unions in `isinstance`) unless Python
supports it at runtime. And some libraries, like Typer and cattrs, use the
annotations at runtime.

You can use the above in earlier Python versions if you use strings manually,
with the same caveats.

## Tips for good types

These are some guidelines to help you in writing good type hints.

### Loose vs. specific types

When you have a function, you should take as generic a type as possible, and
return as specific a type as possible. For example:

```python
from __future__ import annotations
from collections.abc import Iterable, Mapping


# Bad!!!
def count(x: list[str]) -> Mapping[str, int]:
    result = {}
    for item in x:
        result[x] = result.get(x, 0) + 1
    return result
```

This will require the user pass a list to use this function, when in fact any
iterable of strings would work just fine. Then, using valid dictionary
operations on the return value, like mutating operations, will be marked as
invalid, since your type checker don't know you have an actual dict. Compare
with this:

```python
# Good
def count(x: Iterable[str]) -> dict[str, int]:
    result = {}
    for item in x:
        result[x] = result.get(x, 0) + 1
    return result
```

Now all iterables are accepted, and the type checkers knows you have an actual
dict in the return. Usually functions should take `Iterable` (if the argument is
iterated once) or `Sequence` (if it is iterated multiple times or used with
`in`), or `Mapping`, or `Set`. Very rarely you might need `MutableMapping` or
`MutableSet`, and if you really do, having it in the type helps a reader know
that it's going to be mutated.

If you have an output type that depends on an input type, try to pass that
through, usually using TypeVar (or the new generic syntax in Python 3.12, but
that's not available for older Pythons via an import).

Also note that the best place to get these in modern Python is
`collections.abc`, but if you need to subscript them at runtime, you'll need
Python 3.9+ or the versions in `typing`.

## Final words

When run alongside a good linter like flake8, this can catch a huge number of
issues before tests or they are discovered in the wild! It also prompts _better
design_, because you are thinking about how types work and interact. It's also
more readable, since if I give you code like this:

```python
def compute(timestamp):
    ...
```

You don't know "what" timestamp is. Is it an int? A float? An object? With
types, you'll know what I was intending to give you. You can use type aliases to
really give expressive names here!
