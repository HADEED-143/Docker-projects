from django.db import models
from .job import Job
from utils.helper import BID_STATUS
from users.models import Worker


class JobBid(models.Model):
    # worker who is bidding on the job
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    # job on which the worker is bidding
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    # offer made by the worker
    offer = models.DecimalField(max_digits=6, decimal_places=2)
    # message which can be typed optionally by the worker
    message = models.TextField(blank=True, null=True)

    # days that worker think he takes
    days = models.IntegerField(default=1)
    status = models.CharField(
        max_length=100, default='pending', choices=BID_STATUS)  # status of the bid
    # date/time when the bid was created
    created_at = models.DateTimeField(auto_now_add=True)
    # date/time when the bid was updated
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.worker} - {self.job}'

    class Meta:
        ordering = ['id']  # order by id
        unique_together = ('worker', 'job',)
