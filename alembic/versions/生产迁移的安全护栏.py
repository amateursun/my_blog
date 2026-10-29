# 生产部署流程（CI/CD 中的位置）
#标准的零停机迁移流程如下：

#阶段 1：开发环境（生成 + 审查）
# 开发者修改 ORM 模型后，生成迁移文件
#alembic revision --autogenerate -m "add_user_phone_column"
# 生成 SQL 预览，提交到 PR 供审核
#alembic upgrade head --sql > migration_preview.sql

# 阶段 2：CI 流水线（验证）
# 在 CI 的临时数据库上执行迁移，确保能跑通
#alembic upgrade head
# 检查模型与迁移是否同步（防止漏迁移）
#alembic check
#alembic check 会检测 ORM 模型与迁移脚本之间是否存在未捕获的差异。

# 阶段 3：生产部署（独立执行）
# 部署前：先备份数据库（常规备份策略之外，再做一次迁移前快照）
#pg_dump production_db > backup_before_migration.sql
# 执行迁移（通过 Redis 锁防止并发）
#python scripts/run_migrations_with_lock.py

# 阶段 4：应用滚动更新
#迁移完成后，再滚动更新 FastAPI 应用实例。这样新代码启动时，数据库结构已经就绪



# 一、防止多实例并发迁移; 方案：Redis 分布式锁; 如果部署了多个 Pod/实例，必须确保同一时间只有一个实例在执行迁移
# 迁移执行器（独立于 Alembic，放在部署脚本中）
import asyncio
import redis.asyncio as redis

async def run_migrations_with_lock():
    r = redis.from_url(os.getenv("REDIS_URL"))
    lock = r.lock("alembic_migration_lock", timeout=300)  # 5 分钟超时
    
    if not await lock.acquire(blocking=False):
        print("另一个实例正在执行迁移，跳过")
        return
    
    try:
        from alembic.config import Config
        from alembic import command
        cfg = Config("alembic.ini")
        command.upgrade(cfg, "head")
    finally:
        await lock.release()

# 二、设置锁超时与语句超时; 在生产数据库上执行 DDL（如加列、改索引）时，可能会因为锁等待而阻塞其他写入
from alembic import op

def upgrade():
    # 设置锁等待超时（5 秒），避免迁移无限期阻塞
    op.execute("SET lock_timeout = '5s'")
    
    op.add_column('users', sa.Column('phone', sa.String(20)))

# 三、大表操作使用 CONCURRENTLY; 在 PostgreSQL 中，给已有大表加索引必须使用 CONCURRENTLY，否则会锁表
def upgrade():
    with op.get_context().autocommit_block():
        op.create_index(
            'ix_users_phone', 'users', ['phone'],
            postgresql_concurrently=True,
        )

# 四、幂等性与不可逆操作; 生产迁移脚本应尽量幂等（重复执行不报错），并且避免不可逆操作（如 DROP COLUMN 除非确认数据已备份
def upgrade():
    # 幂等：先检查列是否存在
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [c["name"] for c in inspector.get_columns("users")]
    if "phone" not in columns:
        op.add_column("users", sa.Column("phone", sa.String(20)))

