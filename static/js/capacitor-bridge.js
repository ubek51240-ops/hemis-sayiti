/**
 * Test-sinov-ucun - Capacitor Bridge
 * Mobile ilova ichida ishlaganda native funksiyalarni qo'shadi.
 */
(function () {
    'use strict';

    // Capacitor mavjudligini tekshirish
    const isNativeApp = !!(window.Capacitor && window.Capacitor.isNativePlatform && window.Capacitor.isNativePlatform());

    if (!isNativeApp) return;

    console.log('[Capacitor] Native app rejimida');
    document.documentElement.classList.add('is-native-app');

    // Native back button → browser back
    if (window.Capacitor.Plugins && window.Capacitor.Plugins.App) {
        window.Capacitor.Plugins.App.addListener('backButton', ({ canGoBack }) => {
            if (canGoBack) {
                window.history.back();
            } else {
                window.Capacitor.Plugins.App.exitApp();
            }
        });
    }

    // Network plugin - network status listener
    if (window.Capacitor.Plugins && window.Capacitor.Plugins.Network) {
        const Network = window.Capacitor.Plugins.Network;
        Network.addListener('networkStatusChange', status => {
            console.log('[Capacitor] Network:', status.connected);
            if (status.connected && window.OfflineSync) {
                window.OfflineSync.syncNow();
            }
        });
    }
})();
