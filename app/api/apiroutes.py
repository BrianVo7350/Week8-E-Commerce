from . import api
from ..models import Product, Carts, Users, db
from .apiauthhelper import token_auth, basic_auth
from flask import request, flash, url_for, redirect, render_template
from flask_login import current_user
import stripe
import os


FRONT_END_URL = os.environ.get('FRONT_END_URL')


# @app.route('/')
# def homePage():
#     all_products = Product.query.all()
#     return render_template('index.html',all_products=all_products)


@api.get('/product/<int:product_id>')
# @basic_auth.login_required
@token_auth.login_required
def GetproductAPI(product_id):
    product = Product.query.get(product_id)
    if product:
        return {
            'status':'ok',
            'results': 1,
            'product': product.to_dict()
        }
    else:
        return {
            'status' : 'not ok',
            'message' : 'product does not exist'
        }, 404
    

@api.get('/addToCart/<int:product_id>')
# @basic_auth.login_required
@token_auth.login_required
def addToCartAPI(product_id):
# def getProductAPI(product_id):
    product = product.query.get(product_id)
    if not product:
        return redirect(url_for("homePage"))
    
    user_id = current_user.id

    cart_entry = Carts.query.filter(db.and_(Carts.user_id==user_id,Carts.product_id==product_id)).all()

    if not cart_entry:
        print("not carts")
        new_entry = Carts(user_id,product_id,1)
        new_entry.saveToDB()
    else:
        cart_entry[0].item_quantity += 1
        cart_entry[0].saveToDB()
    
    flash(f"You successfully added {product.product_name} to your cart","success")
    return redirect(url_for("showMyCart"))

       
@api.get('removeitem/<int:product_id>')
def getProductAPI(product_id):
    product = product.query.get(product_id)


# @api.get('/checkout')
# @basic_auth.login_required
# def checkout():
#     cart_items = current_user.cart_items
#     if not cart_items:
#         flash("You have nothing in your cart, nothing to checkout","danger")
#         return redirect(url_for("showMyCart"))
    
#     for cart_item in cart_items:
#         cart_item.deleteFromDB()

    # flash("Thanks for shopping with us, you've successfully checked out. Use used your credit we found on the dark web","success")
    # return redirect(url_for("homePage"))

@api.get('/removeFromCart/<int:product_id>')
# @basic_auth.login_required
@token_auth.login_required
def removeFromCartAPI(product_id):
# def removeItemFromCart(product_id):
    product = Product.query.get(product_id)

    if not product:
        flash("Product does not exist","danger")
        return redirect(url_for("homePage"))
    
    user_id = current_user.id

    cart_entry = Carts.query.filter(db.and_(Carts.user_id==user_id,Carts.product_id==product_id)).all()

    if not cart_entry:
        flash("This item is not in your cart, you can't remove it","danger")
        return redirect(url_for("homePage"))
    
    cart_entry = cart_entry[0]
    cart_quantity = cart_entry.item_quantity

    if cart_quantity == 1:
        cart_entry.deleteFromDB()
        flash(f"You successfully removed {product.product_name}","success")
        return redirect(url_for("showMyCart"))
    else:
        cart_entry.item_quantity -= 1
        cart_entry.saveToDB()
        flash(f"You successfully removed one {product.product_name}","success")
        return redirect(url_for("showMyCart"))


@api.get('/emptycart')
# @basic_auth.login_required
@token_auth.login_required
def emptyCartAPI():
    cart_items = current_user.cart_items
    if not cart_items:
        flash("Your cart was already empty, nothing was removed","danger")
        return redirect(url_for("showMyCart"))
    
    for cart_item in cart_items:
        cart_item.deleteFromDB()

    flash("You successfully removed all items from your cart","success")
    return redirect(url_for("showMyCart"))

@api.get('/cart')
# @basic_auth.login_required
@token_auth.login_required
def CartAPI():
    return render_template("cart.html")



stripe.apikey = os.environ.get('STRIPE_API_KEY')
@api.post('/checkout')
def checkout():
    try:
        data = request.form
        line_items = []
        for price, qty in data.items():
            line_items.append({
                'price': price,
                'quantity': qty
            })
        checkout_session = stripe.checkout.Session.create(
            # line_items=line_items,
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "IPHONE"},
                    "unit_amount": 1000,
                    "tax_behavior": "exclusive",
                },
                'quantity':1
            }],
            mode='payment',
            success_url=FRONT_END_URL + '?success=true',
            cancel_url=FRONT_END_URL + '?canceled=true',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)
