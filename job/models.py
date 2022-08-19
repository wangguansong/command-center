from django.db import models

PLATFORMS = [
        ('zhipin', 'Boss Zhipin'),
        ('lagou', 'Lagou'),
        ('liepin', 'Liepin'),
        ('zhaopin', 'Zhilian Zhaopin'),
    ]


class Company(models.Model):
    company_name = models.CharField(max_length=16)
    legal_name = models.CharField(max_length=32, null=True, blank=True)
    legal_address = models.CharField(max_length=64, null=True, blank=True)
    usci = models.CharField('Unified Social Credit Identifier',
                            max_length=32, null=True, blank=True)
    company_size_min = models.IntegerField(null=True, blank=True)
    company_size_max = models.IntegerField(null=True, blank=True)
    industry = models.CharField(max_length=16, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.company_name


class PostingCompany(models.Model):
    company_name = models.CharField(max_length=16)
    company =  models.ForeignKey(Company, on_delete=models.CASCADE)
    posting_platform = models.CharField(max_length=16, choices=PLATFORMS)
    platform_id = models.CharField(max_length=32, null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'job_posting_company'
        verbose_name_plural = 'posting companies'

    def __str__(self):
        return self.company_name


class Position(models.Model):
    title = models.CharField(max_length=16)
    company =  models.ForeignKey(Company, on_delete=models.CASCADE)
    city = models.CharField(max_length=16)
    address = models.CharField(max_length=32, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + ' | ' + self.company.company_name


class Posting(models.Model):
    POSTING_STATUS_INT = [
        (0, 'Normal'),
        (1, 'Closed'),
        (2, 'Inactive')
    ]
    title = models.CharField(max_length=16)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)
    posting_company = models.ForeignKey(PostingCompany, on_delete=models.CASCADE, null=True, blank=True)
    posting_id = models.CharField(max_length=32)
    posting_status = models.PositiveSmallIntegerField(choices=POSTING_STATUS_INT, default=0)
    monthly_min = models.PositiveIntegerField(null=True, blank=True)
    monthly_max = models.PositiveIntegerField(null=True, blank=True)
    salary_months = models.SmallIntegerField(default=12)
    description = models.TextField()
    requirement = models.TextField()
    poster_name = models.CharField(max_length=8, blank=True)
    poster_id = models.CharField(max_length=32, blank=True)
    head_hunter = models.CharField(max_length=16, blank=True)
    posted_at = models.DateTimeField()
    refreshed_at = models.DateTimeField()
    applied_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
