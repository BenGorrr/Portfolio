from flask import Flask, render_template, request, jsonify
from models import *
from steamapi import *

app = Flask(__name__)
#config
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:76541@localhost:5432/web"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/") #Route for Index page
def index():
    return render_template("index.html")

@app.route("/projects") #Route for Project page
def project():
    return render_template("project.html")

@app.route("/steamAccstats") #Route for steamAccstats page
def steamAccstats():
    columns = ["#","Steam ID", "Username", "Password", "Community Banned", "Vac Banned", "No. Of Vac", "Days Since Last Ban", "Profile Name"]
    selColumns = ["#","Steam ID", "Username", "Vac Banned", "Profile Name"]
    accounts = Account.query.all()
    #delAcc("76561198835787127")
    return render_template("steamAccstats.html", columns=columns, selColumns=selColumns, accounts=accounts)

@app.route('/handle_new_acc', methods=['POST']) #Route for handle new account page
def handle_new_acc():
    steamID = request.form.get("steamid")
    username = request.form.get("username")
    password = request.form.get("password")
    accounts = Account.query.all()
    if validateSteamID(steamID):
        print(steamID, "is a valid ID")
        for acc in accounts:
            if(steamID == acc.steamID):
                return jsonify({'error':"ID already Exist!"})

    if (addAcc(steamID, username, password)):
        account = Account.query.get(steamID)
        #account = Account.query.filter(Account.steamID == steamID)
        print(account.steamID)
        return jsonify(steamid=account.steamID,
        username=account.username,
        password=account.password,
        community_banned=account.community_banned,
        vac_banned=account.vac_banned ,
        numberOfVACBans=account.numberOfVACBans,
        daysSinceLastBan=account.daysSinceLastBan,
        personaname=account.personaname)
        #columns = ["#","Steam ID", "Username", "Password", "Community Banned", "Vac Banned", "No. Of Vac", "Days Since Last Ban", "Profile Name"]
        #return render_template("steamAccstats.html", columns=columns, accounts=accounts)
    else:
        return jsonify({'error':"ID not found!"})

@app.route('/delete_acc', methods=['POST'])
def delete_acc():
    steamID = request.form.get("steamid")
    account = Account.query.filter(Account.steamID == steamID).delete()
    print(f"Deleted {steamID} from the Database")
    db.session.commit()
    return jsonify({'msg':"Delete Success!"})

def addAcc(steamID, username="-", password="-"):
    infos = get_Acc_Info([steamID])
    try:
        info = infos[0]
    except:
        return False
    account = Account(steamID=steamID, username=username, password=password,
                community_banned=info['CommunityBanned'], vac_banned=info['VACBanned'], numberOfVACBans=info['NumberOfVACBans'],
                daysSinceLastBan=info['DaysSinceLastBan'], personaname=info['personaname'])
    db.session.add(account)
    print(f"Added {account.steamID} into the Database")
    db.session.commit()
    return True



def delAcc():
    account = Account.query.filter(Account.steamID == steamID).delete()
    print(f"Deleted {steamID} from the Database")
    db.session.commit()

def displayAllAcc():
    accounts = Account.query.all()
    for acc in accounts:
        print(f"STEAM ID:{acc.steamID}\nUserName:{acc.username}\nPasswordL{acc.password}\n")

def main():
    #pass
    #db.create_all()
    account = Account(steamID="76561198143127438", username="-", password="-",
                community_banned=False, vac_banned=False, numberOfVACBans=0, daysSinceLastBan=0, personaname=":D")
    db.session.add(account)
    print(f"Added {account.steamID} into the Database")
    db.session.commit()

    #info = get_Acc_Info(["76561198247525724", "76561198381813642"])
    #print(info.acc_id)

if __name__ == '__main__':
    with app.app_context():
        #delAcc("76561198150922114")
        app.run(debug=True)
        #main()
