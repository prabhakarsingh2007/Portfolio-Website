from django.contrib import admin
from .models import Category, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'published_date', 'views')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'summary', 'body', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'published_date'
    actions = ['make_published']

    def make_published(self, request, queryset):
        rows_updated = queryset.update(status='published')
        for obj in queryset:
            # triggers save to set published_date if not set
            obj.save()
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = f"{rows_updated} stories were"
        self.message_user(request, f"{message_bit} successfully marked as published.")
    make_published.short_description = "Mark selected stories as published"
