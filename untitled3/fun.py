import datetime

from hack.models import Project, Hacker


def active(request):
    info = ""
    if  "id" in request.GET and "time" in request.GET :
        if "pid" in request.GET:
            info="Joined Succesfully"
            get = Hacker.objects.get(id=request.GET["id"], time=request.GET["time"])
            get.active = True
            get.project = Project.objects.get(id=request.GET["pid"],privacy=True)
            get.time = datetime.datetime.now()
            get.save()

        else:
            try:
                info = "Activated Succesfully"
                get = Project.objects.get(id=request.GET["id"],time=request.GET["time"])
                get.active = True
                get.save()
            except Project.DoesNotExist:
                info="There is no such Such"
    return info




def getProjects():
    ret = Project.objects.filter(active=True);
    for r in ret:
        r.description = r.description[:60];
    return ret
