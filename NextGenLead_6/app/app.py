from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker
from database import engine, session
from models import Account, Dealer, Opportunity
import uuid
from datetime import datetime

app = Flask(__name__)

# POST: Create a new customer (opportunity)
@app.route('/new_customer', methods=['POST'])
def create_new_customer():
    payload = request.get_json()

    # Validate account_name in the account table
    account = session.query(Account).filter_by(account_name=payload.get('account_name')).first()
    if not account:
        return jsonify({"error": "Account does not exist"}), 400

    # Validate dealer information in the dealer table
    dealer = session.query(Dealer).filter_by(dealer_id=payload.get('dealer_id'),
                                             dealer_code=payload.get('dealer_code'),
                                             opportunity_owner=payload.get('dealer_name_or_opportunity_owner')).first()
    if not dealer:
        return jsonify({"error": "Dealer does not exist"}), 400

    # Insert new opportunity record
    new_opportunity = Opportunity(
        opportunity_name=payload.get('opportunity_name'),
        account_id=account.account_id,
        close_date=payload.get('close_date'),
        amount=payload.get('amount'),
        description=payload.get('description'),
        dealer_id=dealer.dealer_id,
        dealer_code=payload.get('dealer_code'),
        dealer_name_or_opportunity_owner=payload.get('dealer_name_or_opportunity_owner'),
        stage=payload.get('stage'),
        probability=payload.get('probability'),
        next_step=payload.get('next_step'),
        created_date=datetime.now()
    )

    session.add(new_opportunity)
    session.commit()

    return jsonify({"message": "Customer (opportunity) created successfully", "opportunity_id": new_opportunity.opportunity_id})

# GET: Retrieve all customers for a dealer
@app.route('/get_customers', methods=['GET'])
def get_customers():
    dealer_id = request.args.get('dealer_id')
    dealer_code = request.args.get('dealer_code')
    opportunity_owner = request.args.get('opportunity_owner')

    # Validate dealer information
    dealer = session.query(Dealer).filter_by(dealer_id=dealer_id, dealer_code=dealer_code, opportunity_owner=opportunity_owner).first()
    if not dealer:
        return jsonify({"error": "Dealer does not exist"}), 401

    # Fetch opportunities for the given dealer
    opportunities = session.query(Opportunity).filter_by(dealer_code=dealer_code).all()

    return jsonify([{
        "opportunity_name": opp.opportunity_name,
        "account_id": opp.account_id,
        "close_date": opp.close_date,
        "amount": opp.amount,
        "description": opp.description,
        "stage": opp.stage
    } for opp in opportunities])

if __name__ == '__main__':
    app.run(debug=True)
