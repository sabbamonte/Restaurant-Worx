document.addEventListener('DOMContentLoaded', function() {
    
    // Used to toggle the menu on smaller screens when clicking on the menu button
    function openNav() {
        var x = document.getElementById("navDemo");
        if (x.className.indexOf("w3-show") == -1) {
            x.className += " w3-show";
        } else { 
            x.className = x.className.replace(" w3-show", "");
        }
    }

    // Select My Reviews button
    review_button = document.querySelectorAll('.my_review_button')
    review_button.forEach((review) => {
        review.addEventListener('click', () => {
            show_review(review.name)
        })
    
    })

    // Select all edit buttons and pass them to function
    add_edit = document.querySelectorAll('.edit')
    add_edit.forEach((button) => {
        button.addEventListener('click', () => {
            add_edit_info(button.id)
        })
    })

    // If Checkbox is checked pass it to function
    check_button = document.querySelectorAll('.position_review')
    check_button.forEach((button) => {
        button.addEventListener('click', () => {
            if (button.checked) {
                console.log(button.name)
                position_reviews(button.name)
            }
            else {
                location.href = ""
            }
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
                address: document.querySelector('#inputAddress').value,
                zip: document.querySelector('#inputZip').value,
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

    // Function to show the selected review from my reviews
    function show_review(review) {
        fetch(`/show/${review}`)
        .then(response => response.json())
        .then(review => {
            Array.prototype.forEach.call(review.review, rev => {
                document.getElementById('show_review').innerHTML = 
                `<div class="w3-card w3-round w3-white pop-in">
                    <div class="w3-container text-center">
                    <br>
                        <div class="row w3-center">
                            <div class=col-12 col-md-1>
                                <a role="button" href="" class="w3-button w3-theme btn-sm float-right">x</a>
                            </div>
                        <a href="restaurant/${rev.name}"> <h4 class="w3-center">${rev.name}</h4> </a>
                        <p class="text-center" style="font-size: small;">${rev.address}, NY, ${rev.zip}</p>
                        </div>
                        <hr>
                        <div class="row w3-center">
                            <div class="col-12 col-md-6 text-center">
                                <p class="fa fa-star checked"></p> ${rev.rating} / 5
                            </div>
                            <div class="col-12 col-md-6">
                                <p>${rev.position}</p>
                            </div>
                        </div>
                    </div>
                    <div class="card-body text-center">
                        <table class="table">
                            <thead class="text-center thead-light">
                            <tr>
                            <th scope="col">Days per Week</th>
                            <th scope="col">Hours per Shift</th>
                            <th scope="col">Pay per Week</th>
                            </tr>
                            </thead>
                            <tbody class="text-center ">
                                <tr>
                                <td>${rev.days}</td>
                                <td>${rev.hours}</td>
                                <td>$${rev.pay}</td>
                                </tr>
                            </tbody>
                        </table>
                        <br>
                        <table class="table">
                        <thead class="text-center thead-light">
                            <tr>
                                <th scope="col">Environment</th>
                                <th scope="col">Management</th>
                            </tr>
                        </thead>
                        <tbody class="text-center">
                            <tr>
                                <td>${rev.envo}</td>
                                <td>${rev.mngmt}</td>
                            </tr>
                        </tbody>
                        </table>
                        <br>
                        <table class="table">
                            <thead class="text-center thead-light">
                            <tr>
                                <th scope="col">Comments</th>
                            </tr>
                        </thead>
                        <tbody class="text-center">
                            <tr>
                                <td>${rev.comments}</td>
                            </tr>
                        </tbody>
                        </table>
                        <div class="col-12">
                            <button class="w3-button w3-theme btn-sm" id="${rev.id}" type="button">
                                Delete Review
                            </button>
                        </div>
                    </div>
                </div> `

                button = document.getElementById(rev.id)
                button.addEventListener('click', () => {
                    delete_review(button.id)
                })
            })
        });
    }

    function delete_review(review) {
        fetch(`delete/${review}`, {
            method: 'DELETE'
        })
        window.location.reload();
    }

    function position_reviews(position) {
        fetch(`/position/${position}`)
        .then(response => response.json())
        .then(position => {
            document.getElementById('show_review').innerHTML = ''
            Array.prototype.forEach.call(position.position, pos => {
                new_element = document.createElement(`div`)
                add_br = document.createElement(`br`)
                new_element.className = `w3-card w3-round w3-white pop-in`
                new_element.innerHTML = 
                `<div class="w3-container text-center">
                    <br>
                        <div class="row w3-center">
                            <a href="restaurant/${pos.name}"> <h4 class="w3-center">${pos.name}</h4> </a>
                            <p class="text-center" style="font-size: small;">${pos.address}, NY, ${pos.zip}</p>
                        </div>
                        <hr>
                        <div class="row w3-center">
                            <div class="col-12 col-md-6 text-center">
                                <p class="fa fa-star checked"></p> ${pos.rating} / 5
                            </div>
                            <div class="col-12 col-md-6">
                                <p>${pos.position}</p>
                            </div>
                        </div>
                    </div>
                    <div class="card-body text-center">
                        <table class="table">
                            <thead class="text-center thead-light">
                            <tr>
                            <th scope="col">Days per Week</th>
                            <th scope="col">Hours per Shift</th>
                            <th scope="col">Pay per Week</th>
                            </tr>
                            </thead>
                            <tbody class="text-center ">
                                <tr>
                                <td>${pos.days}</td>
                                <td>${pos.hours}</td>
                                <td>$${pos.pay}</td>
                                </tr>
                            </tbody>
                        </table>
                        <br>
                        <table class="table">
                        <thead class="text-center thead-light">
                            <tr>
                                <th scope="col">Environment</th>
                                <th scope="col">Management</th>
                            </tr>
                        </thead>
                        <tbody class="text-center">
                            <tr>
                                <td>${pos.envo}</td>
                                <td>${pos.mngmt}</td>
                            </tr>
                        </tbody>
                        </table>
                        <br>
                        <table class="table">
                            <thead class="text-center thead-light">
                            <tr>
                                <th scope="col">Comments</th>
                            </tr>
                        </thead>
                        <tbody class="text-center">
                            <tr>
                                <td>${pos.comments}</td>
                            </tr>
                        </tbody>
                        </table>
                    </div>
                </div>
                `
                document.getElementById('show_review').append(new_element, add_br)
            });
        })
    }
});