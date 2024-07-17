import os
import requests
import pandas as pd
import whisper
from openai import OpenAI
from datetime import datetime, timedelta

# Configurar as chaves de API
FLUXOTI_API_KEY = "sua api key discador"

# Carregar o modelo Whisper
modelo = whisper.load_model("medium")

# Função para obter a data desejada (ontem ou sábado anterior)
def get_target_date():
    today = datetime.now()
    if today.weekday() == 0:  # Segunda-feira
        target_date = today - timedelta(days=2)  # Sábado
    else:
        target_date = today - timedelta(days=1)  # Ontem
    return target_date.strftime('%Y-%m-%d')

# Função para obter os IDs das ligações, campanha e agente
def get_call_ids(date):
    start_date = f"{date}+00:00:00"
    end_date = f"{date}+23:59:59"
    url = f"url para conseguir os id"
    headers = {
        'Authorization': f'Bearer {FLUXOTI_API_KEY}',
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    if 'data' not in data:
        print("No 'data' in API response:", data)
        return []

    calls = data['data']
    call_info = []
    for call in calls[:50]:  # Limitar a 50 chamadas
        call_id = call['id']
        campaign = call['campaign_rel']['name'] if 'campaign_rel' in call else 'N/A'
        agent = call['agent'] if 'agent' in call else 'N/A'
        number = call['number'] if 'number' in call else 'N/A'
        call_date = call['call_date'] if 'call_date' in call else 'N/A'
        call_info.append({'id': call_id, 'campaign': campaign, 'agent': agent, 'number': number, 'call_date': call_date})
    
    return call_info

# Função para obter e salvar a gravação de uma chamada
def download_call_recording(call_id, download_path):
    url = f"url para fazer o dowload por id de ligação"
    headers = {
        'Authorization': f'Bearer {FLUXOTI_API_KEY}',
        'Accept': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        audio_file_path = os.path.join(download_path, f"{call_id}.mp3")
        with open(audio_file_path, 'wb') as audio_file:
            audio_file.write(response.content)
        
        return audio_file_path
    except requests.exceptions.HTTPError as e:
        print(f"Error downloading recording for call {call_id}: {e}")
        return None

# Função para verificar se o arquivo de áudio está vazio
def is_audio_file_empty(audio_file_path):
    return os.path.getsize(audio_file_path) == 0

# Função para conversão de áudio para texto usando Whisper
def transcribe_audio(audio_file_path):
    if is_audio_file_empty(audio_file_path):
        print(f"Audio file is empty: {audio_file_path}")
        return None
    
    try:
        result = modelo.transcribe(audio_file_path)
        return result['text']
    except Exception as e:
        print(f"Error transcribing {audio_file_path}: {e}")
        return None

# Função para enviar transcrição para OpenAI
def send_transcription_to_openai(transcription):
    client = OpenAI(api_key='openai api key')

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "aqui vai o prompt de comando com as definiçõues que voce quer solicitar para o chat faça"},
            {"role": "user", "content": transcription}
        ]
    )
    corrected_text = completion.choices[0].message.content
    return corrected_text

# Função para remover arquivos de áudio baixados
def clean_downloaded_files(download_path):
    for file_name in os.listdir(download_path):
        file_path = os.path.join(download_path, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

# Função principal de monitoria
def monitor_process():
    date = get_target_date()
    call_info = get_call_ids(date)
    download_path = "caminho do dowload das ligações"
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    results = []C:/Users/Admin/Desktop/teste
    
    for call in call_info:
        call_id = call['id']
        try:
            audio_file_path = download_call_recording(call_id, download_path)
            if audio_file_path:
                transcript = transcribe_audio(audio_file_path)
                if transcript:
                    corrected_transcript = send_transcription_to_openai(transcript)
                    result = {
                        "score": corrected_transcript,
                        "numero": call['number'],
                        "agente": call['agent'],
                        "campanha": call['campaign'],
                        "data": call['call_date'],
                        "id": call_id
                    }
                    results.append(result)
                else:
                    print(f"Failed to transcribe {audio_file_path}")
            else:
                print(f"Failed to download recording for call {call_id}")
        except Exception as e:
            print(f"Error processing call {call_id}: {e}")

    # Salvar os resultados em um arquivo Excel com a data atual no nome do arquivo
    today_date = datetime.now().strftime('%Y%m%d')
    file_name = f"monitoria_{today_date}.xlsx"
    df = pd.DataFrame(results)
    df.to_excel(file_name, index=False)
    print(f"Results saved to {file_name}")

    # Limpar arquivos de áudio baixados
    clean_downloaded_files(download_path)

if __name__ == "__main__":
    monitor_process()
