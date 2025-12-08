// Sistema de Favoritos con LocalStorage y Backend
(function($) {
    'use strict';

    // Verificar si el usuario está autenticado (variable global desde template)
    const isAuthenticated = typeof window.userAuthenticated !== 'undefined' && window.userAuthenticated;

    // Objeto para manejar los favoritos
    const Favoritos = {
        // Obtener CSRF token para peticiones POST
        getCsrfToken: function() {
            return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
        },

        // Obtener todos los favoritos del localStorage
        obtenerFavoritos: function() {
            try {
                const favoritos = localStorage.getItem('bandasFavoritas');
                return favoritos ? JSON.parse(favoritos) : [];
            } catch(e) {
                console.warn('Favoritos localStorage corruptos, reseteando.', e);
                localStorage.removeItem('bandasFavoritas');
                return [];
            }
        },

        // Guardar favoritos en localStorage
        guardarFavoritos: function(favoritos) {
            localStorage.setItem('bandasFavoritas', JSON.stringify(favoritos));
        },

        // Verificar si una banda está en favoritos
        esFavorito: function(bandaId) {
            const favoritos = this.obtenerFavoritos();
            return favoritos.some(banda => banda.id === bandaId);
        },

        // Agregar banda a favoritos
        agregarFavorito: function(bandaData) {
            let favoritos = this.obtenerFavoritos();
            
            // Evitar duplicados
            if (!this.esFavorito(bandaData.id)) {
                favoritos.push(bandaData);
                this.guardarFavoritos(favoritos);
                return true;
            }
            return false;
        },

        // Quitar banda de favoritos
        quitarFavorito: function(bandaId) {
            let favoritos = this.obtenerFavoritos();
            favoritos = favoritos.filter(banda => banda.id !== bandaId);
            this.guardarFavoritos(favoritos);
            return true;
        },

        // Toggle favorito (agregar o quitar)
        toggleFavorito: function(bandaData) {
            // Normalizar ID a número
            bandaData.id = Number(bandaData.id) || 0;
            
            if (this.esFavorito(bandaData.id)) {
                this.quitarFavorito(bandaData.id);
                return false; // Se quitó
            } else {
                this.agregarFavorito(bandaData);
                return true; // Se agregó
            }
        },

        // Toggle favorito con sincronización backend
        toggleFavoritoConBackend: function(bandaData) {
            bandaData.id = Number(bandaData.id) || 0;
            const esFavorito = this.esFavorito(bandaData.id);
            
            if (isAuthenticated) {
                // Si está autenticado, usar backend
                return fetch('/api/favoritos/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCsrfToken()
                    },
                    body: JSON.stringify({ banda_id: bandaData.id })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.action === 'added') {
                        // Añadir también a localStorage para sincronización
                        this.agregarFavorito(bandaData);
                        return true;
                    } else if (data.action === 'removed') {
                        this.quitarFavorito(bandaData.id);
                        return false;
                    }
                    throw new Error(data.error || 'Error desconocido');
                })
                .catch(error => {
                    console.error('Error al sincronizar con backend:', error);
                    // Fallback a localStorage si falla backend
                    return Promise.resolve(this.toggleFavorito(bandaData));
                });
            } else {
                // Usuario no autenticado: usar solo localStorage
                return Promise.resolve(this.toggleFavorito(bandaData));
            }
        },

        // Sincronizar favoritos de localStorage con backend al login
        sincronizarConBackend: function() {
            if (!isAuthenticated) return Promise.resolve();
            
            const favoritosLocal = this.obtenerFavoritos();
            const bandaIds = favoritosLocal.map(b => Number(b.id));
            
            if (bandaIds.length === 0) {
                // Si no hay favoritos locales, cargar los del servidor
                return this.cargarDesdeBackend();
            }
            
            // Enviar IDs locales al servidor para sincronizar
            return fetch('/api/favoritos/sincronizar/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({ banda_ids: bandaIds })
            })
            .then(response => response.json())
            .then(data => {
                console.log('Sincronización completada:', data);
                // Cargar todos los favoritos del servidor
                return this.cargarDesdeBackend();
            })
            .catch(error => {
                console.error('Error al sincronizar favoritos:', error);
            });
        },

        // Cargar favoritos desde backend y actualizar localStorage
        cargarDesdeBackend: function() {
            if (!isAuthenticated) return Promise.resolve();
            
            return fetch('/api/favoritos/')
                .then(response => response.json())
                .then(favoritos => {
                    if (Array.isArray(favoritos)) {
                        // Actualizar localStorage con datos del servidor
                        this.guardarFavoritos(favoritos);
                        actualizarContadorFavoritos();
                        return favoritos;
                    }
                })
                .catch(error => {
                    console.error('Error al cargar favoritos desde backend:', error);
                });
        },

        // Obtener cantidad de favoritos
        contarFavoritos: function() {
            return this.obtenerFavoritos().length;
        }
    };

    // Actualizar contador de favoritos en el navbar
    function actualizarContadorFavoritos() {
        const cantidad = Favoritos.contarFavoritos();
        const $contador = $('.favoritos-counter');
        
        $contador.text(cantidad);
        
        // Mostrar/ocultar el badge según la cantidad
        if (cantidad > 0) {
            $contador.fadeIn(300);
        } else {
            $contador.fadeOut(300);
        }
    }

    // Actualizar el estado visual del botón de favoritos
    function actualizarEstadoBoton($boton, esFavorito) {
        const $icono = $boton.find('i');
        
        if (esFavorito) {
            $icono.removeClass('fa-heart-o').addClass('fa-heart');
            $boton.addClass('is-favorite');
            $boton.attr('title', 'Quitar de favoritos');
        } else {
            $icono.removeClass('fa-heart').addClass('fa-heart-o');
            $boton.removeClass('is-favorite');
            $boton.attr('title', 'Agregar a favoritos');
        }
    }

    // Inicializar botones de favoritos
    function inicializarBotonesFavoritos() {
        $('.btn-favorito').each(function() {
            const $boton = $(this);
            const bandaId = parseInt($boton.data('banda-id'));
            const esFavorito = Favoritos.esFavorito(bandaId);
            
            // Establecer estado inicial
            actualizarEstadoBoton($boton, esFavorito);
        });
    }

    // Animación al agregar/quitar favorito
    function animarBotonFavorito($boton, agregado) {
        // Animación de pulso
        $boton.addClass('pulse-animation');
        
        setTimeout(function() {
            $boton.removeClass('pulse-animation');
        }, 600);

        // Mostrar mensaje temporal
        const mensaje = agregado ? '¡Agregado a favoritos!' : 'Quitado de favoritos';
        mostrarNotificacion(mensaje, agregado);
    }

    // Mostrar notificación temporal
    function mostrarNotificacion(mensaje, esExito) {
        const tipoClase = esExito ? 'success' : 'info';
        const icono = esExito ? 'fa-check-circle' : 'fa-info-circle';
        
        // Crear elemento de notificación
        const $notificacion = $(`
            <div class="favoritos-notification ${tipoClase}">
                <i class="fa ${icono}"></i>
                <span>${mensaje}</span>
            </div>
        `);
        
        // Agregar al body
        $('body').append($notificacion);
        
        // Mostrar con animación
        setTimeout(function() {
            $notificacion.addClass('show');
        }, 10);
        
        // Ocultar y remover después de 2 segundos
        setTimeout(function() {
            $notificacion.removeClass('show');
            setTimeout(function() {
                $notificacion.remove();
            }, 300);
        }, 2000);
    }

    // Manejar click en botón de favoritos
    $(document).on('click', '.btn-favorito', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        const $boton = $(this);
        const bandaData = {
            id: parseInt($boton.data('banda-id')),
            nombre: $boton.data('banda-nombre'),
            pais: $boton.data('banda-pais'),
            imagen: $boton.data('banda-imagen'),
            url: $boton.data('banda-url')
        };
        
        // Toggle favorito con sincronización backend
        const togglePromise = Favoritos.toggleFavoritoConBackend(bandaData);
        
        // Manejar resultado (puede ser Promise o valor directo)
        Promise.resolve(togglePromise).then(agregado => {
            // Actualizar estado visual
            actualizarEstadoBoton($boton, agregado);
            
            // Animar botón
            animarBotonFavorito($boton, agregado);
            
            // Actualizar contador
            actualizarContadorFavoritos();
            
            // Si estamos en la página de favoritos, actualizar la vista
            if ($('body').hasClass('pagina-favoritos')) {
                setTimeout(function() {
                    cargarFavoritosEnPagina();
                }, 300);
            }
        }).catch(error => {
            console.error('Error al manejar favorito:', error);
            mostrarNotificacion('Error al guardar favorito', false);
        });
    });

    // Cargar favoritos en la página de favoritos
    function cargarFavoritosEnPagina() {
        const favoritos = Favoritos.obtenerFavoritos();
        const $container = $('.favoritos-container');
        
        if (favoritos.length === 0) {
            $container.html(`
                <div class="col-12">
                    <div class="no-favoritos text-center">
                        <i class="fa fa-heart-o"></i>
                        <h3>No tienes bandas favoritas</h3>
                        <p>Explora nuestro catálogo y agrega tus bandas favoritas</p>
                        <a href="/bandas/" class="btn oneMusic-btn mt-30">Ver Bandas</a>
                    </div>
                </div>
            `);
            return;
        }
        
        let html = '';
        favoritos.forEach(function(banda) {
            const imagenSrc = banda.imagen || '/static/img/bg-img/a1.jpg';
            html += `
                <div class="col-12 col-sm-4 col-md-3 col-lg-2 single-album-item favorito-item" data-banda-id="${banda.id}">
                    <div class="single-album">
                        <div class="album-thumb-wrapper">
                            <img src="${imagenSrc}" alt="${banda.nombre}">
                            <button class="btn-favorito btn-favorito-overlay is-favorite" 
                                    data-banda-id="${banda.id}"
                                    data-banda-nombre="${banda.nombre}"
                                    data-banda-pais="${banda.pais}"
                                    data-banda-imagen="${banda.imagen}"
                                    data-banda-url="${banda.url}"
                                    title="Quitar de favoritos">
                                <i class="fa fa-heart"></i>
                            </button>
                        </div>
                        <div class="album-info">
                            <a href="${banda.url}">
                                <h5>${banda.nombre}</h5>
                            </a>
                            <p>${banda.pais}</p>
                        </div>
                    </div>
                </div>
            `;
        });
        
        $container.html(html);
    }

    // Inicialización cuando el documento está listo
    $(document).ready(function() {
        // Si el usuario está autenticado, sincronizar favoritos
        if (isAuthenticated) {
            Favoritos.sincronizarConBackend().then(() => {
                // Después de sincronizar, actualizar UI
                actualizarContadorFavoritos();
                inicializarBotonesFavoritos();
                
                if ($('body').hasClass('pagina-favoritos')) {
                    cargarFavoritosEnPagina();
                    setTimeout(cargarCancionesFavoritas, 500);
                }
            });
        } else {
            // Usuario no autenticado: usar localStorage
            actualizarContadorFavoritos();
            inicializarBotonesFavoritos();
            
            if ($('body').hasClass('pagina-favoritos')) {
                cargarFavoritosEnPagina();
                setTimeout(cargarCancionesFavoritas, 500);
            }
        }
    });

    // Cargar canciones de bandas favoritas en el reproductor
    function cargarCancionesFavoritas() {
        const favoritos = Favoritos.obtenerFavoritos();
        
        // Hacer petición AJAX para obtener canciones de las bandas favoritas
        if (favoritos.length === 0) {
            return;
        }
        
        const bandasIds = favoritos.map(b => b.id);
        
        // Simular carga de canciones (en producción esto vendría del backend)
        // Por ahora creamos una estructura de ejemplo
        fetch('/api/canciones-favoritos/?ids=' + bandasIds.join(','))
            .then(response => response.json())
            .then(canciones => {
                if (window.reproductorAudio && canciones.length > 0) {
                    window.reproductorAudio.loadPlaylist(canciones);
                    $('.playlist-count').text(canciones.length + ' canciones');
                }
            })
            .catch(error => {
                console.log('No se pudieron cargar las canciones:', error);
                // Cargar canciones de ejemplo si falla
                cargarCancionesEjemplo(favoritos);
            });
    }

    // Cargar canciones de ejemplo cuando no hay backend
    function cargarCancionesEjemplo(favoritos) {
        const cancionesEjemplo = [];
        
        favoritos.forEach(banda => {
            // Crear 2-3 canciones de ejemplo por banda
            for (let i = 1; i <= 2; i++) {
                cancionesEjemplo.push({
                    titulo: `Canción ${i}`,
                    banda: banda.nombre,
                    imagen: banda.imagen,
                    archivo: '', // No hay archivo de audio
                    duracion: '3:45'
                });
            }
        });
        
        if (window.reproductorAudio && cancionesEjemplo.length > 0) {
            window.reproductorAudio.loadPlaylist(cancionesEjemplo);
            $('.playlist-count').text(cancionesEjemplo.length + ' canciones');
        }
    }

})(jQuery);
