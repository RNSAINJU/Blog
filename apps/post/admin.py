from django.contrib import admin
from .models import Post, Category, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category','created_at','created_by','views','status')
    list_editable = ('status',)
    list_filter = ('category','created_at','created_by')
    search_fields = ('title',)

admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)

