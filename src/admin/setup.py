# src/admin/setup.py
from fastapi import FastAPI
from sqladmin import Admin
from src.admin.views import UserAdmin, UserProfileAdmin, PostAdmin, TagAdmin

def init_admin(app: FastAPI) -> Admin:
    # 初始化 SQLAdmin;具备后台管理系统;默认自带登录认证
    admin = Admin(                  # 绑定到 FastAPI app 和数据库引擎,设置标题和基础 URL (/admin)
        app,                        # 将后台挂载到当前的 FastAPI 实例上
        app.state.engine,           # 传入数据库引擎,SQLAdmin 需要用它来执行 SQL
        title="My Blog Admin",      # 后台网页左上角显示的标题
        base_url="/admin",)         # 后台的访问网址,即 http://127.0.0.1:8000/admin; 权限控制,在生产环境中,必须继承 AuthenticationBackend 类,对接你自己的 JWT 或 Session
    admin.add_view(UserAdmin)       # 添加视图
    admin.add_view(UserProfileAdmin)
    admin.add_view(PostAdmin)
    admin.add_view(TagAdmin)
    return admin                    # 返回 Admin 实例,供其他模块使用