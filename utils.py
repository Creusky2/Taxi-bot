def find_closest_match(target, summary_data):
    """ Trouve le joueur correspondant au mieux en insensible à la casse """
    if not target or not summary_data:
        return None

    target_lower = target.lower()
    matches = [name for name in summary_data.keys() if target_lower in name.lower()]

    return matches[0] if matches else None  # Retourne le premier match trouvé (ou None si rien)


def generate_summary_text(stats, joueur):
    """ Génère le texte de synthèse formaté pour Discord """
    return (
        f"\n👤 **{joueur}**\n"
        f"🧾 Factures envoyées : {stats['factures']} | 💰 {stats['montant_factures']} $\n"
        f"🚖 Missions complétées : {stats['missions']} | 💰 {stats['montant_missions']} $\n"
        f"💵 **Total généré : {stats['total_dollars']} $**\n"
    )
