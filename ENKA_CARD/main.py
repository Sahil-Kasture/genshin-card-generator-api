import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
from enkanetwork import EnkaNetworkAPI, Language, Assets
from ENKA_CARD.character_card.generator import generate_image
from profile_card.profile_full import profile_template2_full
from profile_card.src.utils.translation import translationLang
import fastapi
from fastapi import HTTPException
from fastapi.responses import Response
import io
import uvicorn

enka_session = EnkaNetworkAPI(lang=Language.EN)

app = fastapi.FastAPI(title="Genshin Card Generator API", version="1.0.0")

async def update():
    try:    
        await enka_session.update_assets()
        return {"message": "Update successful"}
    except Exception as e:
        print(f"Update error: {e}")
        return {"message": "Update failed"}

@app.get("/update")
async def update_endpoint():
    """Manual update endpoint that can be called while server is live"""
    return await update()

@app.get("/")
@app.head("/")
async def root():
    return {"message": "Genshin Card Generator API is running!"}

@app.get("/character_card/{uid}/{character_id}")
async def character_card2(uid: str, character_id: int):
    try:
        async with EnkaNetworkAPI(lang=Language.EN) as client:
            data = await client.fetch_user(int(uid))
            if not data.characters or len(data.characters) < 3:
                raise HTTPException(status_code=404, detail="Character not found")
            character = data.characters[character_id]
            img = generate_image(data=data, character=character)
            
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            return Response(content=img_byte_arr, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating character card: {str(e)}")

@app.get("/profile_card/{uid}")
async def profile_card(uid: str):
    try:
        lang_code = "en"
        hide = False
        assets = Assets(lang=lang_code)
        lang_dict = translationLang[lang_code]
        
        async with EnkaNetworkAPI(lang=lang_code) as client:
            data = await client.fetch_user(uid)
            player = data.player
            result = await profile_template2_full(player, lang_dict, hide, uid, assets, image=True)
            
            img_byte_arr = io.BytesIO()
            result["img"].save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            return Response(content=img_byte_arr, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating profile card: {str(e)}")


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    
    print("Starting Genshin Card Generator API...")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
        
