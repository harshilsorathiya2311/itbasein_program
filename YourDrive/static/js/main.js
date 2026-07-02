document.addEventListener('DOMContentLoaded', function () {
    // Auto-dismiss alerts after 5s
    document.querySelectorAll('.alert-dismissible').forEach(el => {
        setTimeout(() => { bootstrap.Alert.getOrCreateInstance(el).close() }, 5000);
    });

    // Animate elements on scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));

    // Price formatting: add comma separators to numeric inputs
    document.querySelectorAll('input[type="number"]').forEach(el => {
        el.addEventListener('blur', function () {
            if (this.value) {
                this.value = parseFloat(this.value).toLocaleString('en-IN');
            }
        });
    });

    // Tooltip init
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltips.length) [...tooltips].map(el => new bootstrap.Tooltip(el));
});
