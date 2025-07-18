import os
import sys
from typing import Optional, Dict, Any
import json
from datetime import datetime

# Import des modules personnalisés
try:
    from QuerytoPromptTransformer import transform_user_query
    from Expert_Web_Gemini import generate_web_code
    from Fonction_re_c_Apply import res_Code_Apply
except ImportError as e:
    print(f"❌ Erreur d'import des modules : {e}")
    print("Assurez-vous que tous les fichiers sont dans le même répertoire")
    sys.exit(1)

class AssistantDux:
    """
    Assistant Dux - Orchestrateur principal du système de modification de code web
    
    Coordonne les trois étapes principales :
    1. Transformation de la requête utilisateur en prompt technique (QuerytoPromptTransformer)
    2. Génération du code modifié avec Gemini (Expert_Web_Gemini) 
    3. Application du code dans le fichier cible (Fonction_re_c_Apply)
    """
    
    def __init__(self, default_page_file: str = "Page_file"):
        """
        Initialise l'Assistant Dux
        
        Args:
            default_page_file (str): Fichier par défaut pour les modifications de code
        """
        self.default_page_file = default_page_file
        self.session_id = self._generate_session_id()
        self.history = []
        
        print("🤖 Assistant Dux initialisé avec succès")
        print(f"📁 Fichier par défaut : {self.default_page_file}")
        print(f"🆔 Session ID : {self.session_id}")
    
    def _generate_session_id(self) -> str:
        """Génère un ID de session unique"""
        return f"dux_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def process_user_request(self, 
                           user_query: str, 
                           target_file: str = None,
                           code_context: str = "") -> Dict[str, Any]:
        """
        Traite une requête utilisateur complète du début à la fin
        
        Args:
            user_query (str): Requête de l'utilisateur
            target_file (str): Fichier cible pour les modifications (optionnel)
            code_context (str): Contexte additionnel du code (optionnel)
            
        Returns:
            Dict: Résultat complet du traitement avec statuts et informations
        """
        
        # Utiliser le fichier par défaut si aucun n'est spécifié
        target_file = target_file or self.default_page_file
        
        print(f"\n{'='*60}")
        print(f"🤖 ASSISTANT DUX - TRAITEMENT DE REQUÊTE")
        print(f"{'='*60}")
        print(f"👤 Requête utilisateur : {user_query}")
        print(f"📁 Fichier cible : {target_file}")
        print(f"🕐 Heure : {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*60}")
        
        # Structure de résultat
        result = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "user_query": user_query,
            "target_file": target_file,
            "success": False,
            "steps": {
                "query_transformation": {"success": False, "data": None, "error": None},
                "code_generation": {"success": False, "data": None, "error": None},
                "code_application": {"success": False, "data": None, "error": None}
            },
            "final_message": ""
        }
        
        try:
            # ÉTAPE 1 : Transformation de la requête en prompt technique
            print("\n🔄 ÉTAPE 1 : Transformation de la requête")
            print("-" * 40)
            
            technical_prompt = self._transform_query(user_query, code_context)
            
            if not technical_prompt:
                result["steps"]["query_transformation"]["error"] = "Échec de la transformation"
                result["final_message"] = "❌ Erreur lors de la transformation de la requête"
                return result
            
            result["steps"]["query_transformation"]["success"] = True
            result["steps"]["query_transformation"]["data"] = technical_prompt
            print("✅ Transformation réussie")
            
            # ÉTAPE 2 : Génération du code avec Gemini
            print("\n🔄 ÉTAPE 2 : Génération du code")
            print("-" * 40)
            
            generated_code_response = self._generate_code(technical_prompt, target_file)
            
            if not generated_code_response:
                result["steps"]["code_generation"]["error"] = "Échec de la génération"
                result["final_message"] = "❌ Erreur lors de la génération du code"
                return result
            
            result["steps"]["code_generation"]["success"] = True
            result["steps"]["code_generation"]["data"] = generated_code_response
            print("✅ Génération réussie")
            
            # ÉTAPE 3 : Application du code dans le fichier
            print("\n🔄 ÉTAPE 3 : Application du code")
            print("-" * 40)
            
            application_success = self._apply_code(generated_code_response, target_file)
            
            if not application_success:
                result["steps"]["code_application"]["error"] = "Échec de l'application"
                result["final_message"] = "❌ Erreur lors de l'application du code"
                return result
            
            result["steps"]["code_application"]["success"] = True
            result["steps"]["code_application"]["data"] = "Code appliqué avec succès"
            print("✅ Application réussie")
            
            # Succès complet
            result["success"] = True
            result["final_message"] = f"✅ Requête traitée avec succès ! Code appliqué dans {target_file}"
            
            # Ajouter à l'historique
            self.history.append(result)
            
            print(f"\n{'='*60}")
            print("🎉 TRAITEMENT TERMINÉ AVEC SUCCÈS")
            print(f"{'='*60}")
            
            return result
            
        except Exception as e:
            error_msg = f"Erreur inattendue dans le traitement : {str(e)}"
            result["final_message"] = f"❌ {error_msg}"
            print(f"❌ {error_msg}")
            return result
    
    def _transform_query(self, user_query: str, code_context: str) -> Optional[str]:
        """
        Étape 1 : Transforme la requête utilisateur en prompt technique
        
        Args:
            user_query (str): Requête utilisateur
            code_context (str): Contexte du code
            
        Returns:
            str: Prompt technique ou None si échec
        """
        try:
            technical_prompt = transform_user_query(user_query, code_context)
            
            if technical_prompt:
                print(f"📝 Prompt technique généré ({len(technical_prompt)} caractères)")
                # Afficher un aperçu du prompt (premiers 200 caractères)
                preview = technical_prompt[:200] + "..." if len(technical_prompt) > 200 else technical_prompt
                print(f"👁️ Aperçu : {preview}")
                return technical_prompt
            else:
                print("❌ Aucun prompt technique généré")
                return None
                
        except Exception as e:
            print(f"❌ Erreur lors de la transformation : {e}")
            return None
    
    def _generate_code(self, technical_prompt: str, target_file: str) -> Optional[str]:
        """
        Étape 2 : Génère le code modifié avec Gemini
        
        Args:
            technical_prompt (str): Prompt technique précis
            target_file (str): Fichier cible
            
        Returns:
            str: Réponse complète de Gemini ou None si échec
        """
        try:
            code_response = generate_web_code(technical_prompt, target_file)
            
            if code_response:
                print(f"🔧 Code généré ({len(code_response)} caractères)")
                # Vérifier si la réponse contient les marqueurs attendus
                if "[CODE_START]" in code_response and "[CODE_END]" in code_response:
                    print("✅ Code correctement formaté avec marqueurs [CODE_START]/[CODE_END]")
                else:
                    print("⚠️ Attention : Marqueurs [CODE_START]/[CODE_END] non détectés")
                
                return code_response
            else:
                print("❌ Aucun code généré")
                return None
                
        except Exception as e:
            print(f"❌ Erreur lors de la génération : {e}")
            return None
    
    def _apply_code(self, code_response: str, target_file: str) -> bool:
        """
        Étape 3 : Applique le code généré dans le fichier cible
        
        Args:
            code_response (str): Réponse complète avec le code
            target_file (str): Fichier cible
            
        Returns:
            bool: True si succès, False sinon
        """
        try:
            success = res_Code_Apply(code_response, target_file)
            
            if success:
                print(f"💾 Code appliqué avec succès dans {target_file}")
                # Vérifier la taille du fichier modifié
                if os.path.exists(target_file):
                    file_size = os.path.getsize(target_file)
                    print(f"📊 Taille du fichier : {file_size} octets")
                return True
            else:
                print(f"❌ Échec de l'application du code dans {target_file}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors de l'application : {e}")
            return False
    
    def get_session_history(self) -> list:
        """Retourne l'historique de la session actuelle"""
        return self.history
    
    def get_last_result(self) -> Optional[Dict[str, Any]]:
        """Retourne le dernier résultat de traitement"""
        return self.history[-1] if self.history else None
    
    def create_file_if_not_exists(self, file_path: str, 
                                 initial_content: str = None) -> bool:
        """
        Crée un fichier s'il n'existe pas
        
        Args:
            file_path (str): Chemin du fichier
            initial_content (str): Contenu initial (optionnel)
            
        Returns:
            bool: True si créé ou existe déjà, False si erreur
        """
        try:
            if not os.path.exists(file_path):
                # Contenu HTML de base si aucun contenu spécifié
                default_content = initial_content or """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page générée par Assistant Dux</title>
</head>
<body>
    <h1>Page vide</h1>
    <p>Cette page a été créée par l'Assistant Dux.</p>
</body>
</html>"""
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(default_content)
                
                print(f"📄 Fichier créé : {file_path}")
                return True
            else:
                print(f"📄 Fichier existant : {file_path}")
                return True
                
        except Exception as e:
            print(f"❌ Erreur création fichier {file_path} : {e}")
            return False
    
    def display_summary(self) -> None:
        """Affiche un résumé de la session"""
        print(f"\n{'='*60}")
        print("📊 RÉSUMÉ DE LA SESSION ASSISTANT DUX")
        print(f"{'='*60}")
        print(f"🆔 Session ID : {self.session_id}")
        print(f"📁 Fichier par défaut : {self.default_page_file}")
        print(f"📈 Nombre de requêtes traitées : {len(self.history)}")
        
        if self.history:
            successful = sum(1 for h in self.history if h["success"])
            print(f"✅ Requêtes réussies : {successful}")
            print(f"❌ Requêtes échouées : {len(self.history) - successful}")
            
            print(f"\n📋 Dernières requêtes :")
            for i, entry in enumerate(self.history[-3:], 1):  # 3 dernières
                status = "✅" if entry["success"] else "❌"
                time = entry["timestamp"][:19].replace("T", " ")
                query_preview = entry["user_query"][:50] + "..." if len(entry["user_query"]) > 50 else entry["user_query"]
                print(f"  {status} {time} - {query_preview}")
        
        print(f"{'='*60}")


# Fonctions utilitaires pour utilisation simplifiée
def quick_process(user_query: str, target_file: str = "Page_file") -> bool:
    """
    Fonction rapide pour traiter une requête
    
    Args:
        user_query (str): Requête utilisateur
        target_file (str): Fichier cible
        
    Returns:
        bool: True si succès complet
    """
    dux = AssistantDux(target_file)
    
    # Créer le fichier s'il n'existe pas
    dux.create_file_if_not_exists(target_file)
    
    # Traiter la requête
    result = dux.process_user_request(user_query, target_file)
    
    # Afficher le résultat final
    print(f"\n{result['final_message']}")
    
    return result["success"]


def interactive_mode():
    """Mode interactif pour tester l'Assistant Dux"""
    print("🤖 Assistant Dux - Mode Interactif")
    print("Tapez 'quit' pour quitter, 'help' pour l'aide")
    
    dux = AssistantDux()
    
    while True:
        print(f"\n{'='*40}")
        user_input = input("👤 Votre requête : ").strip()
        
        if user_input.lower() in ['quit', 'q', 'exit']:
            dux.display_summary()
            print("👋 Au revoir !")
            break
        elif user_input.lower() == 'help':
            print("""
🆘 AIDE ASSISTANT DUX
Commands disponibles :
  - Tapez votre requête de modification de code
  - 'quit' ou 'q' : Quitter
  - 'help' : Afficher cette aide
  - 'history' : Voir l'historique
  - 'summary' : Résumé de session

Exemples de requêtes :
  - "Ajoute un bouton rouge centré sur la page"
  - "Change la couleur de fond en bleu"
  - "Ajoute un menu de navigation horizontal"
            """)
            continue
        elif user_input.lower() == 'history':
            history = dux.get_session_history()
            if history:
                print("📚 Historique des requêtes :")
                for i, entry in enumerate(history, 1):
                    status = "✅" if entry["success"] else "❌"
                    print(f"  {i}. {status} {entry['user_query']}")
            else:
                print("📚 Aucun historique disponible")
            continue
        elif user_input.lower() == 'summary':
            dux.display_summary()
            continue
        elif not user_input:
            print("⚠️ Veuillez entrer une requête")
            continue
        
        # Traiter la requête
        dux.process_user_request(user_input)


# Test et démonstration
def demo_assistant_dux():
    """Démonstration de l'Assistant Dux"""
    print("🎭 DÉMONSTRATION ASSISTANT DUX")
    print("="*50)
    
    # Créer l'assistant
    dux = AssistantDux("demo_page.html")
    
    # Créer un fichier de test
    dux.create_file_if_not_exists("demo_page.html")
    
    # Exemples de requêtes
    test_queries = [
        "Ajoute un bouton rouge centré avec du texte blanc",
        "Change la couleur de fond de la page en bleu clair",
        "Ajoute un titre h1 avec le texte 'Bienvenue sur ma page'"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🧪 TEST {i}/{len(test_queries)}")
        result = dux.process_user_request(query)
        
        if result["success"]:
            print(f"✅ Test {i} réussi")
        else:
            print(f"❌ Test {i} échoué")
        
        # Pause entre les tests
        input("Appuyez sur Entrée pour continuer...")
    
    # Résumé final
    dux.display_summary()


if __name__ == "__main__":
    # Lancer le mode interactif par défaut
    interactive_mode()