document.addEventListener("DOMContentLoaded", function() {
    // Récupérer les données KPI
    fetch('/kpi_data')
        .then(response => response.json())
        .then(data => {
            // Mettre à jour les indicateurs KPI
            document.getElementById("total-articles-count").textContent = data.total_articles_count;
            document.getElementById("total-articles").textContent = data.total_articles;
            document.getElementById("total-ventes").textContent = data.total_ventes;
            document.getElementById("total-achats").textContent = data.total_achats;
            document.getElementById("valeur-stock").textContent = data.valeur_stock.toFixed(2) + " €";
            document.getElementById("commandes-non-completes").textContent = data.commandes_non_completes;

            // Initialiser le graphique
            renderArticlesPieChart(data.articles);
        })
        .catch(error => console.error("Erreur lors de la récupération des données KPI:", error));
});

function renderArticlesPieChart(articleData) {
    const ctx = document.getElementById('chart-articles').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: articleData.labels,
            datasets: [{
                label: 'Quantité des Articles',
                data: articleData.data,
                backgroundColor: generateRandomColors(articleData.data.length),
                hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (tooltipItem) {
                            return `${articleData.labels[tooltipItem.dataIndex]}: ${tooltipItem.raw}`;
                        }
                    }
                },
            },
            title: {
                display: true,
                text: 'Répartition des Articles par Quantité'
            }
        }
    });
}

// Fonction pour générer des couleurs aléatoires
function generateRandomColors(num) {
    const colors = [];
    for (let i = 0; i < num; i++) {
        const color = `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 0.6)`;
        colors.push(color);
    }
    return colors;
}
