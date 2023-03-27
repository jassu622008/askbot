from flask import Flask, render_template, request, redirect, url_for, session
from transformers import pipeline
import time

app = Flask(__name__)
app.secret_key = 'jassu122622F' # Change this to a secret key of your choice

# Define a dictionary of valid usernames and passwords
users = {
    'askbot': 'b@@@T!JBpaL&zE7!)CrFQVabdNKCHD&rP!@D!+KewFy8hThLGeZmQDN@CPkzQap+',
}

# Define a function to authenticate users
def authenticate(username, password):
    if username in users and users[username] == password:
        return True
    else:
        return False

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if authenticate(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')

    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/generate_text', methods=['POST'])
def generate_text():
    if 'username' in session:
        prompt = request.form['prompt']
        model_type = request.form['model_type']
        num_words = int(request.form['num_words'])

        # Initialize progress bar values
        progress = 0
        max_progress = 100

        # Initialize pipeline for chosen model type
        if model_type == 'gpt2':
            generator = pipeline('text-generation', model='gpt2')
        elif model_type == 'distilgpt2':
            generator = pipeline('text-generation', model='distilgpt2')

        # Generate text on given prompt
        text = ""
        while len(text.split()) < num_words:
            output = generator(prompt, max_length=100, do_sample=True)
            generated_text = output[0]['generated_text']
            text += generated_text[len(prompt):]
            progress = int(len(text.split()) / num_words * max_progress)

        return render_template('result.html', text=text)

    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
