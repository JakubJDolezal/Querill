from django.http import FileResponse, Http404
from django.conf import settings
import json
import os
from ContextQuery.views import get_names

f = open('config.json')

config = json.load(f)


def display_pdf(request, document_number):
    file_path = get_names(int(document_number))
    file_path = file_path.replace("\\", "/")
    print(file_path)
    if os.path.exists(file_path):
        print('exists')
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
        return response
    else:
        raise Http404
