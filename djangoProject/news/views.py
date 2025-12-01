from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from news.forms import NewsModelForm, CommentsModelForm
from news.models import News, Comment


def index_start(request):
    title = "Главная страница"
    latest_news = News.objects.all().order_by('-date_published')[:3]
    return render(request, 'news/index.html', {'news': latest_news, 'title': title})


def index(request):
    newss = News.objects.all()
    search = request.GET.get('search')
    if search:
        newss = News.objects.filter(title__icontains=search)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        newss = newss.filter(date_published__gte=start_date)
    if end_date:
        newss = newss.filter(date_published__lte=end_date)

    paginator = Paginator(newss, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    title = "Новости"
    return render(request, 'news/news_list.html', {'page_obj': page_obj, 'title': title})


def detail(request, pk):
    newss = News.objects.all()
    news = newss.get(pk=pk)
    title = news.title

    count = str(request.GET.get('post'))
    comments = Comment.objects.filter(news=news).order_by("-date_published")

    if count == "prev":
        if news.id == newss.first().id:
            return redirect("news:news_detail", pk=newss.last().id)
        prev_news = newss.filter(id__lt=news.id).last()
        return redirect("news:news_detail", pk=prev_news.id)
    if count == "next":
        if news.id == newss.last().id:
            return redirect("news:news_detail", pk=newss.first().id)
        next_news = newss.filter(id__gt=news.id).first()
        return redirect("news:news_detail", pk=next_news.id)

    context = {
        "news": news,
        "title": title,
        "comments": comments
    }

    if request.method == "POST":
        form = CommentsModelForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.news = news
            new_comment.save()
            return redirect("news:news_detail", pk=pk)
    else:
        form = CommentsModelForm()
    context["form"] = form
    return render(request, 'news/news_detail.html', context)


@login_required
def create_news(request):
    title = "Создание поста"
    action = "Создать"
    if request.method == 'POST':
        form = NewsModelForm(request.POST, request.FILES)
        if form.is_valid():
            new_news = form.save(commit=False)
            new_news.author = request.user
            new_news.date_published = datetime.now()
            new_news.save()
            return redirect("news:index")
    else:
        form = NewsModelForm()
    return render(request, 'news/create_update_news.html', {'title': title, 'form': form, 'action': action})


def update_news(request, pk):
    action = "Обновить"
    news = News.objects.get(pk=pk)
    title = f"Редактирование {news.title}"
    if request.method == 'POST':
        form = NewsModelForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect("news:news_detail", pk=pk)
    else:
        form = NewsModelForm(instance=news)
    return render(request, 'news/create_update_news.html', {'title': title, 'form': form, 'action': action})


def contacts(request):
    title = "Контакты"
    return render(request, 'news/contacts.html', {'title': title})
