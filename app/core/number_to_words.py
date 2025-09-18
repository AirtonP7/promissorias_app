from num2words import num2words
import locale
from datetime import date

# Garante que estamos usando português
locale.setlocale(locale.LC_TIME, "pt_BR.utf8")

def numero_para_extenso(valor: float) -> str:
    """Converte valor numérico em reais para extenso."""
    reais = int(valor)
    centavos = int(round((valor - reais) * 100))

    if centavos > 0:
        return f"{num2words(reais, lang='pt_BR')} reais e {num2words(centavos, lang='pt_BR')} centavos"
    else:
        return f"{num2words(reais, lang='pt_BR')} reais"

def data_para_extenso(d: date) -> str:
    """Converte uma data em extenso (ex: 11 de setembro de 2025)."""
    return d.strftime("%d de %B de %Y")
