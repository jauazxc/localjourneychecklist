from flask import *
import os
import zxc as db
folder = os.getcwd()

app = Flask(__name__, template_folder=folder, static_folder=folder)
app.config['SECRET_KEY'] = 'Vejqklhwkjash'

def index():
    items = db.show()
    total_count = len(items)
    print(items)
    completed_count = 0
    for item in items:
        if item['checked'] == 1:
            completed_count += 1
    if total_count == 0:
        percentage = 0
    else:
        percentage = round(completed_count / total_count * 100, 1)
    return render_template('main.html', total_count = total_count, completed_count = completed_count, percentage = percentage, checklist = items)



def add():
    new_item_name = request.form.get('item_name')
    db.add(new_item_name)
    return redirect(url_for('index'))

def delete(item_id):
    db.delete(item_id)
    return redirect(url_for('index'))

def check(item_id):
    db.checked(item_id)
    return redirect(url_for('index'))

def reset():
    db.delete_all()
    return redirect(url_for('index'))

app.add_url_rule('/', 'index', index)
app.add_url_rule('/add', 'add', add, methods=['POST'])
app.add_url_rule('/delete/<int:item_id>', 'delete', delete, methods = ['POST'])
app.add_url_rule('/toggle/<int:item_id>', 'check', check, methods=['POST'])
app.add_url_rule('/reset', 'reset', reset, methods = ['POST'])


if __name__ == '__main__':
    app.run(debug=True)