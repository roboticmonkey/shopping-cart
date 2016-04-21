"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, render_template, redirect, flash, session
import jinja2

from flask_debugtoolbar import DebugToolbarExtension

import melons


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<int:melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print melon
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""

    # TODO: Display the contents of the shopping cart.

    # The logic here will be something like:
    #
    # - get the list-of-ids-of-melons from the session cart
    # - loop over this list:
    #   - keep track of information about melon types in the cart
    #   - keep track of the total amt ordered for a melon-type
    #   - keep track of the total amt of the entire order
    # - hand to the template the total order cost and the list of melon types
    shoppe_cart = {}
    order_total = 0
    # # adding object as key with quantity as value into a dict called cart_dict,
    # # which didn't work
    # if session:   
    #     # gets quantity for each melon id
    #     for item in session['cart']:
    #         cart_dict[melons.get_by_id(item)] = cart_dict.get(melons.get_by_id(item), 0) + 1
    # else:
    #     print "empty yo"
    # print "akldfj;aksdjf", cart_dict

    if session:
        for item in session['cart']:
            melon = melons.get_by_id(item)
            if melon.common_name not in shoppe_cart:
                shoppe_cart[melon.common_name] = {'price': melon.price, 'qty': 1}
            else:
                shoppe_cart[melon.common_name]['qty'] += 1

    for item in shoppe_cart:
        total = item['price'] * item['qty']
        order_total += total


    return render_template("cart.html", shop_cart=shoppe_cart, total=order_total)


@app.route("/add_to_cart/<int:melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """

    # TODO: Finish shopping cart functionality

    # The logic here should be something like:
    #
    # - add the id of the melon they bought to the cart in the session
    if session:
        #add a melon
        session['cart'].append(melon_id)
    else:
        #create empty cart
        session['cart'] = []
        # add the melon to cart
        session['cart'].append(melon_id)
    flash("Successfully added to the cart.")
    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!

    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.debug = True
    DebugToolbarExtension(app)
    app.run()