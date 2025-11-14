// const labels = genreData.map(g => g.genre);
// const counts = genreData.map(g => g.count);

// new Chart(document.getElementById('genreChart'), {
//     type: 'pie',
//     data: {
//         labels: labels,
//         datasets: [{
//             data: counts,
//             backgroundColor: [
//                 '#1DB954', '#191414', '#535353', '#b3b3b3', '#282828',
//                 '#404040', '#666', '#999', '#2e2e2e', '#0f0f0f'
//             ],
//             borderColor: '#121212',
//             borderWidth: 2
//         }]
//     },
//     options: {
//         plugins: {
//             legend: {
//                 display: false
//             },
//             tooltip: {
//                 enabled: true
//             },
//             title: {
//                 display: true,
//                 text: 'Genre Distribution',
//                 color: '#1DB954',
//                 font: {
//                     size: 18,
//                     family: 'Segoe UI'
//                 }
//             },
//             datalabels: {
//                 color: '#fff',
//                 font: {
//                     weight: 'bold',
//                     size: 12
//                 },
//                 formatter: (value, context) => {
//                     return context.chart.data.labels[context.dataIndex];
//                 }
//             }
//         }
//     },
//     plugins: [ChartDataLabels]
// });
function renderGenreChart() {
    const labels = genreData.map(g => g.genre);
    const counts = genreData.map(g => g.count);

    new Chart(document.getElementById('genreChart'), {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: counts,
                backgroundColor: ['#1DB954', '#191414', '#535353', '#b3b3b3', '#282828'],
                borderColor: '#121212',
                borderWidth: 2
            }]
        },
        options: {
            plugins: {
                legend: { display: false },
                datalabels: {
                    color: '#fff',
                    font: { weight: 'bold', size: 12 },
                    formatter: (value, context) => context.chart.data.labels[context.dataIndex]
                },
                title: {
                    display: true,
                    text: 'Genre Distribution',
                    color: '#1DB954',
                    font: { size: 18, family: 'Segoe UI' }
                }
            }
        },
        plugins: [ChartDataLabels]
    });
}

