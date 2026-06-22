/**
 * Real-time Notifications System
 * Server-Sent Events orqali real-time xabarlar
 */
class RealtimeNotifications {
    constructor() {
        this.userId = null;
        this.notificationEndpoint = '/api/v1/notifications/stream/';
        this.eventSource = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 5000;
        this.unreadCount = 0;
        this.initialized = false;
    }

    init() {
        if (this.initialized) return;
        
        // Foydalanuvchi ID sini olish
        this.getUserId();
        
        // Agar user ID bo'lsa, ulanishni boshlash
        if (this.userId) {
            this.connect();
        } else {
            console.warn('User ID topilmadi, real-time xabarlar ishlamaydi');
        }
        
        // Sahifa yo'qolganda ulanishni to'xtatish
        this.setupVisibilityHandlers();
        
        this.initialized = true;
    }

    getUserId() {
        // HTML dan yoki cookie dan user ID ni olish
        const metaUserId = document.querySelector('meta[name="user-id"]');
        if (metaUserId) {
            this.userId = metaUserId.getAttribute('content');
        } else {
            // Django template dan olish
            const userIdElement = document.getElementById('current-user-id');
            if (userIdElement) {
                this.userId = userIdElement.textContent.trim();
            }
        }
    }

    connect() {
        // EventSource (SSE) dan foydalanish - soddaroq va ishonchliroq
        this.connectEventSource();
    }

    connectEventSource() {
        const url = `${this.notificationEndpoint}?user_id=${this.userId}`;
        console.log('EventSource ulanishi boshlanmoqda:', url);
        
        try {
            this.eventSource = new EventSource(url);
            
            this.eventSource.onopen = () => {
                console.log('EventSource ulanishi o\'rnatildi');
                this.reconnectAttempts = 0;
                if (window.toast) {
                    window.toast.success('Real-time xabarlar faol');
                }
            };
            
            this.eventSource.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    console.log('SSE xabar qabul qilindi:', data);
                    this.handleNotification(data);
                } catch (error) {
                    console.error('SSE xabar parsing xatolik:', error, event.data);
                }
            };
            
            this.eventSource.onerror = (error) => {
                console.error('EventSource xatolik:', error);
                if (window.toast) {
                    window.toast.error('Real-time xabarlar ulanishda xatolik');
                }
                
                // Ulanishni yopish va qayta ulanishga urinish
                if (this.eventSource) {
                    this.eventSource.close();
                    this.eventSource = null;
                }
                
                this.attemptReconnect();
            };
            
        } catch (error) {
            console.error('EventSource ulanish xatolik:', error);
            if (window.toast) {
                window.toast.error('EventSource ulanib bo\'lmadi');
            }
            // Fallback: polling
            this.startPolling();
        }
    }

    handleNotification(data) {
        console.log('Yangi xabar:', data);
        
        // Toast xabari
        this.showToastNotification(data);
        
        // Notification badge yangilash
        this.updateNotificationBadge(data);
        
        // Xabarlar ro'yxatini yangilash (agar sahifada bo'lsa)
        this.updateNotificationList(data);
        
        // Browser notification
        this.showBrowserNotification(data);
        
        // Audio signal
        this.playNotificationSound();
    }

    showToastNotification(data) {
        let message = data.message || data.title || 'Yangi xabar';
        let type = data.type || 'info';
        
        if (data.sender) {
            message = `${data.sender}: ${message}`;
        }
        
        if (window.toast) {
            window.toast.info(message);
        }
    }

    updateNotificationBadge(data) {
        const badge = document.querySelector('.notification-badge');
        if (badge) {
            this.unreadCount++;
            badge.textContent = this.unreadCount;
            badge.style.display = this.unreadCount > 0 ? 'block' : 'none';
        }
    }

    updateNotificationList(data) {
        // Agar xabarlar sahifasida bo'lsak
        const notificationList = document.getElementById('notifications-list');
        if (notificationList) {
            const notificationHtml = this.createNotificationHtml(data);
            notificationList.insertAdjacentHTML('afterbegin', notificationHtml);
        }
    }

    createNotificationHtml(data) {
        return `
            <div class="notification-item alert alert-info alert-dismissible fade show" role="alert">
                <div class="d-flex align-items-center">
                    <div class="flex-grow-1">
                        <strong>${data.sender || 'System'}</strong>
                        <p class="mb-1">${data.message || data.content}</p>
                        <small class="text-muted">${this.formatTime(data.created_at)}</small>
                    </div>
                    ${data.avatar ? `<img src="${data.avatar}" class="rounded-circle me-2" width="40" height="40">` : ''}
                </div>
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
    }

    showBrowserNotification(data) {
        if ('Notification' in window && Notification.permission === 'granted') {
            const notification = new Notification(data.title || 'Mini Hemis', {
                body: data.message || data.content,
                icon: '/static/img/logo.png',
                badge: '/static/img/badge.png',
                tag: 'mini-hemis-notification'
            });
            
            notification.onclick = () => {
                window.focus();
                notification.close();
                // Xabarlar sahifasiga o'tish
                if (data.url) {
                    window.location.href = data.url;
                }
            };
            
            // Avtomatik yopilish
            setTimeout(() => notification.close(), 5000);
        }
    }

    playNotificationSound() {
        // Notification ovozi
        const audio = new Audio('/static/sounds/notification.mp3');
        audio.volume = 0.3;
        audio.play().catch(e => console.log('Audio o\'ynatib bo\'lmadi:', e));
    }

    formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        
        if (diff < 60000) return 'hozirgina';
        if (diff < 3600000) return `${Math.floor(diff / 60000)} daqiqa oldin`;
        if (diff < 86400000) return `${Math.floor(diff / 3600000)} soat oldin`;
        
        return date.toLocaleDateString('uz-UZ');
    }

    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`${this.reconnectDelay / 1000} soniyadan so'ng qayta ulanishga urinish...`);
            
            setTimeout(() => {
                this.connect();
            }, this.reconnectDelay);
            
            // Exponential backoff
            this.reconnectDelay *= 2;
        } else {
            console.error('Maksimum ulanish urinishlari tugadi');
            if (window.toast) {
                window.toast.error('Real-time xabarlar ulanishni yoqotdi');
            }
        }
    }

    startPolling() {
        // Fallback polling
        console.log('Polling rejimiga o\'tish');
        setInterval(() => {
            this.fetchNotifications();
        }, 30000); // 30 soniyada bir
    }

    fetchNotifications() {
        fetch(`/api/v1/notifications/?user_id=${this.userId}&unread_only=true`)
            .then(response => response.json())
            .then(data => {
                if (data.results && data.results.length > 0) {
                    data.results.forEach(notification => {
                        this.handleNotification(notification);
                    });
                }
            })
            .catch(error => {
                console.error('Polling xatolik:', error);
            });
    }

    setupVisibilityHandlers() {
        // Sahifa active/passive holatini kuzatish
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                // Sahifa yopilganda ulanishni to'xtatish
                this.disconnect();
            } else {
                // Sahifa ochilganda qayta ulanish
                this.connect();
            }
        });
    }

    disconnect() {
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = null;
        }
    }

    // Browser notification ruxsatini so'rash
    requestNotificationPermission() {
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission().then(permission => {
                if (permission === 'granted') {
                    if (window.toast) window.toast.success('Bildirishnomalar yoqildi');
                } else {
                    if (window.toast) window.toast.warning('Bildirishnomar ruxsat berilmadi');
                }
            });
        }
    }
}

// Global instance
window.realtimeNotifications = new RealtimeNotifications();

// Notification ruxsatini boshlash
document.addEventListener('DOMContentLoaded', function() {
    window.realtimeNotifications.requestNotificationPermission();
});
