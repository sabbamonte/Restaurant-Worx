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

    // Create form to submit edited data to database
    function add_edit_info(add_edit) {
        if (add_edit === 'pos_edit') {
            document.getElementById('pos_edit').style.display = 'none'
            document.getElementById('position').innerHTML =
                `<form id="save"><textarea rows="1" cols="20" id="new_pos"></textarea>
                <button class="w3-button w3-theme btn-sm" type="submit"> Save </button></form>`
        }
        else if (add_edit == 'loc_edit') {
            document.getElementById('loc_edit').style.display = 'none'
            document.getElementById('location').innerHTML =
                `<form id="save"><textarea rows="1" cols="20" id="new_loc"></textarea>
                <button class="w3-button w3-theme btn-sm" type="submit"> Save </button></form>`
        }

        document.querySelector('#save').obsubmit = function() {
            fetch(`/index`, {
                method: 'POST',
                body: JSON.stringify({
                    position: document.querySelector('#new_pos').value,
                    location: document.querySelector('#new_loc').value
                })
            })
        }

    }

});