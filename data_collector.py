from config import get_week_date_range

async def collect_data_from_channel(bot, channel_id, data_extractor):
    """ Collecte et extrait les données d'un channel donné """
    channel = bot.get_channel(channel_id)
    if not channel:
        print(f"❌ Erreur : Impossible de trouver le salon {channel_id}.")
        return {}

    date_after, date_before = get_week_date_range()
    print(f"🔍 Récupération des messages entre {date_after} et {date_before} du channel {channel_id}...")

    summary_data = {}

    async for message in channel.history(limit=None, before=date_before, after=date_after, oldest_first=True):
        if message.author != bot.user and message.embeds:
            for embed in message.embeds:
                embed_data = embed.to_dict()
                extracted_data = data_extractor(embed_data)
                player = extracted_data["playerCharacter"]
                discord_id = extracted_data["playerDiscord"]

                if player:
                    if player not in summary_data:
                        summary_data[player] = {
                            "factures": 0,
                            "montant_factures": 0,
                            "missions": 0,
                            "montant_missions": 0,
                            "total_dollars": 0,
                            "playerDiscord": discord_id
                        }

                    if "montant_hors_taxe" in extracted_data and extracted_data["montant_hors_taxe"] > 0:
                        summary_data[player]["factures"] += 1
                        summary_data[player]["montant_factures"] += extracted_data["montant_hors_taxe"]

                    if "montant_mission" in extracted_data and extracted_data["montant_mission"] > 0:
                        summary_data[player]["missions"] += 1
                        summary_data[player]["montant_missions"] += extracted_data["montant_mission"]

                    summary_data[player]["total_dollars"] = (
                        summary_data[player]["montant_factures"] + summary_data[player]["montant_missions"]
                    )

    return summary_data
