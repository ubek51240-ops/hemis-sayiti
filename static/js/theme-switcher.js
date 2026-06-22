/**
 * Theme Switcher System
 * Dark/Light mode almashtirish
 */
class ThemeSwitcher {
    constructor() {
        this.currentTheme = this.getStoredTheme() || this.getPreferredTheme();
        this.initialized = false;
    }

    init() {
        if (this.initialized) return;
        
        // Temani o'rnatish
        this.setTheme(this.currentTheme, false);
        
        // Theme switcher tugmasini qo'shish
        this.addThemeToggle();
        
        // System theme o'zgarishini kuzatish
        this.watchSystemTheme();
        
        this.initialized = true;
    }

    getStoredTheme() {
        try {
            return localStorage.getItem('theme');
        } catch (e) {
            console.warn('localStorage ga murojaat bo\'lmadi:', e);
            return null;
        }
    }

    getPreferredTheme() {
        // System preferensiyasini tekshirish
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        return 'light';
    }

    setTheme(theme, showToast = true) {
        document.documentElement.setAttribute('data-bs-theme', theme);
        
        try {
            localStorage.setItem('theme', theme);
        } catch (e) {
            console.warn('Temani saqlab bo\'lmadi:', e);
        }
        
        this.currentTheme = theme;
        this.updateThemeToggle();
        
        // Toast xabari (faqat foydalanuvchi tanlaganda)
        if (showToast && window.toast) {
            const themeName = theme === 'dark' ? 'Qorong\'u' : 'Yorqin';
            window.toast.info(`Tema ${themeName} rejimga o\'zgartirildi`);
        }
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme, true);
    }

    addThemeToggle() {
        // Navbar ga tema tugmasi qo'shish
        const navbar = document.querySelector('.navbar .container-fluid .d-flex');
        if (navbar && !navbar.querySelector('.theme-toggle')) {
            const toggleButton = document.createElement('button');
            toggleButton.className = 'btn btn-sm btn-outline-light me-2 theme-toggle';
            toggleButton.innerHTML = `
                <i class="bi bi-${this.currentTheme === 'dark' ? 'sun' : 'moon'}-fill"></i>
                <span class="d-none d-md-inline ms-1">Tema</span>
            `;
            toggleButton.title = 'Tema almashtirish';
            toggleButton.setAttribute('aria-label', 'Tema almashtirish');
            
            toggleButton.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggleTheme();
            });
            
            // Profil tugmasidan oldin qo'yish
            const profileButton = navbar.querySelector('a[href*="profile"]');
            if (profileButton) {
                navbar.insertBefore(toggleButton, profileButton);
            } else {
                navbar.appendChild(toggleButton);
            }
        }
    }

    updateThemeToggle() {
        const toggleButton = document.querySelector('.theme-toggle');
        if (toggleButton) {
            const icon = toggleButton.querySelector('i');
            if (icon) {
                icon.className = `bi bi-${this.currentTheme === 'dark' ? 'sun' : 'moon'}-fill`;
            }
        }
    }

    watchSystemTheme() {
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            mediaQuery.addEventListener('change', (e) => {
                if (!this.getStoredTheme()) {
                    // Foydalanuvchi aniq tanlamagan bo'lsa, sistemaga ergashish
                    this.setTheme(e.matches ? 'dark' : 'light', false);
                }
            });
        }
    }

    // CSS o'zgarishlari
    addThemeStyles() {
        // Agar allaqachon qo'shilgan bo'lsa, qaytarmaslik
        if (document.getElementById('theme-switcher-styles')) {
            return;
        }

        const style = document.createElement('style');
        style.id = 'theme-switcher-styles';
        style.textContent = `
            /* Dark theme customizations */
            [data-bs-theme="dark"] {
                --bs-dark: #1a1a1a;
                --bs-dark-rgb: 26,26,26;
                --bs-body-bg: #121212;
                --bs-body-color: #ffffff;
            }
            
            [data-bs-theme="dark"] .navbar {
                background-color: #1a1a1a !important;
                border-color: #333 !important;
            }
            
            [data-bs-theme="dark"] .sidebar {
                background: #1a1a1a !important;
                border-right: 1px solid #333;
            }
            
            [data-bs-theme="dark"] .sidebar a {
                color: #ffffff;
            }
            
            [data-bs-theme="dark"] .sidebar a:hover {
                background: #2d2d2d !important;
                color: #ffffff;
            }
            
            [data-bs-theme="dark"] .sidebar .active {
                background: #0d6efd !important;
                border-left: 4px solid #0b5ed7;
                color: #ffffff;
            }
            
            [data-bs-theme="dark"] .main-content {
                background: #121212;
                color: #ffffff;
            }
            
            [data-bs-theme="dark"] .card {
                background: #1e1e1e;
                border-color: #333;
                color: #ffffff;
            }
            
            [data-bs-theme="dark"] .table {
                color: #ffffff;
            }
            
            [data-bs-theme="dark"] .table thead th {
                background: #2d2d2d;
                border-color: #444;
                color: #ffffff;
            }
            
            [data-bs-theme="dark"] .form-control,
            [data-bs-theme="dark"] .form-select {
                background: #2d2d2d;
                border-color: #444;
                color: #ffffff;
            }
            
            [data-bs-theme="dark"] .form-control:focus,
            [data-bs-theme="dark"] .form-select:focus {
                background: #333;
                border-color: #0d6efd;
                color: #ffffff;
                box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
            }
            
            [data-bs-theme="dark"] .modal-content {
                background: #1e1e1e;
                border-color: #333;
                color: #ffffff;
            }
            
            [data-bs-theme="dark"] .dropdown-menu {
                background: #1e1e1e;
                border-color: #333;
            }
            
            [data-bs-theme="dark"] .dropdown-item {
                color: #ffffff;
            }
            
            [data-bs-theme="dark"] .dropdown-item:hover {
                background: #2d2d2d;
                color: #ffffff;
            }
            
            [data-bs-theme="dark"] .btn-outline-light:hover {
                color: #000;
            }
            
            /* Chat specific dark theme styles */
            [data-bs-theme="dark"] .chat-container,
            [data-bs-theme="dark"] .chat-wrapper {
                background: #1e1e1e !important;
                color: #ffffff;
            }
            
            [data-bs-theme="dark"] .chat-messages,
            [data-bs-theme="dark"] .messages-container {
                background: #1a1a1a !important;
                border-color: #333 !important;
            }
            
            [data-bs-theme="dark"] .chat-message,
            [data-bs-theme="dark"] .message {
                background: #2d2d2d !important;
                color: #ffffff;
                border-color: #444 !important;
            }
            
            [data-bs-theme="dark"] .chat-message.sent,
            [data-bs-theme="dark"] .message.sent {
                background: #0d6efd !important;
                color: #ffffff;
                border-color: #0a58ca !important;
            }
            
            [data-bs-theme="dark"] .chat-message.received,
            [data-bs-theme="dark"] .message.received {
                background: #2d2d2d !important;
                color: #ffffff !important;
                border-color: #444 !important;
            }
            
            [data-bs-theme="dark"] .chat-input,
            [data-bs-theme="dark"] .message-input,
            [data-bs-theme="dark"] .chat-form input,
            [data-bs-theme="dark"] .chat-form textarea {
                background: #2d2d2d !important;
                border-color: #444 !important;
                color: #ffffff;
            }
            
            [data-bs-theme="dark"] .chat-input:focus,
            [data-bs-theme="dark"] .message-input:focus,
            [data-bs-theme="dark"] .chat-form input:focus,
            [data-bs-theme="dark"] .chat-form textarea:focus {
                background: #333 !important;
                border-color: #0d6efd !important;
                color: #ffffff;
                box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
            }
            
            [data-bs-theme="dark"] .chat-sidebar,
            [data-bs-theme="dark"] .users-list {
                background: #1a1a1a !important;
                border-color: #333 !important;
            }
            
            [data-bs-theme="dark"] .chat-user-item,
            [data-bs-theme="dark"] .user-item,
            [data-bs-theme="dark"] .list-group-item {
                background: #2d2d2d !important;
                color: #ffffff;
                border-color: #444 !important;
            }
            
            [data-bs-theme="dark"] .chat-user-item:hover,
            [data-bs-theme="dark"] .user-item:hover,
            [data-bs-theme="dark"] .list-group-item:hover {
                background: #333 !important;
                color: #ffffff;
            }
            
            [data-bs-theme="dark"] .chat-user-item.active,
            [data-bs-theme="dark"] .user-item.active,
            [data-bs-theme="dark"] .list-group-item.active {
                background: #0d6efd !important;
                color: #ffffff;
                border-color: #0a58ca !important;
            }
            
            [data-bs-theme="dark"] .message-time,
            [data-bs-theme="dark"] .time {
                color: #aaa !important;
            }
            
            [data-bs-theme="dark"] .message-sender,
            [data-bs-theme="dark"] .sender {
                color: #ccc !important;
            }
            
            [data-bs-theme="dark"] .typing-indicator {
                background: #2d2d2d !important;
                color: #ffffff;
            }
            
            [data-bs-theme="dark"] .chat-header,
            [data-bs-theme="dark"] .conversation-header {
                background: #1a1a1a !important;
                border-color: #333 !important;
                color: #ffffff;
            }
            
            [data-bs-theme="dark"] .chat-footer,
            [data-bs-theme="dark"] .chat-form {
                background: #1a1a1a !important;
                border-color: #333 !important;
            }
            
            /* Chat card elements */
            [data-bs-theme="dark"] .card-body {
                background: #2d2d2d !important;
                color: #ffffff !important;
            }
            
            [data-bs-theme="dark"] .card-text {
                color: #ffffff !important;
            }
            
            [data-bs-theme="dark"] .text-muted {
                color: #aaa !important;
            }
            
            [data-bs-theme="dark"] .card {
                background: #2d2d2d !important;
                border-color: #444 !important;
                color: #ffffff !important;
            }
            
            [data-bs-theme="dark"] .card-header {
                background: #1a1a1a !important;
                color: #ffffff !important;
                border-color: #444 !important;
            }
            
            [data-bs-theme="dark"] .card-footer {
                background: #1a1a1a !important;
                color: #ffffff !important;
                border-color: #444 !important;
            }
            
            /* Smooth transition */
            body,
            .navbar,
            .sidebar,
            .main-content,
            .card,
            .form-control,
            .form-select {
                transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
            }
            
            .theme-toggle {
                transition: transform 0.2s ease, background-color 0.2s ease;
            }
            
            .theme-toggle:hover {
                transform: scale(1.05);
            }
        `;
        document.head.appendChild(style);
    }
}

// Global instance - DOM yuklangandan so'ng yaratish
window.themeSwitcher = null;

// DOM yuklangandan so'ng initializatsiya
document.addEventListener('DOMContentLoaded', function() {
    window.themeSwitcher = new ThemeSwitcher();
    window.themeSwitcher.init();
    window.themeSwitcher.addThemeStyles();
});
