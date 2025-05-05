from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Возвращает значение из словаря по ключу"""
    if dictionary is None:
        return None
    return dictionary.get(key)

@register.filter
def filter_by_course(queryset, course):
    """Фильтрует QuerySet по курсу"""
    if queryset is None:
        return None
    return queryset.filter(course=course)

@register.filter
def filter_by_assignment(queryset, assignment):
    """Фильтрует QuerySet по заданию"""
    if queryset is None:
        return None
    return queryset.filter(assignment=assignment).first()

@register.filter
def avg_grade(queryset):
    """Вычисляет среднюю оценку из QuerySet оценок"""
    if queryset is None or not queryset.exists():
        return 0
    total = sum(grade.score for grade in queryset)
    count = queryset.count()
    return total / count if count > 0 else 0