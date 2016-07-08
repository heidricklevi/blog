/**
 * Created by LeviJamesH on 7/3/2016.
 */

$(function () {

    $('#text_post').hover( function () {

        var sib = this.nextElementSibling;
        $(this).focus();

        $('#text_post').keyup( function () {

            sib.value = $(this).html();

        });
    });
});

$(function () {
    $("td").click(function () {
        var sib = this.nextElementSibling;
        var extraSibling = sib.getElementsByTagName('input');
        $(this).children().first().focus();

        $(this).blur(function () {
            if (extraSibling.length == 0) {
                sib.value = $(this).html();
            }

            else if(extraSibling.length > 0) {
                extraSibling = sib.getElementsByTagName('input').item(0);
                extraSibling.value = $(this).html();
            }
        });

    });
});
