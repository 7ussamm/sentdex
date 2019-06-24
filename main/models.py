from django.db import models
from datetime import datetime

# Create your models here.


class TutorialCategory(models.Model):
    tutorial_cat = models.CharField(max_length=255)
    cat_summary = models.CharField(max_length=200)
    cat_slug = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.tutorial_cat


class TutorialSeries(models.Model):
    tutorial_series = models.CharField(max_length=200)

    tutorial_cat = models.ForeignKey(TutorialCategory,
                                     default=1,
                                     verbose_name='Category',
                                     on_delete=models.SET_DEFAULT
                                     )  # This is where we link them together
    series_summary = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Series'

    def __str__(self):
        return self.tutorial_series


class Tutorial(models.Model):  # First class created
    # TODO: Define fields here

    title = models.CharField(max_length=200)
    content = models.TextField()
    published = models.DateTimeField('Date Field', default=datetime.now())

    tutorial_seires = models.ForeignKey(TutorialSeries, default=1,
                                        verbose_name='Series',
                                        on_delete=models.SET_DEFAULT)
    tutorial_slug = models.CharField(max_length=200, default=1)

    class Meta:
        verbose_name = 'Tutorial'
        verbose_name_plural = 'Tutorials'

    def __unicode__(self):
        pass

    def __str__(self):
        return self.title
