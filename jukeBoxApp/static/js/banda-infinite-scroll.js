/**
 * Banda Infinite Scroll - Sistema de carga infinita para lista de bandas
 * Utiliza AJAX, IntersectionObserver e Isotope
 */

(function waitForjQuery(){
    if(!window.jQuery){ 
        return setTimeout(waitForjQuery, 50); 
    }
    
    (function($){
        // Estado de la aplicación
        let page = 1;
        const pageSize = 6; // Cargar 6 bandas cada vez
        let isLoading = false;
        let hasMore = true;
        let currentFilter = '*';
        
        // Variables de configuración (se inicializarán en init)
        let apiUrl;
        let defaultThumb;
        let addFavoritesText;

        /**
         * Construye el HTML para un item de banda
         * @param {Object} b - Objeto con datos de la banda
         * @param {boolean} isNew - Si es una banda cargada dinámicamente
         * @returns {string} HTML de la banda
         */
        function buildItem(b, isNew){
            const img = b.imagen || defaultThumb;
            const firstChar = b.nombre.charAt(0).toLowerCase();
            const letterClass = /[0-9]/.test(firstChar) ? 'number' : firstChar;
            const fadeClass = isNew ? 'fade-in-new' : '';
            
            return `<div class="col-12 col-sm-4 col-md-3 col-lg-2 single-album-item ${letterClass} ${fadeClass}">
    <div class="single-album">
        <div class="album-thumb-wrapper">
            <img src="${img}" alt="${b.nombre}">
            <button class="btn-favorito btn-favorito-overlay" 
                    data-banda-id="${b.id}" 
                    data-banda-nombre="${b.nombre}" 
                    data-banda-pais="${b.pais}" 
                    data-banda-imagen="${img}" 
                    data-banda-url="${b.url}" 
                    title="${addFavoritesText}">
                <i class="fa fa-heart-o"></i>
            </button>
        </div>
        <div class="album-info">
            <a href="${b.url}"><h5>${b.nombre}</h5></a>
            <p>${b.pais}</p>
        </div>
    </div>
</div>`;
        }

        /**
         * Carga la siguiente página de bandas vía AJAX
         */
        function loadNext(){
            if(isLoading || !hasMore) {
                console.log('No se carga más. isLoading:', isLoading, 'hasMore:', hasMore);
                return;
            }
            
            isLoading = true;
            console.log('🔄 Mostrando spinner...');
            $('#loading-indicator').fadeIn(400);
            const nextPage = page + 1;
            
            console.log('⬇️ Cargando página', nextPage, 'filter:', currentFilter);
            
            $.get(apiUrl, { 
                page: nextPage, 
                page_size: pageSize, 
                filter: currentFilter 
            })
            .done(function(data){
                if(data.bands && data.bands.length){
                    let html = '';
                    data.bands.forEach(function(b){ 
                        html += buildItem(b, true); // true = es nueva, añade animación
                    });
                    const $items = $(html);
                    
                    // Esperar a que las imágenes se carguen antes de actualizar Isotope
                    $items.imagesLoaded(function(){
                        $('#band-list').append($items);
                        const $grid = $('.oneMusic-albums');
                        if($grid.data('isotope')){ 
                            $grid.isotope('appended', $items);
                        }
                        page = nextPage;
                    });
                }
                hasMore = data.has_more || false;
            })
            .fail(function(xhr, status, error){ 
                console.error('Error loading bandas:', error); 
            })
            .always(function(){ 
                // Asegurar que el spinner se vea al menos 800ms
                setTimeout(function(){
                    isLoading = false;
                    $('#loading-indicator').fadeOut(400);
                    console.log('✅ Carga completada');
                }, 800);
            });
        }

        /**
         * Configura IntersectionObserver para detectar scroll infinito
         */
        function setupInfiniteScroll(){
            const sentinel = document.getElementById('infinite-sentinel');
            if(!sentinel) {
                console.warn('Sentinel element not found');
                return;
            }
            
            if(window.IntersectionObserver){
                const observer = new IntersectionObserver(function(entries){
                    entries.forEach(function(entry){
                        if(entry.isIntersecting && !isLoading && hasMore){
                            console.log('Sentinel visible - Cargando más bandas...');
                            loadNext();
                        }
                    });
                }, {
                    root: null,
                    rootMargin: '200px', // Reducido para que solo cargue cuando estés más cerca
                    threshold: 0.1
                });
                observer.observe(sentinel);
                console.log('IntersectionObserver configurado');
            } else {
                // Fallback para navegadores antiguos sin IntersectionObserver
                $(window).on('scroll.infinite', function(){
                    if(!hasMore || isLoading) return;
                    if($(window).scrollTop() + $(window).height() > $(document).height() - 400){
                        loadNext();
                    }
                });
            }
        }

        /**
         * Carga bandas con un filtro específico
         * @param {string} filterValue - Letra o '*' para todas
         */
        function loadWithFilter(filterValue){
            currentFilter = filterValue;
            page = 0;
            hasMore = true;
            
            // Vaciar lista actual
            $('#band-list').empty();
            isLoading = true;
            $('#loading-indicator').fadeIn(400);
            
            console.log('Filter changed to:', currentFilter);
            
            // Cargar primera página con el nuevo filtro
            $.get(apiUrl, { 
                page: 1, 
                page_size: pageSize, 
                filter: currentFilter 
            })
            .done(function(data){
                if(data.bands && data.bands.length){
                    let html = '';
                    data.bands.forEach(function(b){ 
                        html += buildItem(b, true); // true = es nueva, añade animación
                    });
                    const $items = $(html);
                    
                    $items.imagesLoaded(function(){
                        $('#band-list').append($items);
                        const $grid = $('.oneMusic-albums');
                        if($grid.data('isotope')){
                            $grid.isotope('reloadItems').isotope('layout');
                        }
                        page = 1;
                        hasMore = data.has_more || false;
                    });
                } else {
                    hasMore = false;
                }
            })
            .fail(function(xhr, status, error){ 
                console.error('Error loading bandas:', error); 
            })
            .always(function(){ 
                // Asegurar que el spinner se vea al menos 800ms
                setTimeout(function(){
                    isLoading = false;
                    $('#loading-indicator').fadeOut(400);
                }, 800);
            });
        }

        /**
         * Inicialización al cargar la página
         */
        function init(){
            // Obtener configuración desde data attributes del contenedor
            const config = $('#band-list-config');
            if(!config.length){
                console.error('Elemento #band-list-config no encontrado');
                return;
            }
            
            apiUrl = config.data('api-url');
            defaultThumb = config.data('default-thumb');
            addFavoritesText = config.data('add-favorites-text') || 'Agregar a favoritos';
            
            console.log('Configuración cargada:', {apiUrl, defaultThumb, addFavoritesText});
            
            if(!apiUrl){
                console.error('No se pudo obtener la URL de la API');
                return;
            }
            
            // Verificar estado inicial
            $.get(apiUrl, { 
                page: 1, 
                page_size: pageSize, 
                filter: currentFilter 
            })
            .done(function(data){
                if(data && data.has_more !== undefined){
                    hasMore = data.has_more;
                    console.log('Initial hasMore:', hasMore);
                }
            })
            .always(function(){
                // Layout de Isotope
                const $grid = $('.oneMusic-albums');
                if($grid.data('isotope')){
                    $grid.isotope('layout');
                }
                // Iniciar observador de scroll
                setupInfiniteScroll();
            });
        }

        /**
         * Event handler para filtros alfabéticos
         */
        function setupFilterHandlers(){
            $('.browse-by-catagories a').on('click', function(e){
                e.preventDefault();
                
                // Actualizar clase active
                $('.browse-by-catagories a').removeClass('active');
                $(this).addClass('active');
                
                // Obtener filtro
                let filterValue = $(this).data('filter') || '*';
                if(typeof filterValue === 'string'){
                    filterValue = filterValue.replace(/^\./, '');
                }
                
                loadWithFilter(filterValue);
            });
        }

        // Inicializar cuando el documento esté listo
        $(document).ready(function(){
            console.log('Banda infinite scroll - Inicializando...');
            init();
            setupFilterHandlers();
        });

    })(jQuery);
})();

