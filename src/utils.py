#gmail
from email.message import EmailMessage
import smtplib

##google sheets
import pandas as pd
import pygsheets
from datetime import datetime

##whatsapp 
from heyoo import WhatsApp

#openai
from openai import OpenAI
from time import sleep
import json

##Obtener el api key
from dotenv import load_dotenv
import os
load_dotenv()

##credenciales
APP_PASSWORD_GMAIL=os.getenv("APP_PASSWORD_GMAIL")
CORREO_REMITENTE=os.getenv("EMAIL_REMITENTE")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
WHATSAPP_API_TOKEN=os.getenv("WHATSAPP_API_TOKEN")
PHONE_NUMBER_ID=os.getenv("PHONE_NUMBER_ID")
GOOGLE_SHEETS_ID= os.getenv("GOOGLE_SHEETS_ID")


client = OpenAI(api_key=OPENAI_API_KEY) 


#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#------------------------------------------------ conexion a email ----------------------------------------------------
def enviar_correo(nombre_lead,correo_lead,mensaje_para_lead):
  try:
    remitente = "kevin.inofuente.colque@gmail.com" #host
    destinatario = correo_lead
    mensaje = mensaje_para_lead

    email = EmailMessage()
    email["From"] = remitente
    email["To"] = destinatario
    email["Subject"] = "Mensaje Importante de Datapath para ti " + nombre_lead
    email.set_content(mensaje)
    smtp = smtplib.SMTP_SSL("smtp.gmail.com")
    print(APP_PASSWORD_GMAIL)
    smtp.login(remitente, APP_PASSWORD_GMAIL)
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()
    return True
  except Exception as e:
    print(e)
    return False

#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#-------------------------------------------- conexion a google sheets ------------------------------------------------
def registrar_google_sheets(nombre,correo,numero_tel,programa):
  ##obtener los datos de google sheets
  sheet_id=GOOGLE_SHEETS_ID
  sheet_name="Interesados"
  url=f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

  ##añadimos el nuevo registro al dataframe
  df=pd.read_csv(url)
  print(df)

  
###................................ mm
###...........................................................................................................
  ### ....................... index para los casos

  # Obtener año actual
  año_actual = datetime.now().year

  # Calcular el siguiente número consecutivo
  existentes = df.iloc[:, 0].dropna()  # Primera columna (asume que ahí está el ID)
  numeros = []

  for valor in existentes:
      try:
          if isinstance(valor, str) and valor.startswith("AI-") and valor.endswith(str(año_actual)):
              numero = int(valor.split("-")[1])
              numeros.append(numero)
      except:
          continue
  siguiente_num = max(numeros) + 1 if numeros else 1
  id_generado = f"AI-{siguiente_num:03d}-{año_actual}"

  ### ..........................................................................................................

### ............................... mm
  

  df.loc[len(df.index)] = ['123',nombre,correo,programa]
  print(df)

  try:
    ##luego cargamos a google sheets
    service_account_path='src/datapath-ai-8-mod-2-d328fbf1fb4b.json'
    gc = pygsheets.authorize(service_file=service_account_path)

    #open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
    sh = gc.open_by_url(url)

    #select the first sheet
    wks = sh[0]
    #update the first sheet with df, starting at cell B2.
    wks.set_dataframe(df,(1,1))
    return True
  except Exception as e:
    print(e)
    return False

#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#------------------------------------------- enviar mensaje por whatsapp ----------------------------------------------
def enviar_whatsapp(numero_whatsapp_asesor,mensaje_asesor):
  #conexion a whatsapp
  """para enviar mensajea a whatsaap"""
  try:
    messenger = WhatsApp(WHATSAPP_API_TOKEN, ## TOKEN
                        phone_number_id=PHONE_NUMBER_ID #ID_NUMBER
                        )
    # For sending a Text messages
    messenger.send_message(mensaje_asesor, numero_whatsapp_asesor)
    return True
  except:
    return False

#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
## Ejecutar el RUN
def run_excecuter(run):
  while True:

    run_status=client.beta.threads.runs.retrieve(
        thread_id=run.thread_id,
        run_id=run.id
    )

    if run_status.status =="completed":
      print("accion terminada")
      break


    elif run_status.status=="requires_action":
      print("requiere accion")

      list_of_actions=run_status.required_action.submit_tool_outputs.tool_calls

      print("-----"*20)
      print(list_of_actions)
      print("-----"*20)

      tools_output_list=[] # guardo las salidas de las funciones/tools

      for accion in list_of_actions:

        if accion.function.name =="registrar_google_sheets":

          nombre=accion.function.name
          argumentos=json.loads(accion.function.arguments)


          print("Nombre de la funcion a ejecutar: ", nombre)
          print("Argumentos de la función: ", argumentos)

          interesado_agregado=registrar_google_sheets(argumentos["nombre_lead"],argumentos["correo_lead"],argumentos["celular_lead"],argumentos["producto_de_interes"])

          tools_output_list.append(
              {
                  "tool_call_id": accion.id,
                  "output": str(interesado_agregado)
              }
          )

        elif accion.function.name =="enviar_correo":

          nombre=accion.function.name
          argumentos=json.loads(accion.function.arguments)


          print("Nombre de la funcion a ejecutar: ", nombre)
          print("Argumentos de la funcion: ", argumentos)

          correo_enviado=enviar_correo(argumentos["nombre_lead"],argumentos["correo_lead"],argumentos["mensaje_para_lead"])

          tools_output_list.append(
              {
                  "tool_call_id": accion.id,
                  "output": str(correo_enviado)
              }
          )

        elif accion.function.name =="enviar_whatsapp":


          nombre=accion.function.name
          argumentos=json.loads(accion.function.arguments)


          print("Nombre de la funcion a ejecutar: ", nombre)
          print("Argumentos de la funcion: ", argumentos)

          whatsapp_enviado=enviar_whatsapp(numero_whatsapp_asesor=argumentos["numero_whatsapp_asesor"],mensaje_asesor=argumentos["mensaje_asesor"])

          tools_output_list.append(
              {
                  "tool_call_id": accion.id,
                  "output": str(whatsapp_enviado)
              }
          )

        else:
          return "No se encontró la accion"


      print("ejecucion de acciones ha terminado")
      print(tools_output_list)
      client.beta.threads.runs.submit_tool_outputs(
          thread_id=run.thread_id,
          run_id=run.id,
          tool_outputs=tools_output_list
      )


    else:
      print("Esperando respuesta del Asistente")
      sleep(3)


#if __name__=="__main__":
#  enviar_correo(correo_lead="kevin.inofuente.colque.27@gmail.com",mensaje_para_lead="hola", nombre_lead="kevin")