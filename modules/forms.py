from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required, Length

class RestaurantForm(FlaskForm):
    name = StringField("Please enter your name")
    restaraunt = StringField("Please enter a restaurant to find out more details")
    submit = SubmitField()

class RestaurantReviewForm(FlaskForm):
    name = StringField("Your name: ", validators=[Required()])
    restaurant = StringField("Name of restaurant: ", validators=[Required()])
    restaurant_review_entry = StringField("Please enter a short review of this \
                              restaurant, no longer than 300 characters please", \
                              validators=[Required(), Length(max=300, \
                              message="The review cannot be longer than 300 characters!")])
    number_of_stars = IntegerField("Rate the restaurant out of 5 stars, whole numbers only!", \
                      validators=[Required()])
    submit = SubmitField("Submit your review")

    def star_validator(form, field):
        if int(field.data) > 5 :
            raise ValidationError('ERROR -- Your score cannot be higher than 5')
        if int(field.data) < 1 :
            raise ValidationError('ERROR -- Your score cannot be lower than 1')

class SearchForm(FlaskForm):
    name = StringField("Please enter restaurant name: ", validators=[Required()])
    submit = SubmitField()

class ServiceForm(FlaskForm):
    worker_name = StringField("Please type the name of an employee", validators=[Required()])
    position = StringField("Please enter the employee position", validators=[Required()])
    submit = SubmitField()

    def position_validator(form, field):
        if field.data.lower() in ["deputy director", "director"]:
            raise ValidationError("ERROR -- Information of such kind is absolutely secret!")
