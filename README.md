# Monitoria de Ligações Telefônicas

Este projeto realiza a monitoria de ligações telefônicas de um call center, utilizando a API da Fluxoti para obter as gravações das chamadas, o modelo Whisper para transcrição de áudios e a API da OpenAI para avaliar as ligações com uma pontuação de 0 a 100.

## Requisitos

- Python 3.6+
- Bibliotecas Python: requests, pandas, whisper, openai
- Chave de API da Fluxoti
- Chave de API da OpenAI

## Instalação

1. Clone este repositório:

```bash
git clone https://github.com/Hipolitoneto/monitoria.git
cd monitoria
```
### Crie um ambiente virtual e ative-o:

```bash
python -m venv venv
source venv/bin/activate
```
### Para Windows: 
```
venv\Scripts\activate
```
### Instale as dependências:
```
pip install -r requirements.txt
```
### Configure suas chaves de API no arquivo Main.py:
```
FLUXOTI_API_KEY = "sua_chave_de_api_fluxoti"
```
Substitua "sua_chave_de_api_fluxoti" pela sua chave de API da Fluxoti.

## Uso
Para executar o script, simplesmente execute o arquivo Main.py:
```
python Main.py
```
### O script realiza as seguintes etapas:

* Obtém a data alvo (ontem ou o sábado anterior).
* Busca os IDs das ligações da Fluxoti API.
* Baixa as gravações das ligações.
* Transcreve as gravações usando o modelo Whisper.
* Envia a transcrição para a API da OpenAI para obter uma pontuação e justificativa.
* Salva os resultados em um arquivo Excel.
* Limpa os arquivos de áudio baixados.


## Arquitetura
### O script Main.py contém as seguintes funções principais:

* get_target_date(): Obtém a data alvo para a análise.
* get_call_ids(date): Busca os IDs das ligações na API da Fluxoti.
* download_call_recording(call_id, download_path): Baixa a gravação de uma ligação.
* is_audio_file_empty(audio_file_path): Verifica se o arquivo de áudio está vazio.
* transcribe_audio(audio_file_path): Converte o áudio em texto usando o modelo Whisper.
* send_transcription_to_openai(transcription): Envia a transcrição para a OpenAI para avaliação.
* clean_downloaded_files(download_path): Remove os arquivos de áudio baixados.
* monitor_process(): Função principal que coordena todas as etapas do processo.








## Contribuição
### Se você encontrar algum problema ou tiver sugestões de melhorias, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Notas Adicionais

- Certifique-se de adicionar um arquivo `requirements.txt` com as dependências do projeto.
- Atualize o caminho `download_path` no script conforme necessário.
- Certifique-se de não incluir chaves de API sensíveis no repositório público.

