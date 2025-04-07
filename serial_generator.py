import uuid
from datetime import datetime

def gerar_numero_serie(codigo_produto):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4().hex[:6].upper()
    return f"{codigo_produto}-{timestamp}-{unique_id}"
