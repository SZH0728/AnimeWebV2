// 生成 X 轴标签（YYYY-MM-DD）
function constructLabels(raws) {
    const labels = raws.map(item => {
        if (!item.date) {
            return '';
        }

        // item.date 可能已是 "YYYY-MM-DD" 字符串
        const d = new Date(item.date);
        if (isNaN(d.getTime())) {
            return String(item.date);
        }

        const y = d.getFullYear();
        const m = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');

        return `${y}-${m}-${day}`;
    });

    return labels;
}

// 收集所有平台名（来自 detail_score 的 key），并保持稳定顺序
function constructPlatformOrder(raws) {
    const platformOrder = [];

    raws.forEach(item => {
        const ds = item.detail_score || {};
        Object.keys(ds).forEach(k => {
            if (!platformOrder.includes(k)) platformOrder.push(k);
        });
    });

    return platformOrder;
}

// 颜色方案：沿用主题色并生成区分度高的系列颜色
const baseColors = [
    'rgba(30,136,229,1)',   // --primary-color
    'rgba(21,101,192,1)',   // --primary-dark
    'rgba(100,181,246,1)',  // --secondary-color
    'rgba(0,150,136,1)',
    'rgba(233,30,99,1)',
    'rgba(255,152,0,1)',
    'rgba(156,39,176,1)'
];
const withAlpha = (c, a) => c.replace(',1)', `,${a})`);

// 平台评分数据（优先 sv.score，其次 sv[0]）
function constructPlatformSeries(platformOrder, raws) {
    const platformSeries = platformOrder.map((pf, idx) => {
        const color = baseColors[idx % baseColors.length];
        const data = raws.map(item => {
            const sv = (item.detail_score && item.detail_score[pf]) ? item.detail_score[pf] : null;

            if (!sv) {
                return null;
            }

            if (typeof sv === 'object') {
                if (Object.prototype.hasOwnProperty.call(sv, 'score')) {
                    return Number(sv.score);
                }

                if (Array.isArray(sv) || sv[0] !== undefined) {
                    return Number(sv[0]);
                }
            }
            return null;
        });

        return {
            label: pf,
            data,
            tension: 0.25,
            borderColor: color,
            backgroundColor: withAlpha(color, 0.12),
            pointRadius: 3,
            pointHoverRadius: 5,
            spanGaps: true
        };
    });

    return platformSeries;
}

function constructChart(rawList) {
    const labels = constructLabels(rawList);
    const platformOrder = constructPlatformOrder(rawList);

    // 总评分数据
    const totalScoreData = rawList.map(item => (item.score != null ? Number(item.score) : null));
    const platformSeries = constructPlatformSeries(platformOrder, rawList);

    // 将“总评分”放在第一条，颜色使用主题主色
    const totalColor = baseColors[0];
    const datasets = [{
        label: '总评分',
        data: totalScoreData,
        tension: 0.25,
        borderColor: totalColor,
        backgroundColor: withAlpha(totalColor, 0.12),
        borderWidth: 2.5,
        pointRadius: 3,
        pointHoverRadius: 5,
        spanGaps: true
    }].concat(platformSeries);

    // 创建图表
    const ctx = document.getElementById('scoreTrendChart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: true, // 由父容器 aspect-ratio 控制
            scales: {
                x: {
                    title: {display: true, text: '日期'},
                    grid: {color: 'rgba(0,0,0,0.05)'},
                    ticks: {
                        autoSkip: true,
                        maxRotation: 0,
                        minRotation: 0
                    }
                },
                y: {
                    title: {display: true, text: '评分'},
                    suggestedMin: 0,
                    suggestedMax: 10,
                    grid: {color: 'rgba(0,0,0,0.05)'}
                }
            },
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        usePointStyle: true
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        // 格式化数值到两位小数
                        label: function (context) {
                            const v = context.parsed.y;

                            if (v == null || isNaN(v)) {
                                return `${context.dataset.label}: -`;
                            }

                            return `${context.dataset.label}: ${Number(v).toFixed(2)}`;
                        }
                    }
                },
                title: {
                    display: false
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            },
            elements: {
                line: {borderWidth: 2}
            }
        }
    });
}