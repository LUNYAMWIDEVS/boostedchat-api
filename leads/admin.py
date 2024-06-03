from django.contrib import admin
from .models import Leads, LeadScore, LeadOutreachTrial, LeadChannel, LeadOutreachActivities

@admin.register(Leads)
class LeadsAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("id",)
        form = super(LeadsAdmin, self).get_form(request, obj, **kwargs)
        return form

@admin.register(LeadScore)
class LeadScoreAdmin(admin.ModelAdmin):
    pass

# @admin.register(LeadSalesRepScore)
# class LeadSalesRepScoreAdmin(admin.ModelAdmin):
#     pass

@admin.register(LeadOutreachTrial)
class LeadOutreachTrialsAdmin(admin.ModelAdmin):
    pass

@admin.register(LeadChannel)
class LeadChannelsAdmin(admin.ModelAdmin):
    pass

@admin.register(LeadOutreachActivities)
class LeadOutreachActivitiesAdmin(admin.ModelAdmin):
    pass

