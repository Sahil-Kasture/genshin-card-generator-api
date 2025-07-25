import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from enkanetwork import EnkaNetworkAPI, Language, Assets
from ENKA_CARD.character_card.generator import generate_image
from enkacard  import encbanner
from profile_card.profile_full import profile_template2_full
from profile_card.src.utils.translation import translationLang


client = EnkaNetworkAPI(lang=Language.EN)

uid = '855170541'

async def local_card(uid):
    # await encbanner.update()
    async with encbanner.ENC(lang="en",uid=uid) as client:
        res=await client.creat(template=2)
        card=res.card[3]
        card=card.card
        card.show()

async def card2(uid):
    async with client:
        data = await client.fetch_user(int(uid))
        character = data.characters[2]
        img=generate_image(data=data,character=character)
        img.show()
        
async def profile(uid,client):
    async with client:
       data = await client.fetch_user(int(uid))
       lang_code = "en"
       hide = False
       assets = Assets(lang=lang_code)
       lang_dict = translationLang[lang_code]
       async with EnkaNetworkAPI(lang=lang_code) as client:
            data = await client.fetch_user(uid)
            player = data.player
            result = await profile_template2_full(player, lang_dict, hide, uid, assets, image=True)
            # Save the resulting image
            result["img"].save(f"{data.player.nickname}.png")
            print(f"Profile card generated and saved as profile2_full_output.png. Time taken: {result['performed']}s")

        
asyncio.run(local_card(uid))
asyncio.run(card2(uid))
# asyncio.run(profile(uid,client))