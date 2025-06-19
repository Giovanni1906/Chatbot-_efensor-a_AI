# Asistente Virtual de la Defensoría Universitaria - UNJBG

Este proyecto implementa un asistente conversacional impulsado por inteligencia artificial para la Defensoría Universitaria de la Universidad Nacional Jorge Basadre Grohmann (UNJBG). El asistente permite atender consultas y registrar casos de estudiantes, docentes y personal administrativo, facilitando la orientación y atención oportuna en base a la normativa vigente.

---

## ⚙️ Tecnologías utilizadas

- **Python 3.10+**
- **Streamlit** – interfaz de usuario conversacional
- **OpenAI API** – motor de IA para generación de respuestas
- **Docker** – contenedorización para despliegue en Google Cloud
- **Google Sheets API (pygsheets)** – registro automático de casos
- **Heyoo (WhatsApp API)** – notificación al defensor responsable
- **SMTP (email.message + smtplib)** – envío de confirmaciones por correo
- **dotenv** – gestión de variables sensibles

---

## 🧩 Funcionalidades principales

- ✅ Consulta conversacional basada en documentos legales institucionales (Ley Universitaria, Reglamento General, Estatuto UNJBG)
- ✅ Registro de consultas en Google Sheets mediante `pygsheets`
- ✅ Notificación automática por WhatsApp al defensor responsable (`heyoo`)
- ✅ Envío de correos personalizados al usuario que consulta
- ✅ Interfaz web simple y ligera usando Streamlit
- ✅ Contenedor Docker listo para despliegue en Cloud Run u otras plataformas

---

## 🔐 Variables de entorno

Se requiere un archivo `.env` con las siguientes claves:

```env
APP_PASSWORD_GMAIL=
EMAIL_REMITENTE=
WHATSAPP_API_TOKEN=
PHONE_NUMBER_ID=
GOOGLE_SHEETS_ID=
ASSISTANT_ID=
OPENAI_API_KEY=

---

## Autenticación con Google Sheets API

Para registrar los casos en Google Sheets, este proyecto utiliza una cuenta de servicio de Google Cloud. El acceso se realiza mediante un archivo JSON de credenciales, el cual no debe incluirse en el repositorio por motivos de seguridad. tener el archivo `datapath-ai-credenciales.json` con los siguientes datos:

```datapath-ai-credenciales.json
{
  "type": ,
  "project_id": ,
  "private_key_id": ,
  "private_key": ,
  "client_id": ,
  "auth_uri": ,
  "token_uri": ,
  "auth_provider_x509_cert_url": ,
  "client_x509_cert_url": ,
  "universe_domain": 
}

