/// Only allow numbers from 1-9 (49-57) and the 'Enter' key to submit form (13)
$('.box').keypress(function(event) {
    return (event.which >= 49 && event.which <= 57) || event.which === 13;
});
// On keyup trigger move focus to the next box
$('.box').keyup(function(event) {
    if ((this.value.length === this.maxLength) || event.which === 48) {
        if ($(this).parent().is('td:last-child')) {
            $(this).closest('tr').next().children().first().find('.box').focus();
        } else {
            $(this).parent().next().find('.box').focus();
        }
    }
});

// Copy the state of the visible checkbox, outside the submitted form,
// onto a hidden checkbox within the form that will be submitted.
// This is a work around, due to imperfect layout design.
function copyOption() {
    var status = document.getElementById('diag-checkbox').checked;
    document.getElementById('submitted-diag').checked = status;
    console.log(document.getElementById('submitted-diag').checked);
}
