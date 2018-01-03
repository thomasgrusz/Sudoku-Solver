    // Only allow numbers from 1-9 (49-57) and the 'Enter' key to submit (13)
    function checkInput(e) {
        return (e.charCode >= 49 && e.charCode <= 57) || e.charCode == 13;
    }

    // Copy the state of the visible checkbox, outside the submitted form,
    // onto a hidden checkbox within the form that will be submitted.
    // This is a work around, due to imperfect layout design.
    function copyOption() {
        var status = document.getElementById('diag-checkbox').checked;
        document.getElementById('submitted-diag').checked = status;
        console.log(document.getElementById('submitted-diag').checked);
    }
