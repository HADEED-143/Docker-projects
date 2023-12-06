from django.contrib.gis.db import models

from utils.helper import JOB_TYPES
from .category import JobCategory
from django.utils import timezone
from utils.helper import JOB_STATUS
from users.models import Worker, CustomUser


class JobImages(models.Model):
    # one job can have many images
    image = models.ImageField(upload_to='job_images/',
                              null=True, blank=True)  # image of the job
    uploaded_at = models.DateTimeField(
        default=timezone.now)  # date when image was uploaded

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.image}'


class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    # user who posted the job
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # protect the category, delete the job only.
    category = models.ForeignKey(JobCategory, on_delete=models.PROTECT)
    budget = models.DecimalField(max_digits=6, decimal_places=2)
    job_type = models.CharField(
        max_length=100, choices=JOB_TYPES, default=JOB_TYPES[0][0])
    city = models.CharField(max_length=255, default='Rawalpindi')
    attachment = models.FileField(
        upload_to='job_media/', null=True, blank=True)

    start_date = models.DateField()  # date when job should started.
    status = models.CharField(
        max_length=100, choices=JOB_STATUS, default=JOB_STATUS[0][0])  # status of the bid
    labors_required = models.PositiveIntegerField(
        null=True, blank=True, default=1)
    location = models.PointField(null=True, blank=True)
    address = models.CharField(
        null=False, blank=False, default='Rawalpindi', max_length=None)

    worker = models.ForeignKey(Worker, on_delete=models.PROTECT, null=True,
                               blank=True, related_name='jobs_worker')  # worker who is assigned to the job
    # allow_contractors = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(
        default=timezone.now, editable=False)  # date when job was created
    updated_at = models.DateTimeField(
        default=timezone.now, editable=True, null=True, blank=True)  # date when job was updated

    def __str__(self):
        return self.title

    def start_contract(self):
        self.status = 'in-progress'
        self.save()

    def complete_contract(self):
        self.status = 'completed'
        self.save()

    def pause_contract(self):
        self.status = 'paused'
        self.save()

    def cancel_contract(self):
        self.status = 'cancelled'
        self.save()

    def set_worker(self, worker_id):
        # get worker from id and set it to the job
        self.worker = Worker.objects.get(id=worker_id)
        self.save()

    class Meta:
        ordering = ['-id']  # order by id
        unique_together = ('title', 'description', 'budget',)
