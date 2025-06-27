from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

from task_model import Task
# Create app
app = Flask(__name__)

# Create Database and configure
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app=app)

@app.route("/", methods=["POST", "GET"])
def index():
    # Add task
    if request.method == "POST":
        current_task_content = request.form["content"]
        new_task = Task(content=current_task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(e)
            return e
    elif request.method == "GET":
        my_tasks = list(db.session.execute(db.select(Task).order_by(Task.createdAt)).scalars())
        return render_template("index.html", tasks=my_tasks)
    
@app.route("/delete/<int:tid>", methods=["GET","POST"])
def delete(tid):
    task = db.get_or_404(Task, ident=tid)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(e)
        # You could flash an error message or return a simple string for now:
        return f"An error occurred deleting the task: {e}", 500

@app.route("/update/<int:tid>", methods=["POST", "GET"])
def edit(tid):
    task = db.get_or_404(Task, ident=tid)
    if request.method == "POST":
        task.content = request.form["content"]
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error: {e}"
            
    else:
        return render_template("edit.html", task=task)
            
if __name__ in "__main__":
    with app.app_context():
        db.create_all()
        
    app.run(debug=True) 
