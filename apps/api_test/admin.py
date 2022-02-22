from django.contrib import admin
from apps.api_test.models import Department, Project, ProjectMember, ProjectDynamic, \
    GlobalEnv, GlobalConst, GlobalHeader, GlobalResponseValidate, GlobalLabel, \
    ApiGroup, ApiInfo, ApiUpdateHistory, TestSuite, TestCase


class ReadOnlyModelAdmin(admin.ModelAdmin):
    """ModelAdmin class that prevents modifications through the admin.

    The changelist and the detail view work, but a 403 is returned
    if one actually tries to edit an object.
    """

    actions = None

    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    # Allow viewing objects but not actually changing them
    def has_change_permission(self, request, obj=None):
        if request.method not in ('GET', 'HEAD'):
            return True
        return super(ReadOnlyModelAdmin, self).has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False


class ReadAndDeleteModelAdmin(admin.ModelAdmin):
    """ModelAdmin class that prevents modifications through the admin.

    The changelist and the detail view work, but a 403 is returned
    if one actually tries to edit an object.
    """

    actions = None

    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    # Allow viewing objects but not actually changing them
    def has_change_permission(self, request, obj=None):
        if request.method not in ('GET', 'HEAD'):
            return True
        return super(ReadAndDeleteModelAdmin, self).has_change_permission(request, obj)


#  部门、项目、成员
class DepartmentForm(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'leader')
    list_display_links = ('name', 'leader')
    list_filter = ('name', 'leader')
    list_per_page = 20
    ordering = ('id',)
    fieldsets = ([
        '部门', {
            'fields': ('name', 'leader')
        }],
    )


admin.site.register(Department, DepartmentForm)


class ProjectMemberForm(admin.ModelAdmin):
    search_fields = ('user', 'project')
    list_display = ('id', 'role', 'status', 'project', 'user')
    list_display_links = ('role', 'status', 'project')
    list_filter = ('role', 'status', 'project', 'user')
    list_per_page = 20
    ordering = ('id',)
    fieldsets = ([
        '项目成员', {
            'fields': ('role', 'status', 'project', 'user')
        }],
    )


admin.site.register(ProjectMember, ProjectMemberForm)


class MemberInProject(admin.TabularInline):
    model = ProjectMember


class DepartmentInProject(admin.TabularInline):
    model = Department


class ProjectForm(admin.ModelAdmin):
    inlines = [MemberInProject, ]
    search_fields = ('name', 'safe_name')
    list_display = ('id', 'name', 'department', 'status', 'creator')
    list_display_links = ('id', 'name', )
    list_filter = ('status', )
    list_per_page = 20
    ordering = ('id',)
    fieldsets = ([
        '项目', {
            'fields': ('name', 'safe_name', 'version', 'department',
                       'creator', 'updater', 'status', 'description')
        }],
    )


admin.site.register(Project, ProjectForm)


class GlobalEnvForm(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'status')
    list_display_links = ('id', 'name')
    list_filter = ('status', )
    list_per_page = 20
    ordering = ('id',)
    fieldsets = ([
        '全局环境配置', {
            'fields': ('name', 'config', 'data', 'mock', 'description', 'status')
        }],)


admin.site.register(GlobalEnv, GlobalEnvForm)


class GlobalConstForm(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'value', 'status', 'description')
    list_display_links = ('id', 'name')
    list_filter = ('status', )
    list_per_page = 20
    ordering = ('id',)
    fieldsets = ([
        '全局Const配置', {
            'fields': ('name', 'value', 'status', 'description')
        }],)


admin.site.register(GlobalConst, GlobalConstForm)


class GlobalHeaderForm(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'value', 'status', 'description')
    list_display_links = ('id', 'name')
    list_filter = ('status', )
    list_per_page = 20
    ordering = ('id',)
    fieldsets = ([
        '全局Header配置', {
            'fields': ('name', 'value', 'status', 'description')
        }],)


admin.site.register(GlobalHeader, GlobalHeaderForm)


class GlobalResponseValidateForm(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'check_status_code', 'check_response_data', 'status', 'description')
    list_display_links = ('id', 'name')
    list_filter = ('status', )
    list_per_page = 20
    ordering = ('id',)
    fieldsets = ([
        '全局通用校验规则配置', {
            'fields': ('name', 'check_status_code', 'check_response_data', 'status', 'description')
        }],)


admin.site.register(GlobalResponseValidate, GlobalResponseValidateForm)


class GlobalLabelForm(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'status', 'description')
    list_display_links = ('id', 'name')
    list_filter = ('status', )
    list_per_page = 20
    ordering = ('id',)
    fieldsets = ([
        '标签配置', {
            'fields': ('name', 'status', 'description')
        }],)


admin.site.register(GlobalLabel, GlobalLabelForm)


class CustomMethodForm(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'project', 'name', 'description', 'type', 'status', 'dataCode')
    list_display_links = ('id', 'project', 'name')
    list_filter = ('project', 'type', 'status')
    list_per_page = 20
    ordering = ('id',)
    fieldsets = ([
        '自定义方法', {
            'fields': ('project', 'name', 'description', 'type', 'status', 'dataCode')
        }],)


class ApiGroupForm(admin.ModelAdmin):
    search_fields = ('name', 'project')
    list_display = ('id', 'project', 'name')
    list_display_links = ('id', 'project', 'name')
    list_per_page = 20
    ordering = ('id',)
    fieldsets = ([
        '接口分组', {
            'fields': ('project', 'name')
        }],)


admin.site.register(ApiGroup, ApiGroupForm)


class ApiInfoForm(admin.ModelAdmin):
    search_fields = ('name', 'http_type', 'method', 'path')
    list_display = ('id', 'project', 'name', 'http_type', 'method', 'path', 'status')
    list_display_links = ('id', 'name', 'project')
    list_filter = ('project', 'http_type', 'method', 'status')
    list_per_page = 20
    ordering = ('id',)
    fieldsets = ([
        '接口信息', {
            'fields': ('project', 'api_group', 'name', 'http_type', 'method', 'path', 'host_tag',
                       'req_header', 'req_params', 'req_json', 'req_data', 'validator', 'update_status',
                       'labels', 'creator', 'updater', 'status', 'description')
        }],)


admin.site.register(ApiInfo, ApiInfoForm)


class ApiUpdateHistoryForm(ReadOnlyModelAdmin):
    search_fields = ('api', )
    list_display = ('id', 'api', 'content', 'update_time', 'update_status')
    list_display_links = ('id', 'api')
    list_filter = ('api', )
    list_per_page = 20
    ordering = ('id',)
    fieldsets = ([
        '接口变更历史', {
            'fields': ('id', 'api', 'content', 'update_time', 'update_status')
        }],)


admin.site.register(ApiUpdateHistory, ApiUpdateHistoryForm)


class TestSuiteForm(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    list_per_page = 20
    ordering = ('id',)
    fieldsets = ([
        '用例集', {
            'fields': ('department', 'name', 'headers', 'type', 'labels',
                       'creator', 'updater', 'status', 'description')
        }],
    )


admin.site.register(TestSuite, TestSuiteForm)


class TestCaseForm(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    list_filter = ('name',)
    list_per_page = 20
    ordering = ('id',)
    fieldsets = ([
        '用例', {
            'fields': ('name', 'apiInfo', 'test_suite',
                       'labels', 'creator', 'updater', 'status', 'description')
        }],)


admin.site.register(TestCase, TestCaseForm)


class ProjectDynamicForm(ReadOnlyModelAdmin):
    search_fields = ('operationObject', 'user')
    list_display = ('id', 'project', 'time', 'type', 'operationObject', 'description', 'user')
    list_display_links = ('id', 'project', 'time')
    list_filter = ('project', 'type')
    list_per_page = 20
    ordering = ('-id',)


admin.site.register(ProjectDynamic, ProjectDynamicForm)
