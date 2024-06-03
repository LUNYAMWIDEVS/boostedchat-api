# Register your models here.
from django.contrib import admin

from .models import SalesRep, SalesRepProfile, SalesRepChannel, SalesRepChannelActivity, SalesRepsChannelWorkingShift, SalesRepChannelRunningAverage, SalesRepProfileList # SalesRepChannelWorkingShiftActivity


@admin.register(SalesRep)
class SalesRepAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("id",)
        form = super(SalesRepAdmin, self).get_form(request, obj, **kwargs)
        return form

@admin.register(SalesRepProfileList)
class SalesRepProfileListAdmin(admin.ModelAdmin):
    pass
@admin.register(SalesRepProfile)
class SalesRepProfileAdmin(admin.ModelAdmin):
    pass
    
@admin.register(SalesRepChannel)
class SalesRepChannelAdmin(admin.ModelAdmin):
    pass

@admin.register(SalesRepChannelActivity)
class SalesRepChannelActivitiesAdmin(admin.ModelAdmin):
    pass

@admin.register(SalesRepsChannelWorkingShift)
class SalesRepsChannelWorkingShiftsAdmin(admin.ModelAdmin):
    pass

@admin.register(SalesRepChannelRunningAverage)
class SalesRepChannelRunningAverageAdmin(admin.ModelAdmin):
    pass

# @admin.register(SalesRepChannelWorkingShiftActivity)
# class SalesRepChannelWorkingShiftActivityAdmin(admin.ModelAdmin):
#     pass

