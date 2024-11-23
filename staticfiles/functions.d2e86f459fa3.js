var addToCartUrl = "cart/add/''/0/";
var deleteItemUrl = "delete/''/0/"


function addToCart(item_type, productId) {
    fetch(addToCartUrl.replace("''", item_type).replace("0", productId), {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                let text = "Successfully added a product to the cart!\nGo see your cart.";
                document.getElementById('menu-cart').innerHTML = data.cart_html;
                if (confirm(text) === true) {
                    window.location.href = data.redirect_url;
                }
            } else {
                alert("Failed to add the product to the cart.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
}

function deleteCartItem(item_type, productId) {
    let confirmation = confirm("Are you sure you want to delete this item from the cart?");

    if (confirmation === true) {
        fetch(deleteItemUrl.replace("''", item_type).replace("0", productId), {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken'),
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById(`cart-item-${productId}`).remove();

                    document.getElementById('cart-length-text').innerText = data.cart_length + ' items';

                    document.getElementById('menu-cart').innerHTML = data.cart_html;
                } else {
                    console.error('Failed to delete item from the cart');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Check if the cookie name matches the requested name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

filterSelection("all")

function filterSelection(c) {
    var x, i, welcome_text;
    x = document.getElementsByClassName("filterDiv");
    welcome_text = document.getElementsByClassName("welcome");

    if (c === "all") c = "";
    for (i = 0; i < x.length; i++) {
        w3RemoveClass(x[i], "show");
        if (x[i].className.indexOf(c) > -1) w3AddClass(x[i], "show");

    }
    w3RemoveClass(welcome_text, "show");


}

function w3AddClass(element, name) {
    var i, arr1, arr2;
    arr1 = element.className.split(" ");
    arr2 = name.split(" ");
    for (i = 0; i < arr2.length; i++) {
        if (arr1.indexOf(arr2[i]) === -1) {
            element.className += " " + arr2[i];
        }
    }
}

function w3RemoveClass(element, name) {
    var i, arr1, arr2;
    arr1 = element.className.split(" ");
    arr2 = name.split(" ");
    for (i = 0; i < arr2.length; i++) {
        while (arr1.indexOf(arr2[i]) > -1) {
            arr1.splice(arr1.indexOf(arr2[i]), 1);
        }
    }
    element.className = arr1.join(" ");
}


var btnContainer = document.getElementById("myBtnContainer");
var btns = btnContainer.getElementsByClassName("navbtn");
for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", function () {
        var current = document.getElementsByClassName("activebtn");
        current[0].className = current[0].className.replace(" activebtn", "");
        this.className += " activebtn";
    });
}


function toggleNavbar() {
    var navbarElements = document.getElementsByClassName('navitem');
    var arrayNavbarElements = Array.from(navbarElements);

    arrayNavbarElements.forEach((element, index) => {
        if (index === 0) {
            element.classList.toggle('show-navitem', true);
        } else {
            element.classList.toggle('show-navitem');
        }
    });
}
