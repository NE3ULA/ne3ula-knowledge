# Identity Stack

The Identity Stack is the canonical identity framework within the E3 human
engine.

It defines how a participant's identity is structured, how that structure moves
over time, and how the system reads change without collapsing the person into a
fixed type.

## Why It Lives in `human-engine`

The Identity Stack belongs in
`WORKING_DOCS/engine/E3/human-engine/` because it describes the participant,
not the interface and not the software implementation.

Its role is to help a participant:

- distinguish authored identity from inherited patterning
- define the stable layers the system is orienting around
- interpret drift, friction, and coherence as developmental signals
- support return, refinement, and longer-term integration

WORLD provides meaning and symbolic context.
The Identity Stack provides the participant-centered structure that the human
engine uses to interpret identity.

## Relationship to Other E3 Systems

### Alchemist Pyramid

The Alchemist Pyramid provides structured transformation paths and practice
layers.

The Identity Stack provides the participant-centered identity architecture those
paths are acting upon.

The Pyramid answers: how transformation is worked.
The Identity Stack answers: what in the participant is being organized,
stabilized, and interpreted.

### Decision Engine

The Decision Engine should remain a separate layer.

The Identity Stack defines authored identity, signals, and movement.
The Decision Engine later translates that context into action heuristics,
prioritization, and execution logic.

This folder therefore establishes the identity foundations that future
decision-engine work can reference without importing decision logic here.

### AXZIO

AXZIO is the interface layer through which users may later receive identity
readings, prompts, and navigation support.

AXZIO should present and operationalize this framework, but it should not define
the framework. The engine layer comes first.

## Canonical Files

The following files in this directory are canonical:

- `README.md`
- `identity-core.md`
- `four-primitives.md`
- `identity-engine.md`
- `identity-signals.md`
- `identity-reading-model.md`

These documents are the editable source of truth for the Identity Stack inside
`WORKING_DOCS`.

## `archive_source/`

`archive_source/` is a preserved raw import subtree copied selectively from
`NOTION_ARCHIVE/` during migration.

It exists for:

- source traceability
- fidelity checking
- recovery of details not yet synthesized
- validation of canonical interpretations

It is reference-only.

Do not treat `archive_source/` as canonical.
Do not let edits accumulate there.
Update the canonical documents outside `archive_source/` when the framework is
clarified.

## Structural Intent

This folder should remain a clear identity layer within the E3 human engine:

- `identity-core.md` defines foundational identity structure
- `four-primitives.md` defines a practical stabilization and development lens
  used by AXZIO
- `identity-engine.md` defines identity movement and integration
- `identity-signals.md` defines what the system can observe or infer
- `identity-reading-model.md` defines how the system turns signals into guidance
