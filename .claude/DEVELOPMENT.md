# 开发规范

## 代码风格

- 使用 type hints 标注类型
- 函数添加 docstring
- 遵循 ruff 格式规范

## 数据库

- 所有表继承 `models/base.py` 的 Base
- 添加 `created_at` 和 `updated_at` 时间戳
- 外键使用 `ForeignKey` 约束

## API 设计

- RESTful 风格
- 版本控制 `/api/v1/`
- 使用 `APIRouter` 组织路由
- 响应使用统一 Schema

## 测试

- 测试 async 函数使用 `@pytest.mark.asyncio`
- 使用 fixture 管理数据库状态
- 测试覆盖正常和异常情况

## Git 提交

- 使用语义化提交信息
- 格式：`<type>: <description>`
- 类型：feat, fix, docs, chore, refactor, test
