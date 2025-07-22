from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'
DATE_OPTIONS = ["2025-07-25", "2025-07-26", "2025-07-27", "2025-07-28", "2025-07-29"]

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        selected_dates = request.form.getlist('dates')

        with open(DATA_FILE, 'r') as f:
            data = json.load(f)

        data[name] = selected_dates

        with open(DATA_FILE, 'w') as f:
            json.dump(data, f)

        return redirect('/result')
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    count = len(data)
    return render_template('index.html', dates=DATE_OPTIONS,count=count)

@app.route('/result')
def result():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    if not data:
        return """
        <h2>目前還沒有人填寫喔！</h2>
        <a href='/'>回主畫面</a>
        """


    all_sets = [set(dates) for dates in data.values()]
    common_dates = set.intersection(*all_sets) if all_sets else set()

    return f"""
    <h2>大家都有空的日子：</h2>
    <ul>{''.join(f'<li>{d}</li>' for d in sorted(common_dates))}</ul>
    <a href="/">回去填表</a>
    """

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
