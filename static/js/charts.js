$(document).ready(function() {
    // Récupérer les résultats du sessionStorage
    const resultatsStr = sessionStorage.getItem('resultats');
    const dataStr = sessionStorage.getItem('data');
    
    if (!resultatsStr || !dataStr) {
        $('#noData').show();
        $('#resultsContainer').hide();
        return;
    }
    
    const resultats = JSON.parse(resultatsStr);
    const data = JSON.parse(dataStr);
    
    $('#noData').hide();
    $('#resultsContainer').show();
    
    // Afficher les résultats de Whipple
    displayWhippleResults(resultats.whipple);
    
    // Afficher les résultats de Myers
    displayMyersResults(resultats.myers);
    
    // Afficher les résultats de Bachi
    displayBachiResults(resultats.bachi);
    
    // Afficher les résultats de l'ICNU
    displayICNUResults(resultats.icnu);
    
    // Créer le graphique
    createPopulationChart(data);
});

function displayWhippleResults(whipple) {
    $('#whipple-homme').text(whipple.homme !== null ? whipple.homme : 'N/A');
    $('#whipple-femme').text(whipple.femme !== null ? whipple.femme : 'N/A');
    $('#whipple-ensemble').text(whipple.ensemble !== null ? whipple.ensemble : 'N/A');
    
    // Qualité pour chaque catégorie
    addWhippleQuality('homme', whipple.homme);
    addWhippleQuality('femme', whipple.femme);
    addWhippleQuality('ensemble', whipple.ensemble);
}

function addWhippleQuality(type, value) {
    if (value === null) return;
    
    let quality = '';
    let className = '';
    
    if (value < 1.05) {
        quality = 'Excellente qualité';
        className = 'quality-good';
    } else if (value < 1.25) {
        quality = 'Qualité acceptable';
        className = 'quality-acceptable';
    } else {
        quality = 'Attraction importante';
        className = 'quality-poor';
    }
    
    $(`#whipple-${type}-quality`).text(quality).addClass(className);
}

function displayMyersResults(myers) {
    $('#myers-homme').text(myers.homme !== null ? myers.homme : 'N/A');
    $('#myers-femme').text(myers.femme !== null ? myers.femme : 'N/A');
    $('#myers-ensemble').text(myers.ensemble !== null ? myers.ensemble : 'N/A');
    
    // Qualité pour chaque catégorie
    addMyersQuality('homme', myers.homme);
    addMyersQuality('femme', myers.femme);
    addMyersQuality('ensemble', myers.ensemble);
}

function addMyersQuality(type, value) {
    if (value === null) return;
    
    let quality = '';
    let className = '';
    
    if (value < 5) {
        quality = 'Très bonne qualité';
        className = 'quality-good';
    } else if (value < 10) {
        quality = 'Qualité acceptable';
        className = 'quality-acceptable';
    } else if (value < 20) {
        quality = 'Qualité médiocre';
        className = 'quality-poor';
    } else {
        quality = 'Très mauvaise qualité';
        className = 'quality-poor';
    }
    
    $(`#myers-${type}-quality`).text(quality).addClass(className);
}

function displayBachiResults(bachi) {
    $('#bachi-homme').text(bachi.homme !== null ? bachi.homme.toFixed(2) + '%' : 'N/A');
    $('#bachi-femme').text(bachi.femme !== null ? bachi.femme.toFixed(2) + '%' : 'N/A');
    $('#bachi-ensemble').text(bachi.ensemble !== null ? bachi.ensemble.toFixed(2) + '%' : 'N/A');
}

function displayICNUResults(icnu) {
    $('#icnu-a').text(icnu.indice_a);
    $('#icnu-b').text(icnu.indice_b);
    $('#icnu-c').text(icnu.indice_c);
    $('#icnu-total').text(icnu.icnu);
    
    // Qualité de l'ICNU
    let quality = '';
    let className = '';
    
    if (icnu.icnu < 20) {
        quality = 'Bonne qualité';
        className = 'quality-good';
    } else if (icnu.icnu < 40) {
        quality = 'Qualité acceptable';
        className = 'quality-acceptable';
    } else {
        quality = 'Qualité médiocre';
        className = 'quality-poor';
    }
    
    $('#icnu-quality').text(quality).addClass(className);
}

function createPopulationChart(data) {
    const ctx = document.getElementById('populationChart').getContext('2d');
    
    const ages = data.map(row => row.Age);
    const hommes = data.map(row => row.Homme);
    const femmes = data.map(row => row.Femme);
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ages,
            datasets: [
                {
                    label: 'Hommes',
                    data: hommes,
                    borderColor: 'rgb(54, 162, 235)',
                    backgroundColor: 'rgba(54, 162, 235, 0.1)',
                    tension: 0.1
                },
                {
                    label: 'Femmes',
                    data: femmes,
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.1)',
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Distribution de la population par âge et sexe'
                },
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Effectif'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Âge'
                    }
                }
            }
        }
    });
}