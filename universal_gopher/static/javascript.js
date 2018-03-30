var g_count = 0;
var selected_vip = new Array();
var selected_n = new Array();


//Getters for seats
function getSeats() {
    var get = $("#seatGetter").text();
    get = parseInt(get);
    return get;
}

function getVIP() {
    var get = $(".VIPGetter").text();
    get = parseInt(get);
    return get;
}

function getN() {
    var get = $(".NGetter").text();
    get = parseInt(get);
    return get;
}
//Checks if passwords match on the form.
function check_password() {
    if (document.registerForm.password.value != document.registerForm.repassword.value) {
        alert('The passwords do not match! Please re-enter matching passwords');
        return false;
    }
}
//Fading backgrounds on nav bar.
function fadein(element) {
    var elem = document.getElementById(element);
    elem.style.transition = "background-color 0.4s linear 0s";
    elem.style.backgroundColor = "#50A6C2";
}
//Fading backgrounds on nav bar.  			
function fadeout(element) {
    var elem = document.getElementById(element);
    elem.style.transition = "background-color 0.6s linear 0s";
    elem.style.backgroundColor = "transparent";
}
//On hover of the VIP seats this changes the image.
function VIPHover(element) {
    var elem = document.getElementById(element);
    var id_num = parseInt(elem.id);
    if (!elem.disabled) {
        if ((id_num) > 60 && (id_num) < 81 && !elem.checked) {
            $(elem).siblings('label').css('background-image', 'url(/static/seat_empty_hover.png)');
        }
        if ((id_num) > 60 && (id_num) < 81 && elem.checked) {
            $(elem).siblings('label').css('background-image', 'url(/static/seat_full_hover.png)');
        }
    }
}
//On hover out of the VIP seats this changes the image.
function VIPHoverOut(element) {
    var elem = document.getElementById(element);
    var id_num = parseInt(elem.id);
    if (!elem.disabled) {
        if ((id_num) > 60 && (id_num) < 81 && !elem.checked) {
            $(elem).siblings('label').css('background-image', 'url(/static/seat_empty_VIP.png)');
        }
        if ((id_num) > 60 && (id_num) < 81 && elem.checked) {
            $(elem).siblings('label').css('background-image', 'url(/static/seat_full_VIP.png)');
        }
    }
}
//On click of the VIP seats this changes the image.
function VIPChange(element) {
    var elem = document.getElementById(element);
    var id_num = parseInt(elem.id);
    if ((id_num) > 60 && (id_num) < 81 && !elem.checked) {
        $(elem).siblings('label').css('background-image', 'url(/static/seat_empty_VIP.png)');
    }
    if ((id_num) > 60 && (id_num) < 81 && elem.checked) {
        $(elem).siblings('label').css('background-image', 'url(/static/seat_full_VIP.png)');
    }


}
//Changes images on load for the VIP and disables pre-booked seats.			
function ticked(element) {
    var elem = document.getElementById(element);
    var id_num = parseInt(elem.id);
    if (elem.checked) {
        elem.disabled = true;
        $(elem).siblings('label').css('background-image', 'url(/static/seat_reserve.png)');
        g_count = g_count + 1;
    } else if ((id_num) > 60 && (id_num) < 81) {
        $(elem).siblings('label').css('background-image', 'url(/static/seat_empty_VIP.png)');
    }


}
//Unslider.com code/////////////////
$(function () {
    $('.banner').unslider({
        speed: 500, //  The speed to animate each slide (in milliseconds)
        delay: 2000, //  The delay between slide animations (in milliseconds)
        keys: true, //  Enable keyboard (left, right) arrow shortcuts
        dots: true, //  Display dot navigation
        fluid: false //  Support responsive design. May break non-responsive designs
    });
});
///////////////////////////////////////////////////////////


$(document).ready(function (e) {
    //Slide for login
    $('#log_button').on('click', function () {
        $('#user').slideToggle();
    });
    //Makes sure a certain number of seats can be checked and runs count checked function.
    $("input[type=checkbox]").on("click", countChecked);
    //Checks how many seats have been clicked and stops from more than the total being clicked.
    $("input[type=checkbox]").click(function (event) {
        //Parses ID of specific seat and checks if it is VIP or normal
        var id = $(this).attr('id');
        id = parseInt(id);
        var found = false;
        var get_normal = getN();
        var get_vip = getVIP();


        // Loads seats into the array if they are first clicked and removed if clicked again
        if ((id) > 60 && (id) < 81) {
            var inarray = false;
            if ((get_vip <= selected_vip.length)) {
                for (var i = 0; i < selected_vip.length; i++) {
                    if (selected_vip[i] === id) {
                        inarray = true;
                    }
                }
                if (inarray === true) {
                    index = $.inArray(id, selected_vip)
                    selected_vip.splice(index, 1)
                } else {
                    event.preventDefault();
                    countChecked();
                }
            } else {
                var index = $.inArray(id, selected_vip)
                if (index === -1) {
                    if (get_vip > selected_vip.length) {
                        selected_vip.push(id)
                    }
                } else {
                    selected_vip.splice(index, 1)
                }
            }

        } else {
            var index = $.inArray(id, selected_n)
            if (get_normal <= selected_n.length) {
                for (var i = 0; i < selected_n.length; i++) {
                    if (selected_n[i] === id) {
                        inarray = true;
                    }
                }
                if (inarray === true) {
                    index = $.inArray(id, selected_n)
                    selected_n.splice(index, 1)
                } else {
                    event.preventDefault();
                    countChecked();
                }
            } else {
                if (index === -1) {
                    if (get_normal > selected_n.length) {
                        selected_n.push(id)
                    }
                } else {
                    selected_n.splice(index, 1)
                }
				
            }
        }


        //Outputs number of each seat selected to html.
        $("#n_seats").text(selected_n.length);
        $("#v_seats").text(selected_vip.length);
        if (get_normal === selected_n.length && get_vip === selected_vip.length){
            document.getElementById('seat_cont').disabled = false;
        }
        else{
            document.getElementById('seat_cont').disabled = true;
        }
    });
})

// Counts how many seats have been checked
var countChecked = function () {
    var n = $("input:checked").length;
    var get = getSeats();
    if (n - g_count <= get) {
        var x = n - g_count;
        $("#check_no").text(x);
    }
};

function ticTotal() {
    var a1 = document.querySelector('select[name="as"]');
    var b1 = document.querySelector('select[name="av"]');
    var c1 = document.querySelector('select[name="cs"]');
    var d1 = document.querySelector('select[name="cv"]');
    var e1 = document.querySelector('select[name="os"]');
    var f1 = document.querySelector('select[name="ov"]');
    var g1 = document.querySelector('select[name="ss"]');
    var h1 = document.querySelector('select[name="sv"]');
    var i1 = document.querySelector('select[name="ts"]');
    var j1 = document.querySelector('select[name="tv"]');

    if (parseInt(a1.value) != 0) {
        a1 = parseInt(a1.value);
    } else {
        a1 = 0;
    }

    if (parseInt(b1.value) != 0) {
        b1 = parseInt(b1.value);
    } else {
        b1 = 0;
    }
    if (parseInt(c1.value) != 0) {
        c1 = parseInt(c1.value);
    } else {
        c1 = 0;
    }
    if (parseInt(d1.value) != 0) {
        d1 = parseInt(d1.value);
    } else {
        d1 = 0;
    }
    if (parseInt(e1.value) != 0) {
        e1 = parseInt(e1.value);
    } else {
        e1 = 0;
    }
    if (parseInt(f1.value) != 0) {
        f1 = parseInt(f1.value);
    } else {
        f1 = 0;
    }
    if (parseInt(g1.value) != 0) {
        g1 = parseInt(g1.value);
    } else {
        g1 = 0;
    }
    if (parseInt(h1.value) != 0) {
        h1 = parseInt(h1.value);
    } else {
        h1 = 0;
    }
    if (parseInt(i1.value) != 0) {
        i1 = parseInt(i1.value);
    } else {
        i1 = 0;
    }
    if (parseInt(j1.value) != 0) {
        j1 = parseInt(j1.value);
    } else {
        j1 = 0;
    }

    var total = a1 + b1 + c1 + d1 + e1 + f1 + g1 + h1 + i1 + j1;
    if (total > 6) {
        document.getElementById('cont').disabled = true;
        alert("No more than 6 tickets can be purchased at once.");
    } else {
        document.getElementById('cont').disabled = false;
    }
}
