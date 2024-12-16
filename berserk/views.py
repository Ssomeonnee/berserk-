from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from typing import Any

from berserk.models import BerserkCharacter #просто делаю импорт из models

# Create your views here.

class ShowBerserkCharactersView(TemplateView):
    template_name = "show_berserk_personalities.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context['personalities'] = BerserkCharacter.objects.all()
    
        return context


