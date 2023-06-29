---
layout: page
title: Process recommendations
permalink: /principles/process/
nav_order: 1
parent: Principles
---

{% include toc.html %}

# Process recommendations

## Collaborate

Software developed by several people is preferable to software developed by one.
By adopting the conventions and tooling used by many other scientific software
projects, you are well on your way to making it easy for others to contribute.
Familiarity works in both directions: it will be easier for others to understand
and contribute to your project, and it will be easier for you to use other
popular open-source scientific software projects and modify them to your
purposes.

Talking through a design and the assumptions in it helps to clarify your
thinking.

Collaboration takes trust. It is OK to be "wrong"; it is part of the process of
making things better.

Having more than one person understanding every part of the code prevents
systematic risks for the project and keeps you from being tied to that code.

If you can bring together contributors with diverse scientific backgrounds, it
becomes easier to identify functionality that should be generalized for reuse by
different fields.

## Don't be afraid to refactor

No code is ever right the first (or second) time.

Refactoring the code once you understand the problem and the design trade-offs
more fully helps keep the code maintainable. Version control, tests, and linting
are your safety net, empowering you to make changes with confidence.

## Prefer "wide" over "deep"

It should be possible to reuse pieces of software in a way not anticipated by
the original author. That is, branching out from the initial use case should
enable unplanned functionality without a massive increase in complexity.

When building new things, work your way down to the lowest level, understand
that level, and then build back up. Try to imagine what else you would want to
do with the capability you are implementing for other research groups, for
related scientific applications, and next year.

Take the time to understand how things need to work at the bottom. It is better
to slowly deploy a robust extensible solution than to quickly deploy a brittle
narrow solution.
