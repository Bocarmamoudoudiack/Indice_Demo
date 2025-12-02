from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug.utils import secure_filename
import pandas as pd
import os
from utils.calculateurs import (
    calculer_whipple,
    calculer_myers,
    calculer_bachi,
    calculer_icnu
)
from config import Config

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Aucun fichier fourni'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'Aucun fichier sélectionné'}), 400
        
        if not Config.allowed_file(file.filename):
            return jsonify({'error': 'Format de fichier non autorisé. Utilisez .xlsx ou .xls'}), 400
        
        # Sauvegarder le fichier
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Lire le fichier Excel
        df = pd.read_excel(filepath)
        
        # Vérifier les colonnes requises (sans Ensemble)
        required_columns = ['Age', 'Homme', 'Femme']
        if not all(col in df.columns for col in required_columns):
            os.remove(filepath)
            return jsonify({'error': f'Le fichier doit contenir les colonnes: {", ".join(required_columns)}'}), 400
        
        # Calculer automatiquement la colonne Ensemble
        df['Ensemble'] = df['Homme'] + df['Femme']
        
        # Calculer les indices
        resultats = {}
        
        # Indice de Whipple
        whipple = calculer_whipple(df)
        resultats['whipple'] = whipple
        
        # Indice de Myers
        myers = calculer_myers(df)
        resultats['myers'] = myers
        
        # Indice de Bachi
        bachi = calculer_bachi(df)
        resultats['bachi'] = bachi
        
        # Indice combiné des Nations Unies
        icnu = calculer_icnu(df)
        resultats['icnu'] = icnu
        
        # Supprimer le fichier après traitement
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'resultats': resultats,
            'data': df.to_dict('records')
        })
    
    except Exception as e:
        return jsonify({'error': f'Erreur lors du traitement: {str(e)}'}), 500

@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')