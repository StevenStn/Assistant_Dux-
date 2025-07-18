import google.generativeai as genai
import os
from typing import Optional

""" QUESTIONS

- Pourquoi ne pas utiliser une fonction qui Prompt_transform(Requete) qui prend la requete ; fait l'appel du LLM de Gemini puis lui envoit
la rquete avec l'instruction qu'il est un developpeur web et de transformer la requet en prompt precis ; conscis et tres comprehensible pour un expert en developpement web ?

"""
class QueryToPromptTransformer:
    """
    Classe pour transformer les requêtes utilisateur en prompts précis 
    en utilisant l'API Gemini 2.0
    """
    
    def __init__(self, api_key: str):
        """
        Initialise le transformateur avec la clé API Gemini
        
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
            # Utiliser Gemini 2.0 Flash pour des réponses rapides
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            print("✅ API Gemini configurée avec succès")
        except Exception as e:
            print(f"❌ Erreur lors de la configuration de l'API Gemini : {e}")
    
    def transform_query(self, user_query: str, code_context: str = "") -> Optional[str]:
        """
        Transforme une requête utilisateur en prompt précis pour modification de code
        
        Args:
            user_query (str): Requête de l'utilisateur
            code_context (str): Contexte du code existant (optionnel)
            
        Returns:
            str: Prompt précis pour le LLM de génération de code
        """
        
        # Template de prompt pour la transformation
        transformation_prompt = f"""
Tu es un expert en transformation de requêtes utilisateur en prompts techniques précis.

MISSION : Transformer la requête utilisateur en un prompt technique détaillé pour un LLM qui doit générer du code HTML/CSS/JS.

RÈGLES IMPORTANTES :
1. Le prompt de sortie doit être TRÈS PRÉCIS et TECHNIQUE
2. Il doit spécifier exactement ce qui doit être fait au niveau du code
3. Il doit mentionner que la réponse doit être encadrée par [CODE_START] et [CODE_END]
4. Il doit préciser que la réponse doit être un **SEUL bloc de code HTML complet**, avec le CSS et le JS intégrés.
5. Il doit donner des détails sur le style, la structure et les fonctionnalités
6. **Important : Le prompt doit demander que le code généré ne contienne PAS de blocs Markdown (```html, ```css, etc.) entre [CODE_START] et [CODE_END].**

CONTEXTE DU CODE EXISTANT :
{code_context if code_context else "Aucun contexte fourni"}

REQUÊTE UTILISATEUR :
"{user_query}"

GÉNÈRE UN PROMPT TECHNIQUE PRÉCIS :
"""
        
        try:
            response = self.model.generate_content(transformation_prompt)
            
            if response and response.text:
                return response.text.strip()
            else:
                print("❌ Aucune réponse reçue de Gemini")
                return None
                
        except Exception as e:
            print(f"❌ Erreur lors de la transformation : {e}")
            return None
    
    def create_enhanced_prompt(self, technical_prompt: str) -> str:
        """
        Améliore le prompt technique avec des instructions supplémentaires
        
        Args:
            technical_prompt (str): Prompt technique de base
            
        Returns:
            str: Prompt amélioré avec instructions complètes
        """
        
        # NOTE IMPORTANTE : Ce template de prompt est appliqué *après* la transformation initiale.
        # Il doit donc renforcer les instructions clés.
        enhanced_prompt = f"""
{technical_prompt}

INSTRUCTIONS TECHNIQUES SUPPLÉMENTAIRES FINALES POUR LA GÉNÉRATION DE CODE :
- Génère un code HTML complet et fonctionnel (incluant `<!DOCTYPE html>`, `<html>`, `<head>`, `<body>`).
- Utilise les meilleures pratiques de développement web (sémantique, accessibilité, responsivité).
- Inclus des commentaires HTML/CSS pertinents pour expliquer les parties complexes ou les ajouts.
- Le code doit être prêt à être utilisé directement en ouvrant le fichier HTML.

- **TRÈS IMPORTANT CONCERNANT LE FORMAT DE SORTIE :**
  - **La réponse doit être un SEUL bloc de code HTML complet et valide.**
  - **Le CSS doit être intégré dans une balise `<style>` située dans le `<head>` du HTML.**
  - **Le JavaScript (si demandé) doit être intégré dans une balise `<script>` (idéalement à la fin du `<body>` ou dans le `<head>`).**
  - **OBLIGATOIRE : Encadre l'intégralité de cette réponse HTML (du `<!DOCTYPE html>` au `</html>`) avec les marqueurs `[CODE_START]` et `[CODE_END]`.**
  - **Ne place aucun texte, commentaire supplémentaire, ou marqueur de bloc de code Markdown (comme ` ```html`, ` ```css`, etc.) *entre* `[CODE_START]` et `[CODE_END]`. Le contenu entre ces marqueurs doit être du HTML pur et valide, prêt à être sauvegardé directement dans un fichier .html.**

FORMAT DE RÉPONSE ATTENDU (EXEMPLE TRÈS PRÉCIS) :
[CODE_START]
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Titre de la page</title>
    <style>
        /* Ton CSS intégré ici */
        body {{ font-family: sans-serif; margin: 20px; }}
        h1 {{ color: #333; text-align: center; }}
    </style>
    </head>
<body>
    <h1>Bienvenue sur ma page !</h1>
    <p>Ceci est un paragraphe d'exemple.</p>
    <script>
        // console.log("Script chargé !");
    </script>
</body>
</html>
[CODE_END]
"""
        return enhanced_prompt

# Fonction principale de transformation
def transform_user_query(user_query: str, code_context: str = "") -> Optional[str]:
    """
    Fonction principale pour transformer une requête utilisateur
    
    Args:
        user_query (str): Requête de l'utilisateur
        code_context (str): Contexte du code existant
        
    Returns:
        str: Prompt précis pour génération de code
    """
    
    # Clé API Gemini
    # Assurez-vous que cette clé est définie de manière sécurisée (ex: variables d'environnement)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyACLgVtTIE100tJx-PcdH09RfFwSFhoUe0") # Utilisez os.getenv pour une meilleure pratique
    
    # Créer le transformateur
    transformer = QueryToPromptTransformer(GEMINI_API_KEY)
    
    if not transformer.model:
        print("❌ Impossible d'initialiser le transformateur de prompt.")
        return None
    
    # Étape 1 : Transformation de base de la requête utilisateur en prompt technique
    print("🔄 Transformation de la requête utilisateur en prompt technique en cours...")
    technical_prompt = transformer.transform_query(user_query, code_context)
    
    if not technical_prompt:
        print("❌ Échec de la transformation de la requête en prompt technique.")
        return None
    
    # Étape 2 : Amélioration du prompt technique avec les instructions de formatage et de contenu final
    print("🔄 Amélioration du prompt technique avec les contraintes de format de sortie...")
    final_prompt = transformer.create_enhanced_prompt(technical_prompt)
    
    print("✅ Transformation de la requête terminée avec succès. Prompt final généré.")
    return final_prompt
