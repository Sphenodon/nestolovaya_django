import datetime

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Max, F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from social_django.models import UserSocialAuth

from recSys.forms import MenuForm, FoodTypeDetailForm, CustomUserChangeForm
from recSys.models import Menu, TimeCoefficient, EmotionCoefficient, MenuReview, FoodTypeDetail, User

DATE = datetime.datetime.now()
MONTH = DATE.month
HOUR = DATE.hour


def menu_like(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        menu_id = request.GET.get('menu_id')
        remove = request.GET.get('remove')
        remove = True if remove == 'true' else False
        change = request.GET.get('change')
        change = True if change == 'true' else False

        if not remove:
            Menu.objects.filter(id=menu_id).update(likes=F('likes') + 1, views=F('views') + 1)
            MenuReview.objects.update_or_create(
                user_id=user_id, menu_id=menu_id,
                defaults={'review': True}
            )

        if remove:
            Menu.objects.filter(id=menu_id).update(likes=F('likes') - 1, views=F('views') - 1)
            MenuReview.objects.update_or_create(
                user_id=user_id, menu_id=menu_id,
                defaults={'review': None}
            )

        # del dislike
        if change:
            Menu.objects.filter(id=menu_id).update(dislikes=F('dislikes') - 1, views=F('views') + 1)
            print('dislikes -1')

        return JsonResponse({}, status=200)

    if not request.user.is_authenticated:
        errors = "Пожалуйста, авторизуйтесь для оценивания блюда или напитка"
        return JsonResponse({'errors': errors})


def menu_dislike(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        menu_id = request.GET.get('menu_id')
        remove = request.GET.get('remove')
        remove = True if remove == 'true' else False
        change = request.GET.get('change')
        change = True if change == 'true' else False

        if not remove:
            Menu.objects.filter(id=menu_id).update(dislikes=F('dislikes') + 1, views=F('views') - 1)
            MenuReview.objects.update_or_create(
                user_id=user_id, menu_id=menu_id,
                defaults={'review': False}
            )

        if remove:
            Menu.objects.filter(id=menu_id).update(dislikes=F('dislikes') - 1, views=F('views') + 1)
            MenuReview.objects.update_or_create(
                user_id=user_id, menu_id=menu_id,
                defaults={'review': None}
            )

        # del like
        if change:
            Menu.objects.filter(id=menu_id).update(likes=F('likes') - 1, views=F('views') - 1)
            print('likes -1')

        return JsonResponse({}, status=200)

    if not request.user.is_authenticated:
        errors = "Пожалуйста, авторизуйтесь для оценивания блюда или напитка"
        return JsonResponse({'errors': errors})


def menu_review_recommendation(request):
    images = request.GET.getlist('images[]')
    emotion = request.GET.get('emotion')
    review = request.GET.get('review')

    print(images)
    print(emotion)

    emotion_coefficient_ids = Menu.objects.filter(image__in=images, emotioncoefficient__emotion=emotion).values(
        'emotioncoefficient__id')
    print(emotion_coefficient_ids)

    if review == 'correct':
        EmotionCoefficient.objects.filter(id__in=emotion_coefficient_ids).update(coefficient=F('coefficient') + 2)
        for d in emotion_coefficient_ids:
            emotion_id = d.get('emotioncoefficient__id')
            menu_id = EmotionCoefficient.objects.filter(id=emotion_id).values('menu_id')[0].get('menu_id')
            TimeCoefficient.objects.filter(month=MONTH, hour=HOUR, menu_id=menu_id).update(
                coefficient=F('coefficient') + 2)

    if review == 'indifferent':
        EmotionCoefficient.objects.filter(id__in=emotion_coefficient_ids).update(coefficient=F('coefficient') + 1)
        for d in emotion_coefficient_ids:
            emotion_id = d.get('emotioncoefficient__id')
            menu_id = EmotionCoefficient.objects.filter(id=emotion_id).values('menu_id')[0].get('menu_id')
            TimeCoefficient.objects.filter(month=MONTH, hour=HOUR, menu_id=menu_id).update(
                coefficient=F('coefficient') + 1)

    if review == 'wrong':
        EmotionCoefficient.objects.filter(id__in=emotion_coefficient_ids).update(coefficient=F('coefficient') - 1)
        for d in emotion_coefficient_ids:
            emotion_id = d.get('emotioncoefficient__id')
            menu_id = EmotionCoefficient.objects.filter(id=emotion_id).values('menu_id')[0].get('menu_id')
            TimeCoefficient.objects.filter(month=MONTH, hour=HOUR, menu_id=menu_id).update(
                coefficient=F('coefficient') - 1)

    emotion_list = list(Menu.objects.filter(image__in=images, emotioncoefficient__emotion=emotion).values('title',
                                                                                                          'emotioncoefficient__coefficient'))

    response = {
        'emotion_coefficient': emotion_list,
    }

    return JsonResponse(response)


def emotion_coefficient_goc(emotion):
    all_menu_id = Menu.objects.values('id').all()
    for d in all_menu_id:
        menu_id = d.get('id')
        _, _ = EmotionCoefficient.objects.get_or_create(
            emotion=emotion,
            menu_id=menu_id
        )


def get_menu_by_emotion(request):
    print(request.GET)
    emotion = request.GET.get('emotion')
    print(emotion)
    emotion_coefficient_goc(emotion)
    menu_by_em = list(Menu.objects.filter(emotioncoefficient__emotion=emotion, available=True)
                      .order_by('emotioncoefficient__coefficient')
                      .values('id', 'title', 'food_type', 'image', 'final_coefficient',
                              'emotioncoefficient__emotion', 'emotioncoefficient__coefficient'))
    response = {
        'menu_by_em': menu_by_em,
    }

    return JsonResponse(response)


def food_type(request):
    instance = FoodTypeDetail.objects.all()

    if request.user.is_staff and request.method == 'GET':
        context = {
            'instance': instance,
        }

        return render(request, 'food_type.html', context)

    if request.user.is_staff and request.method == 'POST':
        form = FoodTypeDetailForm(request.POST)
        if form.is_valid():
            form.save()

            context = {
                'instance': instance,
                'status': 'success',
                'response_message': 'Успешно добавлено'
            }

            return render(request, 'food_type.html', context)
        else:
            context = {
                'instance': instance,
                'status': 'warning',
                'response_message': 'Не удалось добавить',
            }

            return render(request, 'food_type.html', context)


def food_type_update(request, food_type_id):
    instance = get_object_or_404(FoodTypeDetail, id=food_type_id)

    if request.user.is_staff and request.method == 'GET':
        context = {
            'instance': instance,
        }

        return render(request, 'food_type_update.html', context)

    if request.user.is_staff and request.method == 'POST':
        form = FoodTypeDetailForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()

            context = {
                'instance': instance,
                'status': 'success',
                'response_message': 'Успешно изменено'
            }

            return render(request, 'food_type_update.html', context)
        else:
            context = {
                'instance': instance,
                'status': 'warning',
                'response_message': 'Не удалось изменить',
            }

            return render(request, 'food_type_update.html', context)

    return HttpResponseRedirect('/')


def food_type_delete(request, food_type_id):
    if request.user.is_staff and FoodTypeDetail.objects.filter(id=food_type_id).exists():
        FoodTypeDetail.objects.filter(id=food_type_id).delete()

    return HttpResponseRedirect('/menu/food-type/')


def menu_detail(request, menu_id):
    instance = get_object_or_404(Menu, id=menu_id)
    user_id = request.user.id
    Menu.objects.filter(id=menu_id).update(views=F('views')+1)
    TimeCoefficient.objects.filter(menu_id=menu_id, month=MONTH, hour=HOUR).update(coefficient=F('coefficient') + 1)

    try:
        review = MenuReview.objects.filter(user_id=user_id, menu_id=menu_id).values('review')[0].get('review')
    except IndexError:
        review = None

    context = {
        'instance': instance,
        'review': review
    }

    return render(request, 'menu_detail.html', context)


def menu_add(request):
    if request.user.is_staff and request.method == 'GET':
        food_type = Menu.FOOD_TYPE
        food_type_detail = FoodTypeDetail.objects.values('id', 'title')
        context = {
            'food_type': food_type,
            'food_type_detail': food_type_detail,
        }

        return render(request, 'menu_add.html', context)

    if request.user.is_staff and request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            saved_form = form.save()

            for month in range(1, 13):
                for hour in range(24):
                    TimeCoefficient.objects.create(
                        month=month,
                        hour=hour,
                        menu_id=saved_form.id
                    )

            context = {
                'status': 'success',
                'response_message': 'Успешно добавлено'
            }

            return render(request, 'menu_add.html', context)
        else:
            context = {
                'status': 'warning',
                'response_message': 'Не удалось добавить в меню',
            }

            return render(request, 'menu_add.html', context)

    return HttpResponseRedirect('/')


def menu_update(request, menu_id):
    instance = get_object_or_404(Menu, id=menu_id)
    food_type = Menu.FOOD_TYPE
    food_type_detail = FoodTypeDetail.objects.values('id', 'title')

    if request.user.is_staff and request.method == 'GET':

        context = {
            'instance': instance,
            'food_type': food_type,
            'food_type_detail': food_type_detail,
        }

        return render(request, 'menu_update.html', context)

    if request.user.is_staff and request.method == 'POST':
        form = MenuForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            if request.FILES:
                Menu.objects.get(id=menu_id).image.delete()
                form.save()
            else:
                form.save()

            return HttpResponseRedirect(f'/menu/detail/{menu_id}/')
        else:
            context = {
                'instance': instance,
                'food_type': food_type,
                'food_type_detail': food_type_detail,
                'status': 'warning',
                'response_message': 'Не удалось изменить',
            }

            return render(request, 'menu_update.html', context)

    return HttpResponseRedirect('/')


def menu_delete(request, menu_id):
    if request.user.is_staff and Menu.objects.filter(id=menu_id).exists():
        Menu.objects.get(id=menu_id).image.delete()
        Menu.objects.filter(id=menu_id).delete()

    return HttpResponseRedirect('/')


def main_list(request):
    queryMenu = Menu.objects \
        .filter(timecoefficient__month=MONTH, timecoefficient__hour=HOUR) \
        .order_by('-views') \
        .values('id', 'views', 'timecoefficient__coefficient')

    # list_queryMenu = list(queryMenu)
    # print(list_queryMenu)

    max_views = queryMenu.aggregate(Max('views')).get('views__max')
    max_time_coefficient = queryMenu.aggregate(Max('timecoefficient__coefficient')).get('timecoefficient__coefficient__max')
    print(f'max_val: {max_views}')
    print(f'max_time_coefficient: {max_time_coefficient}')

    for i in queryMenu:
        menu_id = i.get('id')
        views = i.get('views')
        time_coefficient = i.get('timecoefficient__coefficient')
        try:
            final_coefficient = views / max_views * 100 + time_coefficient / max_time_coefficient * 100
        except ZeroDivisionError:
            final_coefficient = 0
        i['final_coefficient'] = final_coefficient
        Menu.objects.filter(id=menu_id).update(final_coefficient=final_coefficient)

    food_types = FoodTypeDetail.objects.values('id', 'title')
    dict_queryset = []
    popular = Menu.objects.filter(available='True').order_by('-final_coefficient')[:6]
    dict_queryset.append({'food_type': 'Популярное', 'queryset': popular})

    for ft in food_types:
        print(ft['title'])
        menu_by_food_type = Menu.objects.filter(food_type_detail=ft['id'], available=True).order_by('-final_coefficient')
        dict_queryset.append({'food_type': ft['title'], 'queryset': menu_by_food_type})

    print(dict_queryset)

    context = {
        'dict_queryset': dict_queryset,
    }

    return render(request, 'main.html', context)


def menu_for_staff(request):
    if request.user.is_staff:
        food_types = FoodTypeDetail.objects.values('id', 'title')
        dict_queryset = []

        for ft in food_types:
            menu_by_food_type = Menu.objects.filter(food_type_detail=ft['id']).order_by('-final_coefficient')
            dict_queryset.append({'food_type': ft['title'], 'queryset': menu_by_food_type})

        context = {
            'dict_queryset': dict_queryset,
        }

        return render(request, 'menu_for_staff.html', context)

    return HttpResponseRedirect('/')


def user_profile(request, username):
    user_data = User.objects.values('id', 'username', 'first_name', 'last_name', 'university_id', 'is_active', 'email')
    user_profile_data = get_object_or_404(user_data, username=username)
    print(user_profile_data.get('id'))
    try:
        user_id_social = UserSocialAuth.objects.filter(user_id=user_profile_data.get('id')).only('uid')[0]
    except IndexError:
        user_id_social = 0
    print(user_id_social)

    context = {
        'user_id_social': user_id_social,
        'user_profile': user_profile_data,
    }

    return render(request, 'user_profile.html', context)


def user_profile_editing(request, username):
    if request.user.is_staff or request.user.username == username:
        user_data = User.objects.values('username', 'first_name', 'last_name', 'university_id', 'is_active')
        user_profile_data = get_object_or_404(user_data, username=username)

        if request.method == 'POST':
            form = CustomUserChangeForm(request.POST, instance=user_profile_data)
            if form.is_valid():
                form.save()

                return HttpResponseRedirect(f'/user/{username}/')
            else:
                context = {
                    'user_profile': user_profile_data,
                    'status': 'warning',
                    'response_message': 'Не удалось изменить'
                }

                return render(request, 'user_profile_editing.html', context)

        context = {
            'user_profile': user_profile_data,
        }

        return render(request, 'user_profile_editing.html', context)

    else:
        return HttpResponseRedirect(f'/user/{username}/')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

