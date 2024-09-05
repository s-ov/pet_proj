from django import forms
from .models import Node, NodeMotor


class NodeCreationForm(forms.ModelForm):
    """Form for creating a Node."""

    class Meta:
        model = Node
        fields = ['name', 'index', 'level', 'motor', 'mcc']
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
            'index': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1_1_1_1_1'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'motor': forms.Select(attrs={'class': 'form-control'}),
            'mcc': forms.Select(attrs={'class': 'form-control'}),
        }
       
        labels = {  
            'name': 'Назва',
            'index': 'Індекс',
            'level': 'Відмітка',
            'motor': 'Мотор',
            'mcc': 'MCC'
        }

class NodeMotorCreationForm(forms.ModelForm):
    """Form for creating a motor for the Node."""
    
    class Meta:
        model = NodeMotor
        fields = ['power', 'round_per_minute', 'connection', 'amperage',]
       
        labels = {  
            'power': 'Потужність',
            'round_per_minute': 'Обороти на хвилину',
            'connection': 'Тип з\'єднання',
            'amperage': 'Сила струму',
        }
