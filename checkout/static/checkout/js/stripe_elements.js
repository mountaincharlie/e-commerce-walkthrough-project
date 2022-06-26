/*
    Custom payment flow:
    https://stripe.com/docs/payments/accept-a-payment?platform=web&ui=elements#web-collect-payment-details

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

// getting stripe_public_key and client_secret text without first and last chars ('')
var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
var client_secret = $('#id_client_secret').text().slice(1, -1);

// using stripe's builtin JS to setup Stripe
var stripe = Stripe(stripe_public_key);
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
