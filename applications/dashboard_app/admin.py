from django.contrib import admin
from .models import Consultation_history

class History(admin.ModelAdmin):
    list_display = ('id','datetime','open_price','high_price','low_price','close_price','volume_btc','volume_usd','trend_prediction')
    search_fields = ('id',)

admin.site.register(Consultation_history,History)

