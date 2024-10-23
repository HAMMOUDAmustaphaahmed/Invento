from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timezone
import os
from sqlalchemy import text
from sqlalchemy import Numeric

app = Flask(__name__)

# Database configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key_here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'mysql+pymysql://root:@localhost:3306/glpp')  # Make sure to use pymysql
db = SQLAlchemy(app)
app.config['SQLALCHEMY_ECHO'] = True



class Message(db.Model):
    __tablename__ = 'messages'
    
    id_message = db.Column(db.Integer, primary_key=True, autoincrement=True)
    expéditeur = db.Column(db.String(255), nullable=False)    # Le username de l'expéditeur
    destinataire = db.Column(db.String(255), nullable=False)  # Le username du destinataire principal
    cc = db.Column(db.String(255))            # Liste de usernames séparés par des virgules pour CC
    objet = db.Column(db.String(255), nullable=False)         # Objet du message
    corps = db.Column(db.Text, nullable=False)                 # Le corps du message
    emplacement = db.Column(db.String(255), nullable=False)   # Emplacement du message (lié à l'utilisateur)
    date_envoi = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    est_lu = db.Column(db.Boolean, default=False)             # Indique si le message a été lu

    def __repr__(self):
        return f'<Message {self.objet} from {self.expéditeur} to {self.destinataire}>'


# User model based on the table structure
class User(db.Model):  # Changed class name to User (singular) for clarity
    __tablename__ = 'user'  # Explicitly set the table name

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    emplacement = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)




from functools import wraps

# Décorateur pour restreindre l'accès basé sur les rôles d'utilisateur
def roles_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = session.get('role', None)  # ou utiliser une autre clé si tu stockes différemment
            # Vérifier si l'utilisateur est connecté
            if user_role == None:
                
                return render_template('404.html')  # Rediriger vers la page de connexion
            
            # Récupérer le rôle de l'utilisateur depuis la session
            
            
            # Vérifier si le rôle de l'utilisateur est dans les rôles autorisés
            if user_role not in roles:
                return render_template('404.html')  # Rediriger vers la page d'accueil ou une autre page
            
            return f(*args, **kwargs)
        return decorated_function
    return wrapper


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/maps')
@roles_required('admin','manager','user','achat','responsable')
def maps():
    return render_template('maps.html') 


@app.route('/add_user', methods=['POST'])
@roles_required('admin','manager')
def add_user():
    username = request.form['username']
    password = request.form['password']
    emplacement = request.form['emplacement']
    role = request.form['role']
    
    # Hash the password using generate_password_hash
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')


    # Create new user instance
    new_user = User(username=username, password=hashed_password, emplacement=emplacement, role=role)
    
    db.session.add(new_user)  # Add the new user to the session
    db.session.commit()  # Commit the session to save to the database
    
    flash('User added successfully!', 'success')  # Flash success message
    return redirect(url_for('admin'))

@app.route('/search_user', methods=['GET'])
@roles_required('admin','manager','user','achat','responsable')
def search_user():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()

    if user:
        # Retourner les informations de l'utilisateur
        return jsonify({
            'exists': True,
            'data': {
                'username': user.username,
                'emplacement': user.emplacement,
                'role': user.role
            }
        })
    else:
        return jsonify({'exists': False})


@app.route('/get_user_info', methods=['GET'])
@roles_required('admin','manager','user','achat','responsable')
def get_user_info():
    username = request.args.get('username')  # Prend le nom d'utilisateur depuis les arguments GET
    user = User.query.filter_by(username=username).first()

    if user:
        # Retourner les informations de l'utilisateur en JSON
        return jsonify({
            'id': user.id,
            'username': user.username,
            'emplacement': user.emplacement,
            'role': user.role
        })
    else:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404



@app.route('/edit_user', methods=['POST'])
@roles_required('admin','manager')
def edit_user():
    data = request.get_json()

    username = data.get('username')
    emplacement = data.get('emplacement')
    role = data.get('role')
    password = data.get('password')

    # Vérifier si l'utilisateur existe dans la base de données
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404

    # Mettre à jour les champs avec les nouvelles données
    user.emplacement = emplacement
    user.role = role
    
    # Mettre à jour le mot de passe si un nouveau mot de passe est fourni
    if password:
        hashed_password = generate_password_hash(password)  # Hachage du nouveau mot de passe
        user.password = hashed_password

    try:
        # Sauvegarder les modifications dans la base de données
        db.session.commit()
        return jsonify({'success': 'Utilisateur mis à jour avec succès !'})
    except Exception as e:
        db.session.rollback()  # En cas d'erreur, annuler les modifications
        return jsonify({'error': f'Erreur lors de la mise à jour : {str(e)}'}), 500

@app.route('/delete_user', methods=['DELETE'])
@roles_required('admin','manager')

def delete_user():
    data = request.get_json()  # Getting the JSON data from the request
    username = data.get('username')  # Extracting the username from the JSON payload

    # Find the user by username
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': 'Utilisateur supprimé avec succès !'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erreur lors de la suppression de l\'utilisateur: {str(e)}'}), 500


class Article(db.Model):
    __tablename__ = 'articles'
    
    id_article = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code_article = db.Column(db.String(20), nullable=False)
    libelle_article = db.Column(db.String(255), nullable=False)
    prix_achat = db.Column(db.Float, nullable=False)
    emplacement = db.Column(db.String(255), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    fournisseur = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    quantite_min=db.Column(db.Integer, nullable=False)

@app.route('/get_low_stock_count', methods=['GET'])
@roles_required('admin','manager','user','achat','responsable')
def get_low_stock_count():
    user_emplacement = session.get('emplacement')  # Récupérer l'emplacement de l'utilisateur
    user_role = session.get('role')  # Récupérer le rôle de l'utilisateur
    
    print(user_emplacement,user_role)
    # Si l'utilisateur est admin ou manager, il voit tous les articles en faible stock
    if user_role in ['admin', 'manager']:
        low_stock_count = Article.query.filter(Article.quantite <= Article.quantite_min).count()
        print(str(low_stock_count))
    else:
        # Filtrer les articles uniquement pour l'emplacement de l'utilisateur
        low_stock_count = Article.query.filter(
            Article.emplacement == user_emplacement,
            Article.quantite <= Article.quantite_min
        ).count()
        print(str(low_stock_count))

   
    
    # Retourner directement le nombre d'articles en faible stock
    return str(low_stock_count)  # Retourne une chaîne de caractères pour être utilisé directement dans HTML


@app.route('/get_low_stock_articles', methods=['GET'])
@roles_required('admin', 'manager', 'user', 'achat', 'responsable')
def get_low_stock_articles():
    user_emplacement = session.get('emplacement')  # Récupérer l'emplacement de l'utilisateur
    user_role = session.get('role')  # Récupérer le rôle de l'utilisateur

    # Si l'utilisateur est admin ou manager, il voit tous les articles en faible stock
    if user_role in ['admin', 'manager']:
        low_stock_articles = Article.query.filter(Article.quantite <= Article.quantite_min).all()
    else:
        # Filtrer les articles uniquement pour l'emplacement de l'utilisateur
        low_stock_articles = Article.query.filter(
            Article.emplacement == user_emplacement,
            Article.quantite <= Article.quantite_min
        ).all()

    # Formater les articles en une liste de dictionnaires
    articles = [{
        'code_article': article.code_article,
        'libelle': article.libelle_article,
        'quantite': article.quantite,
        'quantite_min': article.quantite_min
    } for article in low_stock_articles]

    # Retourner les articles au format JSON
    return jsonify({'articles': articles})





@app.route('/fetch_codes_articles', methods=['GET'])
@roles_required('admin','manager','user','achat','responsable')
def fetch_codes_articles():
    input_value = request.args.get('input')
    # Utiliser LIKE pour filtrer tous les articles qui commencent par l'input
    articles = Article.query.filter(Article.code_article.like(f'{input_value}%')).all()

    # Créer une liste de dictionnaires avec code_article et libelle_article
    results = [{'code_article': article.code_article, 'libelle_article': article.libelle_article} for article in articles]
    
    return jsonify(results)



@app.route('/get_article_info', methods=['GET'])
@roles_required('admin','manager','user','achat','responsable')
def get_article_info():
    code_article = request.args.get('code_article')  # Récupérer l'article via son code
    article = Article.query.filter_by(code_article=code_article).first()

    if article:
        # Retourner les informations de l'article en JSON
        return jsonify({
            'id': article.id_article,
            'code_article': article.code_article,
            'libelle_article': article.libelle_article,
            'quantite': article.quantite,
            'prix_achat': article.prix_achat
        })
    else:
        return jsonify({'error': 'Article non trouvé'}), 404




@app.route('/get_usine_info', methods=['GET','POST'])
@roles_required('admin','manager','user','achat','responsable')
def get_usine_info():
    nom_usine = request.args.get('nom_usine')  # Récupérer l'article via son code
    usine = Usine.query.filter_by(nom_usine=nom_usine).first()

    if usine:
        # Retourner les informations de l'article en JSON
        return jsonify({
            
            'nom_usine': usine.nom_usine,
            'region': usine.region,
            'addresse': usine.addresse,
            'telephone': usine.telephone,
            'etat': usine.etat,
            'role': usine.role

        })
    else:
        return jsonify({'error': 'Usine non trouvé'}), 404

@app.route('/edit_usine', methods=['POST'])
@roles_required('admin','manager','user','achat','responsable')
@roles_required('admin','manager')
def edit_usine():
    data = request.get_json()
   
    # Utiliser l'ID de l'usine pour rechercher dans la base de données
    nom_usine = data.get('nom_usine')
    if not nom_usine:
        return jsonify({'error': 'ID de l\'usine manquant'}), 400

    usine = Usine.query.filter_by(nom_usine=nom_usine).first()
    
    if not usine:
        return jsonify({'error': 'Usine non trouvée'}), 404

    # Mettre à jour les champs de l'usine
    usine.nom_usine = data.get('nom_usine')
    usine.region = data.get('region')
    usine.addresse = data.get('addresse')
    usine.telephone = data.get('telephone')
    usine.etat = data.get('etat')
    usine.role = data.get('role')
    
    try:
        # Sauvegarder les modifications dans la base de données
        db.session.commit()
        return jsonify({'success': 'Usine mise à jour avec succès !'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erreur lors de la mise à jour : {str(e)}'}), 500

# Route pour afficher le formulaire d'ajout d'usine
@app.route('/add_usine', methods=['GET', 'POST'])
@roles_required('admin','manager')
def add_usine():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom_usine = request.form.get('nom_usine')
        region = request.form.get('region')
        addresse = request.form.get('addresse')
        telephone = request.form.get('telephone')
        etat = request.form.get('etat')
        role = request.form.get('role')

        # Vérifier si l'usine existe déjà
        usine_existante = Usine.query.filter_by(nom_usine=nom_usine).first()
        if usine_existante:
            flash(f"L'usine {nom_usine} existe déjà.", 'error')
            return redirect(url_for('add_usine'))

        # Créer une nouvelle usine
        nouvelle_usine = Usine(
            nom_usine=nom_usine,
            region=region,
            addresse=addresse,
            telephone=telephone,
            etat=etat,
            role=role
        )

        try:
            # Ajouter la nouvelle usine dans la base de données
            db.session.add(nouvelle_usine)
            db.session.commit()
            flash(f'Usine {nom_usine} ajoutée avec succès!', 'success')
            return jsonify({'success': 'Usine mise à jour avec succès !'})
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de l'ajout de l'usine : {str(e)}", 'error')
            return jsonify({"error": f"Erreur lors de l'ajout de l'usine : {str(e)}"}), 500
    return render_template('admin.html')


@app.route('/delete_usine', methods=['POST'])
@roles_required('admin')
def delete_usine():
    nom_usine = request.form.get('nom-usine')

    # Logique pour supprimer l'usine de la base de données
    usine = Usine.query.filter_by(nom_usine=nom_usine).first()
    if usine:
        db.session.delete(usine)
        db.session.commit()
        flash("Usine supprimée avec succès!", "success")
    else:
        flash("L'ID de l'usine n'existe pas!", "error")

    return redirect(request.referrer)



@app.route('/edit_article', methods=['POST'])
@roles_required('admin','manager')
def edit_article():
    data = request.get_json()

    # Utilise l'ID de l'article pour rechercher dans la base de données
    id_article = data.get('id_article')
    code_article = data.get('code_article')
    libelle_article = data.get('libelle_article')
    quantite = data.get('quantite')
    prix_achat = data.get('prix_achat')
    
    print(id_article,code_article,libelle_article,quantite,prix_achat)
    # Vérifier si l'article existe via l'ID
    article = Article.query.filter_by(code_article=code_article).first()

    if not article:
        return jsonify({'error': 'Article non trouvé'}), 404

    # Mettre à jour les champs de l'article
    article.code_article = code_article
    article.libelle_article = libelle_article
    article.quantite = quantite
    article.prix_achat = prix_achat
    
    try:
        # Sauvegarder les modifications dans la base de données
        db.session.commit()
        return jsonify({'success': 'Article mis à jour avec succès !'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erreur lors de la mise à jour : {str(e)}'}), 500


@app.route('/delete_article', methods=['DELETE'])
@roles_required('admin','manager')
def delete_article():
    data = request.get_json()  # Récupère les données JSON
    code_article = data.get('code_article')  # Récupère le code de l'article

    if not code_article:
        return jsonify({'error': 'Code d\'article manquant'}), 400

    article = Article.query.filter_by(code_article=code_article).first()

    if not article:
        return jsonify({'error': 'Article non trouvé'}), 404

    try:
        db.session.delete(article)
        db.session.commit()
        return jsonify({'success': 'Article supprimé avec succès !'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erreur lors de la suppression: {str(e)}'}), 500


@app.route('/add_article', methods=['POST'])
@roles_required('admin','manager','user','achat','responsable')
@roles_required('admin','manager')
def add_article():
    try:
        data = request.get_json()  # Ou request.form si vous choisissez l'option 2
        new_article = Article(
            code_article=data['code_article'],
            libelle_article=data['libelle_article'],
            prix_achat=data['prix_achat'],
            emplacement=data['emplacement'],
            quantite=data['quantite'],
            fournisseur=data['fournisseur'],
            quantite_min=data['quantite_min']

        )
        db.session.add(new_article)
        db.session.commit()
        return jsonify(success=True)
    except Exception as e:
        db.session.rollback()  # Assurez-vous de revenir à l'état précédent en cas d'erreur
        return jsonify(success=False, error=str(e)), 400


from sqlalchemy import or_
from datetime import datetime


@app.route('/search_articles', methods=['POST'])
@roles_required('admin','manager','user','achat','responsable')
def search_articles():
    search_query = request.form.get('search_query', '')
    date_debut = request.form.get('date_debut', None)
    date_fin = request.form.get('date_fin', None)

    # Initialiser les résultats
    results = Article.query

    if search_query:
        results = results.filter(
            or_(
                Article.code_article.like(f'{search_query}%'),
                Article.libelle_article.like(f'{search_query}%')
            )
        )

    # Filtrer par date si les dates sont fournies
    if date_debut:
        date_debut = datetime.strptime(date_debut, '%Y-%m-%d')
        results = results.filter(Article.date >= date_debut)

    if date_fin:
        date_fin = datetime.strptime(date_fin, '%Y-%m-%d')
        results = results.filter(Article.date <= date_fin)

    # Exécuter la requête pour obtenir les articles filtrés
    articles = results.all()

    # Créer la liste des articles à renvoyer
    articles_list = []
    for article in articles:
        articles_list.append({
            'code_article': article.code_article,
            'libelle_article': article.libelle_article,
            'prix_achat': article.prix_achat,
            'quantite': article.quantite,
            'fournisseur': article.fournisseur,
            'date': article.date.strftime('%Y-%m-%d %H:%M:%S'),  # Formatage de la date
        })

    return jsonify({'articles': articles_list})


class Fournisseur(db.Model):
    __tablename__ = 'fournisseur'
    
    id_fournisseur = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom_fournisseur = db.Column(db.String(255), nullable=False)
    matricule_fiscale = db.Column(db.String(50), nullable=True)
    addresse = db.Column(db.String(50), nullable=True)
    telephone = db.Column(db.String(50), nullable=True)
    
@app.route('/search_fournisseur', methods=['POST'])
@roles_required('admin','manager','user','achat','responsable')
def search_fournisseur():
    input_value = request.form['fournisseur']  # Récupérer le mot saisi par l'utilisateur
    fournisseurs = Fournisseur.query.filter(Fournisseur.nom_fournisseur.ilike(f'{input_value}%')).all()

    # Retourner les résultats au format JSON pour les afficher dans le datalist
    fournisseur_list = [{"nom_fournisseur": f.nom_fournisseur} for f in fournisseurs]
    return jsonify(fournisseur_list)


@app.route('/add_fournisseur', methods=['POST'])
@roles_required('admin','manager','achat')
def add_fournisseur():
    nom_fournisseur = request.form['nom_fournisseur']
    matricule_fiscale = request.form['matricule_fiscale']
    addresse = request.form['addresse']
    telephone = request.form['telephone']
    try:
        new_fournisseur = Fournisseur(nom_fournisseur=nom_fournisseur,matricule_fiscale=matricule_fiscale,addresse=addresse,telephone=telephone)
        db.session.add(new_fournisseur)
        db.session.commit()
        flash('Fournisseur ajoutée avec succès !', 'success')  # Ajoutez une classe de message
        return redirect(url_for('admin'))
    except Exception as e:
        db.session.rollback()
        flash('Une erreur est survenue : ' + str(e), 'error')  # Ajoutez une classe de message
        return jsonify({'message': 'Une erreur est survenue : ' + str(e)}), 500


class DemandeAchat(db.Model):
    __tablename__ = 'demande_d_achat'
    
    code_demande = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code_article = db.Column(db.String(255), nullable=False)
    libelle_article = db.Column(db.String(255), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    emplacement = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    demandeur = db.Column(db.String(255), nullable=False)
    etat = db.Column(db.Integer, nullable=True) # 1: En cours, 0: Approuvé, 2: Annulé
    reception = db.Column(db.Integer, nullable=False) # 1: Non reçu, 0: Reçu
    Fournisseur = db.Column(db.String(255), nullable=False)
    prix_achat = db.Column(db.Integer, nullable=True)


@app.route('/add_demande_achat', methods=['POST'])
@roles_required('admin','manager','user','achat','responsable')
def add_demande_achat():
    code_article = request.form['code_article']
    libelle_article = request.form['libelle_article']
    quantite = request.form['quantite']
    emplacement=session.get('emplacement')
    
    try:
        # Date de création de la demande d'achat
        date_creation = datetime.now(timezone.utc)

        # Créer la nouvelle demande d'achat
        new_demande = DemandeAchat(
            code_article=code_article,
            libelle_article=libelle_article,
            quantite=quantite,
            emplacement=emplacement,  # Utilise l'emplacement de la session
            date=date_creation,  # Utilise la même date pour la demande
            demandeur='user',  # Utilise le demandeur de la session
            etat=1,
            reception=0
        )
        
        db.session.add(new_demande)
        db.session.commit()

        # Appel de la fonction create_demande() pour enregistrer l'action dans l'historique
        history_create_demande(
            code_demande=new_demande.code_demande,  # ID de la demande nouvellement créée
            code_article=new_demande.code_article,
            libelle_article=new_demande.libelle_article,
            quantite=new_demande.quantite,
            emplacement=new_demande.emplacement,
            user=new_demande.demandeur,
            date_action=date_creation,
            date_approuver_demande=datetime.now(timezone.utc),
            date_reception=datetime.now(timezone.utc)  # Passe la même date de création
        )

        flash('Demande ajoutée avec succès !')
        return redirect(url_for('user'))
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Une erreur est survenue : ' + str(e)}), 500


@app.route('/search_demandes_achat', methods=['GET'])
@roles_required('admin','manager','user','achat','responsable')
def search_demandes_achat():
    query = request.args.get('query', '')
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')

    demandes = DemandeAchat.query

    if query:
        demandes = demandes.filter(DemandeAchat.libelle_article.like(f'%{query}%'))

    if start_date and end_date:
        demandes = demandes.filter(DemandeAchat.date.between(start_date, end_date))

    demandes = demandes.all()

    # Préparer les résultats sous forme de dictionnaire JSON
    result = [{
        'code_article': demande.code_article,
        'libelle_article': demande.libelle_article,
        'quantite': demande.quantite,
        'emplacement': demande.emplacement,
        'demandeur': demande.demandeur,
        'date': demande.date.strftime('%Y-%m-%d')
    } for demande in demandes]

    return jsonify(result)

class Achats(db.Model):
    __tablename__ = 'achats'
    
    code_demande = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code_article = db.Column(db.Integer, nullable=False)
    libelle_article = db.Column(db.String(255), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    prix_achat = db.Column(db.Float, nullable=False)
    emplacement = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    fournisseur = db.Column(db.String(255), nullable=False)




def get_count_articles_attente_expedition():
    counter = DemandeVente.query.filter_by(etat=0 ,reception=1).count()
    
    return str(counter) if counter else 0

def get_count_articles_attente_arrive():
    counter = DemandeAchat.query.filter_by(etat=0 ,reception=1).count()
    
    return str(counter) if counter else 0


@app.route('/total_sales')
@roles_required('admin','manager','responsable','user','achat')
def total_sales():
    # Calculate the total sales by summing prix_achat * quantite for all articles
    total = db.session.query(db.func.sum(Article.prix_achat * Article.quantite)).scalar() or 0
    return jsonify({'total_sales': total})  # Return the total sales as JSON


def get_articles_count():
    count=Article.query.count()
    return str(count)  # This returns the count of all articles

@app.route('/articles_count')
@roles_required('admin','manager','responsable','user','achat')
def articles_count():
    count = get_articles_count()
    return jsonify({'articles_count': count})



@app.route('/recent_orders')
@roles_required('admin','manager','responsable','user','achat')
def recent_orders():
    user_emplacement = session.get('emplacement')  # Récupérer l'emplacement de l'utilisateur
    user_role = session.get('role')  # Récupérer le rôle de l'utilisateur
    

    # Si l'utilisateur est admin ou manager, il voit tous les articles en faible stock
    if user_role in ['admin', 'manager']:
        # Fetch the 5 most recent articles/orders
       recent_orders = Article.query.order_by(Article.date.desc()).limit(10).all()
    else:
        recent_orders = Article.query.filter(Article.emplacement == user_emplacement).order_by(Article.date.desc()).limit(10).all()
        
    # Format the orders data into a list of dictionaries
    orders_data = [
        {
            'id_article': order.id_article,
            'code_article': order.code_article,
            'libelle_article': order.libelle_article,  # Replace with libelle_article
            'date_order': order.date.strftime('%d-%m-%Y'),  # Format the date
            'emplacement': order.emplacement,
            'quantite': order.quantite
        }
        for order in recent_orders
    ]
    
    return jsonify(orders_data)  # Return the recent orders as JSON



class Vente(db.Model):
    __tablename__ = 'ventes'

    id_vente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code_demande = db.Column(db.Integer, nullable=True)
    code_article = db.Column(db.Integer, nullable=True)
    libelle_article = db.Column(db.String(20), nullable=True)
    quantite = db.Column(db.Integer, nullable=True)
    prix_vente = db.Column(Numeric(6,3), nullable=True)
    emplacement = db.Column(db.String(20), nullable=True)
    vers = db.Column(db.String(20), nullable=True)

    demandeur = db.Column(db.String(20), nullable=True)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, code_demande, code_article, libelle_article, quantite, prix_vente, emplacement, vers, demandeur):
        self.code_demande = code_demande
        self.code_article = code_article
        self.libelle_article = libelle_article
        self.quantite = quantite
        self.prix_vente = prix_vente
        self.emplacement = emplacement
        self.vers=vers
        self.demandeur = demandeur


@app.route('/recent_sales')
@roles_required('admin','manager','responsable','user','achat')
def recent_sales():
    user_emplacement = session.get('emplacement')  # Récupérer l'emplacement de l'utilisateur
    user_role = session.get('role')  # Récupérer le rôle de l'utilisateur

    # Si l'utilisateur est admin ou manager, il voit tous les articles en faible stock
    if user_role in ['admin', 'manager']:
    # Fetch the 10 most recent sales
        recent_sales = Vente.query.order_by(Vente.date.desc()).limit(10).all()
    else:
    # Join Vente with Article on the code_article column
        recent_sales = Vente.query.filter_by(emplacement=user_emplacement).order_by(Vente.date.desc()).limit(10)
    

    
    sales_data = [
        {
            'code_demande': sale.code_demande,
            'code_article': sale.code_article,
            'libelle_article': sale.libelle_article,
            'quantite': sale.quantite,
            'prix_vente': sale.prix_vente,
            'emplacement': sale.emplacement,
            'vers': sale.vers,
            'demandeur':sale.demandeur,
            'date': sale.date
        }
        for sale in recent_sales
    ]
    return jsonify(sales_data)


@app.route('/recent_buys')
@roles_required('admin','manager','responsable','user','achat')
def recent_buys():
    user_emplacement = session.get('emplacement')  # Récupérer l'emplacement de l'utilisateur
    user_role = session.get('role')  # Récupérer le rôle de l'utilisateur

    # Si l'utilisateur est admin ou manager, il voit tous les articles en faible stock
    if user_role in ['admin', 'manager']:
        # Fetch the 5 most recent articles/orders
       recent_buys = Achats.query.order_by(Achats.date.desc()).limit(10).all()
    else:
        recent_buys = Achats.query.filter_by(
            Article.emplacement == user_emplacement).order_by(
                Achats.date.desc()).limit(10).all()
        
    
    buys_data = [
        {
            'code_demande': buy.code_demande,
            'code_article': buy.code_article,
            'libelle_article': buy.libelle_article,
            'quantite': buy.quantite,
            'prix_vente': buy.prix_achat,
            'emplacement': buy.emplacement,
            'date': buy.date,
            'fournisseur':buy.fournisseur
        }
        for buy in recent_buys
    ]

    return jsonify(buys_data)

class DemandeVente(db.Model):
    __tablename__ = 'demande_vente'
    code_demande = db.Column(db.Integer, primary_key=True)
    code_article = db.Column(db.String(50), nullable=False)
    libelle_article = db.Column(db.String(20), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    prix_vente=db.Column(Numeric(6,3), nullable=True)
    emplacement = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    demandeur = db.Column(db.String(20), nullable=True)
    vers = db.Column(db.String(20), nullable=True)
    commande = db.Column(db.String(20), nullable=True)
    etat = db.Column(db.Integer, nullable=False)
    reception = db.Column(db.Integer, nullable=False)
    commentaire = db.Column(db.String(255), nullable=True)  # Ajout de la colonne Commentaire



@app.route('/add_inventaire', methods=['POST'])
@roles_required('admin','manager','responsable','user','achat')
def add_inventaire():
    code_article = request.form['code_article']
    libelle_article = request.form['libelle_article']
    quantite = request.form['quantite']
    vers = request.form['vers']
    commande = request.form['commande']
    
    quantite_demandee = int(quantite)

    # Étape 1 : Calculer la quantité totale disponible pour cet article (code_article) dans le magasin
    articles = Article.query.filter_by(code_article=code_article).all()
    quantite_disponible = sum(article.quantite for article in articles)  # Somme des quantités disponibles

    # Étape 2 : Comparer la quantité disponible à la quantité demandée
    if quantite_disponible >= quantite_demandee:

        try:
            new_demande = DemandeVente(
                code_article=code_article,
                libelle_article=libelle_article,
                quantite=quantite,
                emplacement='sahel',  # Utilise l'emplacement de la session
                date=datetime.now(timezone.utc),
                demandeur='user',  # Utilise le demandeur de la session
                vers=vers,
                commande=commande,
                etat=1,
                reception=0
            )
            
            db.session.add(new_demande)
            db.session.commit()
            flash('Demande ajoutée avec succès !')
            return redirect(url_for('user'))
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Une erreur est survenue : ' + str(e)}), 500
    else:
        return('<script>alert("La quantité est insuffisante")</script>')



class History(db.Model):
    __tablename__ = 'history'

    id_history = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code_demande = db.Column(db.Integer, nullable=True)
    code_article = db.Column(db.String(50), nullable=True)
    libelle_article = db.Column(db.String(255), nullable=True)
    quantite = db.Column(db.Integer, nullable=True)
    prix = db.Column(db.Float, nullable=True)
    fournisseur = db.Column(db.String(20), nullable=True)
    emplacement = db.Column(db.String(20), nullable=True)
    action = db.Column(db.String(50), nullable=True)
    user = db.Column(db.String(20), nullable=True)
    details = db.Column(db.String(255), nullable=True)
    usine = db.Column(db.String(20), nullable=True)
    date_action = db.Column(db.TIMESTAMP, nullable=True)
    date_approuver_demande = db.Column(db.TIMESTAMP, nullable=True)
    date_reception = db.Column(db.TIMESTAMP, nullable=True)

    def __init__(self, code_demande, code_article=None, libelle_article=None, quantite=None, prix=None,
                 fournisseur=None, emplacement=None, action=None, user=None, details=None, usine=None,
                 date_action=None, date_approuver_demande=None, date_reception=None):
        self.code_demande = code_demande
        self.code_article = code_article
        self.libelle_article = libelle_article
        self.quantite = quantite
        self.prix = prix
        self.fournisseur = fournisseur
        self.emplacement = emplacement
        self.action = action
        self.user = user
        self.details = details
        self.usine = usine
        self.date_action = date_action 
        self.date_approuver_demande= date_approuver_demande
        self.date_reception=date_reception



class Usine(db.Model):
    __tablename__ = 'usine'
    id_usine = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom_usine = db.Column(db.String(20), nullable=False)
    region = db.Column(db.String(20), nullable=False)
    addresse = db.Column(db.String(20), nullable=True)
    latitude = db.Column(db.String(20), nullable=True)
    longitude = db.Column(db.String(20), nullable=True)
    telephone = db.Column(db.String(20), nullable=True)
    etat = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f'<Usine {self.nom_usine}>'

@app.route('/fetch_usines', methods=['GET'])
@roles_required('admin','manager','user','achat','responsable')
def fetch_usines():
    input_value = request.args.get('input', '')
    usines = Usine.query.filter(Usine.nom_usine.ilike(f'{input_value}%')).all()

    usine_list = []
    for usine in usines:
        usine_list.append({
            'nom_usine': usine.nom_usine,
            'region': usine.region,
            'latitude': usine.latitude,
            'longitude': usine.longitude,
            'addresse': usine.addresse
        })

    return jsonify(usine_list)


@app.route('/search_usine', methods=['GET'])
@roles_required('admin','manager','user','achat','responsable')
def search_usine():
    query = request.args.get('query', '')
    results = Usine.query.filter(Usine.nom_usine.like(f'{query}%')).all()
    return jsonify([{'id_usine': usine.id_usine, 'nom_usine': usine.nom_usine} for usine in results])


@app.route('/', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        

        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username.strip()).first()  # Get user by username
        
        # Check if user exists and the password matches
        if user and check_password_hash(user.password, password):  # Direct comparison since passwords are in plaintext
            session['logged_in'] = True
            session['username'] = user.username
            session['emplacement']=user.emplacement
            session['role']=user.role



            username = session.get('username')
            emplacement = session.get('emplacement')
            role = session.get('role')



            if user.role.lower() == 'admin' :
                return redirect(url_for('admin'))  # Redirect to the admin page
            elif user.role.lower() == 'user' : 
                return (redirect(url_for('user')))
            elif user.role.lower() == 'achat' : 
                return redirect(url_for('service_achat_vente'))
            elif user.role.lower() == 'responsablesahel' : 
                 return redirect(url_for('user'))
            elif user.role.lower() == 'responsablegafsa' : 
                 return redirect(url_for('user'))
            elif user.role.lower() == 'responsablekasserine' : 
                 return redirect(url_for('user'))
            elif user.role.lower() == 'manager' : 
                 return redirect(url_for('manager'))
            else:
                flash('Access not allowed for this role.', 'danger')
        else:
            flash('Invalid username or password.', 'danger')
            return jsonify({'message': 'Invalid credentials'}), 401
    
    return render_template('login.html')


@app.route('/manager')
@roles_required('admin','manager')


def manager():
    low_stock_count=get_low_stock_count()
    
    count_ventes_attente_expedition=get_count_articles_attente_expedition()
    count_ventes_attente_arrive=get_count_articles_attente_arrive()
    count = get_orders_count()
    user_count = User.query.count()
    articles_count=get_articles_count()
    sales_count = DemandeVente.query.filter_by(etat=1).count()    
    return render_template('manager.html',low_stock_count=low_stock_count,orders_count=count,count_ventes_attente_arrive=count_ventes_attente_arrive,count_ventes_attente_expedition=count_ventes_attente_expedition,user_count=user_count,articles_count=articles_count,sales_count=sales_count)


@app.route('/responsable')
def responsable():
    
    
    # Récupérer l'emplacement du responsable depuis la session
    emplacement_responsable = session['emplacement']
    username=session['username']
    
    if emplacement_responsable:
        # Filtrer les articles et commandes par emplacement
        recent_orders_vente = DemandeVente.query.filter_by(emplacement=emplacement_responsable).order_by(DemandeVente.date.desc()).all()
        recent_orders_achat = DemandeAchat.query.filter_by(emplacement=emplacement_responsable).order_by(DemandeAchat.date.desc()).all()
        recent_articles = Article.query.filter_by(emplacement=emplacement_responsable).order_by(Article.date.desc()).all()
        
        return render_template('responsable.html', 
                               orders_vente=recent_orders_vente, 
                               orders_achat=recent_orders_achat, 
                               articles=recent_articles, 
                               responsable=username,
                               low_stock_count=str(get_low_stock_count()))
    else:
        flash('Accès refusé : responsable non trouvé.', 'danger')
        return redirect(url_for('login'))


@app.route('/fournisseurs')
@roles_required('admin','manager','responsable','user','achat')

def fournisseurs():
    fournisseurs = Fournisseur.query.all()  # Fetch all fournisseurs
    data = [{
        'nom_fournisseur': f.nom_fournisseur,
        'matricule_fiscale': f.matricule_fiscale,
        'addresse': f.addresse,
        'telephone': f.telephone
    } for f in fournisseurs]
    return jsonify(data)


@app.route('/user', methods=['GET'])
@roles_required('admin','user',)

def user():
    user_emplacement=session.get('emplacement')
    low_stock_count=get_low_stock_count()
    count_ventes_attente_expedition=get_count_articles_attente_expedition()
    count_ventes_attente_arrive=get_count_articles_attente_arrive()
    count = get_orders_count()
    sales_count = DemandeVente.query.filter_by(etat=1,emplacement=user_emplacement).count()
    return render_template('user.html',low_stock_count=low_stock_count,orders_count=count, sales_count=sales_count,count_ventes_attente_expedition=count_ventes_attente_expedition,count_ventes_attente_arrive=count_ventes_attente_arrive)




@app.route('/admin')
@roles_required('admin')

def admin():
    
    count_ventes_attente_expedition=get_count_articles_attente_expedition()
    count_ventes_attente_arrive=get_count_articles_attente_arrive()
    count = get_orders_count()
    user_count = User.query.count()
    articles_count=get_articles_count()
    sales_count = DemandeVente.query.filter_by(etat=1).count()
    low_stock_count = get_low_stock_count()
    response = make_response(render_template('admin.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return render_template('admin.html',low_stock_count=low_stock_count, count_ventes_attente_arrive=count_ventes_attente_arrive,count_ventes_attente_expedition=count_ventes_attente_expedition,sales_count=sales_count,response = response,articles_count=articles_count, orders_count=count, user_count=user_count)


@app.route('/logout', methods=['POST','GET'])
def logout():
    session.clear()  # Clear the session
    flash('Vous avez été déconnecté.', 'info')  # Flash message
    return redirect(url_for('login'))  # Redirect to login

class CounterTable(db.Model):
    __tablename__ = 'counter_table'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    count_value = db.Column(db.Integer, nullable=True, default=0)

@app.route('/orders_count')
@roles_required('admin','manager','user','achat','responsable')
def orders_count():
    count = get_orders_count()  # Call your function that fetches the count
    print(count)
    return int(count)  # Pass the count to the template

def get_orders_count():
    counter = CounterTable.query.first()  # Get the first row
    return counter.count_value if counter else 0



@app.route('/pending_buys')
@roles_required('admin','manager','user','achat','responsable')
def pending_buys():

    user_role=session.get('role')
    user_emplacement=session.get('emplacement')

    if user_role in ['admin','manager','achat']:
        buys = DemandeAchat.query.filter_by(etat=1).all()
    else:
        buys = DemandeAchat.query.filter_by(etat=1,emplacement=user_emplacement).all()
    try:

        buys_data = [
            {
                'code_demande': buy.code_demande,
                'code_article': buy.code_article,
                'libelle_article': buy.libelle_article,
                'quantite': buy.quantite,
                'emplacement': buy.emplacement,
                'date': buy.date.isoformat(),  # Correct date format
                'demandeur': buy.demandeur
            }
            for buy in buys
        ]
        
        # Log the JSON data to be sent
        
        
        return jsonify(buys_data)  # Return as JSON
    
    except Exception as e:
        print("Error fetching buys:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/pending_arrivals')
@roles_required('admin','manager','user','achat','responsable')
def pending_arrivals():
    user_role=session.get('role')
    user_emplacement=session.get('emplacement')

    if user_role in ['admin','manager']:
        # Fetch all pending arrivals where etat == 0 (not yet received) and reception == 1 (approved)
        arrivals = DemandeAchat.query.filter_by(etat=0, reception=1).all()
    else:
        arrivals = DemandeAchat.query.filter_by(etat=0, reception=1,emplacement=user_emplacement).all()

    
    # Convert to JSON
    arrivals_data = [
        {
            'code_demande': arrival.code_demande,
            'code_article': arrival.code_article,
            'libelle_article': arrival.libelle_article,
            'quantite': arrival.quantite,
            'emplacement': arrival.emplacement,
            'date': arrival.date.isoformat(),
            'demandeur': arrival.demandeur
        }
        for arrival in arrivals
    ]
    return jsonify(arrivals_data)

@app.route('/pending_shipments')
@roles_required('admin','manager','user','achat','responsable')
def pending_shipments():

    user_role=session.get('role')
    user_emplacement=session.get('emplacement')

    if user_role in ['admin','manager']:
        # Fetch all pending shipments where etat == 0 (not shipped) and reception == 1 (approved)
        shipments = DemandeVente.query.filter_by(etat=0, reception=1).all()
    else:
        shipments = DemandeVente.query.filter_by(etat=0, reception=1,emplacement=user_emplacement).all()

    
    # Convert to JSON
    shipments_data = [
        {
            'code_demande': shipment.code_demande,
            'code_article': shipment.code_article,
            'libelle_article': shipment.libelle_article,
            'quantite': shipment.quantite,
            'emplacement': shipment.emplacement,
            'date': shipment.date,  # Keep date as string
            'demandeur': shipment.demandeur
        }
        for shipment in shipments
    ]
    return jsonify(shipments_data)

@app.route('/buys_attentes_confirm', methods=['GET','POST'])
@roles_required('admin','manager','user','achat','responsable')

def buys_attentes_confirm():
    user_emplacement=session.get('emplacement')
    achats = DemandeAchat.query.filter_by(etat=0, reception=1,emplacement=user_emplacement).all()
    
    # Convertir les données en JSON
    arriver_data = [
        {
            'code_demande': arriver.code_demande,
            'code_article': arriver.code_article,
            'libelle_article': arriver.libelle_article,
            'quantite': arriver.quantite,
            'prix_achat': arriver.prix_achat,
            'emplacement': arriver.emplacement,
            'demandeur': arriver.demandeur,
            'date': arriver.date.isoformat(),
            'fournisseur': arriver.Fournisseur
        }
        for arriver in achats
    ]

    return jsonify(arriver_data)  # Retourner les données en JSON

@app.route('/sales_attentes_confirm', methods=['GET','POST'])
@roles_required('admin','manager','user','achat','responsable')
def sales_attentes_confirm():
    user_emplacement=session.get('emplacement')
    # Récupérer toutes les demandes de vente avec etat=0 et reception=1
   
    ventes = DemandeVente.query.filter_by(etat=0, reception=1,emplacement=user_emplacement)

    
    # Convertir les données en JSON
    ventes_data = [
        {
            'code_demande': vente.code_demande,
            'code_article': vente.code_article,
            'libelle_article': vente.libelle_article,
            'quantite': vente.quantite,
            'prix_vente': vente.prix_vente,
            'emplacement': vente.emplacement,
            'vers': vente.vers,
            'demandeur': vente.demandeur,
            'date': vente.date.isoformat()  # Convertir la date au format ISO
        }
        for vente in ventes
    ]

    return jsonify(ventes_data)


@app.route('/confirm_vente/<int:code_demande>', methods=['POST'])
@roles_required('admin','manager','user','achat','responsable')
def confirm_vente(code_demande):
    # Récupérer la demande de vente à confirmer
    vente = DemandeVente.query.get(code_demande)
    
    if not vente:
        print(f"Aucune demande de vente trouvée avec le code_demande {code_demande}")
        return jsonify({'status': 'error', 'message': 'Demande de vente introuvable'}), 404
    
    # Confirmer la vente (mettre la réception à 0)
    vente.reception = 0
    db.session.commit()
    print('Vente confirmée ')
    
    # Créer une nouvelle entrée dans la table `Ventes`
    nouvelle_vente = Vente(
        code_demande=vente.code_demande,
        code_article=vente.code_article,
        libelle_article=vente.libelle_article,
        quantite=vente.quantite,
        prix_vente=vente.prix_vente,
        emplacement=vente.emplacement,
        vers=vente.vers,
        demandeur=vente.demandeur,
    )
    
    # Appeler la fonction pour mettre à jour la quantité de l'article
    update_result = update_article_quantity(nouvelle_vente.code_article, nouvelle_vente.quantite)
    print('***********************')
    print(update_result)
    db.session.commit()
    if update_result['status'] != 'success':
        
        return jsonify(update_result), 400
        

    try:
        # Ajouter la nouvelle vente à la table des ventes
        db.session.add(nouvelle_vente)
        db.session.commit()
        
        # Ajouter l'événement dans l'historique
        history_expedition_article(code_demande, session.get('username'))
        print("Vente ajoutée à la table Ventes.")
        
        return jsonify({'status': 'success'})
    
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de la vente: {e}")
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Erreur lors de la confirmation de la vente'}), 500











@app.route('/confirm_arriver/<int:code_demande>', methods=['POST'])
@roles_required('admin','manager','user','achat','responsable')

def confirm_arriver(code_demande):
    arriver = DemandeAchat.query.get(code_demande)
   
    arriver.reception = 0  # Indique que l'article est arrivé
    db.session.commit()
    print('arrivé')
    nouvelle_arriver = Achats(
        code_demande=arriver.code_demande,
        code_article=arriver.code_article,
        libelle_article=arriver.libelle_article,
        quantite=arriver.quantite,
        prix_achat=arriver.prix_achat,
        emplacement=arriver.emplacement,
        date=datetime.now(),
        fournisseur=arriver.Fournisseur
        
    )
    update_article_after_achat(nouvelle_arriver.code_article,nouvelle_arriver.prix_achat,nouvelle_arriver.quantite)
    try:
        db.session.add(nouvelle_arriver)
        db.session.commit()
        print('nouvelle achat ajouté')
       
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()  # Annuler la transaction en cas d'erreur
        return jsonify({'status': 'error', 'message': 'Erreur lors de la confirmation de l\'arrivée'}), 500





@app.route('/pending_sales')
@roles_required('admin','manager','user','achat','responsable')
def pending_sales():
    user_emplacement=session.get('emplacement')
    user_role=session.get('role')
    try:
        if user_role in ['admin','manager','achat']:
            sales = DemandeVente.query.filter_by(etat=1).all()
        else:
            # Fetch all pending sales where etat == 1 (for approved but not yet processed)
            sales = DemandeVente.query.filter_by(etat=1,emplacement=user_emplacement).all()

        # Log the sales being fetched
        

        sales_data = [
            {
                
                'code_article': sale.code_article,
                'libelle_article': sale.libelle_article,
                'quantite': sale.quantite,
                'emplacement': sale.emplacement,
                'date': sale.date.isoformat(),  # Correct date format
                'demandeur': sale.demandeur
            }
            for sale in sales
        ]
        
        # Log the JSON data to be sent
       
        
        return jsonify(sales_data)  # Return as JSON
    
    except Exception as e:
        print("Error fetching sales:", str(e))
        return jsonify({'error': str(e)}), 500



@app.route('/get_articles')
@roles_required('admin','manager','achat','user','responsable')
def get_articles():
    # Query all articles from the database
    
    articles = Article.query.all()

    # Format the data into a list of dictionaries
    articles_data = [
        {
            'code_article': article.code_article,
            'libelle_article': article.libelle_article,
            "prix_d'achat": article.prix_achat,
            'emplacement': article.emplacement,
            'quantite': article.quantite,
            'fournisseur': article.fournisseur
        }
        for article in articles
    ]

    # Return the data as a JSON response
    return jsonify(articles_data)


@app.route('/analytics')
@roles_required('admin','manager')

def analytics():
    # Récupérer toutes les données des articles
    articles = Article.query.all()
    all_data = {}
    
    for article in articles:
        # Récupérer les données pour chaque article (par exemple, prix au fil du temps)
        # Remplace ceci par ta logique pour obtenir les prix
        data = db.session.query(Article).filter(Article.code_article == article.code_article).all()
        all_data[article.code_article] = [{'date': d.date.strftime('%Y-%m-%d'), 'prix_achat': d.prix_achat} for d in data]
    
    # Extraire les libellés et quantités pour chaque article
    labels = [article.libelle_article for article in articles]
    quantities = [article.quantite for article in articles]

    # Passer les données sous forme JSON au template
    return render_template('analytics.html', articles=articles, all_data=all_data,labels=labels, quantities=quantities)

# app.py


from sqlalchemy import func



@app.route('/kpi_data')
@roles_required('admin','manager')

def kpi_data():
    # Récupérer les articles avec leur quantité et libellé
    articles = db.session.query(Article.code_article, Article.libelle_article, Article.quantite).all()
    
    total_articles_count = db.session.query(Article).count()
    # Calculer le total des articles disponibles
    total_articles = sum(article.quantite for article in articles)

    # Récupérer d'autres KPI
    total_ventes = db.session.query(func.sum(Vente.quantite)).scalar()
    total_achats = db.session.query(func.sum(Achats.quantite)).scalar()
    valeur_stock = db.session.query(func.sum(Article.quantite * Article.prix_achat)).scalar()
    commandes_non_completes = db.session.query(func.count(CounterTable.id)).scalar()

    # Préparer les données pour le pie chart
    article_data = {
        "labels": [article.libelle_article for article in articles],
        "data": [article.quantite for article in articles]
    }

    return jsonify({
        "total_articles_count":total_articles_count or 0,
        "total_articles": total_articles or 0,
        "total_ventes": total_ventes or 0,
        "total_achats": total_achats or 0,
        "valeur_stock": valeur_stock or 0.0,
        "commandes_non_completes": commandes_non_completes or 0,
        "articles": article_data  # Ajouter les données des articles pour le graphique
    })




@app.route('/users', methods=['GET'])
@roles_required('admin','manager','achat','user','responsable')
def get_users():
    users = User.query.all()  # Fetch all users from the database
    users_data = [{
        'id': user.id,
        'username': user.username,
        'emplacement': user.emplacement,
        'role': user.role
    } for user in users]
    
    return jsonify(users_data)  # Return the users data as JSON

from sqlalchemy.orm import Session

@app.route('/service_achat_vente', methods=['GET', 'POST'])
@roles_required('admin','achat')

def service_achat_vente():
    count_ventes_attente_expedition=get_count_articles_attente_expedition()
    count_ventes_attente_arrive=get_count_articles_attente_arrive()
    demandes_achats = DemandeAchat.query.filter_by(etat=1).all()
    demandes_ventes = DemandeVente.query.filter_by(etat=1).all()
    count = get_orders_count()
    sales_count = DemandeVente.query.filter_by(etat=1).count()
    
    
    if request.method == 'POST':
        # Récupérer les données du formulaire
        demande_id = request.form.get('demande_id')
        type_demande = request.form.get('type_demande')
        action = request.form.get('action')  # 'approuver' ou 'annuler'
        
        app.logger.info(f"Demande ID: {demande_id}, Type Demande: {type_demande}, Action: {action}")

        if not demande_id:
            flash('ID de la demande manquant.', 'danger')
            return redirect(url_for('service_achat_vente'))

        # Gestion des demandes d'achat
        if type_demande == 'achat':
            fournisseur = request.form.get('fournisseur')
            prix_achat = request.form.get('prix_achat')

            if not fournisseur or not prix_achat:
                flash('Veuillez renseigner toutes les informations nécessaires.', 'danger')
                return redirect(url_for('service_achat_vente'))

            # Récupérer la demande d'achat
            demande = DemandeAchat.query.get(demande_id)
            if demande:
                if action == 'approuver':
                   
                    demande.prix_achat = prix_achat
                    demande.date_achat = datetime.now(timezone.utc)
                    demande.etat = 0  # Approuvé
                    demande.reception = 1  # Reçu
                    demande.fournisseur=fournisseur
                    history_approuver_demande(demande_id,prix_achat,fournisseur,session.get('username'))
                    flash('La demande d\'achat a été approuvée et reçue avec succès.', 'success')
                elif action == 'annuler':
                    demande.etat = 2  # Annulé
                    demande.reception = 2  # Annulé
                    history_annuler_demande(demande_id,session.get('username'))
                    flash('La demande d\'achat a été annulée.', 'warning')
                db.session.commit()
            else:
                flash('Demande d\'achat non trouvée.', 'danger')
            return redirect(url_for('service_achat_vente'))

        # Gestion des demandes de vente
        if type_demande == 'vente':
            demande = DemandeVente.query.get(demande_id)
            if demande:
                if action == 'approuver':
                    demande.etat = 0  # Changer l'état à 0 pour approuvé
                    demande.reception = 1  # Marquer comme reçu
                    flash('La demande de vente a été approuvée avec succès.', 'success')
                elif action == 'annuler':
                    demande.etat = 2  # Changer l'état à 2 pour annulé
                    demande.reception = 2  # Marquer comme annulé
                    flash('La demande de vente a été annulée.', 'warning')
                db.session.commit()
        else:
            flash('Demande de vente non trouvée.', 'danger')
        

        return redirect(url_for('service_achat_vente'))
    # Si la méthode est GET, afficher les demandes d'achat et de vente
    return render_template('achats.html', orders_count=count, sales_count=sales_count, demandes_achats=demandes_achats, demandes_ventes=demandes_ventes,count_ventes_attente_expedition=count_ventes_attente_expedition,count_ventes_attente_arrive=count_ventes_attente_arrive)


@app.route('/search_usine2', methods=['GET'])
@roles_required('admin','manager','achat','user','responsable')
def search_usine2():
    query = request.args.get('query', '')
    if query:
        usines = Usine.query.filter(Usine.nom_usine.like(f'{query}%')).all()
        result = [{'id': usine.id_usine, 'nom_usine': usine.nom_usine} for usine in usines]
    else:
        result = []
    
    return jsonify(result)




@app.route('/search_article_code', methods=['GET'])
@roles_required('admin','manager','achat','user','responsable')
def search_article_code():
    query = request.args.get('query', '')
    if query:
        articles = Article.query.filter(Article.code_article.like(f'{query}%')).all()  # Utiliser libelle_article
        result = [{'id_article': article.id_article, 'code_article': article.code_article} for article in articles]  # Utiliser libelle_article
    else:
        result = []
    
    return jsonify(result)



@app.route('/search_article', methods=['GET'])
@roles_required('admin','manager','achat','user','responsable')
def search_article():
    query = request.args.get('query', '')
    if query:
        articles = Article.query.filter(Article.libelle_article.like(f'{query}%')).all()  # Utiliser libelle_article
        result = [{'id_article': article.id_article, 'libelle_article': article.libelle_article} for article in articles]  # Utiliser libelle_article
    else:
        result = []
    
    return jsonify(result)








def history_create_demande(code_demande, code_article, libelle_article, quantite, emplacement, user, date_action,date_approuver_demande,date_reception):
    # Créer une nouvelle entrée dans l'historique avec la même date que la demande d'achat
    nouvelle_entree = History(
        code_demande=code_demande,
        code_article=code_article,
        libelle_article=libelle_article,
        quantite=quantite,
        prix=None,  # Remplissez ce champ selon vos besoins
        fournisseur=None,  # Remplissez ce champ selon vos besoins
        emplacement=emplacement,
        action="Création de demande d'achat",
        user=user,
        details="Demande créée",
        usine=emplacement,  # ou un autre champ pour l'usine si applicable
        date_action=date_action,  # Utilisation de la date de création de la demande
        date_approuver_demande=date_approuver_demande,
        date_reception=date_reception
    )
    
    db.session.add(nouvelle_entree)
    db.session.commit()



def history_approuver_demande(code_demande, prix_achat, fournisseur,user):
    # Récupérer l'utilisateur courant
   
    # Mettre à jour la demande dans la table history
    nouvelle_entree = History(
        code_demande=code_demande,
        prix=prix_achat,
        fournisseur=fournisseur,
        action="Demande d'achat approuvée",
        user=user,
        date_approuver_demande=datetime.now(),
        
    )
    db.session.add(nouvelle_entree)
    db.session.commit()



def history_annuler_demande(code_demande,user):
    
    
    # Insérer dans la table history avec un message d'annulation
    nouvelle_entree = History(
        code_demande=code_demande,
        action="Demande d'achat annulée",
        details="Demande d'achat annulée par l'utilisateur",
        user=user,
        date_action=datetime.now()
    )
    db.session.add(nouvelle_entree)
    db.session.commit()


def history_reception_article(code_demande,user):
    # Récupérer l'utilisateur courant
   
    
    # Insérer dans la table history avec un message de réception
    nouvelle_entree = History(
        code_demande=code_demande,
        action="Article reçu",
        details="L'article correspondant à la demande a été reçu en magasin",
        user=user,
        date_reception=datetime.now(),
        
    )
    db.session.add(nouvelle_entree)
    db.session.commit()


def history_expedition_article(code_demande,user):
    # Récupérer l'utilisateur courant
   
    
    # Insérer dans la table history avec un message de réception
    nouvelle_entree = History(
        code_demande=code_demande,
        action="Article Vendue",
        details="L'article correspondant à la demande a été vendue",
        user=user,
        date_reception=datetime.now(),
        
    )
    db.session.add(nouvelle_entree)
    db.session.commit()





@app.route('/history')
@roles_required('admin')

def show_history():
    user_role=session.get('role')
    if user_role == 'admin':

        # Récupérer toutes les entrées de la table History
        all_history = History.query.all()

        # Passer les données au template HTML
        return render_template('history.html', history=all_history)
    else : 
        return render_template(login.html)



def update_article_quantity(code_article, quantity_sold):
    # Récupérer l'article correspondant à partir du code_article
    article = Article.query.filter_by(code_article=code_article).first()
    print(article)
    if not article:
        # Si aucun article n'est trouvé, retourner False
        print(f"Aucun article trouvé avec le code_article {code_article}")
        return {'status': 'error', 'message': 'Article introuvable'}
    
    # Vérifier que la quantité en stock est suffisante
    if article.quantite < quantity_sold:
        print("Quantité insuffisante pour cette vente")
        return {'status': 'error', 'message': 'Quantité insuffisante pour cette vente'}
    
    try:
        # Mettre à jour la quantité de l'article
        article.quantite -= quantity_sold
        print(f"Nouvelle quantité de l'article: {article.quantite}")
        
        # Sauvegarder les modifications dans la base de données
        db.session.commit()
        return {'status': 'success'}
    
    except Exception as e:
        # En cas d'erreur lors de l'enregistrement, annuler la transaction
        print(f"Erreur lors de la mise à jour de la quantité de l'article: {e}")
        db.session.rollback()
        return {'status': 'error', 'message': 'Erreur lors de la mise à jour de la quantité'}



def update_article_after_achat(nouveau_code_article,nouveau_prix_achat,nouveau_quantite):
    # Récupérer l'article existant dans la table `articles` avec le même `code_article`
    article = Article.query.filter_by(code_article=nouveau_code_article).first()
    print(article)
    if article:
        # Calcul du nouveau prix moyen pondéré (PMP)
        ancien_prix_total = article.prix_achat * article.quantite
        print(ancien_prix_total)
        nouveau_prix_total = nouveau_prix_achat * nouveau_quantite
        print(nouveau_prix_total)
        nouvelle_quantite_totale = article.quantite + nouveau_quantite
        print(nouvelle_quantite_totale)

        # Calcul du nouveau PMP
        nouveau_pmp = (ancien_prix_total + nouveau_prix_total) / nouvelle_quantite_totale
        print(nouveau_pmp)

        # Mettre à jour les informations de l'article
        article.prix_achat = nouveau_pmp
        article.quantite = nouvelle_quantite_totale
        print(article.prix_achat,article.quantite)
        # Enregistrer les changements dans la base de données
        db.session.commit()
        print(True)

        return True  # Indiquer que la mise à jour a été réussie
    else:
        print(False)
        return False  # Si l'article n'existe pas dans la table `articles`
    



@app.route('/get_unread_count', methods=['GET'])
@roles_required('admin', 'user', 'manager', 'responsable')
def get_unread_count():
    username=session.get('username')
    # Récupérer les messages non lus destinés à l'utilisateur actuel
    unread_count = Message.query.filter_by(destinataire=username, est_lu=False).count()
    
    return jsonify({'unread_count': unread_count})


@app.route('/get_unread_messages', methods=['GET'])
@roles_required('admin', 'user', 'manager', 'responsable')
def get_unread_messages():
    filter_type = request.args.get('filter', 'mon_magasin')
    username = session.get('username')
    emplacement = session.get('emplacement')

    if filter_type == 'mon_magasin':
        messages = Message.query.filter_by(destinataire=username, est_lu=False, emplacement=emplacement).all()
    else:
        messages = Message.query.filter_by(destinataire=username, est_lu=False).all()

    result = [{
        'expéditeur': msg.expéditeur,
        'destinataire': msg.destinataire,
        'objet': msg.objet,
        'corps': msg.corps,
        'date_envoi': msg.date_envoi.strftime('%Y-%m-%d %H:%M')
    } for msg in messages]
    
    return jsonify(result)



@app.route('/send_message', methods=['POST'])
@roles_required('admin', 'user', 'manager', 'responsable')
def send_message():
    destinataire = request.form.get('destinataire')
    cc = request.form.get('cc', '')
    objet = request.form.get('objet')
    corps = request.form.get('corps')
    emplacement = session.get('emplacement')
    username=session.get('username')

    # Créer un nouvel objet message
    new_message = Message(
        expéditeur=username,
        destinataire=destinataire,
        cc=cc,
        objet=objet,
        corps=corps,
        emplacement=emplacement,
        date_envoi=datetime.now(timezone.utc),
        est_lu=False
    )
    
    db.session.add(new_message)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Message envoyé avec succès.'})








if __name__ == '__main__':
    app.run("0.0.0.0", debug=False)
