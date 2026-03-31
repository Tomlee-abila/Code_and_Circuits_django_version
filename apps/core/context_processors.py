from apps.courses.models import Category


def site_context(request):
    return {
        'site_name': 'Code & Circuits',
        'categories': Category.objects.all(),
    }
