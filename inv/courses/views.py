from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from wsgiref.util import FileWrapper
from inv.settings import BASE_DIR
import os
from .tasks import task1
from json import dumps


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


def comparisons(request):
    template_name = 'compare.html'

    clusters = {
        'Istek Turu': ['Hata', 'Yeni', 'Degisiklik', 'Destek', 'Fast'],
        'Sure': ['0-4', '4-8', '4-12', '>12'],
        'Etki': ['Düşük Etki', 'Orta Etki', 'Yüksek Etki'],
        'Aciliyet': ['DüşükA', 'OrtaA', 'YüksekA'],
        'Kontrat': ['Dusuk Kon', 'Orta Kon', 'Yüksek Kon']
    }
    cluster_comps = {

    }

    data = {'clusters': clusters,
            'pair': cluster_comps,
            'comps': {'Istek Turu': ['Sure'],
                      'Etki': ['Sure'],
                      'Aciliyet': ['Sure']
                      }
            }

    dataJSON = dumps(data)

    if request.method == 'POST':

        uploaded_file = request.POST
        print(uploaded_file)

    return render(request, template_name, {'data': dataJSON})


def createComps(nodes):
    comps = []
    nodes_len = len(nodes)

    for i in range(nodes_len - 1):
        for j in range(i + 1, nodes_len):
            comps.append([nodes[i], nodes[j]])

    return comps
