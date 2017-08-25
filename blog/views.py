from django.shortcuts import render,redirect
from . import models


# Create your views here.


def index(request):
    articles = models.Article.objects.all()
    return render(request, 'blog/index.html', {'articles': articles})


def article_page(request, article_id):
    article = models.Article.objects.get(pk=article_id)
    return render(request, 'blog/article_page.html', {'article': article})


def article_change(request, article_id):
    if str(article_id) == '0':
        request.session["Post"] = "allow"
        return render(request, 'blog/add_page.html')
    else:
        article = models.Article.objects.get(pk=article_id)
        return render(request, 'blog/add_page.html', {'article': article})


def edt_action(request):
    alert = "yes"
    title = request.POST.get('title', 'TITLE')
    content = request.POST.get('content', 'CONTENT')
    time = request.POST.get('time', 'TIME')
    article_id = request.POST.get('article_id', '0')
    try:
        article = models.Article.objects.get(title=title)
        exist = True
    except:
        exist = False
    if not exist or (article_id != 0 and str(article.id) == str(article_id)):
        request.session["alert"] = "Yes"
        if str(article_id) == '0':
            if request.session["Post"] == "allow":
                models.Article.objects.create(title=title, content=content, time=time)
                request.session["Post"] = "disable"
        else:
            article = models.Article.objects.get(pk=article_id)
            article.title = title
            article.content = content
            article.save()
        return redirect('/index/')
    else:
        alert = "warning"
        if str(article_id) == '0':
            if request.session["Post"] == "allow":
                request.session['Post'] = "disable"
                return render(request, 'blog/add_page.html', {'Alert': alert})
            else:
                return redirect('/index/edt/0/')
        else:
            request.session['Post'] = "disable"
            return render(request, 'blog/add_page.html', {'Alert': alert, 'article': models.Article.objects.get(pk=article_id)})


def delete(request, article_id):
    models.Article.objects.filter(pk=article_id).delete()
    return redirect('/index/')