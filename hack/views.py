import datetime
import hashlib
from _hashlib import openssl_md5

import time
from django.core.mail.message import EmailMultiAlternatives
from django.db.models.aggregates import Sum
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlencode

from hack.forms import ProjectForm, JoinForm
from hack.models import Project, Hacker
from untitled3.fun import active, getProjects


def send_activision(to, id, time):
    html_content = render_to_string('email.html', {"url": urlencode({'id': id, 'time': time})})  # ...
    text_content = strip_tags(html_content)  # this strips the html, so people will have the text as well.
    msg = EmailMultiAlternatives(to, text_content, "no-reply@smartstuff.me", [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_join(to, pid, uid, time):
    html_content = render_to_string('join.html', {"url": urlencode({'id': uid, 'pid': pid, 'time': time})})  # ...
    text_content = strip_tags(html_content)  # this strips the html, so people will have the text as well.
    msg = EmailMultiAlternatives(to, text_content, "no-reply@smartstuff.me", [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def getStat():

    maxx=Project.objects.filter(active=True).aggregate(max=Sum('people_limit'))["max"]
    ppl=Hacker.objects.exclude(project=None).filter(project__active=True).count()
    return {"mem":ppl, "max":maxx}


def sex(pussy):
    for dick in pussy:
        dick.email=dick.email.split("@")[0]
    return pussy

def proform(request):
    form = ProjectForm(request.POST)
    if form.is_bound and not form.is_valid():
        return render(request, "../templates/form.html",
                      {"errors": form.errors, "form": form, "title": "Project Registration Form"})
    else:
        model = form.save(commit=False)
        model.time = datetime.datetime.now()
        model.save()
        key = model.pk
        send_activision(form.data['email'], key, model.time )
        print(model.time)
        return render(request, "../templates/index.html", {"title" : "Scruffy Hackaton 2017", "info" : "You registered your project - I am very proud of you", "projects":getProjects() });

    return render(request, "../templates/form.html", {"form": ProjectForm(), "title": "Project Registration Form"});


def project(request, ide):
    proj = Project.objects.get(id=ide);
    join = JoinForm(request.POST);

    if join.is_bound and join.is_valid() and proj.privacy:
        model=None
        try:
            model=Hacker.objects.get(email=join.cleaned_data["email"])
        except Hacker.DoesNotExist:
            model=Hacker(email=join.cleaned_data["email"])
            pass
        model.time = datetime.datetime.now()
        model.save()
        send_join(model.email,ide,model.pk,model.time)
        return render(request, "../templates/index.html",
                      {"title": "Scruffy Hackaton 2017", "info": "Check your email for registration confirmation", "projects": getProjects(), "stat": getStat()});

    members = Hacker.objects.filter(project=proj);

    return render(request, "../templates/project.html",
                  {"project": proj, "join" :join, "members" : sex(members)});

def main(request):
    info = ""
    info +=active(request);
    return render(request, "../templates/index.html", {"title" : "Scruffy Hackaton 2017","info" : info, "projects":getProjects(), "stat" : getStat() });

def edit(request):
    insta = Project.objects.get(id=request.GET['id'], time=request.GET['time']);

    if request.method == "POST":
        join = ProjectForm(request.POST, instance=insta);
        if join.is_valid():
            join.save();
            return render(request, "../templates/index.html", {"title": "Scruffy Hackaton 2017",
                                                               "info": "Project Updated!",
                                                               "projects": getProjects()});
        else:
            return render(request, "../templates/form.html", {"form": join, "title": "Project Registration Form"});

    else:
        join = ProjectForm(instance=insta);
        return render(request, "../templates/form.html", {"form": join, "title": "Project Registration Form"});





def delete(request):
    info = "You removed your project succesfully ;-"

    get = Project.objects.get(id=request.GET['id'],time=request.GET['time']).delete()

    return render(request, "../templates/index.html",
                  {"title": "Scruffy Hackaton 2017", "info": info, "projects": getProjects(), "stat": getStat()});