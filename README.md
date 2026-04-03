# 🚗 Uber Trips Extractor

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-MIT-green)
![Maintained](https://img.shields.io/badge/maintained-yes-brightgreen)

Script para extrair, processar e exportar viagens da Uber para Excel, permitindo análises personalizadas.

---

## 📦 Funcionalidades

- 🔐 Autenticação via cookies
- 📅 Busca de viagens por mês/ano
- 📄 Conversão para DataFrame (Pandas)
- 📊 Exportação para Excel
- 🔎 Filtros personalizados

---

## ⚙️ Pré-requisitos

- Python 3.10+
- pip

```bash
pip install pandas openpyxl
```

---

## 🔑 Como pegar o cURL no navegador (PASSO A PASSO)

### 🧭 Chrome / Edge / Firefox

1. Acesse a Uber e faça login  
2. Pressione **F12**  
3. Vá em **Network (Rede)**  
4. Clique em **Fetch/XHR** (opcional)  
5. Aperte **F5** para recarregar  
6. Clique em uma requisição (ex: *graphql*, *activities*)  
7. Botão direito → **Copy → Copy as cURL**

---


---

## 🔄 Converter o cURL

```python
from app.curl.converter import CurlConverterUber

CurlConverterUber(curl="SEU_CURL_AQUI").convert_to_data()
```

Gera:

```
data/session.json
```

---

## 🚀 Como usar

```python
from time import sleep
import pandas as pd

from app.client.uber_client import UberClient
from app.parsers.dict_parser import trip_to_dict
from app.logging import logger

uber_client = UberClient()

riders = uber_client.get_activities(ano=2026, mes=4)

trips = []

for i, rider in enumerate(riders):
    logger.info(f"Buscando viagem: {i} de {len(riders)}")

    trip = uber_client.get_trip(trip_id=rider)
    trips.append(trip)

    sleep(1)

df = pd.DataFrame(trip_to_dict(trip) for trip in trips)

df.to_excel("data/uber.xlsx", index=False)
```

---

## 📊 Filtros

### ✅ Apenas concluídas

```python
df = df[df["status"] == "COMPLETED"]
```

### 👤 Por pessoa

```python
felipe = df[df["pagamento"].str.contains("Felipe")]
felipe.to_excel("data/felipe.xlsx", index=False)
```

### 📍 Por localização

```python
academia = df[
    df["origem"].str.contains("Irajá") |
    df["destino"].str.contains("Irajá")
]

academia.to_excel("data/academia.xlsx", index=False)
```

---

## 📁 Estrutura

```
project/
├── app/
├── data/
│   ├── session.json
│   ├── uber.xlsx
│   ├── felipe.xlsx
│   └── academia.xlsx
```

---

## ⚠️ Cuidados

- 🔒 Não compartilhe `session.json`
- ⏳ Sessão expira
- 🛑 Use `sleep` para evitar bloqueio
- 🌐 Pode haver validação por IP/User-Agent

---

## 💡 Melhorias futuras

- CLI (`--mes`, `--ano`)
- Dashboard
- API com FastAPI
- Automação de login

---

## 📄 Licença

MIT