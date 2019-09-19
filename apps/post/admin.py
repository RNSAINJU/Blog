from django.contrib import admin
from .models import Post, Category, Comment

class InLineLesson(admin.TabularInline):
    model = Comment
    extra=1
    max_num = 1

class PostAdmin(admin.ModelAdmin):
    inlines = [InLineLesson]
    list_display = ('title','created_at','created_by','views','status')
    list_editable = ('status',)
    list_filter = ('created_at','created_by')
    search_fields = ('title',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('message','post','created_by','created_at')
    list_filter = ('post', 'created_by')

admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Comment,CommentAdmin)

