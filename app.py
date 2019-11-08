from flask import Flask
from flask import render_template, redirect, request, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
import secrets

conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
#conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbuser, dbpass, dbhost, dbname)

app = Flask(__name__)
app.config['SECRET_KEY']='!QAZ1qaz'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)

class aahelf_brandsapp(db.Model):
    brandID = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(255))

    def __repr__(self):
        return "id: {0} | Brand name: {1}".format(self.id, self.brand)

class BrandForm(FlaskForm):
    brand = StringField('Brand Name:', validators=[DataRequired()])

@app.route('/')
def index():
    all_brands = aahelf_brandsapp.query.all()
    return render_template('index.html', brands=all_brands, pageTitle='Adam\'s Brands')

@app.route('/add_brand', methods=['GET', 'POST'])
def add_brand():
    form = BrandForm()
    if form.validate_on_submit():
        brand = aahelf_brandsapp(brand=form.brand.data)
        db.session.add(brand)
        db.session.commit()
        return redirect('/')

    return render_template('add_brand.html', form=form, pageTitle='Add A New Brand')    

@app.route('/brand/<int:brandID>', methods=['GET','POST'])
def brand(brandID):
    brand = aahelf_brandsapp.query.get_or_404(brandID)
    return render_template('brand.html', form=brand, pageTitle='Brand Details')

@app.route('/brand/<int:brandID>/delete', methods=['POST'])
def delete_brand(brandID):
    if request.method == 'POST': #if it's a POST request, delete the friend from the database
        brand = aahelf_brandsapp.query.get_or_404(brandID)
        db.session.delete(brand)
        db.session.commit()
        flash('brand was successfully deleted!')
        return redirect("/")
    else: #if it's a GET request, send them to the home page
        return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)