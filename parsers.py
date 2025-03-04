import re

def extract_facture_data(embed_data):
    player_character = None
    player_discord = None
    montant_hors_taxe = 0

    if "fields" in embed_data:
        for field in embed_data["fields"]:
            if field["name"] == "playerCharacter":
                player_character = field["value"]
            if field["name"] == "playerDiscord":
                player_discord = field["value"]

    description = embed_data.get("description", "")
    montant_match = re.search(r"facture de (\d+)", description)
    taxe_match = re.search(r"taxes (\d+)%", description)

    if montant_match:
        montant_total = int(montant_match.group(1))
        taux_taxe = int(taxe_match.group(1)) if taxe_match else 0
        montant_hors_taxe = int((montant_total / (1 + taux_taxe / 100)) / 2) if taux_taxe else int(montant_total / 2)

    return {
        "playerCharacter": player_character,
        "playerDiscord": player_discord,
        "montant_hors_taxe": montant_hors_taxe
    }

def extract_mission_data(embed_data):
    """ Extrait les informations des missions """
    player_character = None
    player_discord = None
    montant_mission = 0

    if "fields" in embed_data:
        for field in embed_data["fields"]:
            if field["name"] == "playerCharacter":
                player_character = field["value"]
            if field["name"] == "playerDiscord":
                player_discord = field["value"]

    description = embed_data.get("description", "")
    montant_match = re.search(r"\((\d+)\$", description)

    if montant_match:
        montant_mission = int(montant_match.group(1))

    return {
        "playerCharacter": player_character,
        "playerDiscord": player_discord,
        "montant_mission": montant_mission
    }
