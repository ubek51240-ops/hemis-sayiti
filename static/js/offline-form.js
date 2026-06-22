/**
 * Test-sinov-ucun - Offline Form Handler
 *
 * Foydalanish: Forma elementiga `data-offline-enabled="true"` qo'shing.
 * Optional: data-offline-label="Talaba qo'shildi" - sync xabari uchun.
 *
 * Misol: <form data-offline-enabled="true" data-offline-label="Talaba">...</form>
 *
 * Offline holatda forma submit qilinganda OfflineSync.enqueue() chaqiriladi.
 * Online bo'lsa standart yo'l bilan submit qilinadi.
 */
(function () {
    'use strict';

    /**
     * Forma ma'lumotlarini olish
     */
    async function extractFormData(form) {
        const fd = new FormData(form);
        const data = {};
        const files = [];

        for (const [key, value] of fd.entries()) {
            if (value instanceof File) {
                if (value.size > 0) {
                    // Faylni base64 ga aylantirib saqlash kerak emas - blob saqlaymiz
                    const buf = await value.arrayBuffer();
                    files.push({
                        field: key,
                        name: value.name,
                        type: value.type,
                        size: value.size,
                        blob: new Blob([buf], { type: value.type }),
                    });
                }
            } else {
                // Bir nomdagi bir nechta qiymat (checkbox) uchun array
                if (data[key] !== undefined) {
                    if (!Array.isArray(data[key])) data[key] = [data[key]];
                    data[key].push(value);
                } else {
                    data[key] = value;
                }
            }
        }

        return { data, files };
    }

    /**
     * Submit interceptor
     */
    async function handleSubmit(e) {
        const form = e.target;
        if (!form.matches('form[data-offline-enabled="true"]')) return;

        // Online bo'lsa standart submit
        if (navigator.onLine) {
            return; // ruxsat berish - default submit
        }

        // Offline - to'xtatamiz va navbatga qo'shamiz
        e.preventDefault();

        const label = form.dataset.offlineLabel || 'Yozuv';
        const action = form.action || window.location.href;
        const method = (form.method || 'POST').toUpperCase();

        try {
            const { data, files } = await extractFormData(form);

            await window.OfflineSync.enqueue({
                type: form.dataset.offlineType || 'form',
                label,
                url: action,
                method,
                data,
                files,
            });

            showOfflineToast(`✓ ${label} mahalliy saqlandi! Internet kelganda yuklanadi.`, 'success');

            // Forma ni tozalash yoki redirect (ixtiyoriy)
            const redirect = form.dataset.offlineRedirect;
            if (redirect) {
                setTimeout(() => { window.location.href = redirect; }, 1500);
            } else if (form.dataset.offlineReset !== 'false') {
                form.reset();
            }
        } catch (err) {
            console.error('[OfflineForm] Error:', err);
            showOfflineToast(`Xatolik: ${err.message}`, 'error');
        }
    }

    function showOfflineToast(msg, type = 'info') {
        const toast = document.createElement('div');
        const colors = {
            success: '#22c55e',
            error: '#ef4444',
            info: '#3b82f6',
        };
        toast.style.cssText = `
            position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
            padding: 14px 24px; border-radius: 12px;
            background: ${colors[type] || colors.info};
            color: white; font-weight: 600; font-size: 14px;
            z-index: 10000; box-shadow: 0 8px 32px rgba(0,0,0,0.25);
            max-width: 90%;
        `;
        toast.textContent = msg;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 4000);
    }

    /**
     * Forma elementlariga offline indicator qo'shish
     */
    function decorateOfflineForms() {
        document.querySelectorAll('form[data-offline-enabled="true"]').forEach(form => {
            if (form.dataset.offlineDecorated) return;
            form.dataset.offlineDecorated = '1';

            // Ko'rinadigan offline-mode badge
            const badge = document.createElement('div');
            badge.className = 'offline-form-badge';
            badge.style.cssText = `
                display: inline-flex; align-items: center; gap: 6px;
                padding: 6px 12px; background: #dbeafe; color: #1e40af;
                border-radius: 20px; font-size: 12px; font-weight: 600;
                margin-bottom: 10px;
            `;
            badge.innerHTML = `<i class="bi bi-cloud-arrow-up-fill"></i> Bu forma offline ishlaydi`;
            form.insertBefore(badge, form.firstChild);
        });
    }

    document.addEventListener('submit', handleSubmit, true);
    document.addEventListener('DOMContentLoaded', decorateOfflineForms);

    // Public
    window.OfflineForm = {
        extractFormData,
        showToast: showOfflineToast,
    };
})();
