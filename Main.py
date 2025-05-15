# Importando as bibliotecas
import fitz
import json
import re

file = r"C:\Users\carin\OneDrive\Documentos\Willdanthê\Estácio\AnaliseDeDados\Chat2.pdf"

# Extrando Texto do Pdf
def extract_text(path):
    doc = fitz.open(path) # Armazenando o pdf
    return "\n".join([page.get_text() for page in doc]) 

def cleaning_text(text):
    clean_text = re.sub(r"Visitor ID.*", "", text, flags=re.DOTALL)
    clean_text = re.sub(r"^.*?Chat Transcript\s", "", clean_text, flags=re.DOTALL)
    return clean_text.strip()

def convert_to_censored_json(text):
    talks = []
    current_autor = None
    buffer = []

    rows = text.splitlines()

    for row in rows:
        row = row.strip()

        # Ignorando linhas vazias
        if (not row):
            continue
        
        # Ignora horários como: 5:03:56 PM
        if re.match(r"\d{1,2}:\d{2}:\d{2} [AP]M", row):
            continue

        # Ignora mensagem do sistema
        if (row.startswith("O visitante")):
            continue

        if row == "Chat Donzito":
            if (buffer and current_autor):
                talks.append({
                    "Autor" : current_autor,
                    "Mensagem" : " ".join(buffer).strip()
                })
                buffer = []

            current_autor = "chatbot"
            continue

        elif re.match(r"^[A-Z][a-z]+$", row):
            if (buffer and current_autor):
                talks.append({
                    "Autor" : current_autor,
                    "Mensagem" : " ".join(buffer).strip()
                })
                buffer = []

            current_autor = "cliente"
            continue

        buffer.append(row)
        
    if (buffer and current_autor):
        talks.append({
            "Autor" : current_autor,
            "Mensagem" : " ".join(buffer).strip()
        })
        
    return talks
def Run():
    conversa = extract_text(file)
    conversa_limpa = cleaning_text(conversa)
    
    print(json.dumps(convert_to_censored_json(conversa_limpa), indent=2, ensure_ascii=False))

    # print(conversa_limpa)
    # print(type(conversa))
    

Run()