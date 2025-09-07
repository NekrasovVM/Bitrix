from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.core import serializers

import asyncio
from random import choices

from .forms import QuoteForm
from .models import Quote, acreate_quote

# главная страница, выбор случайной цитаты и её вывод
def index(request):

    weights = Quote.objects.all().values("id", "weight")
    # выбор в соответствии с вероятностным распределением
    selected_id = choices([o["id"] for o in weights], weights=[o["weight"] for o in weights])[0]

    quote = Quote.objects.get(id=selected_id)
    quote.views += 1

    Quote.objects.filter(id=selected_id).update(views=quote.views)

    return render(request, "index.html", context={"quote": quote})

# добавления цитаты
def addition(request):
    # отправка формы
    if request.method == "POST":
        quoteform = QuoteForm(request.POST)
        if quoteform.is_valid():
            text = quoteform.cleaned_data["text"]
            source = quoteform.cleaned_data["source"]
            source_type = quoteform.cleaned_data["source_type"]
            weight = quoteform.cleaned_data["weight"]

            
            authors_quotes = Quote.objects.filter(source=source)
            # Согласно ТЗ, у одного источника не должно быть одновременно больше трех цитат
            if len(authors_quotes) > 2 :
                return render(request, "error.html", {"error": "Один источник не может иметь более 3 цитат!"})

            try:
                asyncio.run(acreate_quote(text, source, source_type, weight))
            # обработка случая, если цитата уже есть в базе
            except IntegrityError as e:
                print(e.args[0])
                if 'UNIQUE constraint' in e.args[0]:
                    return render(request, "error.html", {"error": "Такая цитата уже есть в базе!"})

            return redirect("/")
        else:
            return HttpResponse("Invalid data")
    
    # отрисовка страницы с формой
    else:
        quoteform = QuoteForm()
        return render(request, "addition.html", {"form": quoteform})

def top(request):
    # цитаты сортируются в порядке убывания лайков и отбираются 10 с наибольшим значением
    quotes = Quote.objects.order_by("-likes")[:10]

    print(quotes)

    return render(request, "top.html", context={"quotes": quotes})

# обработчик кнопки лайка
def like(request, id):
    quote = get_object_or_404(Quote, id=id)
    quote.likes += 1

    Quote.objects.filter(id=id).update(likes=quote.likes)

    return redirect("/")

# обработчик кнопки дизлайка
def dislike(request, id):
    quote = get_object_or_404(Quote, id=id)
    quote.dislikes += 1

    Quote.objects.filter(id=id).update(dislikes=quote.dislikes)

    return redirect("/")
