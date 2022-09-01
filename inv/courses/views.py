from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from wsgiref.util import FileWrapper
from inv.settings import BASE_DIR
import os
from .tasks import task1


def site(request):

    template_name = 'main.html'

    if request.method == 'POST':
        uploaded_file = request.FILES['data']
        print(type(uploaded_file))

        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        # url = fs.url(name)

        print(fs.path(name))
        if task1.delay(fs.path(name)):
            file_path = f'{BASE_DIR}/assignments.xlsx'
            wrapper = FileWrapper(open(file_path, 'rb'))
            response = HttpResponse(
                wrapper, content_type='application/force-download')
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(file_path)
            return response
        # return HttpResponse('df_c')

    return render(request, template_name, {})
