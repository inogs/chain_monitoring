from django.shortcuts import render

# Create your views here.
def view_index(request):
    return render(request, 'slideshow/index.html')