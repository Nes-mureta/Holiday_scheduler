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