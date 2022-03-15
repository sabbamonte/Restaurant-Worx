document.addEventListener('DOMContentLoaded', function() {
    
    // Accordion
    function myFunction(id) {
        var x = document.getElementById(id);
        if (x.className.indexOf("w3-show") == -1) {
            x.className += " w3-show";
            x.previousElementSibling.className += " w3-theme-d1";
        } else { 
            x.className = x.className.replace("w3-show", "");
            x.previousElementSibling.className = 
            x.previousElementSibling.className.replace(" w3-theme-d1", "");
        }
    }

    // Used to toggle the menu on smaller screens when clicking on the menu button
    function openNav() {
        var x = document.getElementById("navDemo");
        if (x.className.indexOf("w3-show") == -1) {
            x.className += " w3-show";
        } else { 
            x.className = x.className.replace(" w3-show", "");
        }
    }

    // Select all edit buttons and pass them to function
    add_edit = document.querySelectorAll('.edit')
    add_edit.forEach((button) => {
        button.addEventListener('click', () => {
            add_edit_info(button.id)
            console.log(button.id)
        })
    })
    
    // Create form to submit edited positon and location to database
    function add_edit_info(add_edit) {
        if (add_edit === 'pos_edit') {
            document.getElementById('pos_edit').style.display = 'none'
            document.getElementById('position').innerHTML =
                `<form id="save"><textarea rows="1" cols="20" id="new_pos"></textarea>
                <button class="w3-button w3-theme btn-sm" type="submit"> Save </button></form>`

            document.querySelector('#save').onsubmit = function() {
                fetch(`/add`, {
                    method: 'POST',
                    body: JSON.stringify({
                        position: document.querySelector('#new_pos').value,
                    })
                })
            } 
        }
        else if (add_edit == 'loc_edit') {
            document.getElementById('loc_edit').style.display = 'none'
            document.getElementById('location').innerHTML =
                `<form id="save"><textarea rows="1" cols="20" id="new_loc"></textarea>
                <button class="w3-button w3-theme btn-sm" type="submit"> Save </button></form>`

            document.querySelector('#save').onsubmit = function() {
                fetch(`/add`, {
                    method: 'POST',
                    body: JSON.stringify({
                        location: document.querySelector('#new_loc').value,
                    })
                }) 
            } 
        }
    }

    // Error checking review form submission and saving it to database
    document.querySelector('#review').onsubmit = function() {
        
        // Check if a rating was selected
        if(document.review.rating.value == "") {
            new_alert = document.getElementById('alert')
            new_alert.className = `alert alert-danger alert-dismissible fade show `
            new_alert.innerHTML = `You need to provide a rating  
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
            </button>`
            return false;
        }

        // Check Pay and tips are not below or equal to 0
        if(document.review.Pay.value <= 0 || document.review.Stips.value <= 0
            || document.review.Btips.value <= 0) {
            new_alert = document.getElementById('alert')
            new_alert.className = `alert alert-danger alert-dismissible fade show `
            new_alert.innerHTML = `Pay and tip amounts need to be above $0
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
            </button>`
            document.review.Pay.focus();
            return false;
        }

        // Send data to Django via JSON API
        fetch(`review`, {
            method: 'POST',
            body: JSON.stringify({
                name: document.querySelector('#inputName').value,
                position: document.querySelector('#inputPosition').value,
                days: document.querySelector('#inputDays').value,
                hours: document.querySelector('#inputHours').value,
                pay: document.querySelector('#inputPay').value,
                slow: document.querySelector('#inputStips').value,
                busy: document.querySelector('#inputBtips').value,
                envo: document.querySelector('#inputEnvo').value,
                mngmt: document.querySelector('#inputMgmt').value,
                comments: document.querySelector('#inputComment').value,
                rating: document.review.rating.value
            })
        })
    }
});