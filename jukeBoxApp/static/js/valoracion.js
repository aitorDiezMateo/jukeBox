document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('#star-rating .star');
    const input = document.getElementById('id_puntuacion');
    let selected = 0;

    function setVisual(value) {
        stars.forEach(function (s) {
            const v = parseInt(s.getAttribute('data-value'));
            if (v <= value) {
                s.classList.remove('fa-star-o');
                s.classList.add('fa-star');
            } else {
                s.classList.remove('fa-star');
                s.classList.add('fa-star-o');
            }
        });
    }

    stars.forEach(function (star) {
        star.addEventListener('mouseover', function () {
            const v = parseInt(this.getAttribute('data-value'));
            setVisual(v);
            this.classList.add('hovered');
        });
        star.addEventListener('mouseout', function () {
            this.classList.remove('hovered');
            setVisual(selected);
        });
        star.addEventListener('click', function () {
            selected = parseInt(this.getAttribute('data-value'));
            if (input) input.value = selected;
            setVisual(selected);
        });
    });

    // Initialize as empty
    setVisual(0);

    // Validate before submit
    const form = document.getElementById('valoracion-form');
    if (form) {
        form.addEventListener('submit', function (e) {
            if (!input || !input.value || parseInt(input.value) < 1) {
                e.preventDefault();
                // Simple inline feedback; the project can replace with messages later
                alert('Por favor selecciona una puntuación (1-5 estrellas) antes de enviar.');
            }
        });
    }
});
