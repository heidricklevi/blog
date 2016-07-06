/**
 * Created by LeviJamesH on 7/3/2016.
 */

$(function () {
    $("td").click(function () {
        var sib = this.nextElementSibling;
        var extraSibling = sib.getElementsByTagName('input');
        console.log("Sib = " );
        console.log(sib);
        console.log("Extra Sib = ");
        console.log(extraSibling);


        $(this).children().first().focus();
        var contents = $(this).html();
        console.log("Original Contents = " + contents);

        $(this).blur(function () {
            if (extraSibling.length == 0) {
                sib.value = $(this).html();
                console.log("Sib New Value: ");
                console.log(sib);
            }

            else if(extraSibling.length > 0) {
                extraSibling = sib.getElementsByTagName('input').item(0);
                extraSibling.value = $(this).html();
                console.log("Extra Sibling New Value = ");
                console.log(extraSibling);
            }
        });

    });
});
