from django.shortcuts import render, redirect
from .models import Tutorial, TutorialCategory, TutorialSeries
from .forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import  HttpResponse
# Create your views here.


def single_slug(request, single_slug):

    cat = [c.cat_slug for c in TutorialCategory.objects.all()]
    if single_slug in cat:
        # from models.py we look and get what connected with ForignKeys
        matching_series = TutorialSeries.objects.filter(tutorial_cat__cat_slug=single_slug)
        series_urls = {}
        for m in matching_series.all():
            part_one = Tutorial.objects.filter(tutorial_seires__tutorial_series=m.tutorial_series).earliest('published')
            series_urls[m] = part_one.tutorial_slug
        return render(request, 'main/category.html', {'part_one': series_urls})

    tutorial = [t.tutorial_slug for t in Tutorial.objects.all()]
    if single_slug in tutorial:
        this_tutorial = Tutorial.objects.get(tutorial_slug=single_slug)
        # tutorial_from_series = Tutorial.objects.filter(tutorial_seires__tutorial_seires=this_tutorial.tutorial_seires).order_by('published')
        # this_tutorial_idx = list(tutorial_from_series).index(this_tutorial)
        return render(request, 'main/tutorial.html',
                      {'tutorial': this_tutorial,
                       # 'sidebar': tutorial_from_series,
                       # 'this_tutorial_idx': this_tutorial_idx
                       }
                      )

    return HttpResponse('This doesn\'t exist {}'.format(single_slug))


def homepage(request):

    category = TutorialCategory.objects.all()
    context = {
        'category': category
    }
    return render(request, 'main/categories.html', context=context)


def register(request):

    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            username = form.cleaned_data.get('username')
            messages.success(request, 'New user {} has been created.'.format(username))
            return redirect('main:home')
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])

    form = NewUserForm
    return render(request, 'register.html', context={'form': form})


def logout_request(request):
    logout(request)
    messages.info(request, 'You are logged out successfully!!')
    return redirect('main:home')


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'You are now logged in as {} .'.format(username.upper()))
                return redirect('main:home')
        else:
            messages.error(request, 'Invalid username or password!')

    form = AuthenticationForm()
    return render(request, 'login.html', context={'form': form})
