// 全局 JavaScript

document.addEventListener('DOMContentLoaded', () => {
    // 搜索表单：空值校验（全站通用）
    document.querySelectorAll('.search-form').forEach(form => {
        form.addEventListener('submit', (e) => {
            const input = form.querySelector('.search-input');
            if (input && input.value.trim() === '') {
                e.preventDefault();
                alert('请输入搜索关键词');
            }
        });
    });
});

// 通用平滑滚动
function smoothScrollTo(target, duration = 600) {
    const el = typeof target === 'string' ? document.querySelector(target) : target;
    if (!el) return;
    const start = window.pageYOffset;
    const end = el.getBoundingClientRect().top + start;
    const distance = end - start;
    let startTime = null;

    function easeInOutQuad(t) {
        return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    }

    function step(timestamp) {
        if (!startTime) startTime = timestamp;
        const progress = Math.min((timestamp - startTime) / duration, 1);
        const eased = easeInOutQuad(progress);
        window.scrollTo(0, start + distance * eased);
        if (progress < 1) requestAnimationFrame(step);
    }

    requestAnimationFrame(step);
}

window.AppUtils = {smoothScrollTo};