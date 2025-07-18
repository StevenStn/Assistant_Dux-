import google.generativeai as genai
import os
from typing import Optional

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
        
        # Template de prompt amélioré pour maintenir la qualité et l'intégrité du design de la page tout en le modifiant de manière fluide
        enhanced_prompt = f"""
Tu es un expert en développement web avec une maîtrise avancée de HTML, CSS et JavaScript. 
Tu dois respecter les meilleures pratiques de développement, en préservant la structure, l'accessibilité et la performance du code, tout en répondant précisément à la demande de l'utilisateur.

MISSION : Adapter et modifier le code de la page web existante tout en conservant son style de base. 
Chaque modification doit respecter les éléments suivants :
1. **Préservation du style de base** : Le style actuel de la page doit être conservé dans la mesure du possible. Les modifications doivent être effectuées de manière à maintenir l’harmonie du design global.
2. **Progression dans l'adaptation** : Les modifications doivent être réalisées de manière progressive, en adaptant le design de la page selon la requête utilisateur tout en gardant une cohérence visuelle.
3. **Responsivité et accessibilité** : Le code généré doit être responsive, et doit respecter les normes d'accessibilité (par exemple, les contrastes de couleur, les balises HTML sémantiques, les ARIA attributes).
4. **Optimisation de la performance** : Assure-toi que les modifications ne nuisent pas aux performances de la page. Évite les lourdes images ou les scripts inutiles qui ralentiraient le chargement de la page.
5. **Commentaires de code** : Ajoute des commentaires détaillés pour expliquer chaque modification, surtout pour les parties complexes du code. Sois précis dans la description des raisons derrière chaque modification.
6. **Séparation claire des éléments CSS et JavaScript** : Si tu ajoutes des styles ou des scripts JavaScript, veille à ce qu'ils soient placés de manière ordonnée dans le code. Utilise les balises `<style>` dans le `<head>` pour le CSS et les balises `<script>` avant la fermeture du `<body>` pour le JavaScript.

INSTRUCTIONS TECHNIQUES REÇUES :
{user_query}

CODE EXISTANT À MODIFIER :
{code_context if code_context else "Aucun code existant - Créer depuis zéro"}

RÈGLES IMPORTANTES :
1. **Génération du code HTML/CSS/JS complet** : Assure-toi de générer un code HTML complet, avec tous les éléments nécessaires et une mise en page correcte.
2. **Encapsulation des modifications dans les balises [CODE_START] et [CODE_END]** : Ton code doit être entièrement encadré par ces balises. Ne mets rien d'autre à l'intérieur de ces balises que le code HTML.
3. **Séparation du CSS et du JavaScript** : Si des styles ou des scripts sont ajoutés, ils doivent être intégrés dans la structure HTML appropriée, en respectant les conventions de développement.

STRUCTURE DE RÉPONSE ATTENDUE :
- **Brève explication** : Commence par une explication claire de ce que tu vas faire (exemple : "Je vais ajouter un bouton centré avec une couleur de fond rouge et du texte blanc").
- **Le code complet** : Fournis le code HTML généré, en respectant les règles et la structure demandée.
- **Explication des modifications** : Fournis des commentaires dans le code expliquant pourquoi chaque changement a été effectué et quel est l'impact de ces changements sur la page.

Génère maintenant le code selon ces spécifications :
"""
        return enhanced_prompt
