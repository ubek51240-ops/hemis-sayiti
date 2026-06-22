/**
 * Test-sinov-ucun - Online/Offline indicator
 * Sahifaga online status va sync queue indicator qo'shadi
 */
(function () {
    'use strict';

    function init() {
        // Indicator yaratish
        const indicator = document.createElement('div');
        indicator.id = 'offline-indicator';
        indicator.innerHTML = `
            <style>
                #offline-indicator {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    z-index: 9999;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    padding: 10px 16px;
                    border-radius: 50px;
                    font-size: 13px;
                    font-weight: 600;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
                    transition: all 0.3s ease;
                    cursor: pointer;
                    user-select: none;
                    backdrop-filter: blur(10px);
                }
                #offline-indicator.online {
                    background: rgba(34, 197, 94, 0.95);
                    color: white;
                }
                #offline-indicator.offline {
                    background: rgba(239, 68, 68, 0.95);
                    color: white;
                }
                #offline-indicator.syncing {
                    background: rgba(59, 130, 246, 0.95);
                    color: white;
                }
                #offline-indicator .oi-dot {
                    width: 8px;
                    height: 8px;
                    border-radius: 50%;
                    background: white;
                    animation: oi-pulse 2s infinite;
                }
                @keyframes oi-pulse {
                    0%, 100% { opacity: 1; transform: scale(1); }
                    50% { opacity: 0.5; transform: scale(0.85); }
                }
                #offline-indicator .oi-badge {
                    background: rgba(255,255,255,0.3);
                    padding: 2px 8px;
                    border-radius: 12px;
                    font-size: 11px;
                }
                #offline-banner {
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    background: #ef4444;
                    color: white;
                    text-align: center;
                    padding: 8px;
                    font-size: 13px;
                    font-weight: 600;
                    z-index: 9998;
                    transform: translateY(-100%);
                    transition: transform 0.3s ease;
                }
                #offline-banner.show {
                    transform: translateY(0);
                }
                @media (max-width: 768px) {
                    #offline-indicator {
                        bottom: 80px;
                        right: 10px;
                        font-size: 12px;
                        padding: 8px 12px;
                    }
                }
            </style>
            <span class="oi-dot"></span>
            <span class="oi-text">Online</span>
            <span class="oi-badge" style="display:none;">0</span>
        `;
        document.body.appendChild(indicator);

        const banner = document.createElement('div');
        banner.id = 'offline-banner';
        banner.innerHTML = '<i class="bi bi-wifi-off"></i> Internet aloqasi yo\'q - barcha o\'zgarishlar mahalliy saqlanadi';
        document.body.appendChild(banner);

        const dot = indicator.querySelector('.oi-dot');
        const text = indicator.querySelector('.oi-text');
        const badge = indicator.querySelector('.oi-badge');

        function update(state = {}) {
            const online = navigator.onLine;
            indicator.classList.remove('online', 'offline', 'syncing');

            if (state.syncing) {
                indicator.classList.add('syncing');
                text.textContent = 'Sinxronizatsiya...';
                banner.classList.remove('show');
            } else if (online) {
                indicator.classList.add('online');
                text.textContent = 'Online';
                banner.classList.remove('show');
            } else {
                indicator.classList.add('offline');
                text.textContent = 'Offline';
                banner.classList.add('show');
            }

            if (state.pendingCount > 0) {
                badge.style.display = 'inline-block';
                badge.textContent = state.pendingCount;
                indicator.title = `${state.pendingCount} ta yozuv navbatda kutmoqda`;
            } else {
                badge.style.display = 'none';
                indicator.title = '';
            }
        }

        // Click - sync now
        indicator.addEventListener('click', async () => {
            if (window.OfflineSync && navigator.onLine) {
                update({ syncing: true });
                const res = await window.OfflineSync.syncNow();
                if (res && res.success > 0) {
                    showToast(`${res.success} ta yozuv yuklandi!`, 'success');
                }
                update();
            }
        });

        // Online/offline events
        window.addEventListener('online', () => update());
        window.addEventListener('offline', () => update());

        // Listen to sync changes
        if (window.OfflineSync) {
            window.OfflineSync.onChange((state) => update(state));
            window.OfflineSync.notifyChange();
        }

        // Initial
        update();
    }

    function showToast(msg, type = 'info') {
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed; top: 20px; right: 20px;
            padding: 12px 20px; border-radius: 12px;
            background: ${type === 'success' ? '#22c55e' : '#3b82f6'};
            color: white; font-weight: 600;
            z-index: 10000; box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            animation: slideIn 0.3s ease;
        `;
        toast.textContent = msg;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
