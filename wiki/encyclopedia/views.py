from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import random
from random import choice   
import markdown2
from . import util

class createcontent(forms.Form):
    title = forms.CharField(label="Title")
    markdowncontent = forms.CharField(label="MarkDown Content",
    widget = forms.Textarea(attrs={'class':'content'}))

class editcontent(forms.Form):
    title = forms.CharField(label="Title")
    markdowncontent = forms.CharField(label="MarkDown Content",
    widget = forms.Textarea(attrs = {'class':'editedcontent'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request,title):
    entries =  util.get_entry(title)
    return render(request,"encyclopedia/wiki.html",{
        "entries": markdown2.markdown(util.get_entry(title)),
        "entrytitle": title,
    })


def create(request):
    if request.method == "POST":
        form = createcontent(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            markdowncontent=form.cleaned_data["markdowncontent"]
            entry= util.list_entries().copy()
            entrycounter = 0
            for var in entry:
                if var == title:
                    entrycounter = 1
                    break
                else:
                    entrycounter = 0
            if entrycounter == 1:
                messages.error(request,' already exists')
                return render(request,"encyclopedia/create.html",{
                "form": form})
            else:
                util.save_entry(title,markdowncontent)
                return HttpResponseRedirect(f"/wiki/{title}")
        else:
            return render(request,"encyclopedia/create.html",{
                "form":form
            })
    return render(request,"encyclopedia/create.html",{
        "form":createcontent()
    })

def randome(request):
    entry = util.list_entries().copy()
    randomname = random.choice(entry)
    return render(request,"encyclopedia/randome.html",{
        "entries": markdown2.markdown(util.get_entry(randomname)),
        "entrytitle": randomname
    })

def search(request):
    if request.method == "GET":
        q = request.GET['q']
        if util.get_entry(q):
            return render(request,"encyclopedia/search.html",{
            "entries":markdown2.markdown( util.get_entry(q)),
            "entrytitle": q
            })
        else:
            listitems = util.list_entries()
            filtered_list=[]
            for entry in listitems:
                if str(q.lower()) in str(entry.lower()):
                    filtered_list.append(entry)
            if not filtered_list:
                return render(request,"encyclopedia/search.html",{
                "message": "No Result Matched Your Search"
                })
            return render(request,"encyclopedia/search.html",{
            "entry": filtered_list
            })
    return render(request,"encyclopedia/search.html")

def edit(request,title):
    inital_content = util.get_entry(title)
    form1 = editcontent()
    form1.fields["markdowncontent"].initial = inital_content
    form1.fields["title"].initial = title
    if request.method == "POST":
        form = editcontent(request.POST)
        if form.is_valid():
            markdowncontent = form.cleaned_data["markdowncontent"]
            title = form.cleaned_data["title"]
            util.save_entry(title,markdowncontent)
            initalcontent = util.get_entry(title)
            return HttpResponseRedirect(reverse('wiki', args=[title]))
    return render(request,"encyclopedia/edit.html",{
            "form": form1,
            "title": title
    })