import logging
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render

from .forms import InquiryForm 

logger = logging.getLogger(__name__)

# Create your views here.
# トップ画面
class IndexView(generic.TemplateView):
    template_name = 'index.html'

# 問い合わせフォーム
class InquiryViwe(generic.FormView):
    template_name = 'inquiry.html'
    form_class = InquiryForm
    success_url = reverse_lazy('ascension:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logging.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)
