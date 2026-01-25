from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Report(models.Model):
    Report_Types = [
        ('revenue', 'Revenue Report'),
        ('users', 'User Report'),
        ('transactions', 'Transactions Report'),
        ('custom', 'Custom Report'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=50, choices=Report_Types)
    data = models.JSONField(default=dict)
    start_date = models.DateField()
    end_date = models.DateField()
    generated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"{self.title} ({self.report_type})"