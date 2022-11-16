from distutils.log import debug
from flask import Flask, render_template, request, redirect, url_for
import agents
from form import Order
from facts import MyFact
from experta import *
import time
import json

app = Flask(__name__, template_folder='../templates',
            static_folder="../static")
app.config['SECRET_KEY'] = 'password'

regles = []


def recherche_result(output, source):
    engine = MyFact()
    engine.rules = []
    engine.reset()

    if source == 'vehicul':
        nb_roues = output.get("nb_roues")
        nb_portes = output.get("nb_portes")
        taille = output.get("taille")
        print(int(nb_portes), taille)
        if output.get("Motor") == None:
            motor = 'no'
        else:
            motor = 'yes'

        engine.declare(
            Fact(number_wheels=int(nb_roues)),
            Fact(motor=motor),
            Fact(number_doors=int(nb_portes)),
            Fact(size=taille)
        )
    else:
        brand = output.get("brand")
        ram = output.get("ram")
        stockage = output.get("stockage")
        price = output.get("price")

        engine.declare(
            Fact(brand=brand),
            Fact(ram=int(ram)),
            Fact(stockage=int(stockage)),
            Fact(price=int(price))
        )

    engine.run()
    if source == 'vehicul':
        engine.rules.remove('os = Android')

    global regles
    regles = []
    regles = engine.rules

    print("os:", engine.os,
          "\nphone:", engine.phone,
          "\nfacts are:", engine.facts,
          "\nrules used:", engine.rules)

    if engine.resultat != '':
        the_result = engine.resultat
    else:
        the_result = 'Pas de resultat'

    return the_result


@app.route('/')
def index():
    return render_template('partie_1.html')


@app.route('/partie_1')
def partie_1():
    return render_template('partie_1.html')


@app.route('/partie_2')
def partie_2():
    return render_template('partie_2.html', erreur="")


@app.route("/vehicules", methods=(['POST', 'GET']))
def vehicul():
    the_result = ''
    if request.method == 'POST':
        print(request.form)
        if request.form.get('Rechercher') == 'Rechercher':
            the_result = recherche_result(request.form, 'vehicul')

    elif request.method == 'GET':
        the_result = "Resultat"
        global regles
        regles = []
    return render_template('vehiculs_es.html', result=the_result, request_methode=request.method)


@app.route("/phones", methods=(['POST', 'GET']))
def phone():
    the_result = ''
    if request.method == 'POST':
        print(request.form)
        if request.form.get('Rechercher') == 'Rechercher':
            the_result = recherche_result(request.form, 'phone')

    elif request.method == 'GET':
        the_result = "Resultat"
        global regles
        regles = []
    return render_template('phones_es.html', result=the_result, request_methode=request.method)


# ceci est supposé etre la fct du bouton

@app.route("/Rechercher", methods=(['POST', 'GET']))
def recherche():
    the_result = ''
    if request.method == 'POST':
        if request.form.get('Recherche') == 'Recherche':
            the_result = recherche_result(request.form)
    return render_template('vehiculs_es.html', result=the_result, request_methode=request.method)


@app.route("/regles")
def regles_page():
    global regles
    return render_template('regles.html', regles=regles)


messageSend = ""
validationMessage = ""


@app.route("/resultat_d'achat", methods=(['POST', 'GET']))
def order_result():
    # time.sleep(3)
    if request.method == 'POST':
        brand = request.form.get("brand")
        ram = request.form.get("ram")
        stockage = request.form.get("stockage")
        price = request.form.get("price")
        chargeur = request.form.get("chargeur")
        cache = request.form.get("cache")
        ecouteurs = request.form.get("ecouteurs")
        kit = request.form.get("kit")

        # Si les champs du spesifications ne sont pas tous remplient alors afficher message d'erreur
        if brand == "def" or ram == "def" or stockage == "def":
            return render_template("partie_2.html", erreur="Veuillez remplir toutes les spécifications du téléphone.")

        the_result = recherche_result(request.form, 'phone')

        # Si le systeme expert n'as aucune resultat alors afficher message d'erruer
        if the_result == "No result":
            return render_template("partie_2.html", erreur="Il n'existe pas de téléphone avec les spécifications saisies, veuillez les saisir à nouveau.")

        # Si tout est ok alors continue vers le check d'achat
        if chargeur is not None:
            chargeur = "yes"
        else:
            chargeur = "no"

        if cache is not None:
            cache = "yes"
        else:
            cache = "no"

        if ecouteurs is not None:
            ecouteurs = kit
        else:
            ecouteurs = "no"

        all_agents = agents.Agents()
        # message de checkStore
        global messageSend
        messageSend = ""
        messageSend = "phone :" + the_result + "; chargeur :" + \
            chargeur + "; cache :" + cache + "; ecouteurs :" + ecouteurs

        # message de validation_achat
        global validationMessage
        validationMessage = ""
        validationMessage = messageSend.split(";")
        validationMessage[0] += ":yes"

        validationMessage = ";".join(validationMessage)

        if not validationMessage.endswith("no"):
            validationMessage += ":yes"

        print("check:", messageSend)
        print("validation:", validationMessage)

        # pour enlever le conflit en cas de re execution
        agents.interactions = []
        agents.products_Founded = []

        all_agents.chechStore(messageSend)

        # separation des resultat obtenue des agents chaqun dans son magasin
        total_result = []

        magasin1 = {}
        magasin1 = {"magasin": '1', "accessoires": [],
                    "prix": {"remise": '0.5'}}
        magasin2 = {}
        magasin2 = {"magasin": '2', "accessoires": [],
                    "prix": {"remise": '0.65'}}
        magasin3 = {}
        magasin3 = {"magasin": '3', "accessoires": [],
                    "prix": {"remise": '0.9'}}

        total_result.extend([magasin1, magasin2, magasin3])

        for product in agents.products_Founded:
            acc = {}
            phone = {}
            if product["Name"] == "chargeur" or product["Name"] == "cache" or product["Name"] == "ecouteurs":
                acc["Name"] = product["Name"]
                if product["Name"] == "ecouteurs":
                    acc["Name"] += " " + product["type"]
                acc["prix"] = product["prix"]
            else:
                phone["Name"] = product["Name"]
                phone["ram"] = product["ram"]
                phone["stockage"] = product["stockage"]
                phone["prix"] = product["prix"]

            if phone != {}:
                total_result[int(product["magasin"]) - 1]["phone"] = phone
            if acc != {}:
                total_result[int(product["magasin"]) -
                             1]["accessoires"].append(acc)

        # calcul de remise par rapport au nombre des accessoires, et calcul de prix total avant et apres le remise
        for result in total_result:
            if "phone" in result.keys():
                prix_total = 0
                remise = float(result["prix"]["remise"]) * \
                    (len(result["accessoires"]) / 100)

                prix_total += int(result["phone"]["prix"])
                for accs in result["accessoires"]:
                    prix_total += int(accs["prix"])

                prix_apres_remise = int(prix_total - prix_total * remise)

                result["prix"]["remise"] = "{:.1f}".format(remise * 100)
                result["prix"]["total"] = str(prix_total)
                result["prix"]["prix_remise"] = str(prix_apres_remise)

        # enlever les magasin qui ne fournit pas des telephone mais juste des accessoires
        total_result = [
            result for result in total_result if "phone" in result.keys()]

        return render_template("order_result.html", total_result=total_result)


@app.route('/valider_magasin_1')
def valider_order_1():
    all_agents = agents.Agents()
    global validationMessage
    all_agents.validation_achat(validationMessage, 1)
    return render_template('valider.html', magasin='1')


@app.route('/valider_magasin_2')
def valider_order_2():
    all_agents = agents.Agents()
    global validationMessage
    all_agents.validation_achat(validationMessage, 2)
    return render_template('valider.html', magasin='2')


@app.route('/valider_magasin_3')
def valider_order_3():
    all_agents = agents.Agents()
    global validationMessage
    all_agents.validation_achat(validationMessage, 3)
    return render_template('valider.html', magasin='3')


@app.route('/interactions')
def interactions_page():
    main_interactions = []
    magasin1_interactions = []
    magasin2_interactions = []
    magasin3_interactions = []

    # separation des interactions de chaque agent
    for interaction in agents.interactions:
        if "Main" in interaction.split(':')[0]:
            main_interactions.append(interaction)

        if "Magasin1" in interaction.split(':')[0]:
            magasin1_interactions.append(interaction)

        if "Magasin2" in interaction.split(':')[0]:
            magasin2_interactions.append(interaction)

        if "Magasin3" in interaction.split(':')[0]:
            magasin3_interactions.append(interaction)

        combined_interactions = []
        combined_interactions.extend(
            [main_interactions, magasin1_interactions, magasin2_interactions, magasin3_interactions])

    return render_template('interactions.html', combined_interactions=combined_interactions)


if __name__ == '__main__':
    app.run(debug=True)
