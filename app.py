from flask import Flask
from flask import render_template, redirect, request, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
#import secrets
import os

dbuser = os.environ.get('DBUSER')
dbpass = os.environ.get('DBPASS')
dbhost = os.environ.get('DBHOST')
dbname = os.environ.get('DBNAME')

#conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbuser, dbpass, dbhost, dbname)

app = Flask(__name__)
app.config['SECRET_KEY']='!QAZ1qaz'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)

class aahelf_brandsapp(db.Model):
    brandID = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(255))

    def __repr__(self):
        return "Brand name: {0}".format(self.brand)

class BrandForm(FlaskForm):
   brandID = IntegerField('Brand ID:', )
   brand = StringField('Brand Name:', validators=[DataRequired()])

@app.route('/')
def index():
    all_brands = aahelf_brandsapp.query.all()
    return render_template('index.html', brands=all_brands, pageTitle='Adam\'s Brands')

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        print('post method')
        form = request.form
        search_value = form['search_string']
        print(search_value)
        search = "%{0}%".format(search_value)
        print(search)
        results = aahelf_brandsapp.query.filter(aahelf_brandsapp.brand.like(search)).all()
        print(results)
        return render_template('index.html', brands=results, pageTitle='Adam\'s Brands', legend="Search Results")
    else:
        return redirect('/')


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
def get_brand(brandID):
    brand = aahelf_brandsapp.query.get_or_404(brandID)
    return render_template('brand.html', form=brand, pageTitle='Brand Details', 
                            legend="Brand deatils")

@app.route('/brand/<int:brandID>/update', methods=['GET','POST'])
def update_brand(brandID):
    brand = aahelf_brandsapp.query.get_or_404(brandID)
    form = BrandForm()
    
    if form.validate_on_submit():
        brand.brand = form.brand.data
        db.session.commit()
        flash('Your brand has been updated.')
        return redirect(url_for('get_brand', brandID=brand.brandID))
    #elif request.method == 'GET':
    form.brandID.data = brand.brandID
    form.brand.data = brand.brand
    return render_template('update_brand.html', form=form, pageTitle='Update Brand',
                            legend="Update A Brand")

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