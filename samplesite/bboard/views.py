"""
    Description:
        Модуль содержащий контроллеры
    Attributes:
        None
    Example:
        None
"""

from django.views.decorators.http import require_GET, require_POST, require_safe, require_http_methods
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
# from django.urls import path
from bboard.models import Bb
# from django.template import loader
from django.shortcuts import render
from .models import Rubric
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.list import ListView
from django.views.generic.dates import ArchiveIndexView, DateDetailView
from django.views.generic import View
from django.core.paginator import Paginator
from .forms import BbForm, BbFormFromFactory, BbFormFastCreate
from django.urls import reverse_lazy, reverse
import os


# def index(request):
#     s = 'List of orders\n\n\n'
#
#     for order in Bb.objects.order_by('-published'):
#         s += order.title + '\n' + order.content + '\n\n'
#
#     return HttpResponse(s, content_type='text/plain; charset=utf-8')

# ###

# def index(request):
#     template = loader.get_template('bboard/index.html')
#     bbs = Bb.objects.order_by('-published')
#     context = {'bbs': bbs}
#     return HttpResponse(template.render(context, request))

# ###

# def index(request):
#     bbs = Bb.objects.order_by('-published')
#     bbs = Bb.objects.all()
#     return render(request, 'bboard/index.html', {'bbs': bbs})

# ###

# def index(request):
#     bbs = Bb.objects.all()
#     rubrics = Rubric.objects.all()
#     context = {'bbs':bbs, 'rubrics':rubrics}
#     return render(request, 'bboard/index.html', context)


def by_rubric(request, pk):
    """
    Description:
        Вьюха для сортировки по рубрикам
    Args:
        rubric_id айди рубрики в базе
    Attributes:
        bbs коллекция записей соответсвующих данной рубрике
        rubrics список всех рубрик в базе
        current_rubric имя текущей рубрики
        context словарь с bbs, rubrics, current_rubric
    """
    bbs = Bb.objects.filter(rubric=pk)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=pk)
    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'bboard/by_rubric.html', context)


class BbCreateView(CreateView):
    """
    Description:
        Вьюха для создания новой записи
    Args:
        None
    Attributes:
        template_name имя темплейта где создается запись
        form_class класс формы для создания записи
        success_url урл по которой перейдет после удачного создания
    """
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('bboard:index')  # '/bboard/'

    def get_context_data(self, **kwargs):
        """
        Description:
            Метод для внесения нового контекста
        Args:
            None
        Returns:
            context контекст с нужными переменными
        """
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['mode'] = False
        return context

def add_test(request):
    """
    Description:
        Создает форму и выводит на экран страницу добавления
    Args:
        request запрос от браузера
    Returns:
        результат метода render()
    """

    bbf = BbForm()
    context = {'form':bbf}
    return render(request, 'bboard/create.html', context)

def add_save(request):
    """
    Description:
        сохраняет данные формы от метода add()
    Args:
        request запрос
    Returns:
        HttpResponseRedirect() в случае успешного сохранения информации
        render() перенаправляет обратно на страницу создания в случае неудачи
    """

    bbf = BbForm(request.POST)
    if bbf.is_valid():
        bbf.save()
        return HttpResponseRedirect(reverse('bboard:by_rubric', 
                                    kwargs={'rubric_id':bbf.cleaned_data['rubric'].pk}))
    else:
        context = {'form':bbf, 'mode': True}
        return render(request, 'bboard/create.html', context)

@require_http_methods(['GET', 'POST'])
def add_and_save(request):
    """
    Description:
        Контроллер сочетающий в себе функцию сохранения записи и 
        передачи клиенту страницы с формой сохранения
    Args:
        request запрос от клиента
    Returns:
        HttpResponseRedirect() в случае успешного добавления записи
        render в случае неудачного
    """
    if request.method == 'POST':
        bbf = BbForm(request.POST)
        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(reverse('bboard:by_rubric',
            kwargs={'rubric_id':bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form':bbf, 'mode': True}
            return render(request, 'bboard/create.html', context)
    else:
        bbf_fabric = BbFormFromFactory()
        bbf = BbForm()
        bbf_fast = BbFormFastCreate
        context = {'form':bbf, 'form_fabric':bbf_fabric, 'form_fast': bbf_fast, 'mode': True}
        return render(request, 'bboard/create.html', context)

@require_GET
def send_me_a_file(request):
    """
    Description:
        Контроллер отправляющий файл клиенту. 
        Разблокируй as_attachment=True чтобы отослать сам файл
    Args:
        request запрос от клиента
    Returns:
        FileResponse()
    """

    file_name = os.path.join(os.getcwd(), 'bboard', 'static', 'bboard', 'test.txt')
    return FileResponse(open(file_name, 'rb') 
    # ,as_attachment=True
    )

@require_GET
def send_json(request):
    """
    Description:
        Контроллер отправляющий JSON
    Args:
        request запрос от клиента
    Returns:
        JsonResponse() отправляет JSON
    """

    return JsonResponse({'Main':'JSON', 'Content':'This is JSON response'})
    
    
class TemplateView(TemplateView):
    """
    Description:
        Класс контроллера, отрисовывающий страницу index.html
    Args:
        TemplateView наследует
    Attributes:
        get_context_data() добавляем контекст
    """
    template_name = 'bboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bbs"] =  Bb.objects.all()  
        context["rubrics"] =  Rubric.objects.all()  
        return context

class DetailViewClass(DetailView):
    """
    Description:
        Контроллер отоброжающий страницу по выбранной рубрике c детализацией
    Args:
        None
    Attributes:
        context контекст с переменными
    """

    model = Bb  

    def get_context_data(self, *args, **kwargs):
        """
        Description:
            Добавление контекста
        Args:
            context
        Returns:
            context
        """
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context
    
class BbByRubricVies(ListView):
    """
    Description:
        Класс отображающий список
        в path указан параметр rubric_id по нему и фильтруются записи
    Args:
        rubric_id номер рубрики в таблице Rubrics
        Задается в урле
    Attributes:
        template_name имя темплейта
        context_object_name в него будет сохранен извлеченный список
    """
    template_name = 'bboard/by_rubric.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])
    
    def get_context_data(self, *args, **kwargs):
        """
        Description:
            
        Args:
            None
        Returns:
            None
        """
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
        return context

class showForms(FormView):
    """
    Description:
        Контроллер обрабатывающий форму
    Args:
        
    Attributes:
        
    """
    template_name = 'bboard/create.html'
    form_class = BbForm
    initial = {'price':0.0}

    def get_context_data(self, *args, **kwargs):
        """
        Description:
            Получает и возвращает контекст
        Args:
            
        Returns:
            
        """
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context
    
    def form_valid(self, form):
        """
        Description:
            вызывается в случае успешной валидации формы
        Args:
            
        Returns:
            
        """
        form.save()
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        """
        Description:
            возвращает ссылку на используемую форму
            этот метод тут исопльзуется для того чтобы при перенаправлении
            можно было получить ключ записи
        Args:
            
        Returns:
            
        """
        self.object = super().get_form(form_class)
        return self.object
    
    def get_success_url(self):
        """
        Description:
            возвращает URL на которые перенаправляет в случае успешного заоплнения формы
        Args:
            
        Returns:
            
        """
        return reverse('bboard:by_rubric',
        kwargs={'rubric_id':self.object.cleaned_data['rubric'].pk})

class showUpdate(UpdateView):
    """
    Description:
        Контроллер достающий запись из модели и обновляющий её
    Args:
        
    Attributes:
        
    """
    model = Bb 
    form_class = BbForm

    def get_success_url(self):
        """
        Description:
            возвращает URL на которые перенаправляет в случае успешного заоплнения формы
        Args:
            
        Returns:
            
        """
        return reverse('bboard:index')


    def get_context_data(self, *args, **kwargs):
        """
        Description:
            метод достающий контекст и изменяющий его
        Args:
            
        Returns:
            
        """
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context
    
class deleteTemplate(DeleteView):
    """
    Description:
        контроллер удаляет запись 
    Args:
        
    Attributes:
        
    """
    model = Bb
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, *args, **kwargs):
        """
        Description:
            
        Args:
            
        Returns:
            
        """
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

class showTimeSort(ArchiveIndexView):
    """
    Description:
        Контроллер выводит список отсортированный по дате
    Args:
        
    Attributes:
        
    """

    model = Bb
    date_field = 'published'
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'
    allow_empte = True

    def get_context_data(self, *args, **kwargs):
        """
        Description:
            
        Args:
            
        Returns:
            
        """
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

class showByDate(DateDetailView):
    """
    Description:
        КОнтроллер выводит запись за один день
    Args:
        
    Attributes:
        
    """
    model = Bb
    date_field = 'published'
    month_format = '%m'

    def get_context_data(self, *args, **kwargs):
        """
        Description:
            
        Args:
            
        Returns:
            
        """
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

class BbByRubricView(SingleObjectMixin, ListView):
    """
    Description:
        контроллер выводящий сведения о выбранной записи и набор связанных с ней записей
    Args:
        
    Attributes:
        
    """
    template_name = 'bboard/by_rubric.html'
    pk_url_kwarg = 'rubric_id'
    
    def get(self, request, *args, **kwargs):
        """
        Description:
            Извлекаем рубрику с заданным ключом
        Args:
            
        Returns:
            
        """
        self.object = self.get_object(queryset=Rubric.objects.all())
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """
        Description:
            
        Args:
            
        Returns:
            
        """
        context = super().get_context_data(**kwargs)
        context['current_rubric'] = self.object
        context['rubrics'] = Rubric.objects.all()
        context['bbs'] = context['object_list']
        return context

    def get_query(self):
        """
        Description:
            
        Args:
            
        Returns:
            
        """
        return self.object.bb_set.all()

class viewClassTest(View):
    """
    Description:
        view test
    Args:
        
    Attributes:
        
    """
    def get(self, request, *args, **kwargs):
        """
        Description:
            
        Args:
            
        Returns:
            
        """
        return HttpResponse(f"Hello from View class args{args} kwargs{kwargs}")


def index(request):
    """
    Description:
        пагинатор
    Args:

    Returns:

    """
    rubrics = Rubric.objects.all()
    bbs = Bb.objects.all()
    paginator = Paginator(bbs, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    conext = {
        'rubrics':rubrics,
        'page':page,
        'bbs':page.object_list
    }
    return render(request, 'bboard/index.html', conext)