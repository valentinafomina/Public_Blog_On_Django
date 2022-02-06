from django.shortcuts import render


def moderator_cab(request):

    title: 'Модерация'
    content = {'title': title}

    return render(request, 'adminapp/moderator_cab.html', content)