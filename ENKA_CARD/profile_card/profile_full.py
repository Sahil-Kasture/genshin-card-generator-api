import time
import asyncio
from PIL import ImageDraw, Image, ImageFont
import math
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from profile_card.src.utils.openFile import font, charter_bg, charter_icon_4, charter_icon_5, charter_icon_mask, bgProfile, info_user, banner_light, banner_mask, ram_avatar, avatar_user_bg, avatar_user_mask
from profile_card.src.utils.FunctionsPill import imagSize, imgD
from enkanetwork import EnkaNetworkAPI, Assets
from profile_card.src.utils.translation import translationLang

# Helper: drawText
async def drawText(text):
    line = []
    lineText = ""
    if len(text) > 13:
        for key in text.split():
            lineText += f"{key} "
            if len(lineText) > 13:
                line.append(lineText)
                lineText = ""
        line.append(lineText)
        return "\n ".join(line[:3])
    else:
        return text

# Helper: avatar
async def avatar(fullBg, player):
    picturesProfile = await imagSize(link=player.avatar.icon.url, fixed_width=159)
    avatar_bg = avatar_user_bg.copy()
    avatar_bg.alpha_composite(picturesProfile, (0, 0))
    avatar_bg = avatar_bg.resize((159, 159))
    fullBg.paste(avatar_bg, (475, 25), avatar_user_mask)
    fullBg.alpha_composite(ram_avatar, (475, 25))
    return fullBg

# Helper: nameCard
async def nameCard(player, fullBg):
    if player.namecard.navbar.url == "https://enka.network/ui/.png":
        # Fallback/default image path may need to be adjusted
        raise NotImplementedError("DEFAULT namecard image not implemented in this extraction.")
    else:
        bannerUserNamecard = await imgD(link=player.namecard.banner.url)
    bannerUserNamecard = bannerUserNamecard.transpose(Image.FLIP_LEFT_RIGHT)
    bannerUserNamecard = bannerUserNamecard.rotate(90, expand=True)
    bannerUserNamecard = bannerUserNamecard.resize((194, 327))
    fullBg.paste(bannerUserNamecard, (26, 0), banner_mask.convert("L"))
    fullBg.alpha_composite(banner_light, (26, 0))
    return fullBg

# Helper: usersInfo
async def usersInfo(player, lang, hide, uid):
    fullBg = bgProfile.copy().convert("RGBA")
    bg = info_user.copy()
    d = ImageDraw.Draw(bg)
    t20 = ImageFont.truetype(font, 20)
    t14 = ImageFont.truetype(font, 14)
    bbox = t20.getbbox(player.nickname)
    xx, y = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text((int(109 - xx / 2), 43), str(player.nickname), font=t20, fill=(255, 255, 255, 255))
    d.text((330, 10), f"{lang['WL']}:", font=t20, fill=(255, 255, 255, 255))
    d.text((371, 10), str(player.world_level), font=t20, fill=(203, 75, 75, 255))
    d.text((348, 47), f"{lang['AR']}:", font=t20, fill=(255, 255, 255, 255))
    d.text((388, 47), str(player.level), font=t20, fill=(203, 75, 75, 255))
    bbox = t14.getbbox(lang['AB'])
    xx, y = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text((349, 84), f"{lang['AB']}:", font=t14, fill=(255, 255, 255, 255))
    d.text((349 + xx + 10, 84), f"{player.abyss_floor}-{player.abyss_room}", font=t14, fill=(203, 75, 75, 255))
    bbox = t14.getbbox(lang['AC'])
    xx, y = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text((336, 114), f"{lang['AC']}:", font=t14, fill=(255, 255, 255, 255))
    d.text((336 + xx + 10, 115), str(player.achievement), font=t14, fill=(203, 75, 75, 255))
    if hide:
        d.text((70, 10), "UID:", font=t14, fill=(255, 255, 255, 255))
        d.text((106, 10), "Hidden", font=t14, fill=(203, 75, 75, 255))
    else:
        d.text((70, 10), "UID:", font=t14, fill=(255, 255, 255, 255))
        d.text((108, 10), str(uid), font=t14, fill=(203, 75, 75, 255))
    signature = player.signature
    result = await drawText(signature)
    d.multiline_text((23, 85), result, font=t14, fill=(255, 255, 255, 255))
    fullBg.alpha_composite(bg, (285, 26))
    fullBg = await avatar(fullBg, player)
    return await nameCard(player, fullBg)

# Helper: charactersTwo
async def charactersTwo(player, assets, image):
    t12 = ImageFont.truetype(font, 11)
    result = []
    charterList = {}
    charactersArg = ""
    for key in player:
        charter_bg_img = charter_bg.copy()
        person = assets.character(key.id)
        nameCharter = key.name
        nameCharters = key.icon.filename.split("Costume")[0].split("AvatarIcon_")[1]
        if nameCharters in ["PlayerGirl", "PlayerBoy"]:
            linkImgCard = "https://api.ambr.top/assets/UI/namecard/UI_NameCardPic_0_P.png"
        else:
            linkImgCard = f"https://enka.network/ui/UI_NameCardPic_{nameCharters}_P.png"
        try:
            banner = await imagSize(link=linkImgCard, size=(130, 57))
        except:
            try:
                linkImgCard = f"https://enka.network/ui/UI_NameCardPic_{nameCharters}1_P.png"
                banner = await imagSize(link=linkImgCard, size=(130, 57))
            except:
                banner = None
        charter_icon_mask_img = charter_icon_mask
        if not key.name in charterList:
            charterList[key.name] = {"rarity": person.rarity, "image": key.icon.url, "element": key.element.value, "id": key.id}
            charactersArg += f"{key.name},"
        if image:
            if person.rarity == 4:
                iconCharter = charter_icon_4.copy()
            else:
                iconCharter = charter_icon_5.copy()
            iconsCharterImg = await imagSize(link=key.icon.url, fixed_width=71)
            lvlCharter = str(key.level)
            iconCharters = Image.composite(iconCharter, iconsCharterImg, charter_icon_mask_img.convert("L"))
            if banner:
                if banner.mode != charter_bg_img.mode:
                    banner = banner.convert(charter_bg_img.mode)
                if banner.size != charter_bg_img.size:
                    banner = banner.resize((130, 57))
                charter_bg_img.alpha_composite(banner, (32, 11))
            charter_bg_img.alpha_composite(iconCharter, (0, 5))
            # Ensure iconCharters is same mode and size as charter_bg_img before alpha_composite
            if iconCharters.mode != charter_bg_img.mode:
                iconCharters = iconCharters.convert(charter_bg_img.mode)
            if iconCharters.size != charter_bg_img.size:
                # Place iconCharters at (0,5) on a blank image of charter_bg_img size
                temp = Image.new(charter_bg_img.mode, charter_bg_img.size, (0,0,0,0))
                temp.paste(iconCharters, (0,5), iconCharters)
                iconCharters = temp
            charter_bg_img.alpha_composite(iconCharters, (0, 0))
            bbox = t12.getbbox(nameCharter)
            xx, y = bbox[2] - bbox[0], bbox[3] - bbox[1]
            d = ImageDraw.Draw(charter_bg_img)
            d.text((int(111 - xx / 2), -1), nameCharter, font=t12, fill=(255, 255, 255, 255))
            d.text((26, 69), lvlCharter, font=t12, fill=(0, 0, 0, 255))
            d.text((27, 69), lvlCharter, font=t12, fill=(255, 255, 255, 255))
            result.append(charter_bg_img)
    return {"r": result, "c": charterList, "ca": charactersArg}

# Main extraction: profile_template2
async def profile_template2(player, lang, hide, uid, assets, image=True):
    """
    Generate a profile card (template 2) for a player.
    Args:
        player: The player object (must have .nickname, .world_level, .level, .abyss_floor, .abyss_room, .achievement, .signature, .avatar, .namecard, .characters_preview)
        lang: Translation dictionary with keys 'WL', 'AR', 'AB', 'AC'
        hide: Whether to hide the UID
        uid: The user's UID
        assets: The assets object (must have .character method)
        image: Whether to include character images (default True)
    Returns:
        dict: {"characters": ..., "charactersArg": ..., "img": <PIL.Image>, "performed": <float>}
    """
    start = time.time()
    # Run usersInfo and charactersTwo in parallel
    task = [usersInfo(player, lang, hide, uid), charactersTwo(player.characters_preview, assets, image)]
    it = await asyncio.gather(*task)
    fullBg = it[0]
    charactersListImage, charactersList, charactersArg = it[1]["r"], it[1]["c"], it[1]["ca"]
    positions = [
        (265, 201), (448, 201), (641, 201),
        (265, 305), (448, 305), (641, 305),
        (369, 400), (552, 400)
    ]
    i = 0
    for key in charactersListImage:
        if i >= len(positions):
            break
        fullBg.alpha_composite(key, positions[i])
        i += 1
    return {"characters": charactersList, "charactersArg": charactersArg, "img": fullBg, "performed": float('{:.2f}'.format(time.time() - start))}

async def profile_template2_full(player, lang, hide, uid, assets, image=True):
    """
    Generate a profile card (template 2) for a player, showing ALL characters in a grid (like my.jpg), scaled to fit the red container at the bottom right.
    """
    start = time.time()
    # Run usersInfo and charactersTwo in parallel
    task = [usersInfo(player, lang, hide, uid), charactersTwo(player.characters_preview, assets, image)]
    it = await asyncio.gather(*task)
    fullBg = it[0]
    charactersListImage, charactersList, charactersArg = it[1]["r"], it[1]["c"], it[1]["ca"]

    # Red container position and size 
    container_x = 210  # left edge of red box
    container_y = 180  # top edge of red box
    container_w = 600  # width of red box
    container_h = 300  # height of red box

    # Layout: 4 columns per row, dynamic rows
    num_chars = len(charactersListImage)
    cols = 4
    rows = math.ceil(num_chars / cols)
    # Scale each card to 0.8 
    orig_card_w, orig_card_h = charactersListImage[0].size
    scale = 0.8
    card_w, card_h = int(orig_card_w * scale), int(orig_card_h * scale)
    
    x_spacing = 15
    y_spacing = 40

    # x_spacing = (container_w - (card_w * cols)) // (cols - 1) if cols > 1 else 0
    # y_spacing = (container_h - (card_h * rows)) // (rows - 1) if rows > 1 else 0

    # Top-left of grid inside container
    x0 = container_x + 44
    y0 = container_y + 30

    # Resize all cards
    scaled_cards = [img.resize((card_w, card_h), Image.LANCZOS) for img in charactersListImage]

    # Place all character cards inside the container
    for idx, card in enumerate(scaled_cards):
        row = idx // cols
        col = idx % cols
        x = x0 + col * (card_w + x_spacing)
        y = y0 + row * (card_h + y_spacing)
        fullBg.alpha_composite(card, (x, y))

    return {"characters": charactersList, "charactersArg": charactersArg, "img": fullBg, "performed": float('{:.2f}'.format(time.time() - start))}
