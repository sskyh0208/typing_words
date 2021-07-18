from django.http.response import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import ModelFormMixin
from .models import WordBooks, Words
from .forms import WordBooksForm, WordsForm
import os


class HomeView(TemplateView): 
    template_name = os.path.join('english', 'home.html')


class WordBooksListView(LoginRequiredMixin, ListView, ModelFormMixin):
    model = WordBooks
    form_class = WordBooksForm
    paginate_by = 5
    template_name = os.path.join('english', 'wordbooks.html')
    success_url = reverse_lazy('english:wordbooks')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user).order_by('-update_at')

    def get(self, request, *args, **kwargs):
        # ModelFormMixinには↓が必要
        self.object = None
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # formに必要な値を渡して、フォームクラス内のsave()でモデルに追加する
        form.user = self.request.user
        return super().form_valid(form)


class WordsListView(LoginRequiredMixin, ListView, ModelFormMixin):
    model = Words
    paginate_by = 20
    template_name = os.path.join('english', 'words.html')
    form_class = WordsForm

    def get_success_url(self):
        # get_success_urlはurlを返さないとだめ
        return reverse_lazy('english:words', kwargs={'pk':self.kwargs.get('pk')})

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        return queryset.filter(wordbook=self.kwargs.get('pk')).order_by('-create_at')

    def get_context_data(self, **kwargs):
        self.object = None
        context_data = super().get_context_data(**kwargs)
        context_data['wordbook'] = WordBooks.objects.filter(pk=self.kwargs.get('pk')).first()
        # 総登録単語数表示用
        context_data['count'] = Words.objects.filter(wordbook=self.kwargs.get('pk')).all().count()
        return context_data

    def get(self, request, *args, **kwargs):
        if not self.check_owner_user(kwargs.get('pk'), request.user):
            return redirect('english:wordbooks')  
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        context_data = self.get_context_data()
        form.wordbook = context_data['wordbook']
        return super().form_valid(form)

    # 単語帳の作成ユーザーか判定
    def check_owner_user(self, wordbook_id, user):
        wordbook = WordBooks.objects.filter(pk=wordbook_id, user=user).all()
        if not wordbook:
            return False
        return True
        

class TypingWordsView(DetailView):
    """タイピングゲームのビュー。

    Wordbooksに紐づく単語を、タイピングゲームとして遊べる

    """
    model = WordBooks
    template_name = os.path.join('english', 'typing.html')

    def get(self, request, *args, **kwargs):
        """ゲットアクション

        公開・非公開かかわらず、タイピングゲームのビューは一つだけなので
        Wordbooksの公開設定、リクエストユーザーとWordbooksの作者の比較で
        GETリクエストを変える。

        Returns:
            HttpResponse: 公開設定 → ok
            HttpResponse: 非公開 and リクエストユーザ == Wordbooks作者 → ok
            HttpResponse: 非公開 and リクエストユーザ != Wordbooks作者 → redirect
        """
        user = request.user
        wordbook = WordBooks.objects.filter(pk=kwargs.get('pk')).first()
        if wordbook.publish:
            # 公開設定されているwordbookの場合
            return super().get(request, *args, **kwargs)
        else:
            if user == wordbook.user:
                # 公開設定されていないけど、リクエストユーザと作者が同じ
                return super().get(request, *args, **kwargs)
            else:
                # 公開設定されていなくて、リクエストユーザと作者が違う
                return redirect('english:publish_wordbooks')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['wordbook'] = WordBooks.objects.filter(pk=self.kwargs.get('pk')).values('id', 'user', 'name', 'description').first()
        # 単語を並べ替えて入れる
        words = Words.objects.filter(wordbook=self.kwargs.get('pk')).order_by('?')
        context_data['words'] = list(words.values('id', 'wordbook', 'name', 'description'))

        return context_data
        

class PublishWordBooksListView(ListView):
    model = WordBooks
    paginate_by = 5
    template_name = os.path.join('english', 'publish_wordbooks.html')

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        return queryset.filter(publish=True).order_by('-create_at')


@login_required
def update_wordbook_publish(request):
    # words内のWordBookの公開非公開
    if request.is_ajax:
        wordbook_id = request.POST.get('wordbook_id')
        publish = True if request.POST.get('publish') == 'true' else False
        wordbook = get_object_or_404(WordBooks, id=wordbook_id)
        wordbook.publish = publish
        wordbook.save()
        if publish:
            return JsonResponse({'message': '公開に設定しました'})
        else:
            return JsonResponse({'message': '非公開に設定しました'})


@login_required
def delete_wordbook(request, pk):
    # WordBookの削除
    wordbook = WordBooks.objects.filter(pk=pk, user=request.user).first()
    if wordbook:
        wordbook.delete()
    return redirect('english:wordbooks')

@login_required
def delete_word(request, pk, wordbook_id):
    word = Words.objects.filter(pk=pk, wordbook=wordbook_id).first()
    if not word:
        return redirect('english:wordbooks')
    if word.wordbook.user == request.user:
        # wordの作成者とリクエストユーザが同じ場合のみ
        word.delete()
    return redirect('english:words', wordbook_id)