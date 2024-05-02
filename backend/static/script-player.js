document.addEventListener("DOMContentLoaded", function() {
    const queryParams = new URLSearchParams(window.location.search);
    const id = queryParams.get('id');
    
    videoElement.src = "/uploads/"+id;

});