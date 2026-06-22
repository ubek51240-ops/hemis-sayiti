// Global Theme Manager v2.0
(function() {
    'use strict';
    
    // Global setTheme function - IMMEDIATELY AVAILABLE
    window.setTheme = function(theme) {
        console.log('>>> setTheme called with:', theme);
        
        try {
            // Save to localStorage first
            localStorage.setItem('theme', theme);
            console.log('Theme saved to localStorage:', theme);
            
            // Update HTML and BODY attributes
            document.documentElement.setAttribute('data-theme', theme);
            document.body.setAttribute('data-theme', theme);
            console.log('data-theme attributes updated');
            
            // Update button states
            updateButtonStates(theme);
            
            // Update logo
            updateLogoVisibility(theme);
            
            // Save to server if logged in
            saveThemeToServer(theme);
            
            console.log('>>> Theme switch completed:', theme);
        } catch (e) {
            console.error('Theme switch error:', e);
        }
    };
    
    // Update button states
    function updateButtonStates(theme) {
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
            console.log('Button states updated');
        }
    }
    
    // Update logo visibility
    function updateLogoVisibility(theme) {
        const navbarBrand = document.querySelector('.navbar-brand');
        if (navbarBrand) {
            const logoImg = navbarBrand.querySelector('img');
            const logoIcon = navbarBrand.querySelector('.bi-building');
            
            if (logoImg && logoIcon) {
                if (theme === 'dark') {
                    logoImg.style.display = 'none';
                    logoIcon.style.display = 'inline';
                } else {
                    logoImg.style.display = 'inline';
                    logoIcon.style.display = 'none';
                }
            }
        }
    }
    
    // Save to server
    function saveThemeToServer(theme) {
        const userIdMeta = document.querySelector('meta[name="user-id"]');
        if (userIdMeta) {
            const csrftoken = getCookie('csrftoken');
            fetch('/save-theme/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ theme: theme })
            })
            .then(r => r.json())
            .then(d => console.log('Server saved:', d))
            .catch(e => console.error('Server save error:', e));
        }
    }
    
    // Get cookie helper
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie) {
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
    
    // Clock functionality
    function startClock() {
        updateClock();
        setInterval(updateClock, 1000);
    }
    
    function updateClock() {
        const now = new Date();
        const timeString = now.toLocaleString('uz-UZ', {
            year: 'numeric', month: '2-digit', day: '2-digit',
            hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false
        });
        const timeElement = document.getElementById('current-time');
        if (timeElement) {
            timeElement.textContent = timeString;
        }
    }
    
    // Initialize on DOM ready
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Theme system initializing...');
        
        // Load and apply saved theme
        const savedTheme = localStorage.getItem('theme') || 'light';
        console.log('Saved theme:', savedTheme);
        
        // Apply theme immediately
        document.documentElement.setAttribute('data-theme', savedTheme);
        document.body.setAttribute('data-theme', savedTheme);
        
        // Update UI
        updateButtonStates(savedTheme);
        updateLogoVisibility(savedTheme);
        
        // Start clock
        startClock();
        
        console.log('Theme system ready!');
    });
    
    // Also try to set theme immediately if body exists
    if (document.body) {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.body.setAttribute('data-theme', savedTheme);
    }
    
})();
