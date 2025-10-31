import tools
import pandas as pd
from flask import Flask, render_template, request, url_for, redirect, session

app = Flask(__name__)
app.secret_key = 'hello'

@app.route('/', methods=['POST', 'GET'])
def homepage():
    final_date = None
    error_message = None
    session.clear()

    if request.method == 'POST':
        date_input = request.form['final_date']

        try:
            final_date = tools.enter_final_date(date_input)
            session['final_date'] = final_date.isoformat()
            return redirect(url_for('specific_date'))
        except ValueError as ve:
            error_message = str(ve)

    return render_template('index.html', error=error_message)

@app.route('/specific_date', methods=['POST', 'GET'])
def specific_date():
    specific_date = None
    error_message = None
    if 'final_date' not in session:
        return redirect(url_for('homepage'))

    final_date = pd.Timestamp(session['final_date'])

    if request.method == 'POST':
        action = request.form.get('action')
        try: 
            if action == 'specific':
                date_input = request.form.get('specific_date')
                specific_date = tools.enter_specific_date(date_input)
                session['specific_date'] = specific_date.isoformat()
                return redirect(url_for('result'))
            
            elif action == 'current':
                current_date = tools.get_current_date()
                session['current_date'] = current_date.isoformat()
                return redirect(url_for('result'))
        
        except ValueError as ve:
            error_message = str(ve)

    return render_template('specific_date.html', final_date=final_date, error=error_message)

@app.route('/result', methods=['GET'])
def result():
    if not session.get('specific_date') and not session.get('current_date'):
        return redirect(url_for('specific_date'))
    
    if 'final_date' not in session:
        return redirect(url_for('homepage'))

    final_date = pd.Timestamp(session['final_date'])
    result_specific = None
    result_current = None

    if 'specific_date' in session:
        specific_date = pd.Timestamp(session['specific_date'])
        result_specific = final_date - specific_date
        result_specific = str(result_specific)
    
    if 'current_date' in session:
        current_date = pd.Timestamp(session['current_date'])
        result_current = final_date - current_date
        result_current = str(result_current)


    return render_template(
        'result.html',
        result_specific=result_specific,
        result_current=result_current,
        final_date=final_date
        )
    

if __name__ == '__main__':
    app.run(debug=True)
