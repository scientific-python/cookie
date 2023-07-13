---
layout: page
title: Design recommendations
permalink: /principles/design/
nav_order: 2
parent: Principles
---

{% include toc.html %}

# Design recommendations

## Keep I/O separate

One of the biggest impediments to reuse of scientific code is when I/O
code---assuming certain file locations, names, formats, or layouts---is
interspersed with scientific logic.

I/O-related functions should _only_ perform I/O. For example, they should take
in a filepath and return a numpy array, or a dictionary of arrays and metadata.
The valuable scientific logic should be encoded in functions that take in
standard data types and return standard data types. This makes them easier to
test, maintain when data formats change, or reuse for unforeseen applications.

## Duck typing is a good idea

[Duck typing][] treats objects based on what they can _do_, not based on what
type they _are_. "If it walks like a duck and it quacks like a duck, then it
must be a duck."

Python in general and scientific Python in particular leverage _interfaces_
(also known as Protocols) to support interoperability and reuse. For example, it
is possible to pass a pandas DataFrame to the `numpy.sum` function even though
pandas was created long after `numpy.sum`. This is because `numpy.sum` avoids
assuming it will be passed specific data types; it accepts any object that
provides the right methods (interfaces). Where possible, avoid `isinstance`
checks in your code, and try to make your functions work on the broadest
possible range of input types.

## Consider: can this just be a function?

Not everything needs to be object-oriented. Object-oriented design needs to
follow the same principles as other code, like modularity, and be well tested.
If you can get away with writing functions processing existing datatypes like a
DataFrame, do so.

{: .highlight }

> It is better to have 100 functions operate on one data structure than 10
> functions on 10 data structures.
>
> -- From ACM's SIGPLAN publication, (September, 1982), Article "Epigrams in
> Programming", by Alan J. Perlis of Yale University.

A popular talk, ["Stop Writing Classes"][], illustrates how some situations that
_seem_ to lend themselves to object-oriented programming are much more simply
handled using functions. The biggest danger of reaching for OO design when it's
not needed is the following: changing states.

## Avoid changing state

It is often tempting to invent a custom class to express a workflow, along these
lines.

```py
data = Data()
data.load_data()
data.prepare()
data.do_calculations()
data.plot()
```

That’s easy and simple. **Unless you forget a step.** Oh, yeah, and static
analysis tools can't tell you if you forget a step, the API doesn't statically
"know" that `.prepare()` is required, for example. Tab completion tells you that
`.plot()` is valid immediately. The underlying problem is that `Data` has a
implicit changing state, and not all operations are valid in all possible
states.

One alternative replace `Data` with multiple immutable classes representing the
state at each step.

```py
empty_data = EmptyData()
loaded_data = empty_data.load_data()
prepared_data = loaded_data.prepare()
computed_data = prepared_data.do_calculations()
computed_data.plot()
```

We could avoid naming the temporaries, too:

```py
computed_data = EmptyData().load_data().prepare().do_calculations()
computed_data.plot()
```

These classes don’t have to be immutable. Maybe you can load more data to loaded
data. But they are easier to use correctly when they at least avoid a mutating
state that makes subsets of available operations (i.e. methods) invalid. Note
that tab completion in this case would show exactly the allowed set of
operations each time.

## Consider: do I really want a custom class?

Using built-in Python types (`int`, `float`, `str`) and standard scientific
Python types like NumPy array and Pandas DataFrame makes code interoperable. It
enables data to flow between different libraries smoothly, and to be extended in
unforeseen ways.

As an example, the widely-used library scikit-image initially experimented with
using an `Image` class, but ultimately decided that it was better to use plain
old NumPy arrays. All scientific Python libraries understand NumPy arrays, but
they don't understand custom classes, so it is better to pass
application-specific metadata _alongside_ a standard array than to try to
encapsulate all of that information in a new, bespoke object. (Modern NumPy uses
Protocols to make this type of use much easier).

When you want to group data together into one object for convenience, consider
dataclasses.

```py
from dataclasses import dataclass

@dataclass
class Data:
    angle: float
    temperature: float
    count: int
```

## Static typing is verbose, but makes code more readable

Code with static types has a lot of extra characters, but it provides more
_information_ to the reader; `timestamp: int` or `timestamp: float` provides
valuable information to the reader about the types that might be hard to infer
from the variable name alone, and therefore what is valid and what isn't. It
also can be verified in static typing checkers, like MyPy, so that it is more
likely to be correct than types in docstrings.

There's another benefit: if you design your code with types in mind, you'll tend
toward simpler, less dynamic designs with a clearly defined expected usage.
You'll remember (well, at least you are more likely to remember) to handle
special cases like lists vs strings or values that could also be `None`.

When using static typing, duck typing is expressed via Protocols. These should
be strongly preferred over older solutions like inheritance or ABCs if possible,
as they trade a little extra code to remove dependencies between objects.

## Permissiveness isn't always convenient

Overly permissive code can lead to very confusing bugs. If you need a flexible
user-facing interface that tries to "do the right thing" by guessing what the
users wants, separate it into two layers: a thin "friendly" layer on top of a
"cranky" layer that takes in only exactly what it needs and does the actual
work. The cranky layer should be easy to test; it should be constrained about
what it accepts and what it returns. This layered design makes it possible to
write _many_ friendly layers with different opinions and different defaults.

When it doubt, make function arguments required. Optional arguments are harder
to discover and can hide important choices that the user should know that they
are making.

Exceptions should just be raised: don't catch them and print. Exceptions are a
tool for being clear about what the code needs and letting the caller decide
what to do about it. _Application_ code (e.g. GUIs) should catch and handle
errors to avoid crashing, but _library_ code should generally raise errors
unless it is sure how the user or the caller wants to handle them.

## Write useful error messages

Be specific. Include what the wrong value was, what was wrong with it, and
perhaps how it might be fixed. For example, if the code fails to locate a file
it needs, it should say what it was looking for and where it looked.

## Write for readability

Unless you are writing a script that you plan to delete tomorrow or next week,
your code will probably be read many more times than it is written. And today's
"temporary solution" often becomes tomorrow's critical code. Therefore, optimize
for clarity over brevity, using descriptive and consistent names.

## Complexity is always conserved

Complexity is always conserved and is strictly greater than the system the code
is modeling. Attempts to hide complexity from the user frequently backfire.

For example, it is often tempting to hide certain reused keywords in a function,
shortening this:

```python
def get_image(
    filename: Path,
    normalize: bool = True,
    beginning: int = 0,
    end: int | None = None,
) -> np.ndarray:
    ...
```

into this:

```python
def get_image(filename: Path, **kwargs: Any) -> np.ndarray:
    ...
```

Although the interface appears to have been simplified through hidden keyword
arguments, now the user needs to remember what the `kwargs` are or dig through
documentation to better understand how to use them. You also lose static typing.

Because new science occurs when old ideas are reapplied or extended in
unforeseen ways, scientific code should not bury its complexity or overly
optimize for a specific use case. It should expose what complexity there is
straightforwardly.

Even better, you should consider using "keyword-only" arguments, introduced in
Python 3, which require the user to pass an argument by keyword rather than
position.

```python
def get_image(
    filename: Path,
    *,
    normalize: bool = True,
    beginning: int = 0,
    end: int | None = None
) -> np.ndarray:
    ...
```

Every argument after the `*` is keyword-only. Therefore, the usage
`get_image('thing.png', False)` will not be allowed; the caller must explicitly
type `get_image('thing.png', normalize=False)`. The latter is easier to read,
and it enables the author to insert additional parameters without breaking
backward compatibility.

Similarly, it can be tempting to write one function that performs multiple steps
and has many options instead of multiple functions that do a single step and
have few options. The advantages of "many small functions" reveal themselves in
time:

- Small functions are easier to explain and document because their behavior is
  well-scoped.
- Small functions can be tested individually, and it is easy to see which paths
  have and have not yet been tested.
- It is easier to compose a function with other functions and reuse it in an
  unanticipated way if its behavior is well-defined and tightly scoped. This is
  [the UNIX philosophy][], "Do one thing and do it well."
- The number of possible interactions between arguments goes up with the number
  of arguments, which makes the function difficult to reason about and test. In
  particular, arguments whose meaning depends on other arguments should be
  avoided.

Functions should return the same kind of thing no matter what their arguments,
particularly their optional arguments. Violating "return type stability" puts a
burden on the function's caller, which now must understand the internal details
of the function to know what type to expect for any given input. That makes the
function harder to document, test, and use. Python does not enforce return type
stability, but we should try for it anyway. If you have a function that returns
different types of things depending on its inputs, that is a sign that it should
be refactored into multiple functions.

Python is incredibly flexible. It accommodates many possible design choices. By
exercising some restraint and consistency with the scientific Python ecosystem,
Python can be used to build scientific tools that last and grow well over time.

<!-- prettier-ignore-start -->

[the UNIX philosophy]: https://en.wikipedia.org/wiki/Unix_philosophy
[Duck typing]: https://en.wikipedia.org/wiki/Duck_typing
["Stop Writing Classes"]: https://youtube.com/watch?v=o9pEzgHorH0&t=193s

<!-- prettier-ignore-end -->
