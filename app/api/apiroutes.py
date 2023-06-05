from . import api
from ..models import Product, Carts, Users, db
from .apiauthhelper import token_auth, basic_auth, token_auth_required
from flask import request, flash, url_for, redirect, render_template
from flask_login import current_user
import stripe
import os





#SHOWS SINGLE PRODUCT WHEN CLICKED ON FIX THIS 
@api.get('/Singleproduct/<int:product_id>')
def SingleproductAPI(product_id):
    print("IM HERE")
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


@api.post('/addToCart/<int:product_id>')
@token_auth_required
def addToCartAPI(user, product_id):
    # user = token_auth.current_user()
    # data = request.json

    # product_id = data['product_id']
    product = Product.query.get(product_id)

    if product:

        cart_item = Carts(user.id, product.id, 1)
        cart_item.saveToDB()

        return {
            'status': 'ok',
            'message': f'Succesfully added {product.product_name} to your cart!'
        }
    else:
        return {
            'status': 'not ok',
            'message': 'That product does not exist!'
        }

@api.get('/showProducts')
def showProducts():
    products = Product.query.all()
    if products:
        return {
            'status': 'ok',
            'products': [product.to_dict() for product in products]
        }


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

@api.post('/removeFromCart/<int:product_id>')
@token_auth_required
def removeFromCartAPI(user, product_id):
    product = Product.query.get(product_id)
    item = Carts.query.filter_by(user_id=user.id, product_id=product_id).first()
    if item:
        item.deleteFromDB()
        return {
            'status': 'ok',
            'message': f"Successfully removed {product.product_name} from cart."
        }
    return {
            'status': 'not ok',
            'message': f"You do not have that item in your cart."
        }



@api.post('/emptycart')
@token_auth_required
def emptyCartAPI(user):
    cart_items = Carts.query.filter_by(user_id=user.id).all()
    if cart_items:
        for item in cart_items:
            item.deleteFromDB()
        return {
            'status': 'ok',
            'message': "Entire cart has been deleted"
        }
    else:
        return {
            'status': 'not ok',
            'message': 'There is nothing to remove from cart'
        }

@api.get('/cart')
@token_auth_required
def CartAPI(user):
    return {
        'status': 'ok',
        'cart': [Product.query.get(c.product_id).to_dict() for c in Carts.query.filter_by(user_id=user.id).all()]
    }


FRONT_END_URL = os.environ.get('FRONT_END_URL')
stripe.api_key = os.environ.get('STRIPE_API_KEY')
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
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "WATCH"},
                    "unit_amount": 800,
                    "tax_behavior": "exclusive",
                },
                'quantity':1
            }],
            mode='payment',
            success_url=FRONT_END_URL + '/apiroutes?success=true',
            cancel_url=FRONT_END_URL + '/apiroutes?canceled=true',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)
