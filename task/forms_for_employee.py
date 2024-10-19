from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone

from task.models import Task
from node.models import Node
from users.models import Employee


class TaskForEmployeeForm(forms.ModelForm):
    """Form for creating a new task"""
    node_index = forms.CharField(label="Введіть індекс вузла", required=False)

    class Meta:
        model = Task
        fields = ['doer', 'node_index', 'task_description', 'deadline']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(TaskForEmployeeForm, self).__init__(*args, **kwargs)
        self.fields['doer'].queryset = Employee.objects.filter(role='Electrician')
        
        now = timezone.now().strftime('%Y-%m-%dT%H:%M')
        self.fields['deadline'].widget.attrs['min'] = now
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            self.fields['doer'].label = 'Виберіть виконавця'
            self.fields['task_description'].label = 'Опис завдання'
            self.fields['deadline'].label = 'Виконати до'

    def clean_node_index(self):
        node_index = self.cleaned_data.get('node_index')
        if node_index:
            try:
                return Node.objects.get(index=node_index)
            except Node.DoesNotExist:
                raise forms.ValidationError(f"Вузла з індексом {node_index} не знайдено.")
        return None

    def save(self, commit=True):
        instance = super(TaskForEmployeeForm, self).save(commit=False)
        instance.node = self.cleaned_data.get('node_index')
        if commit:
            instance.save()
        return instance
    