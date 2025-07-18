# main.py
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Assistant_Dux import AssistantDux 

app = FastAPI(
    title="Assistant Dux API",
    description="API pour l'Assistant Dux de modification de code web",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")

class UserQuery(BaseModel):
    user_query: str
    target_file_path: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# main.py

# ... (le code précédent est inchangé) ...

@app.post("/modify")
async def modify_code(query_data: UserQuery):
    user_query = query_data.user_query
    target_file_path = query_data.target_file_path

    if not user_query or not target_file_path:
        raise HTTPException(status_code=400, detail="La requête utilisateur et le chemin du fichier cible sont requis.")

    print(f"Requête reçue : '{user_query}' pour le fichier : '{target_file_path}'")

    try:
        dux = AssistantDux(default_page_file=target_file_path)
        dux.create_file_if_not_exists(target_file_path)

        modification_result = dux.process_user_request(user_query, target_file=target_file_path)

        print(f"Résultat de process_user_request : {modification_result}") # Laissez cette ligne pour référence de débogage

        # Vérification et adaptation du format de la réponse
        # Nous allons utiliser 'final_message' si elle existe, sinon 'message', sinon une erreur générique
        
        # Vérification du succès (la clé 'success' est bien présente à la racine)
        success_status = modification_result.get("success", False) 
        
        # Récupération du message : on préfère 'final_message', sinon 'message', sinon un message par défaut
        response_message = modification_result.get("final_message") 
        if response_message is None: # Si 'final_message' n'existe pas
            response_message = modification_result.get("message", "Opération terminée sans message spécifique.")

        # Si le succès est False et qu'il n'y a pas de message détaillé, on peut ajouter une information
        if not success_status and response_message == "Opération terminée sans message spécifique.":
             response_message = "Échec de l'opération. Voir les logs du serveur pour plus de détails."

        updated_file_content = ""
        if os.path.exists(target_file_path):
            with open(target_file_path, 'r', encoding='utf-8') as f:
                updated_file_content = f.read()

        return JSONResponse(content={
            "success": success_status,
            "message": response_message, # <-- C'est ici que le changement a été fait !
            "updated_code": updated_file_content 
        })

    except Exception as e:
        print(f"Erreur interne imprévue lors de la modification du code : {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur lors de la modification du code : {e}")

@app.get("/get-file-content")
async def get_file_content(file_path: str):
    if not file_path:
        raise HTTPException(status_code=400, detail="Le chemin du fichier est requis.")
    
    if not os.path.exists(file_path):
        return JSONResponse(content={"error": "Le fichier n'existe pas.", "content": ""}, status_code=404)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return JSONResponse(content={"content": content})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la lecture du fichier : {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)