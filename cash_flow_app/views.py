from django.shortcuts import render, get_object_or_404, redirect  # ✅ Добавить redirect
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages  # ✅ Импорт messages
from .models import CashFlow, Status, OperationType, Category, Subcategory
from .forms import CashFlowForm


def cash_flow_list(request):
    cash_flows = CashFlow.objects.all().order_by('-created_date')

    # Фильтрация
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    status_id = request.GET.get('status')
    operation_type_id = request.GET.get('operation_type')
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')

    if date_from:
        cash_flows = cash_flows.filter(created_date__gte=date_from)
    if date_to:
        cash_flows = cash_flows.filter(created_date__lte=date_to)
    if status_id:
        cash_flows = cash_flows.filter(status_id=status_id)
    if operation_type_id:
        cash_flows = cash_flows.filter(operation_type_id=operation_type_id)
    if category_id:
        cash_flows = cash_flows.filter(category_id=category_id)
    if subcategory_id:
        cash_flows = cash_flows.filter(subcategory_id=subcategory_id)

    # Подсчет итогов
    total_amount = 0
    income_total = 0
    expense_total = 0

    for cf in cash_flows:
        if cf.operation_type.name == 'Пополнение':
            total_amount += cf.amount
            income_total += cf.amount
        else:  # Списание
            total_amount -= cf.amount
            expense_total += cf.amount

    balance = income_total - expense_total

    context = {
        'cash_flows': cash_flows,
        'statuses': Status.objects.all(),
        'operation_types': OperationType.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
        'total_amount': total_amount,
        'income_total': income_total,
        'expense_total': expense_total,
        'balance': balance,
        'filters': {
            'date_from': date_from or '',
            'date_to': date_to or '',
            'status': status_id or '',
            'operation_type': operation_type_id or '',
            'category': category_id or '',
            'subcategory': subcategory_id or '',
        }
    }
    return render(request, 'cash_flow_app/list.html', context)


def cash_flow_create(request):
    if request.method == 'POST':
        form = CashFlowForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись успешно создана!')
            return redirect('cash_flow_list')
    else:
        form = CashFlowForm()

    return render(request, 'cash_flow_app/form.html', {'form': form, 'title': 'Создать запись'})


def cash_flow_edit(request, pk):
    cash_flow = get_object_or_404(CashFlow, pk=pk)

    if request.method == 'POST':
        form = CashFlowForm(request.POST, instance=cash_flow)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись успешно обновлена!')
            return redirect('cash_flow_list')
    else:
        form = CashFlowForm(instance=cash_flow)

    return render(request, 'cash_flow_app/form.html', {'form': form, 'title': 'Редактировать запись'})


def cash_flow_delete(request, pk):
    cash_flow = get_object_or_404(CashFlow, pk=pk)
    if request.method == 'POST':
        cash_flow.delete()
        messages.success(request, 'Запись успешно удалена!')
        return redirect('cash_flow_list')

    return render(request, 'cash_flow_app/confirm_delete.html', {'cash_flow': cash_flow})


def reference_books(request):
    statuses = Status.objects.all()
    operation_types = OperationType.objects.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()

    # Обработка всех действий
    if request.method == 'POST':
        # Добавление статуса
        if 'add_status' in request.POST:
            name = request.POST.get('status_name')
            if name and name.strip():
                Status.objects.get_or_create(name=name.strip())
                messages.success(request, 'Статус успешно добавлен!')

        # Редактирование статуса
        elif 'edit_status' in request.POST:
            status_id = request.POST.get('edit_status_id')
            new_name = request.POST.get('edit_status_name')
            if status_id and new_name and new_name.strip():
                try:
                    status = Status.objects.get(id=status_id)
                    status.name = new_name.strip()
                    status.save()
                    messages.success(request, 'Статус успешно обновлен!')
                except Status.DoesNotExist:
                    messages.error(request, 'Статус не найден!')

        # Удаление статуса
        elif 'delete_status' in request.POST:
            status_id = request.POST.get('delete_status_id')
            if status_id:
                try:
                    status = Status.objects.get(id=status_id)
                    if CashFlow.objects.filter(status=status).exists():
                        messages.error(request,
                                       f'Нельзя удалить статус "{status.name}", так как он используется в записях!')
                    else:
                        status.delete()
                        messages.success(request, 'Статус успешно удален!')
                except Status.DoesNotExist:
                    messages.error(request, 'Статус не найден!')

        # ... остальной код для типов, категорий и подкатегорий ...

        return redirect('reference_books')

    return render(request, 'cash_flow_app/reference_books.html', {
        'statuses': statuses,
        'operation_types': operation_types,
        'categories': categories,
        'subcategories': subcategories,
    })


# AJAX views для динамической загрузки категорий и подкатегорий
def load_categories(request):
    operation_type_id = request.GET.get('operation_type_id')
    categories = Category.objects.filter(operation_type_id=operation_type_id)
    return JsonResponse(list(categories.values('id', 'name')), safe=False)


def load_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id)
    return JsonResponse(list(subcategories.values('id', 'name')), safe=False)
