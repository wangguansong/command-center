from django.contrib import admin
from .models import Posting, Company, Position, PostingCompany

class PositionAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'city']
    ordering = ['title']

class PostingAdmin(admin.ModelAdmin):
    list_display = ['title', 'posting_company', 'applied_at']

admin.site.register(Company)
admin.site.register(Posting, PostingAdmin)
admin.site.register(PostingCompany)
admin.site.register(Position, PositionAdmin)
