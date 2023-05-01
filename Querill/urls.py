"""
URL configuration for Querill project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.urls import path
from Query.views import get_chat_completions
from ContextQuery.views import get_chat_completions_with_context, view_pdf
from pdf_app.views import display_pdf
urlpatterns = [
    path('chat/', get_chat_completions, name='chat_completions'),
    path('contextchat/', get_chat_completions_with_context, name='chat_completions_with_context'),
    path('display_pdf/<str:document_number>/', display_pdf, name='display_pdf'),
]

