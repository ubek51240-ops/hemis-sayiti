/**
 * Test-sinov-ucun - Offline Sync Manager
 * IndexedDB orqali offline yozuvlarni boshqaradi va internet kelganda sync qiladi
 */
(function (global) {
    'use strict';

    const DB_NAME = 'TalabaQabulOffline';
    const DB_VERSION = 1;
    const STORE_QUEUE = 'syncQueue';
    const STORE_CACHE = 'dataCache';

    let dbPromise = null;

    function openDB() {
        if (dbPromise) return dbPromise;
        dbPromise = new Promise((resolve, reject) => {
            const req = indexedDB.open(DB_NAME, DB_VERSION);
            req.onupgradeneeded = (e) => {
                const db = e.target.result;
                if (!db.objectStoreNames.contains(STORE_QUEUE)) {
                    const store = db.createObjectStore(STORE_QUEUE, {
                        keyPath: 'id',
                        autoIncrement: true,
                    });
                    store.createIndex('synced', 'synced', { unique: false });
                    store.createIndex('createdAt', 'createdAt', { unique: false });
                }
                if (!db.objectStoreNames.contains(STORE_CACHE)) {
                    db.createObjectStore(STORE_CACHE, { keyPath: 'key' });
                }
            };
            req.onsuccess = (e) => resolve(e.target.result);
            req.onerror = (e) => reject(e.target.error);
        });
        return dbPromise;
    }

    // === SYNC QUEUE (Offline yozuvlar navbati) ===

    /**
     * Offline yozuvni navbatga qo'shish
     * @param {Object} payload - { type, url, method, data, files? }
     */
    async function enqueue(payload) {
        const db = await openDB();
        return new Promise((resolve, reject) => {
            const tx = db.transaction(STORE_QUEUE, 'readwrite');
            const store = tx.objectStore(STORE_QUEUE);
            const item = {
                ...payload,
                synced: 0,
                createdAt: Date.now(),
                attempts: 0,
                lastError: null,
            };
            const req = store.add(item);
            req.onsuccess = () => {
                resolve(req.result);
                notifyChange();
            };
            req.onerror = () => reject(req.error);
        });
    }

    /**
     * Sync qilinmagan yozuvlarni olish
     */
    async function getPending() {
        const db = await openDB();
        return new Promise((resolve, reject) => {
            const tx = db.transaction(STORE_QUEUE, 'readonly');
            const store = tx.objectStore(STORE_QUEUE);
            const idx = store.index('synced');
            const req = idx.getAll(IDBKeyRange.only(0));
            req.onsuccess = () => resolve(req.result);
            req.onerror = () => reject(req.error);
        });
    }

    /**
     * Yozuvni sync qilingan deb belgilash
     */
    async function markSynced(id) {
        const db = await openDB();
        return new Promise((resolve, reject) => {
            const tx = db.transaction(STORE_QUEUE, 'readwrite');
            const store = tx.objectStore(STORE_QUEUE);
            const getReq = store.get(id);
            getReq.onsuccess = () => {
                const item = getReq.result;
                if (item) {
                    item.synced = 1;
                    item.syncedAt = Date.now();
                    store.put(item);
                }
                resolve();
                notifyChange();
            };
            getReq.onerror = () => reject(getReq.error);
        });
    }

    /**
     * Yozuvni o'chirish
     */
    async function remove(id) {
        const db = await openDB();
        return new Promise((resolve, reject) => {
            const tx = db.transaction(STORE_QUEUE, 'readwrite');
            tx.objectStore(STORE_QUEUE).delete(id);
            tx.oncomplete = () => { resolve(); notifyChange(); };
            tx.onerror = () => reject(tx.error);
        });
    }

    /**
     * Xato ni qayd qilish
     */
    async function recordError(id, error) {
        const db = await openDB();
        return new Promise((resolve) => {
            const tx = db.transaction(STORE_QUEUE, 'readwrite');
            const store = tx.objectStore(STORE_QUEUE);
            const getReq = store.get(id);
            getReq.onsuccess = () => {
                const item = getReq.result;
                if (item) {
                    item.attempts = (item.attempts || 0) + 1;
                    item.lastError = String(error).slice(0, 500);
                    store.put(item);
                }
                resolve();
            };
        });
    }

    /**
     * Hammasi (sync qilingan ham) - tarix uchun
     */
    async function getAll() {
        const db = await openDB();
        return new Promise((resolve, reject) => {
            const tx = db.transaction(STORE_QUEUE, 'readonly');
            const req = tx.objectStore(STORE_QUEUE).getAll();
            req.onsuccess = () => resolve(req.result);
            req.onerror = () => reject(req.error);
        });
    }

    /**
     * Sync qilingan eski yozuvlarni tozalash
     */
    async function clearSynced() {
        const db = await openDB();
        return new Promise((resolve) => {
            const tx = db.transaction(STORE_QUEUE, 'readwrite');
            const store = tx.objectStore(STORE_QUEUE);
            const idx = store.index('synced');
            const req = idx.openCursor(IDBKeyRange.only(1));
            req.onsuccess = (e) => {
                const cursor = e.target.result;
                if (cursor) {
                    cursor.delete();
                    cursor.continue();
                } else {
                    resolve();
                    notifyChange();
                }
            };
        });
    }

    // === SYNC ENGINE ===

    let syncing = false;

    /**
     * Hozirgi navbatdagi yozuvlarni serverga yuborish
     */
    async function syncNow() {
        if (syncing) return { skipped: true };
        if (!navigator.onLine) return { offline: true };

        syncing = true;
        notifyChange({ syncing: true });

        const pending = await getPending();
        const results = { total: pending.length, success: 0, failed: 0 };

        for (const item of pending) {
            try {
                const headers = {
                    'X-CSRFToken': getCSRFToken(),
                    'X-Requested-With': 'OfflineSync',
                };

                let body;
                if (item.files && item.files.length > 0) {
                    // FormData (fayllar bilan)
                    body = new FormData();
                    Object.entries(item.data || {}).forEach(([k, v]) => body.append(k, v));
                    item.files.forEach(f => body.append(f.field, f.blob, f.name));
                } else {
                    headers['Content-Type'] = 'application/json';
                    body = JSON.stringify(item.data || {});
                }

                const res = await fetch(item.url, {
                    method: item.method || 'POST',
                    headers,
                    body,
                    credentials: 'include',
                });

                if (res.ok) {
                    await markSynced(item.id);
                    results.success++;
                } else {
                    await recordError(item.id, `HTTP ${res.status}`);
                    results.failed++;
                }
            } catch (err) {
                await recordError(item.id, err.message);
                results.failed++;
            }
        }

        syncing = false;
        notifyChange({ syncing: false, results });
        return results;
    }

    // === CHANGE NOTIFICATION ===
    const listeners = new Set();

    function onChange(cb) {
        listeners.add(cb);
        return () => listeners.delete(cb);
    }

    async function notifyChange(extra = {}) {
        const pending = await getPending();
        listeners.forEach(cb => {
            try { cb({ pendingCount: pending.length, ...extra }); } catch (e) { console.error(e); }
        });
    }

    // === HELPERS ===

    function getCSRFToken() {
        const m = document.cookie.match(/csrftoken=([^;]+)/);
        if (m) return m[1];
        const meta = document.querySelector('meta[name="csrf-token"]');
        if (meta) return meta.getAttribute('content');
        const inp = document.querySelector('input[name="csrfmiddlewaretoken"]');
        if (inp) return inp.value;
        return '';
    }

    // === AVTO-SYNC ===

    // Online bo'lganda avtomatik sync
    window.addEventListener('online', () => {
        console.log('[OfflineSync] Online - syncing...');
        syncNow();
    });

    // Sahifa ochilganda online bo'lsa sync
    document.addEventListener('DOMContentLoaded', () => {
        if (navigator.onLine) {
            setTimeout(() => syncNow(), 1500);
        }
        notifyChange();
    });

    // Service worker bilan aloqa
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.addEventListener('message', (event) => {
            if (event.data && event.data.type === 'SYNC_START') {
                syncNow();
            }
        });
    }

    // === PUBLIC API ===
    global.OfflineSync = {
        enqueue,
        getPending,
        getAll,
        markSynced,
        remove,
        clearSynced,
        syncNow,
        onChange,
        isOnline: () => navigator.onLine,
        notifyChange,
    };
})(window);
