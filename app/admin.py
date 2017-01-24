from django.contrib import admin
from app.models import *


# ============  Students  ==================================================
admin.site.register(Student)
# ==========================================================================


# ============  Groups  ====================================================
class StudentsInline(admin.StackedInline):
    model = StudentGroupDistribution
    extra = 1


class LeadsInline(admin.StackedInline):
    model = GroupLead
    extra = 1
    max_num = 1


class GroupsAdmin(admin.ModelAdmin):
    inlines = [
        StudentsInline,
        LeadsInline,
    ]


admin.site.register(StudentGroup, GroupsAdmin)
# ==========================================================================
