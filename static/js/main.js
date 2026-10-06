document.addEventListener('DOMContentLoaded', () => {
  // Auto-dismiss alerts after 6 seconds
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(alert => {
    setTimeout(() => {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 6000);
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId && targetId !== '#') {
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
          e.preventDefault();
          targetElement.scrollIntoView({
            behavior: 'smooth'
          });
        }
      }
    });
  });

  // Typewriter Animation for Hero Section Main Big Headline
  const typewriterEl = document.getElementById('heroTypewriter');
  if (typewriterEl) {
    let phrases = [];
    const phrasesAttr = typewriterEl.getAttribute('data-phrases');
    if (phrasesAttr) {
      try {
        phrases = JSON.parse(phrasesAttr);
      } catch (e) {
        phrases = [typewriterEl.innerText.trim()];
      }
    } else {
      phrases = [typewriterEl.innerText.trim() || 'Inspiring Excellence, Nurturing Character'];
    }

    let phraseIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    const typingSpeed = 65; // ms per character
    const deletingSpeed = 35; // ms per char when deleting
    const pauseDelay = 2600; // pause before deleting

    typewriterEl.textContent = '';

    function typeLoop() {
      const currentPhrase = phrases[phraseIndex] || '';

      if (!isDeleting) {
        // Typing characters
        typewriterEl.textContent = currentPhrase.substring(0, charIndex + 1);
        charIndex++;

        if (charIndex === currentPhrase.length) {
          if (phrases.length > 1) {
            isDeleting = true;
            setTimeout(typeLoop, pauseDelay);
          }
          return;
        }
        setTimeout(typeLoop, typingSpeed);
      } else {
        // Deleting characters
        typewriterEl.textContent = currentPhrase.substring(0, charIndex - 1);
        charIndex--;

        if (charIndex === 0) {
          isDeleting = false;
          phraseIndex = (phraseIndex + 1) % phrases.length;
          setTimeout(typeLoop, 350);
          return;
        }
        setTimeout(typeLoop, deletingSpeed);
      }
    }

    // Start typing after initial load
    setTimeout(typeLoop, 400);
  }

  // =========================================================================
  // Interactive Campus Gallery Slider
  // Auto-play, Touch Drag/Swipe, Navigation Buttons, and Responsive Pagination
  // =========================================================================
  const galleryTrack = document.getElementById('gallerySliderTrack');
  const galleryViewport = document.getElementById('gallerySliderViewport');
  const prevBtn = document.getElementById('galleryPrevBtn');
  const nextBtn = document.getElementById('galleryNextBtn');
  const dotsContainer = document.getElementById('galleryDots');
  const playPauseBtn = document.getElementById('galleryPlayPauseBtn');

  if (galleryTrack && galleryViewport) {
    const slides = Array.from(galleryTrack.children);
    let currentIndex = 0;
    let isPlaying = true;
    let autoplayTimer = null;
    let startX = 0;
    let isDragging = false;

    function getVisibleCount() {
      if (window.innerWidth < 576) return 1;
      if (window.innerWidth < 992) return 2;
      return 3;
    }

    function getMaxIndex() {
      const visible = getVisibleCount();
      return Math.max(0, slides.length - visible);
    }

    function renderDots() {
      if (!dotsContainer) return;
      dotsContainer.innerHTML = '';
      const maxIdx = getMaxIndex();
      
      for (let i = 0; i <= maxIdx; i++) {
        const dot = document.createElement('button');
        dot.type = 'button';
        dot.className = `gallery-dot ${i === currentIndex ? 'active' : ''}`;
        dot.setAttribute('aria-label', `Go to slide ${i + 1}`);
        dot.addEventListener('click', () => {
          goToSlide(i);
          resetAutoplay();
        });
        dotsContainer.appendChild(dot);
      }
    }

    function updateSlider() {
      const maxIdx = getMaxIndex();
      if (currentIndex > maxIdx) currentIndex = maxIdx;
      if (currentIndex < 0) currentIndex = 0;

      const slideWidth = slides[0].getBoundingClientRect().width;
      const gap = 24; // matching CSS gap
      const offset = currentIndex * (slideWidth + gap);

      galleryTrack.style.transform = `translateX(-${offset}px)`;

      // Update dot active state
      if (dotsContainer) {
        const dots = dotsContainer.querySelectorAll('.gallery-dot');
        dots.forEach((dot, idx) => {
          dot.classList.toggle('active', idx === currentIndex);
        });
      }
    }

    function goToSlide(index) {
      currentIndex = index;
      updateSlider();
    }

    function nextSlide() {
      const maxIdx = getMaxIndex();
      if (currentIndex >= maxIdx) {
        currentIndex = 0;
      } else {
        currentIndex++;
      }
      updateSlider();
    }

    function prevSlide() {
      const maxIdx = getMaxIndex();
      if (currentIndex <= 0) {
        currentIndex = maxIdx;
      } else {
        currentIndex--;
      }
      updateSlider();
    }

    function startAutoplay() {
      if (autoplayTimer) clearInterval(autoplayTimer);
      autoplayTimer = setInterval(() => {
        if (isPlaying) nextSlide();
      }, 4000);
    }

    function resetAutoplay() {
      if (isPlaying) {
        startAutoplay();
      }
    }

    // Button controls
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        nextSlide();
        resetAutoplay();
      });
    }

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        prevSlide();
        resetAutoplay();
      });
    }

    if (playPauseBtn) {
      playPauseBtn.addEventListener('click', () => {
        isPlaying = !isPlaying;
        if (isPlaying) {
          playPauseBtn.innerHTML = '<i class="fa-solid fa-pause me-1"></i> <span>Pause Slideshow</span>';
          startAutoplay();
        } else {
          playPauseBtn.innerHTML = '<i class="fa-solid fa-play me-1"></i> <span>Play Slideshow</span>';
          if (autoplayTimer) clearInterval(autoplayTimer);
        }
      });
    }

    // Pause on hover
    galleryViewport.addEventListener('mouseenter', () => {
      if (isPlaying && autoplayTimer) clearInterval(autoplayTimer);
    });

    galleryViewport.addEventListener('mouseleave', () => {
      if (isPlaying) startAutoplay();
    });

    // Touch & Mouse Drag Swipe Support
    galleryViewport.addEventListener('touchstart', (e) => {
      startX = e.touches[0].clientX;
    }, { passive: true });

    galleryViewport.addEventListener('touchend', (e) => {
      const endX = e.changedTouches[0].clientX;
      const diffX = startX - endX;
      if (Math.abs(diffX) > 45) {
        if (diffX > 0) nextSlide();
        else prevSlide();
        resetAutoplay();
      }
    }, { passive: true });

    galleryViewport.addEventListener('mousedown', (e) => {
      isDragging = true;
      startX = e.clientX;
    });

    window.addEventListener('mouseup', (e) => {
      if (!isDragging) return;
      isDragging = false;
      const diffX = startX - e.clientX;
      if (Math.abs(diffX) > 45) {
        if (diffX > 0) nextSlide();
        else prevSlide();
        resetAutoplay();
      }
    });

    // Responsive recalculation on resize
    window.addEventListener('resize', () => {
      renderDots();
      updateSlider();
    });

    // Initialize
    renderDots();
    updateSlider();
    startAutoplay();
  }
});


