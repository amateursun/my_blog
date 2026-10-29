# src/admin/views.py — 1.18 管理员后台设置
from src.data.orm.user import UserORM
from src.data.orm.user_profile import UserProfileORM
from src.data.orm.post import PostORM
from src.data.orm.tag import TagORM
from sqladmin import ModelView
class UserAdmin(ModelView, model=UserORM):                                          # ModelView 作用是告诉 SQLAdmin:这个数据表在后台网页里长什么样,怎么操作
    name = "用户"                                                                   # 菜单栏中单数的显示名(如"新建用户")
    name_plural = "用户管理"                                                        # 菜单栏中多数的显示名
    icon = "fa-solid fa-user"                                                       # # 图标(使用 FontAwesome 的类名)
    column_list = [UserORM.id, UserORM.username, UserORM.email, UserORM.is_active]  # 列表页显示的字段:取核心字段,隐藏密码等
    column_searchable_list = [UserORM.username, UserORM.email]                      # 顶部搜索框支持按哪些字段搜索
    # from_column = [UserORM.username, UserORM.email]                               # 允许在添加/修改时填写的字段;自动生成的字段从表单里剔除

class UserProfileAdmin(ModelView, model=UserProfileORM):
    name = "用户资料"
    name_plural = "用户资料管理"
    column_list = [UserProfileORM.id, UserProfileORM.user_id, UserProfileORM.personal_profile]
    # 一对一关系：显示关联的用户信息
    column_details_list = [UserProfileORM.user]                                     # 详情页(点开具体某一行后)显示的内容

class PostAdmin(ModelView, model=PostORM):
    name = "文章"
    name_plural = "文章管理"
    icon = "fa-solid fa-file-alt"
    column_list = [PostORM.id, PostORM.title, PostORM.slug, PostORM.author, PostORM.is_published]
    column_searchable_list = [PostORM.title, PostORM.slug]
    # 多对一关系:显示作者
    form_ajax_refs = {                           # 作用:在新增/修改文章的表单里,如果作者(author)很多
        "author": {                              # 下拉框会卡死。开启 AJAX 后,会变成一个支持边输入边搜索的下拉框
            "fields": ("username",),             # 搜索时匹配 User 表的 username 字段
            "order_by": "username",              # 搜索时匹配 User 表的 username 字段
        }
    }

class TagAdmin(ModelView, model=TagORM):
    name = "标签"
    name_plural = "标签管理"
    icon = "fa-solid fa-tags"
    column_list = [TagORM.id, TagORM.name]
    column_searchable_list = [TagORM.name]