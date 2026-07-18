/* ===== YourDriveAi Home Page — Premium Interactions ===== */
document.addEventListener('DOMContentLoaded', function () {
    initScrollAnimations();
    initCounters();
    initTestimonialCarousel();
    initCarScroll();
    initWishlist();
});

/* ============================================================
   Scroll-triggered animations
   ============================================================ */
function initScrollAnimations() {
    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.08 });

    document.querySelectorAll(
        '.animate-on-scroll, .stagger'
    ).forEach(function (el) {
        observer.observe(el);
    });
}

/* ============================================================
   Animated Counters
   ============================================================ */
function initCounters() {
    var counters = document.querySelectorAll('.stat-number[data-target]');
    if (!counters.length) return;

    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                var el = entry.target;
                var target = parseFloat(el.getAttribute('data-target')) || 0;
                var suffix = el.getAttribute('data-suffix') || '';
                animateCounter(el, target, suffix);
                observer.unobserve(el);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(function (el) {
        observer.observe(el);
    });
}

function animateCounter(el, target, suffix) {
    var duration = 2200;
    var start = 0;
    var startTime = null;

    function step(timestamp) {
        if (!startTime) startTime = timestamp;
        var progress = Math.min((timestamp - startTime) / duration, 1);
        // Cubic ease-out
        var eased = 1 - Math.pow(1 - progress, 3);
        var current = Math.round(start + (target - start) * eased);

        el.textContent = current.toLocaleString('en-IN') + suffix;

        if (progress < 1) {
            requestAnimationFrame(step);
        } else {
            el.textContent = target.toLocaleString('en-IN') + suffix;
        }
    }
    requestAnimationFrame(step);
}

/* ============================================================
   Testimonial Carousel
   ============================================================ */
function initTestimonialCarousel() {
    var container = document.querySelector('.testimonial-carousel');
    if (!container) return;

    var cards = container.querySelectorAll('.testimonial-card-ui');
    var dots = container.querySelectorAll('.test-dot');
    var current = 0;
    if (cards.length <= 1) return;

    function showSlide(index) {
        cards.forEach(function (card, i) {
            card.style.display = i === index ? 'block' : 'none';
            card.style.opacity = i === index ? '1' : '0';
        });
        dots.forEach(function (dot, i) {
            dot.classList.toggle('active', i === index);
        });
        current = index;
    }

    showSlide(0);

    dots.forEach(function (dot, i) {
        dot.addEventListener('click', function () { showSlide(i); });
    });

    var interval = setInterval(function () {
        showSlide((current + 1) % cards.length);
    }, 5000);

    // Pause on hover
    container.addEventListener('mouseenter', function () { clearInterval(interval); });
    container.addEventListener('mouseleave', function () {
        interval = setInterval(function () {
            showSlide((current + 1) % cards.length);
        }, 5000);
    });
}

/* ============================================================
   Horizontal Car Scroll
   ============================================================ */
function initCarScroll() {
    var wrap = document.querySelector('.cars-scroll-wrap');
    if (!wrap) return;
    var scrollContainer = wrap.querySelector('.cars-scroll');
    if (!scrollContainer) return;

    var leftBtn = document.querySelector('.scroll-btn-left');
    var rightBtn = document.querySelector('.scroll-btn-right');

    if (leftBtn) {
        leftBtn.addEventListener('click', function () {
            scrollContainer.scrollBy({ left: -300, behavior: 'smooth' });
        });
    }
    if (rightBtn) {
        rightBtn.addEventListener('click', function () {
            scrollContainer.scrollBy({ left: 300, behavior: 'smooth' });
        });
    }
}

/* ============================================================
   Wishlist toggle
   ============================================================ */
function initWishlist() {
    document.querySelectorAll('.card-wishlist').forEach(function (btn) {
        btn.addEventListener('click', function () {
            this.classList.toggle('liked');
            var icon = this.querySelector('i');
            if (this.classList.contains('liked')) {
                icon.className = 'bi bi-heart-fill';
            } else {
                icon.className = 'bi bi-heart';
            }
        });
    });
}
