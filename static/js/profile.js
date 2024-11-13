document.getElementById('edit-profile-btn').onclick = function() {
    document.getElementById('edit-profile-form').style.display = 'block';
    document.getElementById('profile-details').style.display = 'none';
    document.getElementById('button').style.display = 'none';
};

document.getElementById('cancel-edit-btn').onclick = function() {
    document.getElementById('edit-profile-form').style.display = 'none';
    document.getElementById('profile-details').style.display = 'block';
};
