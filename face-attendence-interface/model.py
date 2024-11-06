import bcrypt
from conn import criar_conexão_com_MYSQL

class userDAO:

    def generate_password(self, password):
        # Gera o hash da senha
        salt = bcrypt.gensalt()  # Gera um salt aleatório
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)  # Codifica a senha para bytes e aplica o hash
        return hashed # return hash_password

    def check_password(self,provided_password, stored_hash):
        # Se o hash estiver em formato string, converta-o para bytes
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode('utf-8')
        
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash)

    def save_bd_new_user_and_return_id_of_user(self, name, email, password):
        sql = "INSERT INTO users (user_name, email, password) VALUES (%s, %s, %s)"
        valores = (name, email, password)
        mycursor.execute(sql, valores)

        mydb.commit() # Confirmar as alterações

        id_inserido = mycursor.lastrowid
        return id_inserido

    def get_user_info_based_on_email(self, email):
        sql = "SELECT * FROM users WHERE email = %s"  # Correção na consulta
        mycursor.execute(sql, (email,))  # Passando o email como parâmetro
        myresult = mycursor.fetchone()

        return myresult
    
mydb, mycursor = criar_conexão_com_MYSQL() # Por favor, adapte para seu MYSQL