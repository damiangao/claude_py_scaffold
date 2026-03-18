# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- API 版本控制 (`/api/v1/`)
- 增强健康检查（数据库连接检测）
- Ruff 代码质量工具
- Pre-commit hooks
- docker-compose.yml
- .dockerignore
- CORS 中间件
- LICENSE (MIT)
- CI 工作流 (test.yml, lint.yml)

### Changed
- 路由重构为 v1 版本

## [0.1.0] - 2026-03-19

### Added
- 初始项目结构
- FastAPI 框架
- SQLAlchemy 异步数据库
- SQLite 支持
- 用户认证系统 (JWT)
- 密码加密 (bcrypt)
- 配置管理 (pydantic-settings)
- 日志系统
- 全局异常处理
- 单元测试 (pytest)
- Docker 支持
- GitHub Actions CI/CD
- 文档 (README, CLAUDE)
- 专为 Claude Code 优化
