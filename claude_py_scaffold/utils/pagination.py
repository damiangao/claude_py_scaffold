"""分页工具"""

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from claude_py_scaffold.schemas import PageInfo, PaginatedResponse, PaginationParams


async def paginate(
    db: AsyncSession,
    query: Select,
    pagination: PaginationParams,
) -> PaginatedResponse:
    """分页查询

    Args:
        db: 数据库会话
        query: 基础查询语句（不包含 limit/offset）
        pagination: 分页参数

    Returns:
        PaginatedResponse: 分页响应
    """
    # 计算总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # 应用分页
    query = query.offset(pagination.offset).limit(pagination.page_size)
    result = await db.execute(query)
    items = result.scalars().all()

    # 计算分页信息
    total_pages = (total + pagination.page_size - 1) // pagination.page_size

    page_info = PageInfo(
        page=pagination.page,
        page_size=pagination.page_size,
        total=total,
        total_pages=total_pages,
        has_next=pagination.page < total_pages,
        has_prev=pagination.page > 1,
    )

    return PaginatedResponse(
        items=items,  # type: ignore
        page_info=page_info,
    )
