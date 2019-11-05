from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY']='!QAZ1qaz'

class BrandForm(FlaskForm):
    name = StringField('Brand Name:', validators=[DataRequired()])

@app.route('/')
def index():
    return render_template('index.html', pageTitle='Adam\'s Brands')

@app.route('/add_brand', methods=['GET', 'POST'])
def add_brand():
    form =BrandForm()
    if form.validate_on_submit():
        return "my Brands name is {0}".format(form.name.data)
    
    return render_template('add_brand.html', form=form, pageTitle='Add A New Brand')    


if __name__ == '__main__':
    app.run(debug=True)