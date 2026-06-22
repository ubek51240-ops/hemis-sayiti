/**
 * Toast Notifications System
 * Zamonaviy xabarlar uchun klass
 */
class ToastNotification {
    constructor() {
        this.container = null;
        this.init();
    }

    init() {
        // Toast container yaratish
        this.container = document.createElement('div');
        this.container.id = 'toast-container';
        this.container.className = 'toast-container position-fixed top-0 end-0 p-3';
        this.container.style.zIndex = '1050';
        document.body.appendChild(this.container);
    }

    show(message, type = 'info', duration = 5000) {
        const toastId = 'toast-' + Date.now();
        const toastHtml = `
            <div id="${toastId}" class="toast align-items-center text-white bg-${this.getBootstrapClass(type)} border-0" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        ${this.getIcon(type)} ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        `;
        
        this.container.insertAdjacentHTML('beforeend', toastHtml);
        
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement, {
            autohide: true,
            delay: duration
        });
        
        toast.show();
        
        // Toast tugagandan so'ng elementni o'chirish
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    }

    getBootstrapClass(type) {
        const classes = {
            'success': 'success',
            'error': 'danger',
            'warning': 'warning',
            'info': 'info'
        };
        return classes[type] || 'info';
    }

    getIcon(type) {
        const icons = {
            'success': '<i class="bi bi-check-circle-fill me-2"></i>',
            'error': '<i class="bi bi-x-circle-fill me-2"></i>',
            'warning': '<i class="bi bi-exclamation-triangle-fill me-2"></i>',
            'info': '<i class="bi bi-info-circle-fill me-2"></i>'
        };
        return icons[type] || icons['info'];
    }

    // Qisqa metodlar
    success(message, duration = 5000) {
        this.show(message, 'success', duration);
    }

    error(message, duration = 7000) {
        this.show(message, 'error', duration);
    }

    warning(message, duration = 6000) {
        this.show(message, 'warning', duration);
    }

    info(message, duration = 5000) {
        this.show(message, 'info', duration);
    }
}

// Global instance
window.toast = new ToastNotification();

// Django messages uchun avtomatik konvertatsiya
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        const message = alert.textContent.trim();
        let type = 'info';
        
        if (alert.classList.contains('alert-success')) type = 'success';
        else if (alert.classList.contains('alert-danger')) type = 'error';
        else if (alert.classList.contains('alert-warning')) type = 'warning';
        else if (alert.classList.contains('alert-info')) type = 'info';
        
        // Toast ko'rsatish
        window.toast.success(message);
        
        // Eski alertni o'chirish
        alert.remove();
    });
});
