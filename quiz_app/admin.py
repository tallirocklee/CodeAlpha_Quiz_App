from django.contrib import admin
from .models import Quiz, Question, Choice

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_created_by_username', 'get_image_display')  # Update list_display
    search_fields = ('title',)  # Remove 'created_by__username' from search_fields

    def get_created_by_username(self, obj):
        if hasattr(obj, 'created_by'):
            return obj.created_by.username
        return None

    get_created_by_username.short_description = 'Created By'  # Customize column header

    def get_image_display(self, obj):
        return obj.image.url if obj.image else None

    get_image_display.short_description = 'Image'  # Customize column header
admin.site.register(Quiz,QuizAdmin)
admin.site.register(Question)
admin.site.register(Choice)

