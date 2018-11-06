from flask import render_template, redirect, url_for
import requests
import json
from modules import app, db, models, forms
from modules.models import Restaurant, RestaurantReview, Name
from modules.forms import RestaurantForm, SearchForm, RestaurantReviewForm, \
                          ServiceForm

@app.route('/', methods = ['GET', 'POST'])
def home():
    base_url = "https://api.yelp.com/v3/"
    api_key = app.config["API_KEY"]
    headers = {'Authorization': 'Bearer %s' % api_key}

    def save_name(name):
        db.session.add(Name(name=name))
        db.session.commit()

    def obtain_reviews(id, restaurant_id):
        data = requests.get(base_url)
        reviews_url = base_url + "businesses/" + id + "/reviews"
        data = requests.get(reviews_url, headers=headers, params={"api_key": api_key})
        data_loaded = json.loads(data.text)
        for review in data_loaded["reviews"]:
            db.session.add(RestaurantReview(review=review["text"],
                                            restaurant_id=restaurant_id))
            db.session.commit()

    form = RestaurantForm()
    if form.validate_on_submit():
        search = form.restaraunt.data
        save_name(form.name.data)
        search_url = base_url + "businesses/search"
        params = {'api_key': api_key, 'term': search, 'location': 'ann arbor'}
        data = requests.get(search_url, headers=headers, params=params)
        data_loaded = json.loads(data.text)
        for i in data_loaded["businesses"]:
            names = []
            for restaurant in db.session.query(Restaurant).all():
                names.append(restaurant.name)
            if i["name"] not in names:
                restaurant = Restaurant(name=i["name"],
                                        location=i["location"]["address1"],
                                        price=len(getattr(i, "price", "")),
                                        rating=int(i["rating"]))
                db.session.add(restaurant)
                db.session.commit()
                obtain_reviews(i["id"], restaurant.id)
        return redirect(url_for("search"))
    return render_template('base.html',form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/all_restaurants')
def get_all_resteraunts():
    restaurants = db.session.query(Restaurant).all()
    return render_template('restaurant.html', restaurants=restaurants)

@app.route("/find_worker_info", methods = ["GET", "POST"])
def find_worker_info():
    form = ServiceForm()
    if form.validate_on_submit():
        form.position_validator(form.position.data)
        staff = db.session.query(RestaurantStaff).all()
        for worker in staff:
            if worker.name == form.worker_name.data and worker.position == form.position.data:
                service = db.session.query(RestaurantService).filter_by(staff=worker.id)
                return render_template('about_worker.html', worker=worker,
                                       manager_name=service.manager_name)
    return render_template('worker.html', form=form)

@app.route('/find_restaurant')
def find_restaurant():
    form = restaurantForm()
    return render_template('find_restaurant.html', form = form)

@app.route('/leave_review')
def post_review():
    form = RestaurantReviewForm()
    if form.validate_on_submit():
        restaurant = form.restaurant.data
        review = form.restaurant_review_entry.data
        rs = db.session.query(Restaurant).filter_by(name=restaurant)
        if rs.first() is None:
            pass
        else:
            id = rs.first().id
            db.session.add(RestaurantReview(review=review, restaurant_id=id))
            db.session.commit()
    return render_template('post_review.html', form = form)

@app.route('/name_example')
def find_all_names():
    names = db.session.query(Name).all()
    return render_template('name_example.html',names=names)

@app.route("/search", methods = ['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        restaurant_name = form.name.data.lower()
        restaurants = db.session.query(Restaurant).all()
        found = []
        print(found)
        for i in restaurants:
            if i.name.lower() == restaurant_name:
                found.append(i)
        return render_template("restaurant.html", restaurants=found)
    return render_template("search.html", form=form)
