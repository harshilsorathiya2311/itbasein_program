(function () {
  'use strict';

  const doc = document;
  const win = window;

  // ─── DOM Ready ───
  doc.addEventListener('DOMContentLoaded', function () {

    // 1. Sticky Navbar Shadow on Scroll
    const navbar = doc.querySelector('.navbar');
    if (navbar) {
      const toggleClass = () => {
        navbar.classList.toggle('scrolled', win.scrollY > 20);
      };
      toggleClass();
      win.addEventListener('scroll', toggleClass, { passive: true });
    }

    // 2. Auto-dismiss Alerts
    doc.querySelectorAll('.alert-dismissible').forEach(function (alert) {
      setTimeout(function () {
        const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
        bsAlert.close();
      }, 5000);
    });

    // 3. Scroll-Triggered Animations (IntersectionObserver)
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-in');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    doc.querySelectorAll('.animate-on-scroll').forEach(function (el) {
      observer.observe(el);
    });

    // 4. Number Input Formatting (Indian locale)
    doc.querySelectorAll('input[type="number"]').forEach(function (el) {
      el.addEventListener('blur', function () {
        if (this.value) {
          try {
            this.value = parseFloat(this.value).toLocaleString('en-IN');
          } catch (_) { /* ignore */ }
        }
      });
    });

    // 5. Bootstrap Tooltip Init
    const tooltipTriggers = doc.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltipTriggers.length) {
      tooltipTriggers.forEach(function (el) {
        new bootstrap.Tooltip(el);
      });
    }

    // 6. Floating Label Fix for Autofill
    doc.querySelectorAll('.form-floating input, .form-floating textarea').forEach(function (el) {
      el.addEventListener('blur', function () {
        this.classList.toggle('is-valid', this.checkValidity() && this.value);
      });
    });

    // 7. Confirm Dialogs
    doc.querySelectorAll('[data-confirm]').forEach(function (el) {
      el.addEventListener('click', function (e) {
        if (!confirm(this.dataset.confirm || 'Are you sure?')) {
          e.preventDefault();
        }
      });
    });

    // 8. Loading State on Form Submits
    doc.querySelectorAll('form').forEach(function (form) {
      form.addEventListener('submit', function () {
        const btn = this.querySelector('[type="submit"]');
        if (btn) {
          btn.classList.add('btn-loading');
          btn.disabled = true;
        }
      });
    });

    // 9. Active Nav Link Highlighting
    const currentPath = win.location.pathname;
    doc.querySelectorAll('.navbar-nav .nav-link').forEach(function (link) {
      const href = link.getAttribute('href');
      if (href && href !== '#' && currentPath.startsWith(href)) {
        link.classList.add('active');
      }
      if (href && currentPath === '/' && href === '/') {
        link.classList.add('active');
      }
    });

    // 10. Table Search Filter
    doc.querySelectorAll('[data-table-search]').forEach(function (input) {
      input.addEventListener('keyup', function () {
        const query = this.value.toLowerCase();
        const table = doc.querySelector(this.dataset.tableSearch);
        if (!table) return;
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(function (row) {
          const text = row.textContent.toLowerCase();
          row.style.display = text.includes(query) ? '' : 'none';
        });
      });
    });

    // 11. Smooth Anchor Scroll
    doc.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
      anchor.addEventListener('click', function (e) {
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        const target = doc.querySelector(targetId);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });

  });

})();
