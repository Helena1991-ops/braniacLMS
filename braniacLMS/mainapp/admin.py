from django.contrib import admin

from mainapp.models import News, Course, Lesson, CourseTeacher
# Register your models here.

admin.site.register(Course)
#admin.site.register(Lesson)
admin.site.register(CourseTeacher)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'deleted','slug') # Поля
    list_filter = ('deleted', 'created_at') # Фильтры
    ordering = ('pk',) # Порядок
    list_per_page = 3 # Количество новостей на странице
    search_fields = ('title', 'preamble', 'body') # Параметры поиска, изначально
    actions = ('mark_as_delete',) # Добавляем действие пометить на удаление новости

    def slug(self,obj):
        return obj.title.lower().replace(' ','-')

    def mark_as_delete(self,request,queryset):
        queryset.update(deleted=True)

    mark_as_delete.short_description = 'Пометить удаленным'



@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'course', 'deleted','slug') # Поля
    list_filter = ('deleted', 'created_at','course') # Фильтры
    ordering = ('pk',) # Порядок
    list_per_page = 3 # Количество новостей на странице
    search_fields = ('title', 'preamble', 'body', 'course') # Параметры поиска, изначально
    actions = ('mark_as_delete',) # Добавляем действие пометить на удаление новости

    def slug(self,obj):
        return obj.title.lower().replace(' ','-')

    def mark_as_delete(self,request,queryset):
        queryset.update(deleted=True)

    mark_as_delete.short_description = 'Пометить удаленным'
