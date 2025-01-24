function updateCompleted(entryId, isCompleted) {
    $.ajax({
        url: updateTimetableUrl,
        method: "POST",
        data: {
            'entry_id': entryId,
            'completed': isCompleted,
            'csrfmiddlewaretoken': csrfToken
        },
        success: function(response) {
            console.log('Update successful');
        },
        error: function(response) {
            console.log('Update failed');
        }
    });
}

$(document).ready(function() {
    var fullName = window.profileFullName;
    var education = window.profileEducation;

    if (!fullName || !education) {
        $('#incomplete').show();
    } else {
        $('#incomplete').hide();
    }
});