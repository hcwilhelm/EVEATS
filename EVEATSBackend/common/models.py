from django.db import models

class TaskLastRun(models.Model):
  taskName        = models.CharField(max_length=255)
  parameterValue  = models.CharField(max_length=255)
  lastRun         = models.DateTimeField(null=True)

  class Meta:
    unique_together = (("taskName", "parameterValue"),)
