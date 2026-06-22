// Test-sinov-ucun - Service Worker (offline-first)
const CACHE_VERSION = 'v3';
const STATIC_CACHE = `tq-static-${CACHE_VERSION}`;
const DYNAMIC_CACHE = `tq-dynamic-${CACHE_VERSION}`;
const API_CACHE = `tq-api-${CACHE_VERSION}`;

// Asosiy sahifalar va resurslar (precache)
const STATIC_ASSETS = [
    '/',
    '/login/',
    '/offline/',
    '/static/manifest.json',
    '/static/js/theme-global.js',
    '/static/js/drag-drop-upload.js',
    '/static/js/offline-sync.js',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
    'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css',
];

// Install
self.addEventListener('install', event => {
    console.log('[SW] Install');
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then(cache => cache.addAll(STATIC_ASSETS).catch(err => {
                console.warn('[SW] Some assets failed to cache:', err);
            }))
            .then(() => self.skipWaiting())
    );
});

// Activate - eski cachelarni o'chirish
self.addEventListener('activate', event => {
    console.log('[SW] Activate');
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(
                keys.filter(k => ![STATIC_CACHE, DYNAMIC_CACHE, API_CACHE].includes(k))
                    .map(k => caches.delete(k))
            )
        ).then(() => self.clients.claim())
    );
});

// Fetch strategiyalari
self.addEventListener('fetch', event => {
    const req = event.request;
    const url = new URL(req.url);

    // Faqat GET so'rovlar uchun cache
    if (req.method !== 'GET') {
        event.respondWith(handleNonGetRequest(req));
        return;
    }

    // API so'rovlari - Network-first, cache fallback
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(networkFirst(req, API_CACHE));
        return;
    }

    // Static fayllar - Cache-first
    if (url.pathname.startsWith('/static/') || url.pathname.startsWith('/media/') ||
        url.hostname.includes('cdn.jsdelivr.net') || url.hostname.includes('fonts.')) {
        event.respondWith(cacheFirst(req, STATIC_CACHE));
        return;
    }

    // HTML sahifalar - Network-first, offline fallback
    event.respondWith(networkFirstWithOfflineFallback(req));
});

// === STRATEGIYALAR ===

async function cacheFirst(req, cacheName) {
    const cached = await caches.match(req);
    if (cached) return cached;
    try {
        const res = await fetch(req);
        if (res.ok) {
            const cache = await caches.open(cacheName);
            cache.put(req, res.clone());
        }
        return res;
    } catch (e) {
        return new Response('Offline', { status: 503 });
    }
}

async function networkFirst(req, cacheName) {
    try {
        const res = await fetch(req);
        if (res.ok) {
            const cache = await caches.open(cacheName);
            cache.put(req, res.clone());
        }
        return res;
    } catch (e) {
        const cached = await caches.match(req);
        if (cached) return cached;
        return new Response(JSON.stringify({ offline: true, error: 'Internet yo\'q' }), {
            status: 503,
            headers: { 'Content-Type': 'application/json' }
        });
    }
}

async function networkFirstWithOfflineFallback(req) {
    try {
        const res = await fetch(req);
        if (res.ok) {
            const cache = await caches.open(DYNAMIC_CACHE);
            cache.put(req, res.clone());
        }
        return res;
    } catch (e) {
        const cached = await caches.match(req);
        if (cached) return cached;
        // Offline sahifa
        const offlinePage = await caches.match('/offline/');
        if (offlinePage) return offlinePage;
        return new Response('Offline', { status: 503 });
    }
}

// POST/PUT/DELETE so'rovlar - offline bo'lsa background sync queue ga
async function handleNonGetRequest(req) {
    try {
        return await fetch(req);
    } catch (e) {
        // Offline - clientga xabar yuborish
        const clients = await self.clients.matchAll();
        clients.forEach(client => {
            client.postMessage({
                type: 'OFFLINE_REQUEST',
                url: req.url,
                method: req.method,
            });
        });
        return new Response(JSON.stringify({
            offline: true,
            queued: true,
            message: 'So\'rov navbatga qo\'shildi, internet yoqilganda yuboriladi'
        }), {
            status: 202,
            headers: { 'Content-Type': 'application/json' }
        });
    }
}

// Background Sync - online bo'lganda navbatdagi so'rovlarni yuborish
self.addEventListener('sync', event => {
    console.log('[SW] Sync event:', event.tag);
    if (event.tag === 'sync-queue') {
        event.waitUntil(syncQueue());
    }
});

async function syncQueue() {
    // Clientga sync boshlash xabarini yuborish
    const clients = await self.clients.matchAll();
    clients.forEach(client => {
        client.postMessage({ type: 'SYNC_START' });
    });
}

// Push notifications (kelajak uchun)
self.addEventListener('push', event => {
    const data = event.data ? event.data.json() : { title: 'Test-sinov-ucun', body: 'Yangi xabar' };
    event.waitUntil(
        self.registration.showNotification(data.title, {
            body: data.body,
            icon: '/static/img/icon-192.png',
            badge: '/static/img/icon-192.png',
        })
    );
});
