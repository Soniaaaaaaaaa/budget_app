class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    @staticmethod
    def get_user_by_email(cursor, email):
        query = "SELECT user_id, email, password FROM user WHERE email=%s"
        cursor.execute(query, (email,))
        return cursor.fetchone()
    
    @staticmethod
    def get_user_by_id(cursor, id):
        query = "SELECT user_id, email, password FROM user WHERE id=%s"
        cursor.execute(query, (id,))
        return cursor.fetchone()
    
    @staticmethod
    def create_user(cursor, email, password):
        cursor.execute("INSERT INTO user (email, password) VALUES (%s, %s)",
                   (email, password))

    @staticmethod
    def update_passwd(cursor, email, password):
        cursor.execute("UPDATE user SET password = %s WHERE email = %s",
        (password, email))

    @staticmethod
    def has_user_group(cursor, email):
        query_check_user = "SELECT group_id FROM user WHERE email = %s"
        cursor.execute(query_check_user, (email,))
        user_data = cursor.fetchone()

        if user_data and user_data[0] is not None:
            return user_data[0]
        return 0
    
    @staticmethod
    def is_owner(cursor, email):
        query_check_owner = "SELECT group_status FROM user WHERE email = %s"
        cursor.execute(query_check_owner, (email,))
        user_data = cursor.fetchone()

        if user_data and user_data[0] == 'owner':
            return True
        return False
        

    @staticmethod
    def create_group(cursor, email, group_name):
        query_create_group = "INSERT INTO group_info (group_name) VALUES (%s)"
        cursor.execute(query_create_group, (group_name,))
        group_id = cursor.lastrowid
        query_update_user = "UPDATE user SET group_id = %s, group_status = %s WHERE email = %s"
        cursor.execute(query_update_user, (group_id, 'owner', email))

        return "Group created and user assigned successfully", 200

    @staticmethod
    def add_member(cursor, email, member_email):
        query = """
            INSERT INTO user (email, password, group_id, group_status)
            VALUES (%s, %s, %s, "member")
        """
        group_id = User.has_user_group(cursor, member_email)
        is_owner = User.is_owner(cursor, email)
        if group_id == 0 and is_owner == True:
            cursor.execute(query, (email, group_id))
            return "User was assign to your group", 200

    @staticmethod
    def get_group_members(cursor, group_id):
        # SQL запит для отримання учасників групи
        query = "SELECT email, group_status FROM user WHERE group_id = %s"
        cursor.execute(query, (group_id,))
        return cursor.fetchall()
    

        
      

    
        
        