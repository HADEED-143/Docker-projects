from django.db import models
from . import Job
from users.models import Worker, CustomUser


class Feedback(models.Model):
    rating = models.IntegerField(default=5)  # rating out of 5
    comment = models.TextField(blank=True)  # comment by the client/worker
    job = models.ForeignKey(Job, on_delete=models.CASCADE,
                            related_name='job', default=1)  # job on which the feedback is given
    feedback_receiver = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='feedback_receiver', default=1)  # user who is receiving the feedback

    feedback_sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='feedback_sender', default=1)  # user who is giving the feedback

    def __str__(self) -> str:
        return f'{self.receiver.first_name} {self.receiver.last_name} - {self.job.title}'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'
        unique_together = ('job', 'feedback_sender', 'feedback_receiver')
