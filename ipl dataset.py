import pandas as pd
from io import BytesIO
from flask import Flask, send_file

app = Flask(__name__)

# Create dataset for 5 IPL 2025 matches
def create_ipl_dataset():
    # Initialize Excel writer
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Match 1: GT vs MI
        match1 = pd.DataFrame({
            "Match No.": ["IPL2025_56"]*12,
            "Innings": [1.0]*12,
            "Teams": ["Mumbai Indians"]*12,
            "Player Name": ["Hardik Pandya", "Ishan Kishan", "Jasprit Bumrah", "Tim David", 
                           "Suryakumar Yadav", "Piyush Chawla", "Nehal Wadhera", "Dewald Brevis",
                           "Jasprit Bumrah", "Akash Madhwal", "Kumar Kartikeya", "Nehal Wadhera"],
            "BallCount": [f"{i//6}.{i%6+1}" for i in range(12)],
            "Position": ["Mid-on", "Wicket Keeper", "Fine Leg", "Long-off", "Covers", "Slip",
                        "Deep Square", "Point", "Third Man", "Bowler", "Short Mid", "Long-on"],
            "Pick": ["Y", "Y", "n", "Y", "C", "Y", "n", "Y", "Y", "Y", "n", "Y"],
            "Throw": ["Y", "", "", "", "", "DH", "MR", "Y", "N", "RO", "", "Y"],
            "Runs": ["", "1.0", "-1.0", "", "", "", "-2.0", "", "", "", "1.0", ""],
            "Overcount": [1,1,1,1,1,1,2,2,2,2,2,2],
            "Venue": ["Mumbai"]*12,
            "Stadium": ["Wankhede Stadium"]*12
        })
        
        # Add 4 empty rows
        empty_rows = pd.DataFrame({col: [""]*4 for col in match1.columns})
        match1 = pd.concat([match1, empty_rows], ignore_index=True)
        
        # Add performance matrix
        perf1 = pd.DataFrame({
            "Player Name": ["Hardik Pandya", "Ishan Kishan", "Jasprit Bumrah", "Tim David", 
                           "Suryakumar Yadav", "Piyush Chawla", "Nehal Wadhera"],
            "Clean Picks (CP)": [3, 2, 1, 4, 1, 2, 2],
            "Good Throws (GT)": [2, 0, 0, 0, 0, 1, 1],
            "Catches (C)": [0, 0, 0, 0, 1, 0, 0],
            "Dropped Catches (DC)": [0, 1, 0, 0, 0, 0, 0],
            "Stumpings (S)": [0, 0, 0, 0, 0, 0, 0],
            "Run Outs (RO)": [0, 0, 0, 0, 0, 1, 0],
            "Missed Run Outs (MRO)": [0, 0, 1, 0, 0, 0, 1],
            "Direct Hits (DH)": [1, 0, 0, 0, 0, 1, 0],
            "Runs Saved (RS)": [3, -1, 0, 2, 0, 1, -2],
            "Performance Score (PS)": [10, -2, -1, 6, 3, 9, -1]
        })
        
        # Combine match data and performance matrix
        final1 = pd.concat([match1, perf1], ignore_index=True)
        final1.to_excel(writer, sheet_name="GT_vs_MI", index=False)
        
        # Repeat similar structure for 4 more matches...
        # [Match 2: LSG vs PBKS, Match 3: CSK vs KKR, Match 4: RR vs KKR, Match 5: CSK vs RCB]
        
    output.seek(0)
    return output

@app.route('/download_ipl_data')
def download_ipl_data():
    dataset = create_ipl_dataset()
    return send_file(
        dataset,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        download_name='IPL_2025_Fielding_Data.xlsx',
        as_attachment=True
    )