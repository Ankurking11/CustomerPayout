import os
from flask import Flask, request, render_template, redirect, url_for, flash
import stripe


app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace with a secure key

stripe.api_key = 'sk_test_51PSyBeP2wP66hjEFi1dpTphpqHudVe6kqpCntb918jUo6yS7FuAfUIj7VrTE3dlqc98qthGyzbQANiEWhg9QVNhb00Eh245OUR'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        referral_id = request.form['referral_id']
        
        # Create a Stripe customer
        customer = stripe.Customer.create(
            name=name,
            email=email,
            phone='8292759774'
        )
        
        # Handle referral logic
        if referral_id:
            referrer_customer = stripe.Customer.retrieve(referral_id)
            if referrer_customer:
                stripe.Customer.create_balance_transaction(
                    referral_id,
                    amount=-1000,
                    currency="usd",
                    )
        
        return redirect(url_for('add_bank_details', customer_id=customer.id))

    return render_template('register.html')

@app.route('/add_bank_details/<customer_id>', methods=['GET', 'POST'])
def add_bank_details(customer_id):
    if request.method == 'POST':
        account_holder_name = request.form['account_holder_name']
        account_number = request.form['account_number']
        routing_number = request.form['routing_number']

        # Create bank account token
        bank_account = stripe.Token.create(
            bank_account={
                "country": "US",
                "currency": "usd",
                "account_holder_name": account_holder_name,
                "account_holder_type": "individual",
                "routing_number": routing_number,
                "account_number": account_number,
            },
        )

        # Attach bank account to customer
        stripe.Customer.create_source(
            customer_id,
            source=bank_account.id
           
        )
        

        return render_template('success.html')

    return render_template('add_bank_details.html', customer_id=customer_id)

if __name__ == '__main__':
    app.run(debug=True)
