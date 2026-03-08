from app.database.manipulations import ia_manipulations

def process_webhook_data(data:dict):
    """
    Função para processar todos os dados do nosso webhook
    """

    try:
        #Coletar infos basica 
        ia_phone = data["sender"].split("@")[0]
        ia_name = data["instance"]

        # Pesquisar em nosso database qual IA direcionar
        ia_infos = ia_manipulations.filter_ia(ia_phone)
        if not ia_infos:
            raise(Exception("IA Não localizada com esse telefone em nosso DB"))
        
        if ia_infos.status != True:
            raise(Exception(f"IA {ia_infos.nome} está desativada, interceptando mensagem"))
        
        # Extrair conteudo da mensagem
        mensage_id = data["data"]["key"]["id"]
        mensage_type = data["data"]["messageType"]
        message_content = processar_menssagem(data, ia_name, mensage_id, mensage_type, ia_infos)
        if not message_content:
            raise(Exception(f"Tipo de mensagem não foi possivel processar : {mensage_type}"))
        
        # Extraindo informações do lead
        lead_name = data["data"]["pushName"]
        lead_phone = data["data"]["key"]["remoteJid"].split("@")[0]

        print(lead_name, lead_phone, message_content)

    except Exception as ex:
        print(f"ERROR IN PROCESS: {ex}")

def processar_menssagem(data:dict, instance:str, message_id:str, message_type:str, ia_infos: object) -> str:
    if message_type == "conversation":
        return data["data"]["message"]["conversation"]
    
    elif message_type == "extendedTextMessage":
        return data["data"]["message"]["extendedTextMessage"]["text"]
    
    elif message_type == "imageMessage":
        print("Imagem detectada!")
        #return processar_imagem(instance, message_id, ia_infos)
        return "mensagem de imagem"
    
    elif message_type == "audioMessage":
        print("Áudio identificado!")
        #return processar_audio(instance, message_id, ia_infos)
        return "mensagem de audio"
    
    elif message_type == "documentWithCaptionMessage":
        print("Documento identificado!")
        type_file = data.get("data").get("message").get("documentWithCaptionMessage").get("message").get("documentMessage").get("mimetype").split("/")[1]
        #return processar_documento(instance, message_id, type_file, ia_infos), type_file
        return "mensagem de documento"
    else:
        print(f"Tipo de mensagem não identificada: {message_type} retornando...")
        return ""