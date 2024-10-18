from django_filters import rest_framework as django_filters
from apps.notifications import models as notifications_models

class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class NotificationFilter(django_filters.FilterSet):
    created = django_filters.DateTimeFromToRangeFilter(field_name='created')

    category = django_filters.CharFilter(field_name='notification_template__notification_category__name',
                                         lookup_expr='iexact', )
    category_in = CharInFilter(field_name='notification_template__notification_category__name',
                                         lookup_expr='in', )


    class Meta:
        model = notifications_models.UserNotification
        fields = ["status", "notification_type", "created",
                  "category", "category_in" ]
