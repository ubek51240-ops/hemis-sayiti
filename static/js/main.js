/**
 * Main JavaScript Module
 * Barcha JavaScript funksiyalarini birlashtiruvchi modul
 */

// Global funksiyalar
window.App = {
    // Toast yuborish qisqa metod
    showToast: function(message, type = 'info') {
        if (window.toast) {
            window.toast.show(message, type);
        }
    },
    
    // Tema almashtirish
    toggleTheme: function() {
        if (window.themeSwitcher) {
            window.themeSwitcher.toggleTheme();
        }
    },
    
    // Form validatsiya
    validateForm: function(form) {
        let isValid = true;
        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                input.classList.add('is-invalid');
                isValid = false;
            } else {
                input.classList.remove('is-invalid');
            }
        });
        
        return isValid;
    },
    
    // Loading spinner
    showLoading: function(element) {
        const spinner = `
            <div class="spinner-border spinner-border-sm me-2" role="status">
                <span class="visually-hidden">Yuklanmoqda...</span>
            </div>
        `;
        element.insertAdjacentHTML('afterbegin', spinner);
    },
    
    hideLoading: function(element) {
        const spinner = element.querySelector('.spinner-border');
        if (spinner) spinner.remove();
    },
    
    // AJAX so'rovlar
    ajaxRequest: function(url, options = {}) {
        const defaults = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            }
        };
        
        const config = Object.assign(defaults, options);
        
        return fetch(url, config)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .catch(error => {
                console.error('AJAX xatolik:', error);
                if (window.toast) window.toast.error('So\'rovda xatolik yuz berdi');
                throw error;
            });
    },
    
    // CSRF token
    getCSRFToken: function() {
        const token = document.querySelector('meta[name="csrf-token"]');
        return token ? token.getAttribute('content') : '';
    },
    
    // Form data ni JSON ga o'tkazish
    formToJSON: function(form) {
        const formData = new FormData(form);
        const object = {};
        
        formData.forEach((value, key) => {
            if (object[key]) {
                if (!Array.isArray(object[key])) {
                    object[key] = [object[key]];
                }
                object[key].push(value);
            } else {
                object[key] = value;
            }
        });
        
        return object;
    },
    
    // Datatable uchun formatlash
    formatNumber: function(num) {
        return new Intl.NumberFormat('uz-UZ').format(num);
    },
    
    formatDate: function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('uz-UZ', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },
    
    // Copy to clipboard
    copyToClipboard: function(text) {
        navigator.clipboard.writeText(text).then(() => {
            if (window.toast) window.toast.success('Nusxa olindi!');
        }).catch(() => {
            // Fallback
            const textarea = document.createElement('textarea');
            textarea.value = text;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            if (window.toast) window.toast.success('Nusxa olindi!');
        });
    },
    
    // Confirm dialog
    confirm: function(message, callback) {
        if (confirm(message)) {
            callback();
        }
    },
    
    // Debounce funksiya
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Search funksiya
    liveSearch: function(input, container, itemSelector) {
        const searchTerm = input.value.toLowerCase();
        const items = container.querySelectorAll(itemSelector);
        
        items.forEach(item => {
            const text = item.textContent.toLowerCase();
            if (text.includes(searchTerm)) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });
    }
};

// Document ready event
document.addEventListener('DOMContentLoaded', function() {
    // Form validatsiyasi
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!App.validateForm(form)) {
                e.preventDefault();
                if (window.toast) window.toast.warning('Iltimos, barcha majburiy maydonlarni to\'ldiring');
            }
        });
    });
    
    // Live search
    const searchInputs = document.querySelectorAll('input[data-live-search]');
    searchInputs.forEach(input => {
        const target = document.querySelector(input.dataset.target);
        const itemSelector = input.dataset.itemSelector || '.search-item';
        
        if (target) {
            input.addEventListener('input', App.debounce(() => {
                App.liveSearch(input, target, itemSelector);
            }, 300));
        }
    });
    
    // Copy buttons
    const copyButtons = document.querySelectorAll('[data-copy]');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const text = button.dataset.copy;
            App.copyToClipboard(text);
        });
    });
    
    // Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    console.log('Mini Hemis JavaScript modullari yuklandi');
});
