import os
from flask import Flask, request, render_template, send_file, flash
from werkzeug.utils import secure_filename
import tempfile
import shutil
from utils import process_venue_file

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

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
            # Send the Excel file (KML will be downloaded separately)
            return render_template('result.html', 
                                 excel_file=result['excel_filename'],
                                 kml_file=result['kml_filename'],
                                 excel_path=result['excel_path'],
                                 kml_path=result['kml_path'])
        else:
            return render_template('index.html', error=result['error']), 400
            
    except Exception as e:
        if 'temp_dir' in locals():
            shutil.rmtree(temp_dir, ignore_errors=True)
        return render_template('index.html', error=f'Error processing file: {str(e)}'), 500

@app.route('/download/<path:filepath>')
def download(filepath):
    try:
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return f'Error downloading file: {str(e)}', 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
