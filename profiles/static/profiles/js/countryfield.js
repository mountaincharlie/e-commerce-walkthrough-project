// gets and stores the value of the counrty field when the page loads
let countrySelected = $('#id_default_country');

// the first value will be empty and so False
if(!countrySelected.val()){
    countrySelected.css('color', '#b6b2b2');
};

// capturing the change event for when the user makes a new selection
countrySelected.change(function() {
    selection = $(this).val();
    if(!selection){
        $(this).css('color', '#b6b2b2');
    } else {
        $(this).css('color', '#000');
    }
});                        