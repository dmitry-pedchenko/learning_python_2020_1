from django.forms import ModelForm, modelform_factory, DecimalField
from django.forms.widgets import Select
from .models import Bb
from django import forms
from .models import Rubric
import django


class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')


BbFormFromFactory = modelform_factory(
    Bb,
    fields=('title', 'content', 'price', 'rubric'),
    labels={'title': 'Название товара'},
    help_texts={'rubric': 'Не забудьте выбрать рубрику'},
    field_classes={'price': DecimalField},
    widgets={'rubric': Select(attrs={'size': 8})}
)


class BbFormFastCreate(ModelForm):
    """
    Description:
        Быстрое объявление класса формы
    Args:
        
    Attributes:
        
    """
    class Meta:
        """
        Description:
            здесь теже параметры с тем же смыслом
        Args:
            
        Attributes:
            
        """
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')
        labels = {'title': 'Название товара'}
        help_texts = {'rubric': 'Не забудьте выбрать рубрику'}
        field_classes = {'price': DecimalField}
        # widgets = {'rubric': Select(attrs={'size': 4})}
        widgets = {'rubric': django.forms.widgets.RadioSelect}


class FullCreateForm(forms.ModelForm):
    """
    Description:
        Полное описание создания класса Form
    Args:

    Attributes:

    """
    title = forms.CharField(label='Название товара')
    content = forms.CharField(label='Описание',
                              widget=forms.widgets.Textarea()
                              )
    price = forms.DecimalField(label='Цена', decimal_places=2)
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
                                    label='Рубрика',
                                    help_text='Не забудьте задать рубрику',
                                    widget=forms.widgets.Select(attrs={'size': 8})
                                    )

    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')
