from flask import Flask,render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
import requests
import json
from cloudipsp import Api, Checkout

api = Api(merchant_id=1396424,
          secret_key='test')
checkout = Checkout(api=api)
data = {
    "currency": "USD",
    "amount": 10000
}
url = checkout.url(data).get('checkout_url')

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.app_context().push()
db=SQLAlchemy(app)
db.init_app(app)
class Item(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive=db.Column(db.String,nullable=False)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    items=Item.query.order_by(Item.price).all()
    return render_template("index.html",data=items)


@app.route('/buy/1')
def buy1():
    return render_template("about.html")


@app.route('/create',methods=['POST','GET'])
def create():
    if request.method=='POST':
        title=request.form['title']
        price=request.form['price']
        item=Item(title=title,price=price)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "sssss"
    else:
        return render_template("create.html")


if __name__ == "__main__":
    app.run(debug=True)