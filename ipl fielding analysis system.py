# app.py (Backend - Flask)
import os
import pandas as pd
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

WEIGHTS = {
    'CP': 1,    # Clean Picks
    'GT': 1,    # Good Throws
    'C': 3,     # Catches
    'DC': -3,   # Dropped Catches
    'ST': 3,    # Stumpings
    'RO': 3,    # Run Outs
    'MRO': -2,  # Missed Run Outs
    'DH': 2,    # Direct Hits
}

def calculate_performance(df):
    # Preprocess data
    df = df.dropna(subset=['Player Name'])
    df['Runs'] = pd.to_numeric(df['Runs'], errors='coerce').fillna(0)
    
    # Initialize metrics
    metrics = {
        'CP': (df['Pick'] == 'Y').astype(int),
        'GT': (df['Throw'] == 'Y').astype(int),
        'C': (df['Pick'] == 'C').astype(int),
        'DC': (df['Pick'] == 'DC').astype(int),
        'ST': (df['Pick'] == 'S').astype(int),
        'RO': (df['Throw'] == 'RO').astype(int),
        'MRO': (df['Throw'] == 'MR').astype(int),
        'DH': (df['Throw'] == 'DH').astype(int),
    }
    
    # Add metrics to DataFrame
    for k, v in metrics.items():
        df[k] = v
    
    # Group by player and calculate metrics
    grouped = df.groupby('Player Name').agg({
        'CP': 'sum',
        'GT': 'sum',
        'C': 'sum',
        'DC': 'sum',
        'ST': 'sum',
        'RO': 'sum',
        'MRO': 'sum',
        'DH': 'sum',
        'Runs': 'sum'
    }).reset_index()
    
    # Calculate Performance Score
    grouped['PS'] = 0
    for metric, weight in WEIGHTS.items():
        grouped['PS'] += grouped[metric] * weight
    grouped['PS'] += grouped['Runs']

    # Rename columns for frontend display
    grouped = grouped.rename(columns={
        'Player Name': 'Player Name',
        'CP': 'Clean Picks (CP)',
        'GT': 'Good Throws (GT)',
        'C': 'Catches (C)',
        'DC': 'Dropped Catches (DC)',
        'ST': 'Stumpings (ST)',
        'RO': 'Run Outs (RO)',
        'MRO': 'Missed Run Outs (MRO)',
        'DH': 'Direct Hits (DH)',
        'Runs': 'Runs Saved/Conceded (RS)',
        'PS': 'Performance Score (PS)'
    })

    # Reorder columns for better display
    display_cols = [
        'Player Name',
        'Clean Picks (CP)',
        'Good Throws (GT)',
        'Catches (C)',
        'Dropped Catches (DC)',
        'Stumpings (ST)',
        'Run Outs (RO)',
        'Missed Run Outs (MRO)',
        'Direct Hits (DH)',
        'Runs Saved/Conceded (RS)',
        'Performance Score (PS)'
    ]
    grouped = grouped[display_cols]

    return grouped.sort_values('Performance Score (PS)', ascending=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
        try:
            # Read Excel with header at row 5 (0-indexed row 4)
            df = pd.read_excel(filepath, sheet_name=0, skiprows=4)
            # Clean column names
            df.columns = [col.strip() for col in df.columns.astype(str)]
            
            # Process data
            results = calculate_performance(df)
            return jsonify({
                'data': results.to_dict(orient='records'),
                'columns': list(results.columns)
            })
        except Exception as e:
            return jsonify({'error': f'Processing error: {str(e)}'}), 500

@app.route('/sample')
def sample_list():
    dataset_dir = os.path.join(os.getcwd(), 'datasets')
    files = []
    if os.path.exists(dataset_dir):
        files = [f for f in os.listdir(dataset_dir) if os.path.isfile(os.path.join(dataset_dir, f))]
    return render_template('sample_list.html', files=files)

@app.route('/download-dataset/<filename>')
def download_dataset(filename):
    dataset_dir = os.path.join(os.getcwd(), 'datasets')
    return send_from_directory(dataset_dir, filename, as_attachment=True)

@app.route('/ipl-dataset')
def ipl_dataset():
    return send_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)