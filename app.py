from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, request, render_template, send_file, flash, send_from_directory, session
from werkzeug.utils import secure_filename
import tempfile
import shutil
from utils import process_venue_file
import uuid

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create a persistent downloads directory
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'file' not in request.files:
        flash('No file uploaded')
        return render_template('index.html', error='No file uploaded'), 400
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected')
        return render_template('index.html', error='No file selected'), 400
    
    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload an Excel file (.xlsx or .xls)')
        return render_template('index.html', error='Invalid file type'), 400
    
    try:
        # Create temporary directory for processing
        temp_dir = tempfile.mkdtemp()
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        input_path = os.path.join(temp_dir, filename)
        file.save(input_path)
        
        # Process the file
        result = process_venue_file(input_path, temp_dir)
        
        if result['success']:
            # Generate unique session ID for this upload
            session_id = str(uuid.uuid4())
            session_folder = os.path.join(DOWNLOAD_FOLDER, session_id)
            os.makedirs(session_folder, exist_ok=True)
            
            # Copy output files to persistent download folder
            excel_src = result['excel_path']
            kml_src = result['kml_path']
            excel_dst = os.path.join(session_folder, result['excel_filename'])
            kml_dst = os.path.join(session_folder, result['kml_filename'])
            
            shutil.copy2(excel_src, excel_dst)
            shutil.copy2(kml_src, kml_dst)
            
            # Clean up temp directory
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            # Store session info
            session['download_folder'] = session_id
            
            # Return result page with simplified file names
            return render_template('result.html', 
                                 excel_file=result['excel_filename'],
                                 kml_file=result['kml_filename'],
                                 session_id=session_id)
        else:
            shutil.rmtree(temp_dir, ignore_errors=True)
            return render_template('index.html', error=result['error']), 400
            
    except Exception as e:
        if 'temp_dir' in locals():
            shutil.rmtree(temp_dir, ignore_errors=True)
        return render_template('index.html', error=f'Error processing file: {str(e)}'), 500

@app.route('/download/<session_id>/<filename>')
def download(session_id, filename):
    try:
        file_path = os.path.join(DOWNLOAD_FOLDER, session_id, filename)
        
        if not os.path.exists(file_path):
            return f'Error: File not found', 404
        
        return send_file(file_path, as_attachment=True, download_name=filename)
    except Exception as e:
        return f'Error downloading file: {str(e)}', 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)