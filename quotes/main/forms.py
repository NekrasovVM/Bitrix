from django import forms

# source_type_choises = ((1, "Фильм"), (2, "Книга"))
source_type_choises = {1: "Фильм", 2: "Книга"}

class QuoteForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea, 
        max_length=256, 
        label="Текст", 
        help_text="Введите текст цитаты (максимум 256 символов)"
    )
    source = forms.CharField(
        max_length=48, 
        label="Источник",
        help_text="Введите название книги или фильма (максимум 256 символов)",
        widget=forms.TextInput(attrs={"class":"myfield"})
    )
    source_type = forms.TypedChoiceField(
        choices=source_type_choises,
        coerce=str,
        label="Тип источника",
    )
    weight = forms.IntegerField(
                                min_value=1,
                                max_value=100, 
                                initial=50,
                                label="Вес", 
                                help_text="Введите вес цитаты. Чем выше вес, тем больше шанс выдачи на главной странице",
                                widget=forms.NumberInput(attrs={"class":"myfield"})
    )
    required_css_class = "field"
    error_css_class = "error"

    # name = forms.CharField(min_length=3, widget=forms.TextInput(attrs={"class":"myfield"}))
    # age = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={"class":"myfield"}))
    # required_css_class = "field"
    # error_css_class = "error"