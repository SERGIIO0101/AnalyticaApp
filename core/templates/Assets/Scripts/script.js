document.addEventListener('DOMContentLoaded',function() {
const sidebarLinks = document.querySelectorAll('.sidebar ul li a');

sidebarLinks.forEach(Link => {
    link.addEventListener('click', function(event){
        event.preventDefault();
        alert('Este enlace aun no está activo.');
        });
    });
}); 