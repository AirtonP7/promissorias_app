from datetime import timedelta, date
from num2words import num2words

# ---------------------------
# Funções auxiliares
# ---------------------------
def formatar_reais(valor: float) -> str:
    """Formata o valor como moeda brasileira."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def data_extenso(d: date) -> str:
    """Retorna a data por extenso em português (manual, sem depender de locale)."""
    meses = [
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
    ]
    return f"{d.day:02d} de {meses[d.month - 1]} de {d.year}"

def valor_por_extenso(valor: float) -> str:
    """Retorna o valor por extenso em maiúsculas."""
    inteiro = int(valor)
    centavos = int(round((valor - inteiro) * 100))

    if centavos > 0:
        texto = f"{num2words(inteiro, lang='pt_BR')} reais e {num2words(centavos, lang='pt_BR')} centavos"
    else:
        texto = f"{num2words(inteiro, lang='pt_BR')} reais"

    return texto.upper()

# ---------------------------
# Gerador de promissórias
# ---------------------------
def gerar_promissorias(
    nome_devedor: str,
    valor_total: float,
    num_parcelas: int,
    data_primeira: date,
    intervalo: int,
    nome_beneficiario: str,
    cnpj_empresa: str,
    cpf_emitente: str,
    modelo_texto: str
):
    promissorias = []
    valor_parcela = valor_total / num_parcelas
    data_emissao = date.today()

    for i in range(num_parcelas):
        vencimento = data_primeira + timedelta(days=i * intervalo)

        corpo = modelo_texto
        corpo = corpo.replace("{nome_devedor}", nome_devedor)
        corpo = corpo.replace("{vencimento_extenso}", data_extenso(vencimento))
        corpo = corpo.replace("{valor_parcela_extenso}", valor_por_extenso(valor_parcela))
        corpo = corpo.replace("{nome_empresa}", nome_beneficiario)
        corpo = corpo.replace("{cnpj_empresa}", cnpj_empresa)
        corpo = corpo.replace("{cpf_emitente}", cpf_emitente)

        promissorias.append({
            "devedor": nome_devedor,
            "valor_total": formatar_reais(valor_total),
            "valor_parcela": formatar_reais(valor_parcela),
            "vencimento": vencimento.strftime("%d/%m/%Y"),
            "vencimento_extenso": data_extenso(vencimento),
            "data_emissao": data_emissao.strftime("%d/%m/%Y"),
            "emitente": nome_beneficiario,
            "cnpj_empresa": cnpj_empresa,
            "cpf_emitente": cpf_emitente,
            "corpo": corpo,
            "numero": f"{i+1}/{num_parcelas}"
        })

    return promissorias
