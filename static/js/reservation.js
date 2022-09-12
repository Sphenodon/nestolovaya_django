$(document).ready(function () {
    const startOfWork = {hours: 10, minutes: 0};
    const endOfWork = {hours: 18, minutes: 0};
    const request_user_id = $('#user_id').html()
    let is_staff = $('#is_staff').html()
    if (is_staff === 'true') is_staff = true; else is_staff = false;

    //yyyy-mm-dd today
    let today = new Date().toLocaleDateString();
    let todayStr = `${today.slice(6,10)}-${today.slice(3,5)}-${today.slice(0,2)}`;

    //set min day in calendar
    $('.dateShow').attr('min', todayStr);

    let tableDateShow = function (data, table_id, date){

        let table = $(`#tableDateShow${table_id} tbody`);
        table.html('');

        let timeReserved = [];

        for (let i of data){
            if (request_user_id === i.user_id.toString() || is_staff){
                $( `<tr>
                        <td style="width: 150px;">${i.user__university_id}</td>
                        <td><a href="/user/${i.user__username}/">${i.user__first_name}</a></td>
                        <td>${i.time_of_reservation.slice(0, -3)}</td>
                        <td class="p-1">
                            <span class="user_id" hidden="true">${i.user_id}</span>
                            <span class="table_id" hidden="true">${table_id}</span>
                            <span class="date_of_reservation" hidden="true">${date}</span>
                            <span class="time_of_reservation" hidden="true">${i.time_of_reservation}</span>
                            <a class="btn btn-primary deleteReservation p-1">Удалить</a>
                        </td>
                    </tr>` ).appendTo(table);
            }else {
                $( `<tr>
                        <td style="width: 150px;">${i.user__university_id}</td>
                        <td>${i.user__first_name}</td>
                        <td>${i.time_of_reservation.slice(0, -3)}</td>
                        <td></td>
                    </tr>` ).appendTo(table);
            }

            //remove seconds
            timeReserved.push(i.time_of_reservation.slice(0, -3));
        }

        let selectHour = $(`#timeForTable${table_id}`);
        selectHour.html('<option selected="" disabled="" value="">Выберите...</option>');

        for (let hour = startOfWork.hours; hour <= endOfWork.hours-1; hour++) {
            if (!timeReserved.includes(`${hour}:00`)) {
                $(`<option>${hour}:00</option>`).appendTo(selectHour);
            }
            if (!timeReserved.includes(`${hour}:30`)) {
                $(`<option>${hour}:30</option>`).appendTo(selectHour);
            }
        }

        //show reservation table
        $(`#hForTable${table_id}`).attr('hidden', false);
        $(`#tableDateShow${table_id}`).attr('hidden', false);

        if (table.html() === ''){
            $( `<tr>
                    <td colspan="3">Нет забронированного времени</td>
                </tr>` ).appendTo(table);
        }
    }

    $('.dateShow').on('change', function (e) {
        let date = e.target.value;
        console.log(date);
        let table_id = $(this).siblings('span').html();
        console.log(table_id);

        $.ajax({
            data: {
                table_id: table_id,
                date: date,
            },
            url: 'show_reservation',

            success: function (response) {
                tableDateShow(response.table_date_show, table_id, date);
            },

            error: function (response) {
                console.log(response.responseJSON.errors);
            },
        });
        return false;
    });


    function alertForReservation(message, type, table_id) {
        $(`#alertForReservation${table_id}`).append(`<div class="alert alert-${type} alert-dismissible" role="alert">${message}<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`)
    }


    $('.reservation').submit( function () {
        let fields = $(this).serializeArray();
        let table_id;
        let date_of_reservation;
        let time_of_reservation;
        jQuery.each( fields, function( i, field ) {
            if (field.name === 'table_id') table_id = field.value;
            if (field.name === 'date_of_reservation') date_of_reservation = field.value;
            if (field.name === 'time_of_reservation') time_of_reservation = field.value;
        });

        $.ajax({
            data: $(this).serialize(),
            type: 'POST',
            url: 'reserve_table',

            success: function (response) {
                alertForReservation(`Вы забронировали на ${time_of_reservation}, ${date_of_reservation}`, 'success', table_id)
                $(`#dateShow${table_id}`).change();
            },

            error: function (response) {
                alertForReservation(response.responseJSON.errors, 'warning', table_id)
            },
        });
        return false;
    });


    $(document).on("click", '.deleteReservation', function () {
        let user_id = $(this).siblings('span.user_id').html();
        let table_id = $(this).siblings('span.table_id').html();
        let date_of_reservation = $(this).siblings('span.date_of_reservation').html();
        let time_of_reservation = $(this).siblings('span.time_of_reservation').html();

        $.ajax({
            data: {
                user_id: user_id,
                table_id: table_id,
                date_of_reservation: date_of_reservation,
                time_of_reservation: time_of_reservation,
            },
            url: 'delete_reservation',

            success: function (response) {
                alertForReservation(`Бронирование удалено ${time_of_reservation.slice(0,-3)}, ${date_of_reservation}`, 'success', table_id)
                $(`#dateShow${table_id}`).change();
            },

            error: function (response) {
                alertForReservation(response.responseJSON.errors, 'warning', table_id)
            },
        });
        return false;
    });

})