from django import forms
from .models import CashFlow, Status, OperationType, Category, Subcategory


class CashFlowForm(forms.ModelForm):
    class Meta:
        model = CashFlow
        fields = ['created_date', 'status', 'operation_type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'created_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'operation_type': forms.Select(attrs={'class': 'form-control', 'id': 'id_operation_type'}),
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'id_category'}),
            'subcategory': forms.Select(attrs={'class': 'form-control', 'id': 'id_subcategory'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Сделать поля обязательными
        self.fields['amount'].required = True
        self.fields['operation_type'].required = True
        self.fields['category'].required = True
        self.fields['subcategory'].required = True

        # Динамическая загрузка категорий и подкатегорий
        if 'operation_type' in self.data:
            try:
                operation_type_id = int(self.data.get('operation_type'))
                self.fields['category'].queryset = Category.objects.filter(operation_type_id=operation_type_id)
            except (ValueError, TypeError):
                self.fields['category'].queryset = Category.objects.none()
        elif self.instance.pk:
            self.fields['category'].queryset = self.instance.operation_type.category_set.all()
        else:
            self.fields['category'].queryset = Category.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                self.fields['subcategory'].queryset = Subcategory.objects.none()
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set.all()
        else:
            self.fields['subcategory'].queryset = Subcategory.objects.none()