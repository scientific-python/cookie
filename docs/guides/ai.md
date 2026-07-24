---
short_title: AI
---

# Agentic AI

Around November of 2025, agentic AI exploded in usefulness, and has changed how
a lot of software is written, reviewed, and maintained. "Agentic" AI is more
than a chatbot; it has access to "tool calls", which can read and write files,
and most importantly it runs in a loop so it can verify that code passes
checks. This is closer to how a human codes; we run code and verify outputs,
we do not write working code from scratch without running it.

It helps to separate two very different things that often get lumped together
as "Agentic AI":

- A developer driving an interactive AI harness with a capable model, reading
  the output, and taking responsibility for the result. This is a power tool,
  much like an editor or a linter.
- Low-cost models running unattended in automated systems that mass-produce
  pull requests. This is what most people mean by "AI slop", and it is the
  source of most of the frustration maintainers feel about AI contributions.

The recommendations below are aimed at the first case, and at keeping your
project from being overwhelmed by the second.

:::{attention} The developer using the tool
:class: dropdown
The first point does hide something: the tool depends on the developer guiding
it (just like any other tool). You will also see users with very little coding
experience using these tools to produce low quality contributions. How someone
learns to code in this new era is still something unsolved.

If you maintain a project: Try to engage with the human. If they are willing to
interact (and not just type "address the review" into their harness), treat
them like a human, even if you also see the AI working on their behalf. They
also may use AI to address a language barrier, or accommodate a disability.
:::

## Disclosure and transparency

We recommend **full disclosure**. Knowing what model was used lets a reviewer
run a model from a different model family to help them review the contribution.
A maintainer has a better idea of what to expect based on the model used. And
it's generally more respectful to not keep your process hidden when
contributing to open source - maybe the maintainer would like to try that model
too. If you heavily edit the model output, then use your discretion; but being
open about the whole process is generally better!

**Always follow the policy of the project you are contributing to.** The
following are general guidelines, but follow project policies if they exist.

**Credit AI in commits.** Follow the convention used by the Linux kernel and
add a trailer. Never allow the model to add itself as a co-author. The code is
still yours (and your responsibility); the AI is a tool, not an author or
copyright holder, which is what co-authored-by is for. An AI must never add a
`Signed-off-by:` line, because certifying the DCO is a legal act only a human
can perform.

:::{note} The Linux kernel trailer

The Linux kernel trailer, part of the kernel's official
[coding assistants documentation][kernel-ai], looks like this:

```text
Assisted-by: <harness>:<model>
```

You can usually customize your harness to include this, either in an agents
file (below), or via specific settings.

:::

:::{warning} Not a universal standard
:class: dropdown
Note that the trailer is not universal. Kubernetes, for example, forbids AI
trailers and wants disclosure in the PR description instead. Some projects do
not want to know when AI was used so they can't be singled out later.
:::

**Write your own PR descriptions.** Generated PR summaries tend to be verbose,
impersonal, and a chore to read. Write the description yourself. If a PR or
comment does contain AI-generated prose, mark it clearly, for example with a
short disclaimer line at the top; you can still write a human written message
above that disclaimer.

**Keep human review human-to-human.** Maintainers should never have to argue
with a bot. Don't make a reviewer talk to an AI without knowing it; if an AI is
responding on your behalf, say so (e.g. with an AI disclaimer at top). Don't
belittle a reviewer's time by not responding personally.

**Don't submit slop.** Don't open a PR that a maintainer could finish faster
than they can review it, and don't mass-file unsolicited PRs. Reviewing an
AI-generated PR can take far longer than writing it did. If the change is
trivial with AI, the maintainers probably could just trigger the AI themselves.
Make sure the pull request is welcome: check issues, ask first, etc.

**Don't use AI on "good first issues".** These exist to teach new contributors,
not to be a button an AI presses -- a maintainer could do that. LLVM and
Mozilla explicitly forbid it, and other projects are dropping the label
entirely. (And yes, a human wrote the preceding em-dash!)

## `AI_POLICY.md`

A growing convention is to add an [`AI_POLICY.md`][ai-pr-policy] to your
repository so contributors know what is expected of AI-assisted work. There is
no single right answer; pick the stance that matches your project's tolerance
and capacity. The tabs below sketch three levels you can adapt.

::::{tab-set}
:::{tab-item} All in

AI-assisted contributions are welcome on the same footing as any other, as long
as they meet the project's quality bar and are disclosed.

````markdown
# AI Policy

AI-assisted contributions are welcome. We ask that you:

- Disclose that AI was used and name the tool/model.
- Review and understand every line you submit; you are responsible for it.
- Meet the same quality, testing, and style standards as any contribution.
- Fully autonomous agents may not open issues or PRs.
- Respond to reviewers yourself.
- AI text in descriptions and issues should be clearly marked.

This applies to issues and comments as well as pull requests. Using AI for
translation or grammar help is fine. Contributions that ignore this policy may
be closed.

Only humans can be named as co-authors, and AI can _never_ sign off on comment.
The Linux kernel trailer can be used to credit AI assistance, like this:

```text
Assisted-by: <harness>:<model>
```
````

:::
:::{tab-item} Moderate

AI assistance is fine, but the burden is on the contributor to show real human
involvement and prior buy-in before opening a PR. This mirrors the
[original proposal][ai-pr-policy].

````markdown
# AI Policy

AI-assisted contributions are accepted only if:

- The PR follows the same rules as a non-AI PR.
- It clearly states that it is AI-assisted and names the tool used.
- It links to an issue or discussion where a maintainer agreed to the
  proposed change beforehand.
- AI-generated descriptions/comments are clearly marked and only used when
  required.
- A human drove the tool, reviewed every line, and can explain the change.
- Fully autonomous agents may not open issues or PRs.
- You respond to review comments yourself.

This applies to issues and comments as well as pull requests. Using AI for
translation or grammar help is fine. AI output may infringe copyright; it is
your responsibility to make sure it does not.

Unsolicited, undisclosed, or low-effort AI PRs will be closed.

Only humans can be named as co-authors, and AI can _never_ sign off on a
comment. The Linux kernel trailer should be used to credit AI assistance, like
this:

```text
Assisted-by: <harness>:<model>
```
````

:::
:::{tab-item} Minimal

AI-generated PRs are discouraged or restricted. Use this if you have limited
review capacity.

````markdown
# AI Policy

We do not accept unsolicited AI-generated pull requests. Please open an issue
to discuss before contributing. Fully-reviewed, disclosed AI-assisted fixes may
be considered case by case. PRs suspected to be entirely AI-generated may be
closed without explanation.

This applies to issues, comments, and security reports as well as pull
requests. Autonomous agents may not contribute. Using AI for translation or
grammar help is fine. AI output may infringe copyright; it is your
responsibility to make sure it does not. Repeat violations may lead to a ban.

Only humans can be named as co-authors. The Linux kernel trailer must be used to
credit AI assistance, like this:

```text
Assisted-by: <harness>:<model>
```
````

:::
::::

:::{seealso} Other examples
:class: dropdown

For real examples, see the policies from [PyTorch][pytorch-ai],
[NumPy][numpy-ai], [Ghostty][ghostty-ai], and [LLVM][llvm-ai], whose "golden
rule" (shared with curl) sums the whole topic up: "a contribution should be
worth more to the project than the time it takes to review it." A
[community-maintained list][ai-policy-list] tracks policies across well over a
hundred projects.

Some angles to consider if they matter to your project: AI in security reports
([curl][curl-ai] requires disclosure and human verification after a flood of
fabricated reports), AI on the reviewer side ([Fedora][fedora-ai] lets
reviewers use AI to assist, but not to make the accept/reject decision), and
per-contributor caps on open AI-assisted PRs (Homebrew allows one at a time), a
simple guard against mass-produced PRs.

:::

## `AGENTS.md`

Harnesses read a project context file to learn how your repository works --
preferred command runners, architecture notes, conventions, and gotchas. A good
context file makes the AI far more effective without bloating every prompt. The
cross-tool standard is [`AGENTS.md`][agents-md]; most harnesses can generate a
first draft for you (often via an `/init` command).

Keep it focused on what is *not* obvious from the code: how to run the tests,
which tools to prefer, where generated files live, and any traps. Treat it as
documentation you maintain, not a dumping ground.

:::{note} Claude Code and `AGENTS.md`
:class: dropdown

Claude Code is the only major harness to *not* read `AGENTS.md`. You can support
both with a symlink, keeping a single source of truth:

```bash
ln -s AGENTS.md CLAUDE.md
```

You can also mention `@AGENTS.md` inside `CLAUDE.md` if you want to add
specific instructions; this is true for most other harnesses too
(`copilot-instructions.md`, etc).

:::

How you track the file is a separate decision:

::::{tab-set}
:::{tab-item} Commit it

Commit `AGENTS.md` so every contributor (and their harness) shares the same
project context, and you can enforce project conventions this way. This is a
good default for projects with at least one maintainer also using AI harnesses.
(Ignoring `CLAUDE.md` and `.claude/` in your `.gitignore` is also a good idea,
due to that not supporting standards and being fairly common.)

:::
:::{tab-item} Ignore it

Add `AGENTS.md` to your `.gitignore` if you'd rather each contributor maintain
their own. The ignore entry signals that the file is expected but personal.

:::
:::{tab-item} Leave it out

Don't reference it at all. Contributors who want a personal context file can
keep it out of version control locally by adding it to `.git/info/exclude`,
which (unlike `.gitignore`) is never shared. Some projects don't want to mention
AI at all, even in a `.gitignore`.

:::
::::

## User-level configuration

Beyond per-project context, most harnesses support a user-level config that
applies everywhere (for example `~/.claude/CLAUDE.md` or
`~/.config/opencode/AGENTS.md`). This is the place for your personal,
cross-project preferences, such as:

- Your environment (System setup, GitHub username).
- Tool preferences, e.g. "use `uv run` in Python projects".
- Your commit and PR conventions, including the disclosure trailers above.
- If you use local or small models, you can request relative paths be used
  (easier for them to write).

::::{dropdown} Example user-level file

```markdown
You are on macOS, but have GNU sed. `python3` can be used if python without
dependencies is needed. Use `uv run` if in a python package.

Use `prek -a --quiet` instead of `pre-commit run -a` for linting.

If you make a commit, follow conventional commits and add a trailer:
`Assisted-by: <harness>:<model>`, where `<harness>` is the current agent
harness, and `<model>` is the AI model.

Prefix PR descriptions and comments on PRs with the line ":robot: _AI text
below_ :robot:" to indicate you are an agent speaking on a user's behalf.
```

::::

Claude also allows a per-project `CLAUDE.local.md`; that should never be
committed, so put it in your global gitignore if you use it.

## Skills

Skills are reusable, named sets of instructions for repetitive workflows that
you can invoke on demand: dropping a Python version, checking trusted
publishing, applying a project's changelog style, and so on. They follow a
shared [skills standard][agentskills], so a skill you write can work across
multiple tools. See [skills.sh][] for a catalog and more background.

If you find yourself giving the AI the same multi-step instructions repeatedly,
that's a good candidate for a skill. AI can help you write skills. You can store
skills (like changelog skills) in a repository at `.agents/skills`, or for your
user at `~/.agents/skills`. The `gh skills` command can help you manage them.

:::{note} Claude Skills
:class: dropdown
Yes, you probably guessed by now, Claude Code does not respect the standard
location. You have to symlink `.agents/skills` to `.claude/skills`, of course.
:::

## A few harness features worth knowing

The details vary by tool, but most modern harnesses share a common vocabulary:

- **Slash commands** for built-in actions (e.g. initialize context, plan, or
  review). `/init`, `/review`, `/diff`, `/skills`, `/compact`, etc.
- **`@`-mentions** to pull specific files into context.
- **Planning mode**, where the AI proposes an approach and asks clarifying
  questions before editing. Valuable for anything non-trivial.
- **Subagents**, which run a sub-task in their own context and report back a
  summary, useful for research and parallel work, and keeping your context
  managed.
- **Model tiers**, letting you match a cheap, fast model to simple tasks and a
  frontier model to hard ones. Use good models at first, then you'll learn what
  is easy and hard for an AI, and can match better.

As you'll learn, effective use of AI is mostly context management. If the AI
makes bad decisions, it's probably missing context: load design documents,
issues, conversations, and files (forcibly with `@` if needed) before starting,
and use planning mode to have it ask you questions. If it becomes forgetful
mid-task, the context is too full: use `/compact` liberally, and don't let
verbose output fill the context with junk.

## Common concerns

- **Don't try one-shot.** Watch what the AI is doing and steer it.
  Planning mode and a quick read of the diff catch most problems early. It's
  fine to iterate, you aren't trying to make an AI commercial!
- **Verify, don't trust.** Models hallucinate; confirm invented explanations
  and APIs. Make sure the model validated with testing, ask it to if it doesn't
  first try. Reviewing with a *different* model family can catch issues a model
  won't flag in its own work.
- **You own the result.** AI proposes; you decide. It does not know your
  project's best practices unless you tell it, and it can't judge what is
  "best".
- **Mind security.** Code sent to a hosted model leaves your machine; avoid
  sending confidential code to providers you don't trust, and never grant an
  agent destructive access (for example, to production data). AI tools are
  themselves a supply-chain target; see the [security guide][security] for
  dependency pinning, cooldowns, and CI hardening.
- **Beware untrusted content.** Anything an agent reads can carry instructions:
  issue text, PR comments, a fetched web page, CI logs. A model might confuse
  instructions from a payload buried in the content it was asked to
  process - even in hidden comments. When you point an agent at outside
  material (e.g. "triage these issues" or a CI run URL), review what it does
  rather than letting it act unattended, and don't combine untrusted input with
  destructive or credentialed access. This is unfortunately a big issue with
  setting up an automated issue processing system.

## What AI is good at

AI is fantastic at anything that has a clear pass/fail condition. This means
it's great at fixing up a failing PR, addressing linter failures, polishing off
anything that's failing tests into making it pass tests. That's why good tests
and strong linters and type checking are so helpful to AI, they give it a
better pass/fail to work with. Do keep an eye on it, though, sometimes it will
skip something instead of fixing it; sometimes that's correct, but decision
making is not as strong of an AI skill as pass/fail checks!

AI knows a massive library of tricks and details. It will hallucinate ones
sometimes, of course (that's why the pass/fail is important above!). Make it
validate anything (newer models often have this in the system prompts, so it is
model and harness dependent - for example, Claude Opus 4.8+ acts paranoid
and validates without request).

AI doesn't mind long or annoying tasks - iterating with a CI that takes minutes
or hours, running things through Docker, figuring out how to build projects,
etc. You'll realize that things you know are good ideas, but you were too time
constrained to try before are perfect candidates for AI. Want to find the 20
most important downstream projects and test them all before and after some
change you made? AI is happy to do it!

As new models are coming that are better than humans at finding and exploiting
vulnerabilities, we need to be running those models on our code to find and fix
bugs before they can be exploited.

## What should you try?

Regardless of what AI companies tell you, one of the hardest things to do with
a model is write new code. Especially from scratch (it will mimic the current
style). That's also something that tends to be fairly enjoyable: Don't make AI
do stuff you'd rather do yourself! Start by using the AI to do the stuff you
*don't* like. Then start having it do things you wouldn't do because you don't
have time to do it. Here are some suggestions for prompts to try:

:::{note} Disclaimer
These suggestions are for *your* projects. Never do this to someone else
without them asking for it!
:::

- "Review this project for bugs, performance, simplifications, and
  modernizations" - you might be shocked at how much it can find!
  - Make sure you use a good model, and have it validate the findings (some
    do not need extra prompting to do this).
  - Followup: Put this into an issue, then open up draft PRs for these.
    Group several into one PR when it makes sense. The PRs should reference
    the issue.
- "Categorize all open issues. Highlight issues that can be easily closed,
  and issues that are bugs that you can reproduce."
  - Followup: "Launch subagents to fix all the reproduced bugs in worktrees,
    and open a PR for each"

For an existing PR:

- "You are an adversarial reviewer for the new feature in this branch. Do you
  see any problems? Anything that could be done or written more cleanly? Can
  you break it?"
  - With a good model, this is really powerful.

Smaller ideas

- "Explain the structure and design of this project."
- "What's new since last release? Changelog style."
- "Review the documentation for this project. Look for typos and gaps in
  coverage."
- "Rebase this PR"
- "Review PR #123" (most harnesses provide a `/review` command too).
- Give it the URL to a flaky CI run and ask it to investigate it.
- Ask it to revive an old outdated PR based on the current codebase.
- Write something then ask it to apply what you did to something else similar.
- Point it at a bug report and ask it to reproduce it as a failing test, then
  fix it.
- "Bisect this regression" - finding the commit that broke something is a
  tedious mechanical loop AI is happy to run.
- "Add tests for the change I just made" - good tests and coverage give it a
  clear pass/fail to work against.
- "Add type annotations here until the type checker passes."
- Ask it to draft release notes or a changelog from the git log between two
  tags. It will try to mimic the existing style if there is one.

## Tips

If you want to see your usage across harnesses, Wes McKinney (of Pandas fame)
has [AgentsView][], which reads local files from most harnesses and summarizes
for you. Try `uvx agentsview usage daily`, for example. A similar tool is
`npx ccusage`, which despite the name supports multiple harnesses too.

If you use Claude Code, `npx ccstatusline` is much better than having the AI
try to write its own status line.

A very powerful technique is "rubber duck", where you develop code with one
model, then review it with a different model, feeding the review back into the
original model, and iterate. This can provide a significantly better result
than either model on its own, moving up
[about 74% to the next model class in some tests][rubberduck]. You don't need a
specialized mode (copilot has one), you can do this yourself if you have access
to two model families.

Don't just do what you'd do with AI; have it do what you wouldn't do. If you
are developing a feature, ask AI to take several projects that use yours and
adapt them to your new feature. Take a PR where someone started using your
library and ask for all the pain points they faced transitioning to it. Have AI
try to find a way to break your feature or library. Look for gaps in your docs.
Have it follow your tutorial and tell you what was missing. It is happy to use
Docker or start up a database or other tools that you might not have time to
set up for a small problem.

You can mix it in at your pace. If you are writing, try adding `TODO` comments
for things like adding links, then ask AI to find them and fix them. With
[marimo pair][], you can work on a notebook or slides but have AI connected and
able to help you edit anything you ask for, like splitting a slide into
columns, adding a summary slide, or analyzing a SQLite database and adding a
plot.

If there's something repetitive, use AI to write a script to do it; it will use
fewer tokens and be more reliable than having AI do the repetitive thing
directly.

[ai-policy-list]: https://github.com/melissawm/open-source-ai-contribution-policies
[ai-pr-policy]: https://willmcgugan.github.io/ai-pr-policy/
[agents-md]: https://agents.md
[curl-ai]: https://curl.se/dev/contribute.html#on-ai-use-in-curl
[fedora-ai]: https://docs.fedoraproject.org/en-US/council/policy/ai-policy/
[ghostty-ai]: https://github.com/ghostty-org/ghostty/blob/main/AI_POLICY.md
[kernel-ai]: https://docs.kernel.org/process/coding-assistants.html
[llvm-ai]: https://llvm.org/docs/AIToolPolicy.html
[numpy-ai]: https://numpy.org/devdocs/dev/ai_policy.html
[pytorch-ai]: https://github.com/pytorch/pytorch/blob/main/AI_POLICY.md
[agentskills]: https://agentskills.io
[agentsview]: https://www.agentsview.io
[marimo pair]: https://docs.marimo.io/guides/generate_with_ai/marimo_pair/
[rubberduck]: https://github.blog/ai-and-ml/github-copilot/github-copilot-cli-combines-model-families-for-a-second-opinion/
[skills.sh]: https://www.skills.sh
[security]: /guides/security.md
