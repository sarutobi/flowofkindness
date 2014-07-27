# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, get_object_or_404

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.template import RequestContext

from core.mixins import (
    PaginatorMixin, QueryStringMixin, ExternalScriptsMixin)
from core.models import Infopage


class RyndaCreateView(CreateView):
    pass


class RyndaDetailView(ExternalScriptsMixin, DetailView):
    pass


class RyndaListView(QueryStringMixin, PaginatorMixin, ListView):
    paginator_url = None
    list_title_short = None

    def get_paginator_url(self):
        if self.paginator_url is None:
            raise Exception(
               "You MUST define paginator_url or overwrite get_paginator_url()")
        return self.paginator_url

    def get_context_data(self, **kwargs):
        context = super(RyndaListView, self).get_context_data(**kwargs)
        context['paginator_url'] = self.get_paginator_url()
        sc = self.paginator(
            context['paginator'].num_pages,
            page=context['page_obj'].number)
        context['paginator_line'] = sc
        context['listTitleShort'] = self.list_title_short
        return context


class RyndaFormView(FormView):
    pass


def about(request):
    return render(
        request,
        'about.html',)


def show_page(request, slug):
    page = get_object_or_404(Infopage, slug=slug)
    pages = Infopage.objects.filter(
        active=True).exclude(slug=slug).values('slug', 'title')
    return render_to_response(
        'infopage/show_page.html',
        {'title': page.title, 'text': page.text, 'pages': pages, },
        context_instance=RequestContext(
            request,
        )
    )


def index_info(request):
    page = get_object_or_404(Infopage, default=True)
    pages = Infopage.objects.filter(
        active=True,
        default=False).values('slug', 'title')
    return render_to_response(
        'infopage/show_page.html',
        {'title': page.title, 'text': page.text, 'pages': pages, },
        context_instance=RequestContext(
            request,
        )
    )
