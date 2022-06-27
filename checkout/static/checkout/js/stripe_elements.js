/*
    Custom payment flow:
    https://stripe.com/docs/payments/accept-a-payment?platform=web&ui=elements#web-collect-payment-details

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

// USING JQuery

// getting stripe_public_key and client_secret text without first and last chars ('')
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);

// using stripe's builtin JS to setup Stripe
var stripe = Stripe(stripePublicKey);
// create instance of stripe elements
var elements = stripe.elements();


// the card element can accept a style argument
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        // bootstrap danger class color
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

// create card element and add style
var card = elements.create('card', {style: style});
// mount the card to the #card-element div 
card.mount('#card-element');


// ------ handling real-time errors on card element

/*
    calling a change Ev Listener to check for errors
    -gets the card-errors div (near card div on checkout page)
    so that if there are errors they can be displayed to the user
    through this
    -if theres an error in the event, the message is created and put into
    the card-errors div
*/
card.addEventListener('change', function(ev) {
    var errorDiv = document.getElementById('card-errors');
    if (ev.error) {
        var error_msg_html = `
            <span role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${ev.error.message}</span>
        `
        $(errorDiv).html(error_msg_html);
    } else {
        errorDiv.textContent = '';
    }
});


// ------ handling the form submit with 'submit' Ev Listener
/*
    -gets the 'payment-form' form element
    -applies Ev Listener to this element
    -the default action (POST) is prevented
    -disables the card element and submit button to prevent mutiple
    submissions
    -calls the fadeToggle on 'payment-form' and 'loading-overlay'
    -uses stripe's confirmCardPayment method to securely send
    the card details to stripe with the clientSecret
    -then checks if there is an error
    -if there is, it gets the card-errors div, creates
    the error message and then puts it in the div
    -then it calls the fadeToggle on 'payment-form' and 'loading-overlay'
    and turns off the disable on the card element and submit
    button so the user could correct the error and when the submit
    button is clicked again, the Ev Listener would eb called again
    -if there are no errors, the paymentIntent's status is set to
    'succeeded' and the form is submitted
*/
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();

    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);

    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }

    }).then(function(result) {
        if (result.error) {

            var errorDiv = document.getElementById('card-errors');

            var error_msg_html = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            
            $(errorDiv).html(error_msg_html);

            $('#payment-form').fadeToggle(100);
            $('#loading-overlay').fadeToggle(100);

            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);

        } else {
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});
