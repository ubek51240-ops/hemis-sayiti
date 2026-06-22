// Theme Switcher JavaScript
class ThemeManager {
    constructor() {
        this.init();
    }

    init() {
        // Load saved theme or default to light
        const savedTheme = localStorage.getItem('theme') || 'light';
        this.setTheme(savedTheme);
        
        // Update button states
        this.updateButtonStates(savedTheme);
        
        // Start clock
        this.startClock();
    }

    setTheme(theme) {
        // Save to localStorage
        localStorage.setItem('theme', theme);
        
        // Update HTML attribute
        document.documentElement.setAttribute('data-theme', theme);
        
        // Update button states
        this.updateButtonStates(theme);
        
        // Update logo visibility
        this.updateLogoVisibility(theme);
        
        // Save to server (optional - for logged in users)
        this.saveThemeToServer(theme);
    }

    updateButtonStates(theme) {
        const lightBtn = document.getElementById('light-theme');
        const darkBtn = document.getElementById('dark-theme');
        
        if (lightBtn && darkBtn) {
            if (theme === 'dark') {
                lightBtn.classList.remove('active', 'btn-primary');
                lightBtn.classList.add('btn-outline-primary');
                darkBtn.classList.remove('btn-outline-dark');
                darkBtn.classList.add('active', 'btn-dark');
            } else {
                lightBtn.classList.remove('btn-outline-primary');
                lightBtn.classList.add('active', 'btn-primary');
                darkBtn.classList.remove('active', 'btn-dark');
                darkBtn.classList.add('btn-outline-dark');
            }
        }
    }

    updateLogoVisibility(theme) {
        const navbarBrand = document.querySelector('.navbar-brand');
        if (navbarBrand) {
            const logoImg = navbarBrand.querySelector('img');
            const logoIcon = navbarBrand.querySelector('.bi-building');
            
            if (theme === 'dark') {
                // Qora temada logotipni yashirish
                if (logoImg) logoImg.style.display = 'none';
                if (logoIcon) logoIcon.style.display = 'inline';
            } else {
                // Oq temada logotipni ko'rsatish
                if (logoImg) logoImg.style.display = 'inline';
                if (logoIcon) logoIcon.style.display = 'none';
            }
        }
    }

    saveThemeToServer(theme) {
        // Check if user is logged in by looking for user ID in meta tags
        const userIdMeta = document.querySelector('meta[name="user-id"]');
        if (userIdMeta) {
            fetch('/save-theme/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken')
                },
                body: JSON.stringify({ theme: theme })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    console.log('Theme saved to server:', theme);
                }
            })
            .catch(error => {
                console.error('Error saving theme:', error);
            });
        }
    }

    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    startClock() {
        this.updateClock();
        setInterval(() => this.updateClock(), 1000);
    }

    updateClock() {
        const now = new Date();
        const options = {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false
        };
        
        const timeString = now.toLocaleString('uz-UZ', options);
        const timeElement = document.getElementById('current-time');
        
        if (timeElement) {
            timeElement.textContent = timeString;
        }
    }
}

// Global function for button onclick
function setTheme(theme) {
    if (window.themeManager) {
        window.themeManager.setTheme(theme);
    }
}

// Initialize theme manager when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.themeManager = new ThemeManager();
});

// Export for global access
window.setTheme = setTheme;
