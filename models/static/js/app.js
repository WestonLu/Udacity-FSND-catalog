function logout() {
    var w = window.open('https://github.com/logout');
    setTimeout(function () {
        w.document.getElementsByTagName('form')[0].submit();
    }, 2000);
}


// mouse on first level catagory
// show respoding second level catagory
$(function () {
    $("a.logoutbutton").click(logout);

    $("#f1, #s1").mouseover(function () {
        $("#s1").show();
    }).mouseleave(function () {
        $("#s1").hide();
    });

    $("#f2, #s2").mouseover(function () {
        $("#s2").show();
    }).mouseleave(function () {
        $("#s2").hide();
    });

    var onChangeHandler = function () {
        $('#secondlevel').empty();
        if ($('#firstlevel').val() == 'Clothing, Shoes & Jewelry') {
            $('#secondlevel').append("<option value='3'>Clothing</option>");
            $('#secondlevel').append("<option value='4'>Shoes</option>");
            $('#secondlevel').append("<option value='5'>Jewelry</option>");
        };
        if ($('#firstlevel').val() == 'Electronics & Computers') {
            $('#secondlevel').append("<option value='6'>Electronics</option>");
            $('#secondlevel').append("<option value='7'>Computers</option>");
        };
    };
    $('#firstlevel').change(onChangeHandler);

})




// used for creat new item
// user choose first level catagory
// show respoding second level catagory for user to choose



