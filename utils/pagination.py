from django.core.paginator import Paginator


def pagination(qs, page=1, page_size=10):
    paginator = Paginator(qs, page_size)
    page_obj = paginator.get_page(page)
    return page_obj
