from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
import sentence_structure as ss
import data_structures as ds
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bug_reports.db'
db = SQLAlchemy(app)

class BugReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report = db.Column(db.String(1000))

@app.route('/report_bug', methods=['GET', 'POST'])
def report_bug():
    if request.method == 'POST':
        bug_report = request.form['bug_report']
        conn = sqlite3.connect('mydatabase.db')
        c = conn.cursor()
        c.execute("INSERT INTO bug_report (report) VALUES (?)", (bug_report,))
        conn.commit()
        conn.close()
        return redirect('/')
    return '''
        <h1>Report a Bug</h1>
        <form method="post">
            <label for="bug_report">Bug report:</label>
            <br>
            <textarea id="bug_report" name="bug_report" rows="5" cols="50"></textarea>
            <br>
            <button type="submit">Submit</button>
        </form>
    '''

def process_text(input_text):
    feedback = ""
    lookup = ss.create_lookup_list(input_text)
    count = ss.corpus_lookup(lookup)
    misused_particles, feedback = ss.analyze_string_count(count, feedback)
    return(ss.check_verb_position(input_text, feedback))

@app.route('/', methods=['GET', 'POST'])
def home():
    input_text = ''
    output_text = ''
    pos_dict = {"名詞":"noun","動詞":"verb", "助詞":"adverb", "副詞":"adverb","助詞":"auxiliary", "助動詞":"auxiliary verb", "接続詞":"successive",
                "代名詞":"pronoun", "形状詞":"adjectival noun", "接頭辞":"conjunction","感動詞":"affective","記号":"noun"
                }
    if request.method == 'POST':
        input_text = request.form['input_text']
        original = ds.create_words_list(input_text)
        for i in original:
            output_text += f'<span title="{pos_dict[i.get_pos()]}">{i.get_word()}</span> '
        feedback = process_text(input_text)
        output_text += f"<br><br>{feedback}"
        return '''
            <h1>Error Detection</h1>
            <form method="post">
                <label for="input_text">Input text:</label>
                <br>
                <textarea id="input_text" name="input_text" rows="5" cols="50">{}</textarea>
                <br>
                <input type="submit" value="Process">
            </form>
            <br>
            <label for="output_text">Feedback:</label>
            <div id="output_text">{}</div>
            <br>
            <br>
            <br>
            <a href="/report_bug"><button>Report a Bug</button></a>
            <script>
                var spans = document.getElementsByTagName('span');
                for (var i = 0; i < spans.length; i++) {{
                    spans[i].addEventListener('mouseover', function(event) {{
                        var span = event.target;
                        var title = span.getAttribute('title');
                        span.style.backgroundColor = 'yellow';
                        span.style.cursor = 'help';
                        var tooltip = document.createElement('div');
                        tooltip.innerHTML = title;
                        tooltip.style.position = 'absolute';
                        tooltip.style.left = event.pageX + 10 + 'px';
                        tooltip.style.top = event.pageY + 10 + 'px';
                        tooltip.style.backgroundColor = 'white';
                        tooltip.style.border = '1px solid black';
                        tooltip.style.padding = '5px';
                        document.body.appendChild(tooltip);
                        span.addEventListener('mouseout', function() {{
                            span.style.backgroundColor = '';
                            document.body.removeChild(tooltip);
                        }});
                    }});
                }}
            </script>
        '''.format(input_text, output_text)

    return '''
        <h1>Error Detection</h1>
        <form method="post">
            <label for="input_text">Input text:</label>
            <br>
            <textarea id="input_text" name="input_text" rows="5" cols="50">{}</textarea>
            <br>
            <input type="submit" value="Process">
        </form>
        <br>
        <label for="output_text">Feedback:</label>
        <br>
        <div id="output_text">{}</div>
        <a href="/report_bug"><button>Report a Bug</button></a>
    '''.format(input_text, output_text)


if __name__ == '__main__':
    app.run(port=8080)



