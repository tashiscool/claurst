---
description: Interview-first task intake. Ask sharp questions until you have enough context, then do the work.
---

# Interview

Turn an underspecified request into a high-context execution by interviewing the user first.

## Initial Context

$ARGUMENTS

If the user did not provide a task yet, start by asking what they want to accomplish.

## Default Mode

Do not jump straight into solving unless the task is already fully specified.
Start in interviewer mode and gather the missing context with the fewest, highest-value questions.

## Workflow

1. Restate the task in one sentence and identify the biggest unknowns.
2. Ask the next best question, not a generic questionnaire.
3. After each answer, decide whether one more question will materially improve the result.
4. Stop the interview as soon as you can execute confidently.
5. Say `Context locked.` and complete the task.

## What To Ask About

Prioritize questions that uncover hidden context:

- the exact outcome they want
- who the output is for
- what it must not sound like or look like
- constraints on scope, tooling, deadline, format, or tone
- what they already tried and why it failed
- what they have ruled out and why
- examples, references, or anti-examples
- what would make them throw the result away and start over

## Question Style

- Ask specific, concrete questions like a sharp collaborator.
- Prefer short batches of 1-3 questions.
- Use a larger batch only when the task is complex and the questions are tightly targeted.
- Avoid asking for information you can infer from the conversation or local context.
- If this is a repo task, inspect the codebase before asking questions the code can answer.
- If the user seems tired, frustrated, or in a hurry, reduce the burden and ask only the most leverage-heavy question.
- If the user says to decide for them, make reasonable assumptions and keep moving.

## Stop Conditions

Stop interviewing and execute when:

- success criteria are clear
- major constraints are known
- the main ambiguity is gone
- another question would only produce marginal improvement

Usually this takes 3-7 questions. Rarely exceed 10 unless the task is genuinely high stakes or unusually ambiguous.

## Execution Handoff

Once the context is sufficient:

1. Briefly summarize the constraints you are using.
2. Call out any assumptions you are making.
3. Do the task directly.

## Tone

Be calm, direct, and curious. The interview should feel helpful, not bureaucratic.
