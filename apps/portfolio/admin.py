from django.contrib import admin
from .models import Profile, Skill, Experience, Education

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email', 'location')
    fieldsets = (
        ('Personal Info', {
            'fields': ('name', 'title', 'bio', 'avatar', 'resume')
        }),
        ('Contact & Links', {
            'fields': ('email', 'phone', 'location', 'github', 'linkedin', 'twitter')
        }),
    )

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency', 'order')
    list_filter = ('category',)
    list_editable = ('proficiency', 'order')
    search_fields = ('name',)

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'company', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current', 'company')
    search_fields = ('role', 'company', 'description')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'school', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current', 'school')
    search_fields = ('degree', 'school', 'description')
