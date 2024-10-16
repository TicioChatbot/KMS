from flask import render_template, redirect, url_for, session, request
from app import app
from app.google_auth import get_credentials, authorize, auth_callback
import googleapiclient.discovery

@app.route('/')
def index():
    if 'credentials' not in session:
        return redirect(url_for('authorize'))

    credentials = get_credentials()
    service = googleapiclient.discovery.build('drive', 'v3', credentials=credentials)
    results = service.files().list(pageSize=10).execute()
    items = results.get('files', [])

    return render_template('index.html', files=items)

@app.route('/authorize')
def authorize_route():
    return authorize()

@app.route('/auth_callback')
def auth_callback_route():
    return auth_callback()

@app.route('/projects')
def projects():
    # Lógica para mostrar proyectos
    projects = get_projects()  # Simulamos obtener proyectos
    return render_template('projects.html', projects=projects)

@app.route('/urgent_matters')
def urgent_matters():
    urgent_files = get_urgent_files()  # Simulación de obtener archivos urgentes
    return render_template('urgent_matters.html', urgent_files=urgent_files)

@app.route('/documents/upload', methods=['POST'])
def upload_document():
    file = request.files['file']
    credentials = get_credentials()
    service = googleapiclient.discovery.build('drive', 'v3', credentials=credentials)
    
    file_metadata = {'name': file.filename}
    media = MediaFileUpload(file.filename, mimetype=file.mimetype)
    
    service.files().create(body=file_metadata, media_body=media).execute()
    return redirect(url_for('index'))

@app.route('/documents/delete', methods=['POST'])
def delete_document():
    document_id = request.form['document_id']
    credentials = get_credentials()
    service = googleapiclient.discovery.build('drive', 'v3', credentials=credentials)

    service.files().delete(fileId=document_id).execute()
    return redirect(url_for('index'))
