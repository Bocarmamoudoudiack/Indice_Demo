$(document).ready(function() {
    $('#uploadForm').on('submit', function(e) {
        e.preventDefault();
        
        const fileInput = document.getElementById('fileInput');
        const file = fileInput.files[0];
        
        if (!file) {
            showError('Veuillez sélectionner un fichier');
            return;
        }
        
        // Vérifier l'extension du fichier
        const fileName = file.name;
        const fileExtension = fileName.split('.').pop().toLowerCase();
        
        if (fileExtension !== 'xlsx' && fileExtension !== 'xls') {
            showError('Le fichier doit être au format Excel (.xlsx ou .xls)');
            return;
        }
        
        // Préparer les données
        const formData = new FormData();
        formData.append('file', file);
        
        // Afficher le spinner
        $('#loadingSpinner').show();
        $('#errorMessage').hide();
        
        // Envoyer la requête
        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                $('#loadingSpinner').hide();
                
                if (response.success) {
                    // Stocker les résultats dans sessionStorage
                    sessionStorage.setItem('resultats', JSON.stringify(response.resultats));
                    sessionStorage.setItem('data', JSON.stringify(response.data));
                    
                    // Rediriger vers le dashboard
                    window.location.href = '/dashboard';
                } else {
                    showError('Erreur lors du traitement des données');
                }
            },
            error: function(xhr) {
                $('#loadingSpinner').hide();
                
                let errorMessage = 'Erreur lors du traitement du fichier';
                
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage = xhr.responseJSON.error;
                }
                
                showError(errorMessage);
            }
        });
    });
    
    function showError(message) {
        $('#errorMessage').text(message).show();
        
        setTimeout(function() {
            $('#errorMessage').fadeOut();
        }, 5000);
    }
});