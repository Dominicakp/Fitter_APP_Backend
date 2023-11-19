from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
import django_filters
from .models import User

class UserFilter(django_filters.FilterSet):
    location = django_filters.CharFilter(
        method='filter_location',
        label='Location (within distance)'
    )
    radius = django_filters.NumberFilter(
        method='filter_radius',
        label='Radius (km)'
    )

    class Meta:
        model = User
        fields = ['location', 'radius', 'user_type']

    def filter_location(self, queryset, name, value):
        if value:
            user_location = self.request.query_params.get('location', None)
            if user_location:
                lat, lon = map(float, user_location.split(','))
                user_location = Point(lat, lon)
                return queryset.filter(location__distance_lte=(user_location, Distance(km=float(self.request.query_params.get('radius', 1)))))
        return queryset

    def filter_radius(self, queryset, name, value):
        return queryset  # This method is here to enable the 'Radius' field in the filter
