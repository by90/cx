---
name: cx-design
description: Use for object-oriented design, responsibility splitting, domain object modeling, interface boundaries, collaboration relationships, lifecycles, invariants, data-access layering, and pre-implementation design review; use when the user asks for design, architecture, class splitting, naming, domain models, database-access boundaries, or review finds mixed responsibilities.
version: 0.1.0
---

# cx Object-Oriented Design

## Language Rules

- Use the package language for conversations, explanations, plans, summaries, review decisions, verification evidence, and cx documents.
- Explain unavoidable non-English source terms in English.

## Purpose

Use this skill for object-oriented design before implementation and design review after implementation. It must identify business concepts, responsibility boundaries, object collaborations, lifecycles, and reasons to change before coding or refactoring.

This skill is not a pattern catalog. It prevents database access, domain rules, field enums, collection management, infrastructure, test-only conveniences, and future-extension entrypoints from being mixed into one class.

## Foundations

- The single responsibility principle says a module should have one reason to change.
- Responsibility-driven design starts with object roles, responsibilities, and collaborations before class internals.
- The anemic domain model anti-pattern warns that objects with data but no domain behavior pay domain-model costs without gaining object-oriented benefits.

## Triggers

Use this skill when any of the following is true:

1. The user asks for design, architecture, object-oriented design, responsibility splitting, domain objects, class naming, file splitting, or data-access boundaries.
2. One class or file handles database connection, queries, domain rules, field definitions, collection lifecycle, infrastructure algorithms, test-only conveniences, or legacy compatibility.
3. Review finds a class is too long, has too many methods, passes too many variables, performs too many validations, exposes indirect interfaces, is only a data wrapper, or cannot state its responsibility in one sentence.
4. The work adds or changes shared infrastructure, domain collections, field enums, database gateways, repository objects, domain services, or data containers.
5. The work must decide whether a feature belongs in inheritance, composition, a standalone class, a common package, or a domain package.

## Design Steps

1. Extract business nouns from the user goal and existing cx documents before looking at technical flow, test convenience, or old file names.
2. Classify candidate objects as domain entities, domain collections, value objects, field enums, database gateways, domain services, base data structures, or external adapters.
3. For each candidate object, write one responsibility sentence: what data it owns, what invariant it maintains, what behavior it provides, and what business change makes it change.
4. Write what each object does not own; this boundary is as important as the responsibility.
5. Write collaboration relationships: who creates whom, who holds whom, who calls whom, who receives dependencies, and who must close or release resources.
6. Check reasons to change. Split a class when two independent requirement families would change it.
7. Check information ownership. Put behavior on the object that best knows the required data and rules.
8. Check data-access boundaries. Database connection, command execution, and resource cleanup belong to the database gateway; domain objects must not scatter low-level connection use.
9. Check domain behavior. Domain rules, calculations, and invariants belong to domain objects or domain services; the database gateway must not carry domain rules.
10. Check infrastructure boundaries. Reusable containers, indexes, slicing, and performance semantics belong to common packages; domain readers may inherit or compose them but must not duplicate them.
11. Decide files, classes, constructors, methods, and tests only after the design conclusion is clear.

## Design Artifact

Record this table in `00.design.md` or the current task document. Do not code before the design conclusion is clear.

```text
Object or file:
Object category:
One-sentence responsibility:
Owned data:
Maintained invariants:
Provided behavior:
Does not own:
Collaborators:
Lifecycle:
Reason to change:
Verification:
```

## Candidate Object Categories

- Domain entity: one stable business object with its own business attributes, invariants, and behavior close to its data.
- Domain collection: a set of domain entities plus market, account, user, order, or similar whole-system parameters; it owns ordering, indexing, lookup, lifecycle, and rules that belong to the collection.
- Value object: a value compared by value, such as a date, interval, ratio, status, or composite key.
- Field enum: stable field ordinals, field meaning, and array-column access constraints only; it does not read, calculate, or connect to the database.
- Database gateway: connection, query execution, transactions, resource cleanup, and natural database error surfacing only; it does not perform domain decisions.
- Domain service: use only when behavior naturally crosses several domain objects and no single information expert exists; it coordinates objects and must not become a procedural function dump.
- Base data structure: generic storage, indexing, slicing, and performance semantics only; it does not know concrete business fields or business rules.
- External adapter: converts external systems, files, interfaces, or devices into inputs that project objects understand.

## Hard Gates

1. Every class must have one English responsibility sentence. If that sentence is unclear, do not code.
2. Every class must list what it does not own. If it cannot, the boundary is not formed.
3. Class names must come from stable business concepts or common infrastructure concepts, not temporary process names.
4. Field enums, domain collections, domain entities, database gateways, and readers are split by default; merge only when their responsibilities and reasons to change are identical.
5. Database paths, connections, command execution, and resource cleanup stay inside database gateways or repository boundaries.
6. Domain objects must not access structured fields through string field names; use explicit enums when stable column ordinals are needed.
7. Performance paths must not add bulk prechecks, fallback conversions, compatibility entrypoints, or silent filtering to look complete.
8. Defaults belong in function signatures; function bodies must not stack large `None` branches or duplicate parameter names to express defaults.
9. Old entrypoints, aliases, adapters, and compatibility branches are deleted during development unless the current user explicitly requires them.
10. If a behavior can be expressed with a few fields, direct object collaboration, and one clear constructor, do not turn it into hundreds of template lines.

## Red Flags

Pause coding and return to responsibility splitting when any of these appear:

1. A reader class also stores market parameters, field enums, database connections, index containers, and business rules.
2. A field enum is hidden inside a reader, forcing callers to depend on the reader to access field ordinals.
3. A domain collection and a single domain object live in one file while having different reasons to change.
4. Database connections are scattered across domain classes, or every class builds its own connection logic.
5. Service classes contain all business calculations while domain objects become property bags.
6. Code adds clone, rebuild, legacy alias, negative-index support, debug entrypoints, batch fallbacks, or test-only public methods for hypothetical future use.
7. Tests add non-business entrypoints instead of using the real functional entrypoint.
8. Comments explain indirect implementation rather than business meaning.

## Review Checklist

Ask these questions after design or code is produced:

1. What is this class's only reason to change?
2. Does this class hold data it should not know?
3. Is this behavior on the object that knows the data and rules best?
4. Is this object just a data bag; if yes, is it explicitly boundary data or infrastructure data?
5. Is database access centralized in a database gateway or repository boundary?
6. Do field ordinals, business meaning, reading logic, and collection lifecycle each have clear ownership?
7. Are there extra methods, parameters, variables, validation, or future-extension entrypoints added for completeness?
8. Does the implementation complete the main success scenario through the shortest real call path?
9. Does verification cover the real functional entrypoint instead of an internal detour?
10. Do design docs, task docs, code files, and usage docs describe the same object boundaries?

## Collaboration With Other Skills

1. When use cases, tasks, or changes exist, use `$cx-story` to locate and update cx documents before this skill performs responsibility design.
2. For shared capabilities, reusable infrastructure, or shared interfaces, use `$cx-common-module` after this skill clarifies object boundaries.
3. When the user explicitly asks for unit tests or TDD, use `$cx-tdd` or the relevant specialist testing skill after this skill forms the design conclusion.
4. After any code, design, documentation, or process deliverable is produced, use `$cx-review`; before handoff, use `$cx-evidence` according to project rules.

## Output

After using this skill, the final answer must include:

1. The main design problem found.
2. The resulting objects and responsibilities.
3. Explicit non-goals.
4. Files to change and order.
5. Verification and review result.
