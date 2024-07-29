from django.shortcuts import render

# Create your views here.
def depart_list(request):
    return render(request,'depart_list.html')
