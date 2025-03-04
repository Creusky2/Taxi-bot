import discord
from discord import app_commands
from data_collector import collect_data_from_channel
from parsers import extract_facture_data, extract_mission_data
from config import DISCORD_CHANNEL_FACTURES, DISCORD_CHANNEL_MISSIONS
from utils import find_closest_match, generate_summary_text

def setup_commands(bot):
    @bot.tree.command(name="quotas", description="Affiche le résumé des quotas d'un joueur ou de l'utilisateur actuel par défaut.")
    @app_commands.describe(joueur="Nom du joueur (ex: John Dupont)")
    async def quotas(interaction: discord.Interaction, joueur: str = None):
        """ Récupère et affiche la synthèse des quotas sur demande """

        print(f"🔍 Commande `/quotas {joueur if joueur else ''}` reçue par {interaction.user}...")

        await interaction.response.defer(ephemeral=True)

        # Collecte les données
        factures_data = await collect_data_from_channel(bot,DISCORD_CHANNEL_FACTURES, extract_facture_data)
        missions_data = await collect_data_from_channel(bot,DISCORD_CHANNEL_MISSIONS, extract_mission_data)

        # Fusionner les données
        summary_data = factures_data
        for player, data in missions_data.items():
            if player in summary_data:
                summary_data[player]["missions"] += data["missions"]
                summary_data[player]["montant_missions"] += data["montant_missions"]
                summary_data[player]["total_dollars"] += data["montant_missions"]
            else:
                summary_data[player] = data

        # Récupérer l'ID Discord de l'utilisateur exécutant la commande
        user_discord_id = str(interaction.user.id)

        # Déterminer le joueur correspondant
        joueur_match = next((p for p, data in summary_data.items() if data["playerDiscord"] == user_discord_id), None)

        # Si un nom est précisé, on cherche le match le plus proche
        if joueur:
            joueur_lower = joueur.lower()
            joueur_match = next((p for p in summary_data if joueur_lower in p.lower()), joueur_match)

        if not joueur_match:
            await interaction.followup.send("📊 Aucun quota enregistré pour cet utilisateur.", ephemeral=True)
            return

        summary_text = generate_summary_text(summary_data[joueur_match], joueur_match)
        await interaction.followup.send(summary_text, ephemeral=True)
