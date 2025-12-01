// Reproductor de Audio Mejorado (Corregido)
(function($) {
    'use strict';

    // Constructor del reproductor
    function ReproductorAudio() {
        this.audio = null;
        this.playlist = [];
        this.currentIndex = 0;
        this.isPlaying = false;
        this.isContinuous = false;
        this.volume = 0.7;
        this.isSeeking = false;
        this.init();
    }

    ReproductorAudio.prototype = {
        init: function() {
            this.audio = new Audio();
            this.audio.volume = this.volume;
            
            // DEBUG: Escuchar cuando el audio se reinicia
            const self = this;
            this.audio.addEventListener('emptied', function() {
                // console.warn('⚠️ AUDIO EMPTIED - El audio fue vaciado!');
            });
            
            this.setupEventListeners();
        },

        setupEventListeners: function() {
            const self = this;

            // Cuando la canción está lista
            this.audio.addEventListener('loadedmetadata', function() {
                self.updateDuration();
            });

            // Actualizar progreso
            this.audio.addEventListener('timeupdate', function() {
                self.updateProgress();
            });

            // Cuando termina la canción
            this.audio.addEventListener('ended', function() {
                if (self.isContinuous && self.currentIndex < self.playlist.length - 1) {
                    self.next();
                } else {
                    self.stop();
                }
            });

            // DEBUG events
            this.audio.addEventListener('seeking', function() {
                // console.log('📍 Evento SEEKING');
            });
            
            this.audio.addEventListener('seeked', function() {
                // console.log('📍 Evento SEEKED');
            });

            // Control de play/pause
            $(document).on('click', '.player-play-btn', function() {
                self.togglePlay();
            });

            // Control de siguiente
            $(document).on('click', '.player-next-btn', function() {
                self.next();
            });

            // Control de anterior
            $(document).on('click', '.player-prev-btn', function() {
                self.prev();
            });

            // Control de reproducción continua
            $(document).on('click', '.player-loop-btn', function() {
                self.toggleContinuous();
            });

            // --- CORRECCIÓN BARRA DE PROGRESO ---
            var progressBar = document.querySelector('.player-progress-bar');
            if (progressBar) {
                // Handler para seek corregido
                var handleSeek = function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    if (!self.audio || !self.audio.duration || isNaN(self.audio.duration)) {
                        return false;
                    }
                    
                    // CORRECCIÓN PRINCIPAL:
                    // Siempre usamos la barra principal (progressBar) como referencia,
                    // nunca e.currentTarget porque eso podría ser el 'fill' (hijo).
                    var bar = progressBar; 
                    var rect = bar.getBoundingClientRect();
                    
                    // Obtener posición X
                    var clientX = e.clientX;
                    if (e.touches && e.touches[0]) {
                        clientX = e.touches[0].clientX;
                    }
                    
                    var offsetX = clientX - rect.left;
                    var width = rect.width;
                    
                    // Asegurar porcentaje entre 0 y 1
                    var percentage = Math.max(0, Math.min(1, offsetX / width));
                    var newTime = self.audio.duration * percentage;
                    
                    // console.log('🎵 Seek a:', newTime.toFixed(2) + 's');
                    
                    // Cambiar el tiempo
                    self.audio.currentTime = newTime;
                    
                    // Actualizar la barra visual inmediatamente
                    self.updateProgress();
                    
                    return false;
                };
                
                // Agregar listeners solo al padre (progressBar)
                progressBar.addEventListener('mousedown', handleSeek, true);
                progressBar.addEventListener('touchstart', handleSeek, true);
                
                // Bloquear el click estándar
                progressBar.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                }, true);
                
                console.log('✅ Barra de progreso configurada correctamente');
            } else {
                console.warn('⚠️ No se encontró .player-progress-bar');
            }

            // Control de volumen
            $(document).on('input', '.player-volume-slider', function() {
                self.setVolume($(this).val() / 100);
            });

            // Click en canción para reproducir
            $(document).on('click', '.play-song-btn', function() {
                const index = $(this).data('index');
                self.playSongAtIndex(index);
            });
        },

        loadPlaylist: function(songs) {
            this.playlist = songs;
            this.renderPlaylist();
        },

        renderPlaylist: function() {
            const $container = $('.player-playlist');
            if (!$container.length) return;

            let html = '';
            this.playlist.forEach((song, index) => {
                html += `
                    <div class="playlist-item ${index === this.currentIndex ? 'active' : ''}" data-index="${index}">
                        <div class="playlist-item-info">
                            <button class="play-song-btn" data-index="${index}">
                                <i class="fa fa-play"></i>
                            </button>
                            <div class="song-details">
                                <h6>${song.titulo}</h6>
                                <p>${song.banda}</p>
                            </div>
                        </div>
                        <span class="song-duration">${song.duracion || '--:--'}</span>
                    </div>
                `;
            });
            $container.html(html);
        },

        playSongAtIndex: function(index) {
            if (index < 0 || index >= this.playlist.length) return;

            this.currentIndex = index;
            const song = this.playlist[index];

            if (!song.archivo) {
                this.showNotification('Esta canción no tiene archivo de audio', 'error');
                return;
            }

            this.audio.src = song.archivo;
            this.audio.load();
            this.play();
            this.updatePlayerInfo(song);
            this.updateActivePlaylistItem();
        },

        play: function() {
            const self = this;
            this.audio.play().then(function() {
                self.isPlaying = true;
                self.updatePlayButton();
                self.startEqualizer();
            }).catch(function(error) {
                console.error('Error al reproducir:', error);
                self.showNotification('Error al reproducir', 'error');
            });
        },

        pause: function() {
            this.audio.pause();
            this.isPlaying = false;
            this.updatePlayButton();
            this.stopEqualizer();
        },

        stop: function() {
            this.audio.pause();
            this.audio.currentTime = 0;
            this.isPlaying = false;
            this.updatePlayButton();
            this.stopEqualizer();
        },

        togglePlay: function() {
            if (this.isPlaying) {
                this.pause();
            } else {
                if (this.playlist.length === 0) {
                    this.showNotification('No hay canciones', 'info');
                    return;
                }
                if (!this.audio.src) {
                    this.playSongAtIndex(0);
                } else {
                    this.play();
                }
            }
        },

        next: function() {
            if (this.currentIndex < this.playlist.length - 1) {
                this.playSongAtIndex(this.currentIndex + 1);
            } else if (this.isContinuous) {
                this.playSongAtIndex(0);
            }
        },

        prev: function() {
            if (this.currentIndex > 0) {
                this.playSongAtIndex(this.currentIndex - 1);
            } else if (this.isContinuous) {
                this.playSongAtIndex(this.playlist.length - 1);
            }
        },

        // Nota: La función seek interna ya no es estrictamente necesaria para el click de la barra
        // ya que lo manejamos en el evento mousedown, pero se mantiene por si se usa externamente.
        seek: function(percentage) {
            if (!this.audio.duration || isNaN(this.audio.duration)) return;
            
            const newTime = this.audio.duration * percentage;
            this.audio.currentTime = newTime;
            this.updateProgress();
        },

        setVolume: function(volume) {
            this.volume = volume;
            this.audio.volume = volume;
            $('.player-volume-slider').val(volume * 100);
            
            const $icon = $('.player-volume-icon i');
            if (volume === 0) {
                $icon.attr('class', 'fa fa-volume-off');
            } else if (volume < 0.5) {
                $icon.attr('class', 'fa fa-volume-down');
            } else {
                $icon.attr('class', 'fa fa-volume-up');
            }
        },

        toggleContinuous: function() {
            this.isContinuous = !this.isContinuous;
            $('.player-loop-btn').toggleClass('active', this.isContinuous);
            
            const mensaje = this.isContinuous ? 'Loop activado' : 'Loop desactivado';
            this.showNotification(mensaje, 'info');
        },

        updateProgress: function() {
            if (!this.audio.duration) return;

            const percentage = (this.audio.currentTime / this.audio.duration) * 100;
            $('.player-progress-fill').css('width', percentage + '%');

            // Actualizar tiempo
            $('.player-current-time').text(this.formatTime(this.audio.currentTime));
        },

        updateDuration: function() {
            $('.player-total-time').text(this.formatTime(this.audio.duration));
        },

        updatePlayButton: function() {
            const $btn = $('.player-play-btn i');
            if (this.isPlaying) {
                $btn.attr('class', 'fa fa-pause');
            } else {
                $btn.attr('class', 'fa fa-play');
            }
        },

        updatePlayerInfo: function(song) {
            $('.player-song-title').text(song.titulo);
            $('.player-song-artist').text(song.banda);
            if (song.imagen) {
                $('.player-song-image').attr('src', song.imagen);
            }
        },

        updateActivePlaylistItem: function() {
            $('.playlist-item').removeClass('active');
            $(`.playlist-item[data-index="${this.currentIndex}"]`).addClass('active');
        },

        startEqualizer: function() {
            $('.player-equalizer').addClass('playing');
        },

        stopEqualizer: function() {
            $('.player-equalizer').removeClass('playing');
        },

        formatTime: function(seconds) {
            if (isNaN(seconds)) return '00:00';
            const mins = Math.floor(seconds / 60);
            const secs = Math.floor(seconds % 60);
            return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        },

        showNotification: function(message, type) {
            const $notification = $(`
                <div class="player-notification ${type}">
                    <i class="fa ${type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
                    <span>${message}</span>
                </div>
            `);
            
            $('body').append($notification);
            
            setTimeout(function() {
                $notification.addClass('show');
            }, 10);
            
            setTimeout(function() {
                $notification.removeClass('show');
                setTimeout(function() {
                    $notification.remove();
                }, 300);
            }, 2000);
        }
    };

    // Instancia global del reproductor
    window.reproductorAudio = null;

    // Inicializar cuando el documento esté listo
    $(document).ready(function() {
        if ($('.audio-player-container').length) {
            window.reproductorAudio = new ReproductorAudio();
        }
    });

})(jQuery);