import django_filters
from .models import Allat
from django.db.models import F, ExpressionWrapper
import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import TextInput

class AllatFilter(django_filters.FilterSet):
    eletkor_min = django_filters.CharFilter(method='filter_eletkor_min', label=_("minimum életkor"),widget=TextInput(attrs={'placeholder': _('éves')}))
    eletkor_max = django_filters.CharFilter(method='filter_eletkor_max', label=_("maximum életkor"),widget=TextInput(attrs={'placeholder': _('éves')}))
    class Meta:
        model = Allat     
        fields = ('faj', 'meret', 'ivar', 'ivartalanitva', 'eletkor_min', 'eletkor_max')

    
    def filter_eletkor_min(self, queryset, field_name, eletkor_min):
        eletkor_min = datetime.timedelta(days =365*float(eletkor_min), seconds = 0)
        if eletkor_min:   
            age_expr = ExpressionWrapper(datetime.date.today() - F('szuletesiideje'), output_field=models.DurationField())
            queryset = queryset.annotate(age=age_expr).filter(age__gt=eletkor_min)
        return queryset

    def filter_eletkor_max(self, queryset, field_name, eletkor_max):
        eletkor_max = datetime.timedelta(days =365*float(eletkor_max), seconds = 0)
        if eletkor_max:   
            age_expr = ExpressionWrapper(datetime.date.today() - F('szuletesiideje'), output_field=models.DurationField())
            queryset = queryset.annotate(age=age_expr).filter(age__lt=eletkor_max)
        return queryset