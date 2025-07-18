import google.generativeai as genai
import os
from typing import Optional

class GeminiWebExpert:
    """
    Classe pour utiliser Gemini comme expert en développement web
    """
    
    def __init__(self, api_key: str):
        """
        Initialise l'expert Gemini avec la clé API
        
        Args:
            api_key (str): Clé API Gemini
        """
        self.api_key = api_key
        self.model = None
        self.configure_api()
    
    def configure_api(self):
        """Configure l'API Gemini avec la clé fournie"""
        try:
            genai.configure(api_key=self.api_key)
            # Utiliser Gemini 2.0 Flash pour la génération de code
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            print("✅ API Gemini configurée avec succès")
        except Exception as e:
            print(f"❌ Erreur lors de la configuration de l'API Gemini : {e}")
    
    def generate_code(self, prompt: str, existing_code: str = "") -> Optional[str]:
        """
        Génère du code modifié avec Gemini
        
        Args:
            prompt (str): Prompt technique précis (venant du transformateur Gemini)
            existing_code (str): Code existant à modifier (contenu de Page_file)
            
        Returns:
            str: Réponse complète de Gemini avec le code encadré
        """
        
        # Construction du message pour Gemini
        gemini_message = self._build_expert_message(prompt, existing_code)
        
        try:
            # Appel à l'API Gemini
            response = self.model.generate_content(gemini_message)
            
            if response and response.text:
                return response.text.strip()
            else:
                print("❌ Aucune réponse reçue de Gemini")
                return None
                
        except Exception as e:
            print(f"❌ Erreur lors de la génération de code : {e}")
            return None
    
    def _build_expert_message(self, prompt: str, existing_code: str) -> str:
        """
        Construit le message complet pour Gemini en tant qu'expert web
        
        Args:
            prompt (str): Prompt technique
            existing_code (str): Code existant
            
        Returns:
            str: Message complet pour Gemini
        """
        
        message = f"""
Tu es un expert en développement web frontend spécialisé dans HTML, CSS et JavaScript.

MISSION : Modifier le code existant selon les instructions précises fournies.

INSTRUCTIONS TECHNIQUES REÇUES :
{prompt}

CODE EXISTANT À MODIFIER :
```
{existing_code if existing_code else "Aucun code existant - Créer depuis zéro"}
```

RÈGLES IMPORTANTES :
1. Génère un code HTML/CSS/JS complet et fonctionnel
2. Respecte les meilleures pratiques de développement web
3. Assure-toi que le code soit moderne, responsive et accessible
4. Optimise les performances et la lisibilité
5. Ajoute des commentaires pour expliquer les parties complexes
6. OBLIGATOIRE : Encadre ta réponse finale avec [CODE_START] et [CODE_END]

STRUCTURE DE RÉPONSE ATTENDUE :
- Brève explication de ce que tu vas faire
- Le code complet encadré par [CODE_START] et [CODE_END]
- Explication des modifications apportées

Génère maintenant le code selon ces spécifications :
"""
        
        return message

# Fonction principale de génération de code
def generate_web_code(technical_prompt: str, page_file_path: str = "Page_file") -> Optional[str]:
    """
    Fonction principale pour générer du code web avec Gemini
    
    Args:
        technical_prompt (str): Prompt technique précis (venant du transformateur)
        page_file_path (str): Chemin vers le fichier de code existant
        
    Returns:
        str: Réponse complète de Gemini avec le code
    """
    
    # Clé API Gemini
    GEMINI_API_KEY = "AIzaSyACLgVtTIE100tJx-PcdH09RfFwSFhoUe0"
    
    # Créer l'expert Gemini
    expert = GeminiWebExpert(GEMINI_API_KEY)
    
    if not expert.model:
        print("❌ Impossible d'initialiser l'expert Gemini")
        return None
    
    # Lire le code existant depuis Page_file
    existing_code = ""
    if os.path.exists(page_file_path):
        try:
            with open(page_file_path, "r", encoding="utf-8") as file:
                existing_code = file.read()
            print(f"✅ Code existant lu depuis {page_file_path}")
        except Exception as e:
            print(f"⚠️ Erreur lecture fichier {page_file_path}: {e}")
    else:
        print(f"⚠️ Fichier {page_file_path} non trouvé - Création depuis zéro")
    
    # Génération du code avec Gemini
    print("🔄 Génération du code en cours avec Gemini...")
    response = expert.generate_code(technical_prompt, existing_code)
    
    if response:
        print("✅ Code généré avec succès par Gemini")
        return response
    else:
        print("❌ Échec de la génération de code")
        return None

# Fonction de test
def test_gemini_expert():
    """Teste l'expert Gemini avec un exemple"""
    
    # Exemple de prompt technique (comme celui venant du transformateur)
    test_prompt = """
Crée une page HTML avec un bouton stylisé qui a les caractéristiques suivantes :
- Couleur de fond : rouge (#e74c3c)
- Texte blanc
- Bordures arrondies (border-radius: 8px)
- Effet hover qui change la couleur vers un rouge plus foncé (#c0392b)
- Transition douce de 0.3s
- Padding : 12px 24px
- Cursor pointer au survol
- Centré sur la page

OBLIGATOIRE : Encadre ta réponse avec [CODE_START] et [CODE_END]
"""
    
    # Créer un fichier de test avec du code existant
    test_file = "test_page.html"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Page de test</title>
</head>
<body>
    <h1>Page existante</h1>
    <p>Contenu à modifier</p>
</body>
</html>""")
    
    print("=== TEST DE L'EXPERT GEMINI ===\n")
    print("Prompt technique:")
    print(test_prompt)
    print("-" * 50)
    
    # Générer le code
    result = generate_web_code(test_prompt, test_file)
    
    if result:
        print("Réponse de Gemini:")
        print(result)
    else:
        print("❌ Échec du test")
    
    # Nettoyer
    if os.path.exists(test_file):
        os.remove(test_file)

if __name__ == "__main__":
    test_gemini_expert()