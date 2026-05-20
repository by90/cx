# BDD: 001_python_ml_project

Feature: 001_python_ml_project

  In order to keep AI-assisted Python ML work auditable
  As a project maintainer
  I want the example project to use a numbered feature-group documentation set

  Rule: Development starts from the feature documentation set

    Scenario: BDD-CX-001 - 开发使用文档集 BDD/TDD 工作流
      Given 开发者提出功能或缺陷需求
      When 助手规划并实现该工作
      Then 它在实现前更新目标研发主文档和变更记录
      And 它停止并等待用户确认文档和下一步实现计划
      And 用户确认后，它先写失败测试再写生产代码
      And 测试通过后记录验证证据
