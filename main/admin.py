from django.contrib import admin
from .models import Tutorial, TutorialCategory, TutorialSeries
from tinymce.widgets import TinyMCE
from django.db import models


# Register your models here.


class TutorialAdmin(admin.ModelAdmin):
    # fields = ['published',
    #           'title',
    #           'content']

    # to make them in different tables in admin site
    # this does the same as above, the only difference is to make them in table
    fieldsets = [
        ('Title/Date', {'fields': ['published', 'title']}),
        ('Url/Series', {'fields': ['tutorial_slug', 'tutorial_seires']}),
        ('Content', {'fields': ['content']}),
    ]

    formfield_overrides = {
        models.TextField: {
            'widget': TinyMCE(),
        }
    }


admin.site.register(TutorialCategory)
admin.site.register(TutorialSeries)
admin.site.register(Tutorial, TutorialAdmin)
