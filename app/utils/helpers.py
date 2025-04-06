from datetime import date

def format_date(date_obj: date) -> str:
    """
    Formata uma data no formato DD/MM/YYYY.
    Retorna 'Não informado' se a data for None.
    """
    return date_obj.strftime("%d/%m/%Y") if date_obj else "Não informado"