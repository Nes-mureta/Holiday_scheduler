function toggleForm() {
    const form = document.getElementById('subjectForm');
    form.classList.toggle('hidden');
}

function printTimetable() {
    window.print();
}

function addActivity() {
    const activitiesDiv = document.getElementById('activities');
    const activityDiv = document.createElement('div');
    activityDiv.className = 'activity flex items-center space-x-2 mb-4';
    activityDiv.innerHTML = `
        <input type="text" name="activity_name" placeholder="Activity Name" class="flex-1 p-3 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500">
        <select name="activity_day" class="p-3 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="">Select Day</option>
            <option value="Monday">Monday</option>
            <option value="Tuesday">Tuesday</option>
            <option value="Wednesday">Wednesday</option>
            <option value="Thursday">Thursday</option>
            <option value="Friday">Friday</option>
        </select>                
        <select name="activity_time" class="p-3 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="">Select Time Slot</option>
            <option value="08:00 AM - 09:00 AM">08:00 AM - 09:00 AM</option>
            <option value="09:00 AM - 10:00 AM">09:00 AM - 10:00 AM</option>
            <option value="10:00 AM - 11:00 AM">10:00 AM - 11:00 AM</option>
            <option value="11:00 AM - 12:00 PM">11:00 AM - 12:00 PM</option>
            <option value="01:00 PM - 02:00 PM">01:00 PM - 02:00 PM</option>
            <option value="02:00 PM - 03:00 PM">02:00 PM - 03:00 PM</option>
            <option value="03:00 PM - 04:00 PM">03:00 PM - 04:00 PM</option>
            <option value="04:00 PM - 05:00 PM">04:00 PM - 05:00 PM</option>
        </select>
        <button type="button" onclick="removeActivity(this)" class="px-3 py-1 bg-red-500 text-white rounded-lg">Remove</button>
    `;
    activitiesDiv.appendChild(activityDiv);
}

function removeActivity(button) {
    button.parentElement.remove();
}

document.addEventListener('DOMContentLoaded', function () {
    const deleteButton = document.getElementById('deleteButton');
    deleteButton.addEventListener('click', function () {
        const deleteUrl = deleteButton.getAttribute('data-url');  // Get URL from data attribute
        window.location.href = deleteUrl;
    });
});