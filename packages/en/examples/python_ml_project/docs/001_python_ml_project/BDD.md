# BDD: 001_python_ml_project

Feature: 001_python_ml_project

  In order to keep AI-assisted Python ML work auditable
  As a project maintainer
  I want the example project to use a numbered feature-group documentation set

  Rule: Development starts from the feature documentation set

    Scenario: BDD-CX-001 - Development uses the documentation-set BDD/TDD workflow
      Given a developer asks for a feature or bugfix
      When the assistant plans and implements the work
      Then it updates the target engineering spec and changelog before implementation
      And it stops and waits for the user to confirm the documents and next implementation plan
      And after user confirmation, it writes failing tests before production code
      And it records verification evidence after the tests pass
