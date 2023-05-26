from app import app
from app.models import Product, Carts, Users, db
from flask import url_for
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required


@app.route('/')
def homePage():
    all_products = Product.query.all()
    return render_template('index.html',all_products=all_products)

# Temporary fake product 
@app.route('/product')
def fakeProductPage():
    return render_template('product.html')

@app.route('/product/<int:product_id>')
def productPage(product_id):
    product = Product.query.get(product_id)
    return render_template('product.html',product=product)

@app.route('/additem/<int:product_id>')
@login_required
def addItemToCart(product_id):
    product = Product.query.get(product_id)
    if not product:
        flash("Product does not exist","danger")
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

@app.route('/checkout')
@login_required
def checkout():
    cart_items = current_user.cart_items
    if not cart_items:
        flash("You have nothing in your cart, nothing to checkout","danger")
        return redirect(url_for("showMyCart"))
    
    for cart_item in cart_items:
        cart_item.deleteFromDB()

    flash("Thanks for shopping with us, you've successfully checked out. Use used your credit we found on the dark web","success")
    return redirect(url_for("homePage"))

@app.route('/removeitem/<int:product_id>')
@login_required
def removeItemFromCart(product_id):
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


@app.route('/emptycart')
@login_required
def emptyCart():
    cart_items = current_user.cart_items
    if not cart_items:
        flash("Your cart was already empty, nothing was removed","danger")
        return redirect(url_for("showMyCart"))
    
    for cart_item in cart_items:
        cart_item.deleteFromDB()

    flash("You successfully removed all items from your cart","success")
    return redirect(url_for("showMyCart"))

@app.route('/cart')
@login_required
def showMyCart():

    return render_template("cart.html")



@app.route('/runcode')
def runcode():
    
    # CODE TO ADD PRODUCT TO DATABASE
    title = '85" Class QN90C Samsung Neo QLED 4K Smart TV (2023)'
    image_url = "https://image-us.samsung.com/SamsungUS/home/television-home-theater/tvs/03242023/QN90C_85_75_65_55.jpg?$product-details-jpg$"
    price = 4799.99
    description = "Some TVs just have it. They make everything look good—even hard stuff like 4K upscaling, weird viewing angles and daytime sports. But when it's Samsung Neo QLED 4K we're talking about, there's no need to be jealous. Because—thanks to its brilliant picture, dynamic audio and stellar design—it'll make you look good, too."
    product1 = Product(title,price,description,image_url)
    product1.saveToDB()
    
    
    return redirect(url_for("homePage"))