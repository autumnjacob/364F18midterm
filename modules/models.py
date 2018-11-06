from modules import db

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    location = db.Column(db.String(300))
    price = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    service = db.relationship("RestaurantService", backref="Restaurant")
    reviews = db.relationship('RestaurantReview', backref='Restaurant')
    def __repr__(self):
        return "Restaurants:   {} ".format(self.name, self.id)

class RestaurantReview(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.String(1000))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    def __repr__(self):
        return "Review:  {}  ".format(self.review, self.restaurant_id)

class Name(db.Model):
    __tablename__ = "names"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    def __repr__(self):
        return "{} (ID: {})".format(self.name, self.id)

class RestaurantService(db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    manager_name = db.Column(db.String(100))
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))
    staff = db.relationship("RestaurantStaff", backref="RestaurantService")

class RestaurantStaff(db.Model):
    __tablename__ = "staff"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    position = db.Column(db.String(200))
    experience = db.Column(db.Integer)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"))
