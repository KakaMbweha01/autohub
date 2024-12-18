// confirm before deleting a car
document.addEventListener('DOMContentLoaded', function (){
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            if (!confirm('Are you sure you want to delete this car?')) {
                event.preventDefault();
            }
        });
    });
});