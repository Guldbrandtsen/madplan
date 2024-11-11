import streamlit as st
import random
from collections import defaultdict

# Datasæt med måltider kategoriseret ud fra type
meal_recipes = [
    {"name": "fish and chips", "ingredients": ["torsk", "kartofler", "ærter"], "category": ["frostvarer", "grøntsager og frugt"], "type": "fisk"},
    {"name": "pasta og kødboller", "ingredients": ["pasta", "hakket oksekød", "hakkede tomater", "tomatpure"], "category": ["konserves og tørvarer", "frostvarer", "konserves og tørvarer", "konserves og tørvarer"], "type": "kød"},
    {"name": "boller i karry", "ingredients": ["hakket svinekød", "karry", "løg", "ris"], "category": ["andet", "konserves og tørvarer", "grøntsager og frugt", "konserves og tørvarer"], "type": "kød"},
    {"name": "pølsebrød", "ingredients": ["pølsebrød", "pølser", "tomater"], "category": ["brød", "andet", "grøntsager og frugt"], "type": "kød"},
    {"name": "rød karry", "ingredients": ["kylling", "rød karrypasta", "ris", "frosne grøntsager"], "category": ["andet", "konserves og tørvarer", "konserves og tørvarer", "frostvarer"], "type": "kød"},
    {"name": "blomkålssuppe", "ingredients": ["blomkål", "løg", "kikærter", "rugbrød"], "category": ["grøntsager og frugt", "grøntsager og frugt", "konserves og tørvarer", "brød"], "type": "vegetar"},
    {"name": "pasta carbonara", "ingredients": ["pasta", "æg", "parmesanost", "bacon"], "category": ["konserves og tørvarer", "mælkeprodukter", "mælkeprodukter", "andet"], "type": "kød"},
    {"name": "dahl", "ingredients": ["gule linser", "kokosmælk", "løg", "tomat"], "category": ["konserves og tørvarer", "konserves og tørvarer", "grøntsager og frugt"], "type": "vegetar"},
    {"name": "burger", "ingredients": ["burgerboller", "hakket oksekød", "rødbedebøffer", "løg", "avokado", "tomater"], "category": ["brød", "frostvarer", "grøntsager og frugt", "grøntsager og frugt", "grøntsager og frugt"], "type": "kød"},
    {"name": "rødspættefilet", "ingredients": ["rødspættefilet", "pomfritter"], "category": ["frostvarer"], "type": "fisk"},
    {"name": "tortillas-ruller", "ingredients": ["tortillas", "hakkede tomater", "gulerødder", "avokado", "revet ost"], "category": ["brød", "konserves og tørvarer", "grøntsager og frugt", "grøntsager og frugt", "mælkeprodukter"], "type": "vegetar"},
    {"name": "risengrød", "ingredients": ["sødmælk", "grødris"], "category": ["mælkeprodukter", "konserves og tørvarer"], "type": "vegetar"},
    {"name": "tomatsuppe", "ingredients": ["hakkede tomater", "tomatpure", "hvidløg", "hvidløgsflute", "gulerødder", "suppehorn"], "category": ["konserves og tørvarer", "konserves og tørvarer", "grøntsager og frugt", "frostvarer", "grøntsager og frugt", "konserves og tørvarer"], "type": "vegetar"},
    {"name": "klar suppe", "ingredients": ["frostsuppe", "hvidløgsflute"], "category": ["frostvarer", "frostvarer"], "type": "vegetar"},
    {"name": "frikadeller med bulgursalat", "ingredients": ["hakket svinekød", "bulgur", "kål", "falafler"], "category": ["frostvarer", "konserves og tørvarer", "grøntsager og frugt", "frostvarer"], "type": "kød"},
    {"name": "pasta med bacon og broccoli", "ingredients": ["pasta", "bacon", "hakkede tomater", "tomatpure", "broccoli"], "category": ["konserves og tørvarer", "andet", "konserves og tørvarer", "konserves og tørvarer", "grøntsager og frugt"], "type": "kød"},
    {"name": "madpandekager", "ingredients": ["tomater", "mel", "æg", "avokado"], "category": ["grøntsager og frugt", "mel og gryn", "mælkeprodukter", "grøntsager og frugt"], "type": "vegetar"},
    {"name": "chili sin carne", "ingredients": ["bønner", "hakkede tomater", "chili", "sorte bønner"], "category": ["konserves og tørvarer", "konserves og tørvarer", "andet", "konserves og tørvarer"], "type": "vegetar"},
    {"name": "nudelsuppe", "ingredients": ["nudler", "gulerødder", "tomater"], "category": ["konserves og tørvarer", "grøntsager og frugt", "grøntsager og frugt"], "type": "vegetar"},
    {"name": "tærte med bacon og broccolisalat", "ingredients": ["bacon", "broccoli", "tærtebund"], "category": ["andet", "grøntsager og frugt", "brød"], "type": "kød"},
    {"name": "grøntsagslasagne", "ingredients": ["lasagneplader", "hakkede tomater", "tomatpure", "gulerødder", "squash", "aubergine", "revet ost"], "category": ["konserves og tørvarer", "konserves og tørvarer", "grøntsager og frugt", "grøntsager og frugt", "grøntsager og frugt", "mælkeprodukter"], "type": "vegetar"},
    {"name": "tacos", "ingredients": ["pulled pork", "kikærter", "lime", "avokado", "majs", "løg", "tomater", "creme fraiche"], "category": ["andet", "konserves og tørvarer", "grøntsager og frugt", "grøntsager og frugt", "grøntsager og frugt", "grøntsager og frugt", "grøntsager og frugt", "mælkeprodukter"], "type": "kød"},
    {"name": "butter chicken", "ingredients": ["kylling", "hakkede tomater", "fløde", "krydderier", "hvidløg", "ingefær", "ris"], "category": ["andet", "konserves og tørvarer", "mælkeprodukter", "andet", "grøntsager og frugt", "grøntsager og frugt", "konserves og tørvarer"], "type": "kød"},
    {"name": "pizza", "ingredients": ["mozzarella", "pepperoni", "majs", "kylling", "kartofler", "mascarpone"], "category": ["mælkeprodukter", "andet", "konserves og tørvarer", "andet", "grøntsager og frugt", "mælkeprodukter"], "type": "kød"}
]

# Standardvarer med tomater tilføjet
standard_items = [
    {"name": "tomater", "default_quantity": 1, "unit": "bakke", "category": "grøntsager og frugt"},
    {"name": "agurk", "default_quantity": 1, "unit": "stk", "category": "grøntsager og frugt"},
    {"name": "peberfrugt", "default_quantity": 1, "unit": "stk", "category": "grøntsager og frugt"},
    {"name": "havregryn", "default_quantity": 1, "unit": "pakke", "category": "mel og gryn"},
    {"name": "mælk", "default_quantity": 3, "unit": "liter", "category": "mælkeprodukter"},
    {"name": "rugbrød", "default_quantity": 1, "unit": "pakke", "category": "brød"},
    {"name": "figenstænger", "default_quantity": 1, "unit": "pakke", "category": "konserves og tørvarer"},
    {"name": "rosiner", "default_quantity": 1, "unit": "pakke", "category": "mel og gryn"},
    {"name": "cheddarost", "default_quantity": 1, "unit": "stk", "category": "mælkeprodukter"},
    {"name": "æg", "default_quantity": 1, "unit": "bakke", "category": "mælkeprodukter"},
    {"name": "grove havregryn", "default_quantity": 1, "unit": "pakke", "category": "mel og gryn"},
    {"name": "havremælk", "default_quantity": 1, "unit": "liter", "category": "mælkeprodukter"},
    {"name": "boller", "default_quantity": 1, "unit": "pakke", "category": "brød"},
    {"name": "majskiks", "default_quantity": 1, "unit": "pakke", "category": "konserves og tørvarer"},
    {"name": "gær", "default_quantity": 1, "unit": "stk", "category": "mælkeprodukter"},
    {"name": "smør", "default_quantity": 1, "unit": "bakke", "category": "mælkeprodukter"},
    {"name": "spegepølse", "default_quantity": 1, "unit": "stk", "category": "andet"},
    {"name": "leverpostej", "default_quantity": 1, "unit": "stk", "category": "andet"},
    {"name": "skinke", "default_quantity": 1, "unit": "stk", "category": "andet"},
    {"name": "juice", "default_quantity": 1, "unit": "liter", "category": "mælkeprodukter"},
    {"name": "yoghurt", "default_quantity": 1, "unit": "bæger", "category": "mælkeprodukter"},
    {"name": "majs", "default_quantity": 1, "unit": "dåse", "category": "konserves og tørvarer"}
]

# Nonfoodvarer
non_food_items = [
    {"name": "toiletpapir", "category": "andet"},
    {"name": "opvaskemiddel", "category": "andet"},
    {"name": "opvasketabs", "category": "andet"},
    {"name": "vaskepulver", "category": "andet"},
    {"name": "tandpasta", "category": "andet"},
    {"name": "køkkenrulle", "category": "andet"},
    {"name": "afspændingsmiddel", "category": "andet"},
    {"name": "salt til opvaskemaskine", "category": "andet"}
]

# Ekstra valgbare varer pr. kategori
optional_items = {
    "grøntsager og frugt": ["bananer", "æbler", "appelsiner", "kiwi", "vindruer"],
    "konserves og tørvarer": ["marmelade", "mandler", "peanuts", "chips", "kaffe"],
    "mælkeprodukter": ["kærnemælk", "koldskål", "græsk yoghurt", "creme fraiche"],
    "andet": ["sild", "ristede løg", "remoulade", "ketchup", "nachos", "pålægschokolade"],
    "mel og gryn": ["chiafrø", "knækbrød", "flager", "mel"]
}

# Funktion til intelligent kategorigætning
def guess_category(item_name):
    item_name = item_name.lower()
    if "mælk" in item_name or item_name in ["yoghurt", "fløde", "ost"]:
        return "mælkeprodukter"
    elif item_name in ["kartofler", "gulerødder", "æbler", "bananer", "tomater"]:
        return "grøntsager og frugt"
    elif "mel" in item_name or "gryn" in item_name or item_name in ["pasta", "ris", "kiks", "knækbrød"]:
        return "mel og gryn"
    elif "nødder" in item_name or item_name in ["kiks", "chips", "rosiner"]:
        return "konserves og tørvarer"
    else:
        return "andet"

# Funktion til at generere en tilfældig madplan ud fra valgt antal kød-dage
def generate_meal_plan(recipes, days=4, meat_days=1):
    selected_meals = []
    meat_recipes = [recipe for recipe in recipes if recipe["type"] == "kød"]
    non_meat_recipes = [recipe for recipe in recipes if recipe["type"] != "kød"]

    selected_meals.extend(random.sample(meat_recipes, min(meat_days, len(meat_recipes))))
    selected_meals.extend(random.sample(non_meat_recipes, days - meat_days))
    random.shuffle(selected_meals)

    return selected_meals

# Funktion til at generere indkøbslisten
def generate_shopping_list(meal_plan, standard_items, additional_items, selected_non_food):
    shopping_list = defaultdict(lambda: defaultdict(int))

    # Tilføj ingredienser fra måltiderne
    for recipe in meal_plan:
        for ingredient, category in zip(recipe["ingredients"], recipe["category"]):
            shopping_list[category][ingredient] += 1

    # Tilføj standardvarer
    for item in standard_items:
        shopping_list[item["category"]][item["name"]] += item["default_quantity"]

    # Tilføj ekstra varer fra fritekstfelt
    for extra_item in additional_items:
        category = guess_category(extra_item)
        shopping_list[category][extra_item] += 1

    # Tilføj valgte nonfoodvarer
    for item in selected_non_food:
        shopping_list[item["category"]][item["name"]] += 1

    return shopping_list

# Streamlit interface
st.title("Ugentlig madplan generator")
days = st.slider("Vælg antal dage", min_value=1, max_value=7, value=4)
meat_days = st.slider("Vælg antal dage med kød", min_value=0, max_value=days, value=1)

# Generer ny madplan
if "meal_plan" not in st.session_state or st.button("Generer ny madplan"):
    st.session_state.meal_plan = generate_meal_plan(meal_recipes, days=days, meat_days=meat_days)

# Vis madplan med ingredienser i fold-ud vinduer
st.header("Ugens madplan")
selected_meals = []
for day in range(days):
    selected_meal = st.selectbox(
        f"Vælg ret til dag {day + 1}",
        options=[meal["name"].capitalize() for meal in meal_recipes],
        index=meal_recipes.index(st.session_state.meal_plan[day]),
        key=f"meal_{day}"
    )
    meal_details = next(meal for meal in meal_recipes if meal["name"].capitalize() == selected_meal)
    selected_meals.append(meal_details)

    # Folde-ud vindue for ingredienser
    with st.expander(f"Se ingredienser til {selected_meal}"):
        for ingredient in meal_details["ingredients"]:
            st.write(f"- {ingredient}")

# Tilføj ekstra varer
st.subheader("Tilføj ekstra varer til indkøbslisten")
additional_items = []
extra_item = st.text_input("Tilføj ekstra vare", key="extra_item_0")
counter = 1

# Dynamisk oprettelse af flere felter, når de udfyldes
while extra_item:
    additional_items.append(extra_item)
    extra_item = st.text_input("Tilføj ekstra vare", key=f"extra_item_{counter}")
    counter += 1

# Vælg nonfoodvarer
st.subheader("Vælg nonfoodvarer")
selected_non_food = [item for item in non_food_items if st.checkbox(item["name"], key=f"nonfood_{item['name']}")]

# Generer indkøbslisten
shopping_list = generate_shopping_list(selected_meals, standard_items, additional_items, selected_non_food)

# Vis interaktiv indkøbslisten med ekstra søjle for valgbare varer
st.header("Indkøbslisten")
final_shopping_list = {}
for category, items in shopping_list.items():
    st.subheader(category.capitalize())
    col1, col2 = st.columns(2)
    
    # Standard indkøbsliste i venstre kolonne
    with col1:
        final_shopping_list[category] = {item: quantity for item, quantity in items.items() if st.checkbox(f"{item} ({quantity})", value=True, key=f"{item}_{category}")}

    # Ekstra valgbare varer i højre kolonne
    with col2:
        for optional_item in optional_items.get(category, []):
            if st.checkbox(optional_item, key=f"optional_{optional_item}_{category}", value=False):
                final_shopping_list[category][optional_item] = 1

# Download knap for indkøbsliste og madplan
def create_shopping_list_text(shopping_list, meal_plan):
    output = "Ugens madplan:\n"
    for day, meal in enumerate(meal_plan, 1):
        output += f"Dag {day}: {meal['name'].capitalize()}\n"
    output += "\nIndkøbslisten:\n"
    for category, items in shopping_list.items():
        if items:
            output += f"{category.capitalize()}:\n" + "\n".join(f"- {item} ({quantity})" for item, quantity in items.items() if quantity > 0) + "\n"
    return output

shopping_list_text = create_shopping_list_text(final_shopping_list, selected_meals)
st.download_button(
    label="Download indkøbsliste og madplan som tekstfil",
    data=shopping_list_text,
    file_name="madplan_og_indkøbsliste.txt",
    mime="text/plain"
)
