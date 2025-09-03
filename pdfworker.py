from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.ext import  CallbackQueryHandler, CallbackContext

from PyPDF2 import PdfReader, PdfWriter
import re
from typing import Dict



def parse_character_sheet(update, context):
    # Определение шаблонов для поиска
    patterns = {
        "Имя": r"Имя:\s*(.*)",
        "Класс и уровень": r"Класс и уровень:\s*(.*)",
        "Раса": r"Раса:\s*(.*)",
        "Черты личности": r"Черты личности:\s*([\s\S]*?)(?=\n\*\*|$)",
        "Черты характера": r"Черты характера:\s*([\s\S]*?)(?=\n\*\*|$)",
        "Предыстория": r"Предыстория:\s*([\s\S]*?)(?=\n\*\*|$)",
    }

    character = {}
    
    # Поиск по шаблонам и добавление в словарь
    for key, pattern in patterns.items():
        match = re.search(pattern, update.message.text)
        if match:
            character[key] = match.group(1).strip()

    return character








def fill_dnd_character_sheet(input_pdf: str, output_pdf: str, field_values: Dict[str, str]):
    # Открываем исходный PDF
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # Получаем страницы (для этого примера используем первые три страницы)
    pages = reader.pages[:3]
    
    # Получаем текстовые поля на каждой странице
    fields = reader.get_form_text_fields()

    # Обновляем значения в полях для всех страниц
    for key, value in field_values.items():
        if key in fields:
            fields[key] = value
    
    # Обновляем страницы с новыми значениями
    for page in pages:
        writer.add_page(page)
        writer.update_page_form_field_values(writer.pages[-1], fields)
    
    # Сохраняем результат в новый PDF
    with open(output_pdf, "wb") as f:
        writer.write(f)






field_values: Dict[str, str] = {
    'ClassLevel': "Маг 5 уровень",
    'Background': "Отшельник",
    'PlayerName': "Антон",
    'CharacterName': "Тарин Буревестник",
    'Race ': "Эльф",
    'Alignment': "Нейтрально-добрый",
    'XP': "6500",
    'Inspiration': "0",
    'STR': "0",
    'ProfBonus': "0",
    'AC': "0",
    'Initiative': "0",
    'Speed': "0",
    'PersonalityTraits ': "0",
    'STRmod': "0",
    'ST Strength': "0",
    'DEX': "0",
    'Ideals': "0",
    'DEXmod ': "0",
    'Bonds': "0",
    'CON': "0",
    'HDTotal': "0",
    'CONmod': "0",
    'HD': "0",
    'Flaws': "0",
    'INT': "0",
    'ST Dexterity': "0",
    'ST Constitution': "0",
    'ST Intelligence': "0",
    'ST Wisdom': "0",
    'ST Charisma': "0",
    'Acrobatics': "0",
    'Animal': "0",
    'Athletics': "0",
    'Deception ': "0",
    'History ': "0",
    'Wpn Name': "0",
    'Wpn1 AtkBonus': "0",
    'Wpn1 Damage': "0",
    'Insight': "0",
    'Intimidation': "0",
    'Wpn Name 2': "0",
    'Wpn2 AtkBonus ': "0",
    'Wpn Name 3': "0",
    'Wpn3 AtkBonus  ': "0",
    'INTmod': "0",
    'Wpn2 Damage ': "0",
    'Investigation ': "0",
    'WIS': "0",
    'Arcana': "0",
    'Perception ': "0",
    'WISmod': "0",
    'CHA': "0",
    'Nature': "0",
    'Performance': "0",
    'Medicine': "0",
    'Religion': "0",
    'Stealth ': "0",
    'Persuasion': "0",
    'HPMax': "0",
    'HPCurrent': "0",
    'HPTemp': "0",
    'Wpn3 Damage ': "0",
    'SleightofHand': "0",
    'CHamod': "0",
    'Survival': "0",
    'AttacksSpellcasting': "0",
    'Passive': "0",
    'CP': "0",
    'ProficienciesLang': "0",
    'SP': "0",
    'EP': "0",
    'GP': "0",
    'PP': "0",
    'Equipment': "0",
    'Features and Traits': "0",
    'CharacterName 2': "0",
    'Age': "0",
    'Height': "0",
    'Weight': "0",
    'Eyes': "0",
    'Skin': "0",
    'Hair': "0",
    'Allies': "0",
    'FactionName': "0",
    'Backstory': "0",
    'Feat+Traits': "0",
    'Treasure': "0",
    'Spellcasting Class 2': "0",
    'SpellcastingAbility 2': "0",
    'SpellSaveDC  2': "0",
    'SpellAtkBonus 2': "0",
    'SlotsTotal 19': "0",
    'SlotsRemaining 19': "0",
    'Spells 1014': "0",
    'Spells 1015': "0",
    'Spells 1016': "0",
    'Spells 1017': "0",
    'Spells 1018': "0",
    'Spells 1019': "0",
    'Spells 1020': "0",
    'Spells 1021': "0",
    'Spells 1022': "0",
    'Spells 1023': "0",
    'Spells 1024': "0",
    'Spells 1025': "0",
    'Spells 1026': "0",
    'Spells 1027': "0",
    'Spells 1028': "0",
    'Spells 1029': "0",
    'Spells 1030': "0",
    'Spells 1031': "0",
    'Spells 1032': "0",
    'Spells 1033': "0",
    'SlotsTotal 20': "0",
    'SlotsRemaining 20': "0",
    'Spells 1034': "0",
    'Spells 1035': "0",
    'Spells 1036': "0",
    'Spells 1037': "0",
    'Spells 1038': "0",
    'Spells 1039': "0",
    'Spells 1040': "0",
    'Spells 1041': "0",
    'Spells 1042': "0",
    'Spells 1043': "0",
    'Spells 1044': "0",
    'Spells 1045': "0",
    'Spells 1046': "0",
    'SlotsTotal 21': "0",
    'SlotsRemaining 21': "0",
    'Spells 1047': "0",
    'Spells 1048': "0",
    'Spells 1049': "0",
    'Spells 1050': "0",
    'Spells 1051': "0",
    'Spells 1052': "0",
    'Spells 1053': "0",
    'Spells 1054': "0",
    'Spells 1055': "0",
    'Spells 1056': "0",
    'Spells 1057': "0",
    'Spells 1058': "0",
    'Spells 1059': "0",
    'SlotsTotal 22': "0",
    'SlotsRemaining 22': "0",
    'Spells 1060': "0",
    'Spells 1061': "0",
    'Spells 1062': "0",
    'Spells 1063': "0",
    'Spells 1064': "0",
    'Spells 1065': "0",
    'Spells 1066': "0",
    'Spells 1067': "0",
    'Spells 1068': "0",
    'Spells 1069': "0",
    'Spells 1070': "0",
    'Spells 1071': "0",
    'Spells 1072': "0",
    'SlotsTotal 23': "0",
    'SlotsRemaining 23': "0",
    'Spells 1073': "0",
    'Spells 1074': "0",
    'Spells 1075': "0",
    'Spells 1076': "0",
    'Spells 1077': "0",
    'Spells 1078': "0",
    'Spells 1079': "0",
    'Spells 1080': "0",
    'Spells 1081': "0",
    'SlotsTotal 24': "0",
    'SlotsRemaining 24': "0",
    'Spells 1082': "0",
    'Spells 1083': "0",
    'Spells 1084': "0",
    'Spells 1085': "0",
    'Spells 1086': "0",
    'Spells 1087': "0",
    'Spells 1088': "0",
    'Spells 1089': "0",
    'Spells 1090': "0",
    'SlotsTotal 25': "0",
    'SlotsRemaining 25': "0",
    'Spells 1091': "0",
    'Spells 1092': "0",
    'Spells 1093': "0",
    'Spells 1094': "0",
    'Spells 1095': "0",
    'Spells 1096': "0",
    'Spells 1097': "0",
    'Spells 1098': "0",
    'Spells 1099': "0",
    'SlotsTotal 26': "0",
    'SlotsRemaining 26': "0",
    'Spells 10100': "0",
    'Spells 10101': "0",
    'Spells 10102': "0",
    'Spells 10103': "0",
    'Spells 10104': "0",
    'Spells 10105': "0",
    'Spells 10106': "0",
    'SlotsTotal 27': "0",
    'SlotsRemaining 27': "0",
    'Spells 10107': "0",
    'Spells 10108': "0",
    'Spells 10109': "0",
    'Spells 101010': "0",
    'Spells 101011': "0",
    'Spells 101012': "0",
    'Spells 101013': "0",
}

input_pdf = "DnD_5E_CharacterSheet_Form_Fillable.pdf"
output_pdf = "DnD_5E_CharacterSheet_Filled.pdf"

fill_dnd_character_sheet(input_pdf, output_pdf, field_values)

