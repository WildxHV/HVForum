from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from home.models import Categories
from threads.models import Discussions,Comments
from django.contrib import messages

# Create your views here.
def threads(request):
    Id = request.GET['Id']
    if request.method == 'POST':
        queTitle = request.POST['queTitle']
        queDesc = request.POST['queDesc']
        catId = Id
        username = request.user
         
        que = Discussions(queTitle= queTitle , queDesc=queDesc,catId=catId,username= username )
        que.save()
        if que:
            messages.success(request,'Your question has been successfully posted, wait for the community to respond !')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        else:
            messages.error(request,'Try posting the question again!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

    else:
        category = Categories.objects.get(catId=Id)
        alldiscussions = Discussions.objects.filter(catId=Id)
        title = category.title
        context = {
            'category' :category,
            'title': title,
            'alldiscussions' : alldiscussions
        }
        return render(request, "threads/threads.html",context)
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


    

def discussions(request):
    queId = request.GET['queId']
    if request.method == 'POST':
        comment = request.POST['comment']
        queId = queId
        username = request.user
         
        comment = Comments(comment= comment,queId=queId,username= username )
        comment.save()
        if comment:
            messages.success(request,'Your comment has been successfully posted !')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        else:
            messages.error(request,'Try posting the comment again!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

    else:
        question = Discussions.objects.get(queId=queId)
        allcomments = Comments.objects.filter(queId=queId)
        title = "Discussions"
        context = {
            'question' :question,
            'title': title,
            'allcomments' : allcomments
        }
        return render(request, "threads/discussions.html",context)



