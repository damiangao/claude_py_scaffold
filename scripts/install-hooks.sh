# 安装 pre-commit hooks
# 在项目根目录运行

# 1. 安装 pre-commit
uv pip install pre-commit

# 2. 安装 hooks
pre-commit install

echo "✓ pre-commit 已安装"
echo ""
echo "现在每次 git commit 会自动运行:"
echo "  - ruff check (检查错误)"
echo "  - ruff format (格式化代码)"
echo ""
echo "每次 git push 会自动运行:"
echo "  - pytest (运行测试)"
