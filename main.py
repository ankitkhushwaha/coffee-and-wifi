from flask import Flask, render_template ,url_for ,request
from flask_bootstrap import Bootstrap 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField  , SelectField
from wtforms.validators import DataRequired ,URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe_name = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe location on Google map(Url)' ,validators=[DataRequired() , URL()])
    opening_time = StringField('Opening time eg. 8Am' , validators=[DataRequired()])
    closing_time = StringField('Closing time eg. 9pm' , validators=[DataRequired()])
    coffee_rating = SelectField("Coffee rating", validate_choice=[DataRequired()], choices=[("✘","✘"), ("☕️","☕️"), ("☕️☕️","☕️☕️") , ("☕️☕️☕️","☕️☕️☕️") , ("☕️☕️☕️☕️","☕️☕️☕️☕️") , ("☕️☕️☕️☕️☕️","☕️☕️☕️☕️☕️") ])
    wifi_strenth_rating = SelectField("Wifi strenth rating", validate_choice=[DataRequired()], choices=[("✘","✘"),("💪","💪"), ("💪💪","💪💪") , ("💪💪💪","💪💪💪") , ("💪💪💪💪","💪💪💪💪") , ("💪💪💪💪💪","💪💪💪💪💪") ])
    power_socket_availability = SelectField("Power socket availability", validate_choice=[DataRequired()], choices=[("✘","✘"), ("🔌","🔌"), ("🔌🔌","🔌🔌") , ("🔌🔌🔌","🔌🔌🔌") , ("🔌🔌🔌🔌","🔌🔌🔌🔌") , ("🔌🔌🔌🔌🔌","🔌🔌🔌🔌🔌") ])
    submit = SubmitField('Submit')



# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add' , methods = ['GET' , 'POST'])
def add_cafe():
    form = CafeForm()
    if request.method == 'POST' and form.validate_on_submit():
        cafe_name = form.cafe_name.data
        location = form.location.data
        opening_time = form.opening_time.data
        closing_time = form.closing_time.data
        coffee_rating = form.coffee_rating.data
        wifi_strenth_rating = form.wifi_strenth_rating.data
        power_socket_availability = form.power_socket_availability.data
        new_cafe = [cafe_name, location, opening_time , closing_time , coffee_rating  , wifi_strenth_rating , power_socket_availability]
        
        # Reading the csv file
        with open('cafe-data.csv', newline='') as csv_file:
            csv_data = csv.reader(csv_file, delimiter=',')
            list_of_rows = []
            for row in csv_data:
                list_of_rows.append(row)
            # Adding new cafe to list 
            list_of_rows.append(new_cafe)
        # Writing the csv file
        with open('cafe-data.csv' , 'w') as csv_file:
            csvwriter = csv.writer(csv_file)
            csvwriter.writerows(list_of_rows)
    return render_template('add.html', form=form)
        
        
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
