# Fonction_re_c_Apply.py
import re
import os
import traceback 

def res_Code_Apply(answer_LLM, page_file_path, texte_a_supprimer=None):
    """
    Extrait le code HTML de la réponse LLM et l'applique au fichier spécifié.
    (Ignorera le CSS pour l'instant si présent, se concentre sur le HTML principal)
    
    Args:
        answer_LLM (str): Réponse du LLM contenant le code.
        page_file_path (str): Chemin vers le fichier HTML à modifier.
        texte_a_supprimer (str, optional): Non utilisé.
    
    Returns:
        bool: True si succès, False sinon.
    """
    
    print(f"\n--- DÉBOGAGE : res_Code_Apply Démarré ---")
    print(f"DEBUG: page_file_path reçu: '{page_file_path}'")
    
    # Nouveau pattern pour capturer le bloc HTML complet
    # Il cherche <!DOCTYPE html> et capture tout jusqu'à </html>
    # Utilise re.DOTALL pour que . corresponde aux sauts de ligne
    # Utilise re.IGNORECASE pour être insensible à la casse de DOCTYPE
    html_pattern = r'<!DOCTYPE html>(.*?)</html>'
    html_match = re.search(html_pattern, answer_LLM, re.DOTALL | re.IGNORECASE)
    
    extracted_code = ""
    if html_match:
        # Reconstruire le code HTML complet avec le doctype et les balises html
        extracted_code = "<!DOCTYPE html>" + html_match.group(1) + "</html>"
        extracted_code = extracted_code.strip()
    
    if not extracted_code:
        print("Erreur : Aucun bloc HTML valide (commençant par <!DOCTYPE html> et finissant par </html>) trouvé.")
        print(f"DEBUG: Contenu de answer_LLM (premiers 500 caractères): '{answer_LLM[:500]}...'")
        print(f"--- DÉBOGAGE : res_Code_Apply Terminé (Échec Extraction HTML) ---\n")
        return False
    
    print(f"DEBUG: Longueur du code HTML extrait: {len(extracted_code)} caractères.")
    print(f"DEBUG: Début du code HTML extrait: '{extracted_code[:100]}...'")
    print(f"DEBUG: Fin du code HTML extrait: '...{extracted_code[-100:]}'")

    # 2. Application du code au fichier
    try:
        target_dir = os.path.dirname(page_file_path)
        if target_dir and not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
            print(f"DEBUG: Répertoire parent créé : {target_dir}")
        elif not target_dir:
            print(f"DEBUG: Le fichier '{page_file_path}' est dans le répertoire courant. Pas de création de répertoire nécessaire.")

        print(f"DEBUG: Tentative d'écriture dans le fichier: '{page_file_path}'")
        with open(page_file_path, 'w', encoding='utf-8') as f:
            f.write(extracted_code)
        
        print(f"Code appliqué avec succès dans {page_file_path}")
        print(f"--- DÉBOGAGE : res_Code_Apply Terminé (Succès) ---\n")
        return True
    except Exception as e:
        print(f"Erreur lors de l'application du code au fichier '{page_file_path}' : {e}")
        traceback.print_exc() 
        print(f"--- DÉBOGAGE : res_Code_Apply Terminé (Échec Écriture) ---\n")
        return False