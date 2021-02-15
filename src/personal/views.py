from django.shortcuts import render

# Create your views here.


def home_screen(request):
	content = {}
	return render(request, 'personal/home.html', content)
