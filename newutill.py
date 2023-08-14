import streamlit as st
import pymongo, random
from bson.objectid import ObjectId
from data import company_list

uri = st.secrets['mongo']['uri']

@st.cache_resource
def init_connection():
    return pymongo.MongoClient(uri)

client = init_connection()
db = client.stock_game

# STOCK
def initial_stock():
    documents = []
    for company in company_list:
        company_name = company['company']
        price = company['price']
        amount = company['amount']
        news = company['news'][random.randint(0,7)]['content']
        documents.append(dict([("company", company_name), ("price", price), ("amount", amount), ("news", news), ("updown_ratio", 0)]))
    db.users.delete_many({"_id": {"$ne": ObjectId(st.secrets["mongo"]["adminId"])}})
    db.user_stocks_info.delete_many({})
    db.stocks.delete_many({})
    db.stocks.insert_many(documents)
    db.users.update_many({}, {"$set": {"account": 1000000}})

def get_stock_data():
    items = db.stocks.find()
    items = list(items)
    return items

def get_stock_find_one(company):
    return db.stocks.find_one({"company": company})

def update_stock(company, update):
    return db.stocks.find_one_and_update({"company" : company}, update)

def update_stock_info():
    price = 0
    rand_num = random.randint(0,7)
    updown_ratio = 0
    for company in company_list:
        original_price = get_stock_find_one(company['company'])['price']
        if company['news'][rand_num]['진실도'] >= random.random():
            updown_ratio = company['news'][rand_num]['등락도'] * random.random() * 0.4
            price = round(company['price'] + company['price'] *  updown_ratio, -2)
            price_lowerbound = original_price - round(price * 0.3, -2)
            price_upperbound = original_price + round(price * 0.3, -2)
            if price <= price_lowerbound:
                price = price_lowerbound
            elif price >= price_upperbound:
                price = price_upperbound
        else:
            price = original_price
        updown = round((price - original_price) / original_price * 100, 1)    
        result = db.stocks.find_one_and_update(
            {"company": company['company']}, 
            {"$set": {"price" : int(price), "news" : company['news'][rand_num]['content'], "updown_ratio" : updown}})
    return result

# USERS
def create_user(id, username):
    try:
        db.users.insert_one({
            "id": int(id), "name": username, 
            "account":int(1000000)
            })
        return True
    except pymongo.errors.OperationFailure:
        print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
        return False

def get_user(id):
    user = db.users.find_one({"id": int(id)})
    if user is not None:
        return user
    else:
        return False

def get_users():
    user = db.users.find()
    return list(user)

def update_user(id, update):
    return db.users.find_one_and_update({"id": int(id)}, update)

# TRADE FUNCTION
def get_user_stock_info(user_id):
    return db.user_stocks_info.find_one({"id": int(user_id)})

def avg_stock_pice(prev_price, cur_price, amount):
    return (prev_price + cur_price) / amount

def buy_stock(user_id, company, amount):
    user_info = get_user(user_id)
    stock_info = get_stock_find_one(company)
    total = stock_info['price'] * amount

    if stock_info['amount'] >= amount and user_info['account'] >= total:
        user_stocks = db.user_stocks_info.find_one({"id": int(user_id), "stocks.company": company})
        if user_stocks:
            user_stock= [ item for item in user_stocks['stocks'] if item['company'] == company ]
            price = avg_stock_pice(user_stock[0]['total'], total, user_stock[0]['amount'] + amount)
            db.user_stocks_info.update_one(
                {"id": int(user_id), "stocks.company": company},
                {
                    "$inc": {"stocks.$.amount": amount, "stocks.$.total": total},
                    "$set": {"stocks.$.price": price}
                }
            )
        else:
            new_stock = {
                "company": company,
                "amount": amount,
                "price": stock_info['price'],
                "total": total
            }
            db.user_stocks_info.update_one(
                {"id": int(user_id)},
                {
                    "$push": {"stocks": new_stock}
                },
                upsert=True
            )
        update_stock(company, {"$inc" : {"amount" : -amount}})
        update_user(user_id, {"$inc" : {"account" : -total}})
        st.success("정상 매수되었습니다.")
    elif stock_info['amount'] == 0:
        st.error("잔여 주식수가 부족합니다.")
    else:
        st.error("잔액이 부족하거나 구매 가능 주식수량이 부족합니다.")

def sell_stock(user_id, company, amount):
    stock_info = get_stock_find_one(company)
    account_total = stock_info['price'] * amount
    result = db.user_stocks_info.find_one({"id": int(user_id), "stocks.company": company})
    if result:
        user_stock_info = [ item for item in result['stocks'] if item['company'] == company ]
        if user_stock_info:
            new_amount = user_stock_info[0]['amount'] - amount
            if new_amount == 0:
                db.user_stocks_info.update_one(
                    {"id": int(user_id)},
                    {
                        "$pull": {"stocks": {"company": company}}
                    }
                )
            elif new_amount > 0:
                total = amount * user_stock_info[0]['price']
                db.user_stocks_info.update_one(
                    {"id": int(user_id), "stocks.company": company},
                    {
                        "$inc": {"stocks.$.amount": -amount, "stocks.$.total": -total}
                    }
                )
            else:
                st.error("보유한 주식수량 보다 매도수량이 더 많습니다.")
                return
            update_stock(company, {"$inc" : {"amount" : amount}})
            update_user(user_id, {"$inc" : {"account" : account_total}})
            st.success("정상매도 되었습니다.")
    else:
        st.error("해당 주식을 소유하고 있지 않습니다.")