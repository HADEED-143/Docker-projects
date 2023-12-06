from django.db import models

class JobCategory(models.Model): 
    title = models.CharField(max_length=255) # title of the job category e.g. "Plumbing"
    description = models.TextField()  # description of the job category e.g. "Plumbing jobs"
    category_image = models.ImageField(upload_to='category_images/', null=True, blank=True)  # image of the job category e.g. "Plumbing"
    
    def __str__(self) -> str: 
        return self.title
    
    class Meta: 
        ordering = ['id', 'title']
        verbose_name = 'Job Category'
        verbose_name_plural = 'Job Categories'
        