"""
    Description:
        Маршрутизация для приложения bboard
    Attributes:
        urlpatterns коллекция с путями до контроллеров
    Example:
        None
"""


from django.urls import path
from bboard import views
from .views import BbCreateView

app_name = 'bboard'
urlpatterns = [
    path('<int:pk>/', views.by_rubric, name='by_rubric'),
    path('', views.index, name='index'),
    path('add/', BbCreateView.as_view(), name='add'),
    path('add_test/', views.add_test, name='add_test'),
    path('add/save/', views.add_save, name='add_save'),
    path('add_and_save/', views.add_and_save, name='aas'),
    path('send_me_a_file/', views.send_me_a_file, name='send_file'),
    path('send_json/', views.send_json, name='send_json'),
    path('templateview_class/', views.TemplateView.as_view(), name='template_view'),
    path('detail_view_show/<int:pk>/', views.DetailViewClass.as_view(), name='detail'),
    path('show_list/<int:rubric_id>/', views.BbByRubricVies.as_view(), name = 'show_list'),
    path('show_forms/', views.showForms.as_view(), name = 'show_view'),
    path('show_update/<int:pk>', views.showUpdate.as_view(), name='show_update'),
    path('delete_test/<int:pk>', views.deleteTemplate.as_view(), name='delete_template'),
    path('show_time_sort/', views.showTimeSort.as_view(), name='time_sort'),
    path('show_by_date/<int:year>/<int:month>/<int:day>/<int:pk>/', views.showByDate.as_view(), name='show_by_date'),
    path('view_class_test/<int:arg>', views.viewClassTest.as_view(), name='as-view')
]
