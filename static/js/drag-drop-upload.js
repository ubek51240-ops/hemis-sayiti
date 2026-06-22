/**
 * Drag & Drop Upload Enhancer
 * Barcha `input[type="file"][data-dragdrop]` yoki `.dragdrop-upload` klassli elementlarni
 * drag & drop bilan boyitadi.
 */
(function() {
    'use strict';

    const style = document.createElement('style');
    style.textContent = `
        .dd-upload-wrapper {
            position: relative;
            border: 2px dashed #cbd5e1;
            border-radius: 12px;
            padding: 24px;
            text-align: center;
            background: #f8fafc;
            transition: all 0.25s ease;
            cursor: pointer;
        }
        .dd-upload-wrapper:hover {
            border-color: #3b82f6;
            background: #eff6ff;
        }
        .dd-upload-wrapper.dragover {
            border-color: #3b82f6;
            background: #dbeafe;
            transform: scale(1.01);
        }
        .dd-upload-wrapper input[type="file"] {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            opacity: 0;
            cursor: pointer;
        }
        .dd-upload-icon {
            font-size: 2.5rem;
            color: #64748b;
            margin-bottom: 8px;
            transition: color 0.25s ease, transform 0.25s ease;
        }
        .dd-upload-wrapper.dragover .dd-upload-icon {
            color: #3b82f6;
            transform: translateY(-4px);
        }
        .dd-upload-text {
            font-size: 0.95rem;
            color: #475569;
            font-weight: 500;
        }
        .dd-upload-hint {
            font-size: 0.8rem;
            color: #94a3b8;
            margin-top: 4px;
        }
        .dd-upload-filelist {
            margin-top: 12px;
            text-align: left;
        }
        .dd-upload-fileitem {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 8px 12px;
            background: #ffffff;
            border-radius: 8px;
            margin-bottom: 6px;
            border: 1px solid #e2e8f0;
            font-size: 0.9rem;
        }
        .dd-upload-fileitem .file-name {
            display: flex;
            align-items: center;
            gap: 8px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .dd-upload-fileitem .file-size {
            color: #94a3b8;
            font-size: 0.8rem;
            margin-left: 8px;
        }
        [data-theme="dark"] .dd-upload-wrapper {
            background: #1e293b;
            border-color: #475569;
        }
        [data-theme="dark"] .dd-upload-wrapper:hover,
        [data-theme="dark"] .dd-upload-wrapper.dragover {
            background: #0f172a;
            border-color: #3b82f6;
        }
        [data-theme="dark"] .dd-upload-text { color: #e2e8f0; }
        [data-theme="dark"] .dd-upload-fileitem {
            background: #0f172a;
            border-color: #334155;
            color: #e2e8f0;
        }
    `;
    document.head.appendChild(style);

    function formatSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / 1024 / 1024).toFixed(2) + ' MB';
    }

    function getFileIcon(filename) {
        const ext = filename.split('.').pop().toLowerCase();
        if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(ext)) return 'bi-file-image';
        if (['pdf'].includes(ext)) return 'bi-file-pdf';
        if (['doc', 'docx'].includes(ext)) return 'bi-file-word';
        if (['xls', 'xlsx'].includes(ext)) return 'bi-file-excel';
        return 'bi-file-earmark';
    }

    function enhance(input) {
        if (input.dataset.ddEnhanced) return;
        input.dataset.ddEnhanced = '1';

        const wrapper = document.createElement('div');
        wrapper.className = 'dd-upload-wrapper';

        const accept = input.getAttribute('accept') || '';
        const multiple = input.hasAttribute('multiple');
        const labelText = input.dataset.ddLabel || "Faylni shu yerga tashlang yoki tanlash uchun bosing";
        const hintText = input.dataset.ddHint || (accept ? `Ruxsat etilgan: ${accept}` : 'Istalgan fayl turi');

        wrapper.innerHTML = `
            <div class="dd-upload-icon"><i class="bi bi-cloud-arrow-up-fill"></i></div>
            <div class="dd-upload-text">${labelText}</div>
            <div class="dd-upload-hint">${hintText}</div>
            <div class="dd-upload-filelist"></div>
        `;

        input.parentNode.insertBefore(wrapper, input);
        wrapper.appendChild(input);

        const fileList = wrapper.querySelector('.dd-upload-filelist');

        function renderFiles(files) {
            fileList.innerHTML = '';
            Array.from(files).forEach(f => {
                const item = document.createElement('div');
                item.className = 'dd-upload-fileitem';
                item.innerHTML = `
                    <div class="file-name">
                        <i class="bi ${getFileIcon(f.name)}"></i>
                        <span>${f.name}</span>
                    </div>
                    <span class="file-size">${formatSize(f.size)}</span>
                `;
                fileList.appendChild(item);
            });
        }

        // Drag events
        ['dragenter', 'dragover'].forEach(ev => {
            wrapper.addEventListener(ev, e => {
                e.preventDefault();
                e.stopPropagation();
                wrapper.classList.add('dragover');
            });
        });
        ['dragleave', 'drop'].forEach(ev => {
            wrapper.addEventListener(ev, e => {
                e.preventDefault();
                e.stopPropagation();
                wrapper.classList.remove('dragover');
            });
        });

        wrapper.addEventListener('drop', e => {
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                // DataTransfer to assign files to input
                const dt = new DataTransfer();
                Array.from(files).forEach(f => dt.items.add(f));
                if (!multiple && dt.files.length > 1) {
                    // Keep only first file
                    const first = new DataTransfer();
                    first.items.add(dt.files[0]);
                    input.files = first.files;
                } else {
                    input.files = dt.files;
                }
                renderFiles(input.files);
                input.dispatchEvent(new Event('change', { bubbles: true }));
            }
        });

        input.addEventListener('change', function() {
            renderFiles(input.files);
        });
    }

    document.addEventListener('DOMContentLoaded', function() {
        // Avatar va maxsus holatlar uchun "data-no-dragdrop" bilan opt-out qilish mumkin
        document.querySelectorAll('input[type="file"]').forEach(function(input) {
            if (input.dataset.noDragdrop === 'true') return;
            // Avatar input larini qo'shmaymiz (ular alohida preview bilan)
            if (input.accept && input.accept.includes('image') && input.closest('[id*=avatar], [class*=avatar]')) return;
            enhance(input);
        });
    });
})();
