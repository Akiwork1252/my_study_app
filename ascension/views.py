import logging
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View, generic
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, get_object_or_404, redirect

from .forms import InquiryForm, CreateLearningGoalForm, AddInterestCategoryForm
from .models import InterestCategory, LearningGoal, LearningPlan, UserInterest


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
    template_name = 'ascension/index.html'


# 問い合わせフォーム
class InquiryView(generic.FormView):
    template_name = 'ascension/inquiry.html'
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
    template_name = 'ascension/interest_list.html'

    def get_queryset(self):
        return InterestCategory.objects.prefetch_related('users').filter(users=self.request.user)


# 興味分野の追加
class AddInterestCategoryView(LoginRequiredMixin, generic.FormView):
    form_class = AddInterestCategoryForm
    template_name = 'ascension/add_interest_category.html'
    success_url = reverse_lazy('ascension:interest_list')

    def form_valid(self, form):
        # フォームから選択されたカテゴリーを取得
        selected_category = form.cleaned_data['category']
        # InterestCategoryを取得or作成
        interest_category, created = InterestCategory.objects.get_or_create(
            name=selected_category.name
        )
        # 関連付け
        UserInterest.objects.get_or_create(
            user=self.request.user,
            category=interest_category
        )
        return super().form_valid(form)


# 学習目標の表示
class LearningGoalByCategoryView(LoginRequiredMixin, generic.ListView):
    model = LearningGoal
    template_name = 'ascension/learning_goal_by_category.html'
    context_object_name = 'learning_goals'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return LearningGoal.objects.filter(user=self.request.user, category_id=category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        context["category"] = get_object_or_404(InterestCategory, id=category_id)
        return context


# 学習目標の作成(一次)
class CreateLearningGoal(LoginRequiredMixin, generic.CreateView):
    model = LearningGoal
    form_class = CreateLearningGoalForm
    template_name = 'ascension/create_learning_goal.html'

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

# 学習プランの保存
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
        return redirect('ascension:learning_plan_list',learning_goal_id=learning_goal.id)

# 学習プランの表示(講義、テスト選択画面)
class LearningPlanListView(LoginRequiredMixin, generic.ListView):
    model = LearningPlan
    template_name = 'ascension/learning_plan_list.html'

    def get_queryset(self):
        learning_goal_id = self.kwargs.get('learning_goal_id')
        return LearningPlan.objects.filter(user=self.request.user, 
                                           learning_goal_id=learning_goal_id
                                           ).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        learning_goal_id = self.kwargs.get('learning_goal_id')
        learning_goal = get_object_or_404(LearningGoal, id=learning_goal_id)
        category = learning_goal.category
        context['learning_goal_id'] = learning_goal_id
        context['category_id'] = learning_goal.category.id
        context['category_name'] = category.name
        first_incomplete_plan = LearningPlan.objects.filter(
            user=self.request.user,
            learning_goal_id=learning_goal_id,
            completed=False
        ).order_by('id').first()
        context['learning_plan_id'] = first_incomplete_plan.id if first_incomplete_plan else None
        return context
    

# 興味分野の削除(関連付けの削除)
class CategoryUnlinkView(LoginRequiredMixin, View):
    # 確認画面表示
    def get(self, request, *args, **kwargs):
        category = get_object_or_404(InterestCategory, id=kwargs['category_id'])
        return render(request, 'ascension/category_delete.html', {'category': category})

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        # urlから削除カテゴリを取得
        category = get_object_or_404(InterestCategory, id=kwargs['category_id'])
        # ユーザーとカテゴリの関連付け削除
        if request.user.interests.filter(id=category.id).exists():
            request.user.interests.remove(category)
            messages.success(request, f'{category.name}をあなたの興味分野から削除しました。')
        else:
            messages.warning(request, f'{category.name}は関連付けられていません。')

        return redirect('ascension:interest_list')


# 学習目標の削除
class LearningGoalDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = LearningGoal
    template_name = 'ascension/learning_goal_delete.html'
    pk_url_kwarg = 'learning_goal_id'

    def get_success_url(self):
        learning_goal = self.get_object()
        category_id = learning_goal.category.id
        return reverse('ascension:learning_goal_by_category', kwargs={'category_id': category_id})
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        learning_goal = get_object_or_404(LearningGoal, id=self.kwargs.get('learning_goal_id'))
        category = learning_goal.category
        context['learning_goal_title'] = learning_goal.title
        context['category_id'] = learning_goal.category.id
        return context
