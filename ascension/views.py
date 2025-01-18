import logging
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views import View, generic
from django.shortcuts import render, get_object_or_404, redirect

from .forms import InquiryForm, CreateLearningGoalForm
from .models import InterestCategory, LearningGoal, LearningPlan


logger = logging.getLogger(__name__)

class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True
    def test_func(self):
        # URLに埋め込まれた主キーから日記データを一件取得。取得できなければ404エラー
        diary = get_object_or_404(InterestCategory, pk=self.kwargs['pk'])
        # ログインユーザーと日記の作成ユーザーを比較して、異なればraise_exceptionの設定を行う
        return self.request.user == diary.user
    

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


# 興味分野の表示
class InterestListView(LoginRequiredMixin, generic.ListView):
    model = InterestCategory
    template_name = 'interest_list.html'

    def get_queryset(self):
        return InterestCategory.objects.prefetch_related('users').filter(users=self.request.user)


# 興味分野の追加
class AddInterestCategoryView(LoginRequiredMixin, generic.CreateView):
    model = InterestCategory
    template_name = 'add_interest_category'


# 学習目標の表示
class LearningGoalByCategoryView(LoginRequiredMixin, generic.ListView):
    model = LearningGoal
    template_name = 'learning_goal_by_category.html'
    context_object_name = 'learning_goals'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return LearningGoal.objects.filter(user=self.request.user, category_id=category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        context["category"] = get_object_or_404(InterestCategory, id=category_id)
        return context


# 学習目標の作成
class CreateLearningGoal(LoginRequiredMixin, generic.CreateView):
    model = LearningGoal
    form_class = CreateLearningGoalForm
    template_name = 'create_learning_goal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        context['category'] = get_object_or_404(InterestCategory, id=category_id)
        context["learning_goal"] = self.object
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        category_id = self.kwargs.get('category_id')  # URLからid取得
        form.instance.category = get_object_or_404(InterestCategory, id=category_id)  # categoryをセット
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('ai_support:generate_plan_preview', kwargs={'learning_goal_id': str(self.object.id)})

# 学習目標の決定
class SaveSelectedLearningPlanView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        selected_topics = request.POST.getlist('selected_topics')
        learning_goal_id = self.kwargs.get('learning_goal_id')

        learning_goal = get_object_or_404(LearningGoal, 
                                          id=learning_goal_id, 
                                          user=request.user)
        
        for topic in selected_topics:
            LearningPlan.objects.create(
                user=request.user,
                learning_goal=learning_goal,
                topic=topic
            )
        return redirect('learning_plan_list',learning_goal_id=learning_goal.id)

# 学習目標の表示
class LearningPlanListView(LoginRequiredMixin, generic.ListView):
    model = LearningPlan
    template_engine = 'learning_plan_list.html'

    def get_queryset(self):
        learning_goal_id = self.kwargs.get('learning_goal_id')
        return LearningPlan.objects.filter(user=self.request.user, 
                                           learning_goal_id=learning_goal_id
                                           )
