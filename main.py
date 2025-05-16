
from flask import Flask, render_template, request, flash, send_from_directory, url_for, redirect
from dotenv import load_dotenv
import os
from simple_salesforce import Salesforce, SalesforceMalformedRequest
from flask_mail import Mail, Message
import datetime

from flask_bootstrap import Bootstrap5





app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.secret_key = "random_secret_key"

 # Load envrironment variables from .env file
load_dotenv()
sf_username = os.getenv('SF_USERNAME')
sf_password = os.getenv('SF_PASSWORD')
sf_security_token = os.getenv('SF_SECURITY_TOKEN')



# Salesforce login
sf = Salesforce(
    username=os.getenv('SF_USERNAME'),
    password=os.getenv('SF_PASSWORD'),
    security_token= os.getenv('SF_SECURITY_TOKEN'),
    domain='test'
)



############################### Checks  existing records ###########################################################
def record_exists(record_type, FIN, singapore_mobile_no,home_country_no):
    # Query Salesforce to check if a record with the same first name, last name, or email already exists
    query = f"SELECT Id FROM {record_type} WHERE "
    # To prevent blank FINs to considered as similar records
    conditions = []
    if FIN.strip():  # Check if FIN is not blank or only whitespace
        conditions.append(f"FIN__c = '{FIN}'")
    if singapore_mobile_no:
        conditions.append(f"Singapore_Mobile__c = '{singapore_mobile_no}'")
    if home_country_no:
        conditions.append(f"Oversea_Mobile__c = '{home_country_no}'")


    if conditions:
        query += " OR ".join(conditions)

    result = sf.query(query)

    # If the query returns any records, a record with the same first name, last name, or email exists
    return len(result['records']) > 0
#####################################################################################################################







################################# Gets picklist values from salesforce for languages spoken ###################################
object_api_name = 'Unverified_Client__c'
field_api_name = 'Languages_Spoken__c'

object_metadata = sf.__getattr__(object_api_name).describe()

field_description = next((field for field in object_metadata['fields'] if field['name'] == field_api_name), None)

picklist_values = None
if field_description and 'picklistValues' in field_description:
    picklist_values = [value['value'] for value in field_description['picklistValues']]

picklist_values_str = ", ".join([f'"{value}"' for value in picklist_values])

record_type = 'Unverified_Client__c'

###############################################################################################################################










@app.route('/translations.json')
def translations():
    return send_from_directory('templates', 'translations.json')

@app.route("/")
def index():
    return render_template("index.html", picklist_values_str=picklist_values_str)


@app.route("/submit-form", methods=["POST"])
def submit():
    # Extract form data
    name = request.form['name']
    gender = request.form['gender']
    dob = request.form['dob']
    finNum = request.form['finNum']
    sgMobileNum = request.form['sgMobileNum']
    homeCountryMobileNum = request.form['homeCountryMobileNum']
    country = request.form['country']
    yearJoined = request.form['yearJoined']
    languages = request.form.getlist('languages')  # This is how to handle multi-select


    try:
        #Checks if FIN/ Sg Mobile Num / Home Mobile Num is registered already
        if record_exists(record_type, finNum, sgMobileNum, homeCountryMobileNum):
            flash("FIN(နိုင်ငံခြားမှတ်ပုံတင်နံပါတ်/विदेशी पहचान संख्या)/ Singapore Mobile Number (စင်္ကာပူမိုဘိုင်းနံပါတ်/सिंगापुर मोबाइल नंबर)/ Home Mobile Number (အိမ်မိုဘိုင်းနံပါတ်/घर का मोबाइल नंबर) already registered! (စာရင်းသွင်းပြီးသား/पहले से ही पंजीकृत)😵")
            return redirect(url_for('index'))



        else:

        # Create Salesforce record
            record = sf.Unverified_Client__c.create({
                'Name': name,
                'DOB__c': dob,
                'Gender__c': gender,
                'FIN__c': finNum,
                'Singapore_Mobile__c': sgMobileNum,
                'Country__c': country,
                'Year_Joined__c': yearJoined,
                'Oversea_Mobile__c': homeCountryMobileNum,
                'Languages_Spoken__c': '; '.join(languages),
                'Collection_Date__c': datetime.date.today().isoformat()
            })

            # Get the new record URL
            record_url = f"https://brahmcentre.lightning.force.com/lightning/r/Unverified_Client__c/{record['id']}/view"
            flash(f"Salesforce Record URL: {record_url}")


        return render_template("success.html")

    # If receive Salesforce Malformed Request due to field validation failure
    except SalesforceMalformedRequest as e:

        error_content = e.content
        for error_dict in error_content:
            error_message = error_dict.get('message')
            if error_message:
                flash( f"{error_message}")
                return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(debug=True)
