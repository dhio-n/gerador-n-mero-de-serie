import uuid
from datetime import datetime

def gerar_numero_serie(codigo_produto):
    timestamp_data = datetime.now().strftime("%Y%m%d")
    unique_id = uuid.uuid4().hex[:6].upper()
    return f"{codigo_produto}-{timestamp_data}-{unique_id}"
