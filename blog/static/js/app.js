/**
 * Created by LeviJamesH on 7/3/2016.
 */

var main = function () {
    "use strict";


    var beforeName = document.getElementById("name").value;
    console.log("Before" + beforeName);

    document.getElementById("name").value = document.getElementById("name_td").innerHTML;

    var name = document.getElementById("name");




};


$(function () {
    $("td").click(function () {
        var sib = this.nextElementSibling;
        var extraSibling = sib.getElementsByTagName('input');

        //console.log(extraSibling);
        $(this).children().first().focus();
        var contents = $(this).html();
        console.log(contents);

        $(this).blur(function () {
            if (contents != $(this).html() && extraSibling.length == 0) {
                window.alert("Contents have changed");
                sib.value = $(this).html();

                console.log($(this).html());
                console.log(sib);
            }

            else {
                extraSibling = sib.getElementsByTagName('input').item(0)

                //window.alert("ExtraSibling active");
                console.log($(this).html());
                extraSibling.value = $(this).html();
                console.log(extraSibling.value);
            }
        });

    });
});

$(document).ready(main);