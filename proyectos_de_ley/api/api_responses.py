from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework_csv import renderers


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class CSVResponse(HttpResponse):
    """
    An HttpResponse that renders its content into CSV.
    """
    def __init__(self, data, **kwargs):
        content = CSVRenderer().render(data)
        kwargs['content_type'] = 'text/csv'
        super(CSVResponse, self).__init__(content, **kwargs)


class CSVRenderer(renderers.CSVRenderer):
    media_type = 'text/csv'
    format = 'csv'

    def render(self, data, media_type=None, renderer_context=None):
        return super(CSVRenderer, self).render(data, media_type, renderer_context)
