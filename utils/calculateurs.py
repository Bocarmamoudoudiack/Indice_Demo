import pandas as pd
import numpy as np

def calculer_whipple(df):
    """
    Calcul de l'indice de Whipple
    Formule : Iw = (Somme des âges terminés par 0 ou 5) × 5 / (Somme totale 23-62 ans)
    """
    # Filtrer uniquement les lignes avec des âges numériques
    df_clean = df[pd.to_numeric(df['Age'], errors='coerce').notna()].copy()
    df_clean['Age'] = pd.to_numeric(df_clean['Age'])
    
    # Filtrer les âges entre 23 et 62 ans
    df_filtre = df_clean[(df_clean['Age'] >= 23) & (df_clean['Age'] <= 62)].copy()
    
    # Identifier les âges se terminant par 0 ou 5
    df_filtre['termine_0_5'] = df_filtre['Age'].apply(lambda x: x % 10 in [0, 5])
    
    resultats = {}
    
    for sexe in ['Homme', 'Femme', 'Ensemble']:
        somme_0_5 = df_filtre[df_filtre['termine_0_5']][sexe].sum()
        somme_totale = df_filtre[sexe].sum()
        
        if somme_totale > 0:
            iw = (somme_0_5 * 5) / somme_totale
            resultats[sexe.lower()] = round(iw, 4)
        else:
            resultats[sexe.lower()] = None
    
    return resultats

def calculer_myers(df):
    """
    Calcul de l'indice de Myers
    Formule : (1/2) × Σ|((Σᵢ Pᵢ,ᵈ)/(Σᵢ Pᵢ)) × 100 - 10|
    où d = chiffre terminal (0, 1, 2, ..., 9)
    Pᵢ,ᵈ = effectif de la population d'âge i se terminant par le chiffre d
    Σᵢ Pᵢ = effectif total de la population
    
    L'indice se calcule généralement sur les âges 10-89 ans
    """
    # Filtrer uniquement les lignes avec des âges numériques
    df_clean = df[pd.to_numeric(df['Age'], errors='coerce').notna()].copy()
    df_clean['Age'] = pd.to_numeric(df_clean['Age']).astype(int)
    
    # Filtrer la tranche d'âge 10-89 ans (plage standard pour Myers)
    df_filtre = df_clean[(df_clean['Age'] >= 10) & (df_clean['Age'] <= 89)].copy()
    
    resultats = {}
    
    for sexe in ['Homme', 'Femme', 'Ensemble']:
        # Population totale de la tranche 10-89 ans (Σᵢ Pᵢ)
        total_pop = df_filtre[sexe].sum()
        
        if total_pop == 0:
            resultats[sexe.lower()] = None
            continue
        
        somme_deviations = 0
        
        # Pour chaque chiffre terminal d (0 à 9)
        for d in range(10):
            # Somme des effectifs pour tous les âges se terminant par d (Σᵢ Pᵢ,ᵈ)
            pop_avec_chiffre_d = df_filtre[df_filtre['Age'] % 10 == d][sexe].sum()
            
            # Pourcentage : (Σᵢ Pᵢ,ᵈ / Σᵢ Pᵢ) × 100
            pourcentage = (pop_avec_chiffre_d / total_pop) * 100
            
            # Déviation par rapport à 10%
            deviation = abs(pourcentage - 10)
            
            somme_deviations += deviation
        
        # Indice de Myers = (1/2) × Σ déviations
        myers = somme_deviations / 2
        resultats[sexe.lower()] = round(myers, 7)  # 7 décimales pour correspondre à Excel
    
    return resultats

def calculer_bachi(df):
    """
    Calcul de l'indice de Bachi
    Formule : (O - T) / T × 100
    Où O = Effectif observé des âges terminant par 0 ou 5 (âges 10-70)
        T = Effectif théorique = (13/61) × Population totale (10-70 ans)
    """
    # Filtrer uniquement les lignes avec des âges numériques
    df_clean = df[pd.to_numeric(df['Age'], errors='coerce').notna()].copy()
    df_clean['Age'] = pd.to_numeric(df_clean['Age'])
    
    # Filtrer les âges entre 10 et 70 ans
    df_filtre = df_clean[(df_clean['Age'] >= 10) & (df_clean['Age'] <= 70)].copy()
    
    resultats = {}
    
    for sexe in ['Homme', 'Femme', 'Ensemble']:
        # Population totale 10-70 ans
        total_10_70 = df_filtre[sexe].sum()
        
        if total_10_70 == 0:
            resultats[sexe.lower()] = None
            continue
        
        # Effectif observé (âges terminant par 0 ou 5)
        observed = df_filtre[df_filtre['Age'].apply(lambda x: x % 10 in [0, 5])][sexe].sum()
        
        # Effectif théorique
        theoretical = (13 / 61) * total_10_70
        
        # Indice de Bachi
        if theoretical > 0:
            bachi = ((observed - theoretical) / theoretical) * 100
            resultats[sexe.lower()] = round(bachi, 4)
        else:
            resultats[sexe.lower()] = None
    
    return resultats

def calculer_icnu(df):
    """
    Calcul de l'Indice Combiné des Nations Unies (ICNU)
    Formule : ICNU = A + B + 3C
    
    A = Rapport d'âges (Hommes)
    B = Rapport d'âges (Femmes)  
    C = Rapport de masculinité
    """
    # Filtrer uniquement les lignes avec des âges numériques
    df_clean = df[pd.to_numeric(df['Age'], errors='coerce').notna()].copy()
    df_clean['Age'] = pd.to_numeric(df_clean['Age']).astype(int)
    df_clean = df_clean.reset_index(drop=True)
    
    # Indice A (Rapports d'âges - Hommes)
    indice_a = calculer_rapport_ages(df_clean, 'Homme')
    
    # Indice B (Rapports d'âges - Femmes)
    indice_b = calculer_rapport_ages(df_clean, 'Femme')
    
    # Indice C (Rapport de masculinité)
    indice_c = calculer_rapport_masculinite(df_clean)
    
    # ICNU
    icnu = indice_a + indice_b + 3 * indice_c
    
    return {
        'indice_a': round(indice_a, 4),
        'indice_b': round(indice_b, 4),
        'indice_c': round(indice_c, 4),
        'icnu': round(icnu, 4)
    }

def calculer_rapport_ages(df, sexe):
    """
    Calcule le rapport d'âges pour un sexe donné
    Formule : A = (1/n) × Σ|Pᵢ / ((Pᵢ₋₁ + Pᵢ₊₁)/2) × 100 - 100|
    
    Pour chaque âge i, on compare sa population à la moyenne 
    des populations des âges adjacents (i-1 et i+1)
    """
    somme_deviations = 0
    n = 0
    
    # On commence à i=1 et on s'arrête à len(df)-2 pour avoir i-1 et i+1
    for i in range(1, len(df) - 1):
        pi = df.iloc[i][sexe]           # Population à l'âge i
        pi_moins_1 = df.iloc[i - 1][sexe]  # Population à l'âge i-1
        pi_plus_1 = df.iloc[i + 1][sexe]   # Population à l'âge i+1
        
        # Moyenne des populations adjacentes
        moyenne = (pi_moins_1 + pi_plus_1) / 2
        
        if moyenne > 0 and pi > 0:
            # Rapport en pourcentage
            rapport = (pi / moyenne) * 100
            # Déviation par rapport à 100
            deviation = abs(rapport - 100)
            somme_deviations += deviation
            n += 1
    
    return somme_deviations / n if n > 0 else 0

def calculer_rapport_masculinite(df):
    """
    Calcule l'indice de rapport de masculinité
    Formule : C = (1/m) × Σ|RMᵢ - RMᵢ₋₁|
    Où RMᵢ = (Pᵢᴴ / Pᵢᶠ) × 100
    
    On calcule le rapport de masculinité pour chaque âge,
    puis on fait la somme des valeurs absolues des différences successives
    """
    rapports_masc = []
    
    # Calculer le rapport de masculinité pour chaque âge
    for i in range(len(df)):
        homme = df.iloc[i]['Homme']
        femme = df.iloc[i]['Femme']
        
        if femme > 0:
            rm = (homme / femme) * 100
            rapports_masc.append(rm)
        else:
            rapports_masc.append(None)
    
    # Calculer les différences absolues successives
    somme_diff = 0
    m = 0
    
    for i in range(1, len(rapports_masc)):
        if rapports_masc[i] is not None and rapports_masc[i-1] is not None:
            diff = abs(rapports_masc[i] - rapports_masc[i-1])
            somme_diff += diff
            m += 1
    
    return somme_diff / m if m > 0 else 0