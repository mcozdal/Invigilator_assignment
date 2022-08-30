from termios import N_MOUSE
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
# from django.utils.datastructures import MultiValueDictKeyError

# from .forms import schedule
# from django.views.generic.edit import FormView
from .tasks import task1


def site(request):

    template_name = 'main.html'

    if request.method == 'POST':
        uploaded_file = request.FILES['data']
        print(type(uploaded_file))

        # excel_file = pd.ExcelFile(data)
        # df_sch = excel_file.parse('EXAM_SCHEDULE')
        # df_inv = excel_file.parse('INVIGILATORS')
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        # url = fs.url(name)

        print(fs.path(name))
        task1.delay(fs.path(name))

        return HttpResponse('df_c')

    return render(request, template_name, {})
