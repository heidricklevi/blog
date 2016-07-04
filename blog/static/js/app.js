/**
 * Created by LeviJamesH on 7/3/2016.
 */

//$(function (){
//
//    var table = document.getElementById("admin_table");
//    console.log(table);
//
//
//    for (var i = 0, row; row = table.rows[i]; i++) {
//   //iterate through rows
//   //rows would be accessed using the "row" variable assigned in the for loop
//        console.log(row);
//    for (var j = 0, col; col = row.cells[j]; j++) {
//     //iterate through columns
//     //columns would be accessed using the "col" variable assigned in the for loop
//
//        console.log(col);
//   }
//}
//
//
//});

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
