from django_filters import rest_framework as django_filters


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass
