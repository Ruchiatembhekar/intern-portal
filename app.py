from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
CORS(app)

# Dummy data storage (in production, use a proper database)
users_data = {
    "john_doe": {
        "name": "John Doe",
        "email": "john@example.com",
        "referral_code": "JOHN2025",
        "donations_raised": 12500,
        "rewards": ["Bronze Badge", "First Donation", "10K Milestone"],
        "join_date": "2025-01-15"
    },
    "jane_smith": {
        "name": "Jane Smith",
        "email": "jane@example.com",
        "referral_code": "JANE2025",
        "donations_raised": 8750,
        "rewards": ["Bronze Badge", "First Donation"],
        "join_date": "2025-01-20"
    },
    "alex_wilson": {
        "name": "Alex Wilson",
        "email": "alex@example.com",
        "referral_code": "ALEX2025",
        "donations_raised": 15300,
        "rewards": ["Bronze Badge", "First Donation", "10K Milestone", "Top Performer"],
        "join_date": "2025-01-10"
    }
}

# Routes
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple dummy authentication
        if username in users_data:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        email = request.form.get('email')
        
        # Create new user with dummy data
        if username not in users_data:
            users_data[username] = {
                "name": name,
                "email": email,
                "referral_code": f"{username.upper()}2025",
                "donations_raised": 0,
                "rewards": [],
                "join_date": datetime.now().strftime("%Y-%m-%d")
            }
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('signup.html', error="Username already exists")
    
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    user_data = users_data.get(username, {})
    return render_template('dashboard.html', user=user_data)

@app.route('/leaderboard')
def leaderboard():
    # Sort users by donations raised
    sorted_users = sorted(users_data.items(), key=lambda x: x[1]['donations_raised'], reverse=True)
    return render_template('leaderboard.html', users=sorted_users)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# API Routes
@app.route('/api/user/<username>')
def get_user_data(username):
    if username in users_data:
        return jsonify(users_data[username])
    return jsonify({"error": "User not found"}), 404

@app.route('/api/leaderboard')
def api_leaderboard():
    sorted_users = sorted(users_data.items(), key=lambda x: x[1]['donations_raised'], reverse=True)
    return jsonify([{"username": k, **v} for k, v in sorted_users])

@app.route('/api/update_donations', methods=['POST'])
def update_donations():
    if 'username' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    username = session['username']
    amount = request.json.get('amount', 0)
    
    if username in users_data:
        users_data[username]['donations_raised'] += amount
        return jsonify({"success": True, "new_total": users_data[username]['donations_raised']})
    
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000) 
