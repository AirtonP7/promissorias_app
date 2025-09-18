def parse_template(template: str, variaveis: dict) -> str:
    """Substitui marcadores {chave} no template pelo valor em variaveis."""
    for chave, valor in variaveis.items():
        template = template.replace(f"{{{chave}}}", str(valor))
    return template
