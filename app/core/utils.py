def format_currency(valor: float) -> str:
    """Formata número como moeda brasileira."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_cpf(cpf: str) -> str:
    """Formata uma string como CPF (000.000.000-00)."""
    numeros = "".join(filter(str.isdigit, cpf))
    if len(numeros) != 11:
        return cpf
    return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"

def formatar_cnpj(cnpj: str) -> str:
    """Formata uma string como CNPJ (00.000.000/0000-00)."""
    numeros = "".join(filter(str.isdigit, cnpj))
    if len(numeros) != 14:
        return cnpj
    return f"{numeros[:2]}.{numeros[2:5]}.{numeros[5:8]}/{numeros[8:12]}-{numeros[12:]}"
