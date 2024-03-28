from django.contrib.auth.models import User
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect

from .forms import UserForm
from django.contrib.auth.decorators import login_required

def register(request):
    global form
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            confirmation_link = request.build_absolute_uri(reverse('confirm_email', args=[confirmation_code]))
            subject = 'Elektron pochtangizni tasdiqlang'
            message = render_to_string('email_confirmation.html', {'confirmation_link': confirmation_link})
            send_mail(subject, message, 'from@example.com', [user.email])

        return render(request,'base.html', {'form': form})
    #             return HttpResponseRedirect('/confirmation/')  # Redirect to confirmation page
    else:
        form = UserForm()
    return render(request, 'registration/register.html', {'form': form})


def confirm_email(request, code):
    user = User.objects.filter(verification_code=code).first()
    if user:
        user.verified_email = True
        user.save()
        return render(request, 'registration/email_confirmed.html')
    else:
        return render(request, 'registration/invalid_confirmation_code.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return redirect('home')


    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def edit_news(request, news_id):
    # Berilgan ID bo'yicha yangilik obyektini olish
    news_item = get_object_or_404(News, id=news_id)

    if request.method == 'POST':
        news_item.title = request.POST.get('title')
        news_item.content = request.POST.get('content')

        # Ma'lumotni saqlash
        news_item.save()

        return redirect('home')  # O'zgartirilishi mumkin
    else:
        return render(request, 'edit_news.html', {'news_item': news_item})

@login_required
def delete_news(request, news_id):
    try:
        news_item = News.objects.get(id=news_id)
        if request.method == 'POST':
            news_item.delete()
            return redirect('home')
        else:
            return render(request, 'delete_news.html', {'news_item': news_item})
    except News.DoesNotExist:
        return HttpResponseNotFound("News does not exist")

    # Yangilikni o'chirish logikasi

@login_required
def add_news(request):
    if request.method == 'POST':

        title = request.POST.get('title')
        content = request.POST.get('content')

        # Yangi xabar yaratish
        new_news = News(title=title, content=content)
        new_news.save()

        return redirect('home')
    else:
        return render(request, 'add_news.html')