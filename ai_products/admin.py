from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from . import models
from . import models as model


# Register your models here.
class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ["email"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ()}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(model.Project)
admin.site.register(model.ProjectUser)
admin.site.register(model.ApiProvider)
admin.site.register(model.AiType)
admin.site.register(model.Task)
admin.site.register(model.Work)
admin.site.register(model.Prompt)
admin.site.register(model.PromptOutput)
admin.site.register(model.OutputResult)
admin.site.register(model.ScheduleType)
admin.site.register(model.Schedule)
admin.site.register(model.ScheduleLog)
admin.site.register(model.Endpoint)
admin.site.register(model.AiModel)
admin.site.register(model.AiModelType)
admin.site.register(model.AiInputFieldType)
admin.site.register(model.AiInputField)
admin.site.register(model.AiInputTypeAiInputFieldType)
admin.site.register(model.AiInputType)
admin.site.register(model.AiInput)
admin.site.register(model.AiTypeAiInput)
admin.site.register(model.PromptInput)
admin.site.register(model.AiRequest)
