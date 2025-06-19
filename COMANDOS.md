## iniciar para conectar con el proyecto de google cloud (tener el proyecto creado en gloogle cloud console)
gcloud init



## Paso 1: creación del repositorio
gcloud artifacts repositories create repo-chat-streamlit-defu --repository-format docker --project defu-ai-chatbot-v1 --location us-central1


### .......................................................................................
### repo de los archivos
https://github.com/KevinInoCol/deploying-with-gcr-mlops
## Crear los siguientes archivos
touch Dockerfile.prod
### Comandos:
$ touch requirements.txt
$ mkdir src
$ cd src
$ touch main.py

touch cloudbuild.yaml
touch service.yaml

### .......................................................................................
## ir cambiando la V## en los yaml (cloudbuild y service)

# Paso 2: Crear la imagen de mi APLICACION y subir al repositorio
gcloud builds submit --config=cloudbuild.yaml --project defu-ai-chatbot-v1

# Paso 3: Comando para despliegue o ejecución de la imagen en el repositorio
gcloud run services replace service.yaml --region us-central1 --project defu-ai-chatbot-v1

# Paso 4: OPCIONAL. dar permisos de acceso a mi APLICACION
touch gcr-service-policy.yaml
gcloud run services set-iam-policy sservicio-streamlit-datapath-jorge-velasquez gcr-service-policy.yaml --region us-central1 --project defu-ai-chatbot-v1