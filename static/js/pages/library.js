// 动漫库页专属脚本：筛选表单构建 URL 跳转
document.addEventListener('DOMContentLoaded', () => {
    const filterForm = document.querySelector('.filter-form[data-page="library"], .filter-form');
    if (!filterForm) return;

    filterForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const yearEl = filterForm.querySelector('#year');
        const seasonEl = filterForm.querySelector('#season');
        const voteEl = filterForm.querySelector('#min_vote');

        let year = (yearEl && yearEl.value) || '';
        let season = (seasonEl && seasonEl.value) || '';
        let vote = (voteEl && voteEl.value) || '';

        if (year === '') year = 'all';
        if (season === '') season = 'all';
        if (vote === '') vote = '0';

        window.location.href = `/library/${year}/${season}/${vote}`;
    });
});