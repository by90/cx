---
name: cx-ui
description: Use for desktop, web, or mobile UI architecture, implementation, and refactoring. When work involves pages, components, ViewModels, presentation state, events, navigation, or a giant UI file, enforce one-way View, ViewModel, Service, Data layering and one file per page, component, and ViewModel.
version: 0.1.0
---

# cx UI Layering

## Purpose

Organize interface code through explicit View, ViewModel, Service, and Data boundaries so rendering, presentation state, use-case orchestration, database access, network operations, and tests cannot accumulate in one file. The boundary applies to GPUI, web, mobile, and other UI frameworks.

## Required Dependency Direction

```text
View -> ViewModel -> Service -> Data
```

- A View composes pages and components and sends user intent to a ViewModel.
- A ViewModel calls Services and converts domain results into presentation state.
- A Service calls Data and orchestrates one explicit use case.
- Data reads and writes databases, files, networks, or external systems.
- Reverse, cross-layer, and cyclic dependencies are forbidden. A View never accesses Service or Data directly; a ViewModel never accesses databases, networks, files, or UI framework elements directly; Service and Data never depend on pages, components, or presentation state.

## File Layout Gates

- Each navigable page lives in one separate page file, and a page file defines only that page plus tightly private layout helpers.
- Each reusable or independently renderable component lives in one separate component file. Do not accumulate component implementations in page files, the application shell, or a unified `ui.rs`.
- Each page or independent component ViewModel lives in its own file, separate from View, Service, and Data.
- Split Service files by use-case responsibility and Data files by data source or repository responsibility. Split again whenever a file has two independent reasons to change.
- `mod.rs`, index files, and application composition entrypoints declare modules, export public entries, wire dependencies, and choose the initial page only. They contain no page body, component rendering, business rules, queries, or persistence.
- The relevant language test skill owns test layout; production UI files never contain test code.

Adapt this layout to the project language:

```text
src/
  ui/
    app.rs
    pages/
      quote_page.rs
    components/
      task_progress.rs
  view_model/
    quote_page_view_model.rs
  service/
    quote_update_service.rs
  data/
    quote_repository.rs
```

## Layer Responsibilities

### View

- Own layout, style, rendering, navigation declarations, event binding, and forwarding user intent to a ViewModel.
- Do not own business decisions, queries, persistence, protocol parsing, task orchestration, retry policy, or cross-page shared state.
- A page file is not a component repository. Extract repeated or independently rendered units immediately.

### ViewModel

- Own presentation, selection, loading, and display-error state, plus display data derived from domain results.
- Convert clicks, input, and switches into explicit commands, call a Service, and apply results to presentation state.
- Do not construct UI framework elements, manipulate widget trees, open databases, files, sockets, or network connections, or implement low-level business algorithms.

### Service

- Orchestrate the domain objects and Data interfaces for one use case, including business actions, task lifecycle, and cross-source collaboration.
- Do not hold controls, colors, layout, page copy, or framework contexts, and never return UI elements.
- A Service is not a miscellaneous function repository. Separate different use cases and different reasons to change.

### Data

- Own connections, queries, transactions, serialization, protocol access, persistence, and resource cleanup while allowing original lower-level errors to surface.
- Do not decide presentation state, button availability, navigation, messages, or display formatting, and do not absorb domain or Service business rules.

## Refactor a Giant UI File

1. Inventory existing pages, components, presentation state, events, service calls, data access, and tests. Record observable behavior and real call entries.
2. Move tests into the external mirrored layout required by the language skill, then mechanically split pages and components while preserving types, events, and behavior.
3. Move presentation state and user intent into matching ViewModels, use-case orchestration into Services, and database, file, network, and protocol operations into Data.
4. Reduce the application entrypoint to dependency composition and navigation. Delete duplicate implementation and compatibility forwarding from the giant file; do not preserve old and new paths.
5. After each layer extraction, run project formatting, static checks, explicitly required tests, and real-UI verification. Continue only when behavioral evidence matches.

## Review Gates

Any item below fails the UI deliverable:

1. One file contains several pages, several reusable components, or implementation from two or more of View, ViewModel, Service, and Data.
2. A View directly queries a database, reads or writes a file, sends a network request, or implements use-case orchestration.
3. A ViewModel constructs UI elements or reaches Data directly, or Service/Data references UI framework or presentation state.
4. Pages, components, or ViewModels remain concentrated in a unified giant file, or `mod.rs` and the application entrypoint still contain real page implementation.
5. Forwarders, aliases, compatibility entrypoints, or duplicate state sources preserve the old file.
6. Compilation or unit tests are treated as UI completion without launching the real application and observing affected interactions as required by project rules.

## Collaboration With Other Skills

- Use `$cx-design` when the work also concerns object responsibilities, domain models, or data-access boundaries.
- Use `$cx-common-module` to search existing entries before adding a reusable component or public UI capability.
- When the user or current document explicitly requires tests, use `$cx-tdd` and the relevant language test skill; tests remain separate from production files.
- Before delivery, use `$cx-review` to check layering, file layout, behavioral evidence, and real-UI observation.

## Output

Record the page, component, ViewModel, Service, and Data files with one-sentence responsibilities, the dependency direction, removed giant entrypoints, behavior-preservation evidence, real-UI verification, and residual risk.
