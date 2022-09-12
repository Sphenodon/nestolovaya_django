import datetime
import re

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404

from reservation.forms import TableCreationForm, TableChangeForm
from reservation.models import Reservation, Table


def show_reservation(request):
    table_id = request.GET.get('table_id')
    date = request.GET.get('date')
    queryset = list(Reservation.objects.filter(table_id=table_id, date_of_reservation=date)
                    .order_by('time_of_reservation')
                    .values('user_id', 'user__first_name', 'user__university_id', 'time_of_reservation', 'user__username'))
    print(queryset)
    response = {
        'table_date_show': queryset,
    }

    return JsonResponse(response)


def delete_reservation(request):
    true_user_id = request.user.id
    sus_user_id = request.GET.get('user_id')

    # if user staff
    if request.user.is_staff:
        user_id = sus_user_id
    else:
        user_id = true_user_id

    if request.user.is_authenticated:
        table_id = request.GET.get('table_id')
        date_of_reservation = request.GET.get('date_of_reservation')
        time_of_reservation = request.GET.get('time_of_reservation')
        Reservation.objects.filter(user_id=user_id, table_id=table_id, date_of_reservation=date_of_reservation,
                                   time_of_reservation=time_of_reservation).delete()
        return JsonResponse({'status': 'success'}, status=200)

    return JsonResponse({'errors': 'Что-то пошло не так, скорее всего вы не авторизованы'}, status=400)


def reserve_table(request):
    if request.method == "POST" and request.user.is_authenticated:
        user_id = request.user.id
        table_id = request.POST.get('table_id')
        date_of_reservation = request.POST.get('date_of_reservation')
        time_of_reservation = request.POST.get('time_of_reservation')

        # delete old reservations
        date_now = datetime.datetime.now().date()
        Reservation.objects.filter(date_of_reservation__lt=date_now).delete()

        # check that there are 1 reservation per table
        how_many_reservations_per_table = Reservation.objects.filter(user_id=user_id, table_id=table_id,
                                                                     date_of_reservation=date_of_reservation).count()
        if how_many_reservations_per_table >= 1 and not request.user.is_staff:
            return JsonResponse({'errors': f'У вас уже есть бронированиe на этот стол, {date_of_reservation}'},
                                status=400)

        # check time, hours from 10 to 17, minutes 00 or 30
        time_is_correct = re.fullmatch(r'^1[0-7]:[03]0$', time_of_reservation)
        if not time_is_correct:
            return JsonResponse({'errors': 'Неправильное время'}, status=400)

        # check is table reserved
        table_is_reserved = Reservation.objects.filter(table_id=table_id, date_of_reservation=date_of_reservation,
                                                       time_of_reservation=time_of_reservation).exists()
        if table_is_reserved:
            return JsonResponse({'errors': 'Это время занято'}, status=400)

        if not table_is_reserved:
            Reservation.objects.create(user_id=user_id, table_id=table_id, date_of_reservation=date_of_reservation,
                                       time_of_reservation=time_of_reservation)
            return JsonResponse({'status': 'success'}, status=200)

    return JsonResponse({'errors': 'Что-то пошло не так, скорее всего вы не авторизованы'}, status=400)


def reservation_add_table(request):
    if request.user.is_staff and request.method == 'GET':
        context = {

        }

        return render(request, 'reservation_add_table.html', context)

    if request.user.is_staff and request.method == 'POST':
        form = TableCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            context = {
                'status': 'success',
                'response_message': 'Успешно добавлено'
            }

            return render(request, 'reservation_add_table.html', context)
        else:
            context = {
                'status': 'warning',
                'response_message': 'Не удалось добавить',
            }

            return render(request, 'reservation_add_table.html', context)

    return HttpResponseRedirect('/')


def reservation_change_table(request, table_id):
    instance = get_object_or_404(Table, id=table_id)

    if request.user.is_staff and request.method == 'GET':
        context = {
            'instance': instance,
        }

        return render(request, 'reservation_update_table.html', context)

    if request.user.is_staff and request.method == 'POST':
        form = TableChangeForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            if request.FILES:
                Table.objects.get(id=table_id).image.delete()
                form.save()
            else:
                form.save()

            return HttpResponseRedirect(f'/reservation/')
        else:
            context = {
                'instance': instance,
                'status': 'warning',
                'response_message': 'Не удалось изменить',
            }

            return render(request, 'reservation_update_table.html', context)

    return HttpResponseRedirect('/')


def reservation_delete_table(request, table_id):
    if request.user.is_staff and Table.objects.filter(id=table_id).exists():
        Table.objects.get(id=table_id).image.delete()
        Table.objects.filter(id=table_id).delete()

    return HttpResponseRedirect('/reservation/')


def main_list(request):
    queryset = Table.objects.order_by('id')

    context = {
        'queryset': queryset,
    }
    return render(request, 'reservation.html', context)
