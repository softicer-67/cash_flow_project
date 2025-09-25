// Динамическая загрузка категорий и подкатегорий
$(document).ready(function() {
    // Загрузка категорий при изменении типа операции
    $('#id_operation_type').change(function() {
        var operationTypeId = $(this).val();
        var categoryField = $('#id_category');
        var subcategoryField = $('#id_subcategory');

        if (operationTypeId) {
            $.ajax({
                url: '/load-categories/',
                data: {
                    'operation_type_id': operationTypeId
                },
                success: function(data) {
                    categoryField.empty();
                    categoryField.append('<option value="">---------</option>');
                    $.each(data, function(index, category) {
                        categoryField.append('<option value="' + category.id + '">' + category.name + '</option>');
                    });

                    subcategoryField.empty();
                    subcategoryField.append('<option value="">---------</option>');
                },
                error: function() {
                    console.error('Ошибка загрузки категорий');
                }
            });
        } else {
            categoryField.empty();
            categoryField.append('<option value="">---------</option>');
            subcategoryField.empty();
            subcategoryField.append('<option value="">---------</option>');
        }
    });

    // Загрузка подкатегорий при изменении категории
    $('#id_category').change(function() {
        var categoryId = $(this).val();
        var subcategoryField = $('#id_subcategory');

        if (categoryId) {
            $.ajax({
                url: '/load-subcategories/',
                data: {
                    'category_id': categoryId
                },
                success: function(data) {
                    subcategoryField.empty();
                    subcategoryField.append('<option value="">---------</option>');
                    $.each(data, function(index, subcategory) {
                        subcategoryField.append('<option value="' + subcategory.id + '">' + subcategory.name + '</option>');
                    });
                },
                error: function() {
                    console.error('Ошибка загрузки подкатегорий');
                }
            });
        } else {
            subcategoryField.empty();
            subcategoryField.append('<option value="">---------</option>');
        }
    });

    // Подтверждение удаления
    $('.delete-btn').click(function(e) {
        if (!confirm('Вы уверены, что хотите удалить эту запись?')) {
            e.preventDefault();
        }
    });
});
