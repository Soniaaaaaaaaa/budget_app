class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    @staticmethod
    def get_user_by_email(cursor, email):
        query = "SELECT user_id, email, password, username FROM user WHERE email=%s"
        cursor.execute(query, (email,))
        return cursor.fetchone()
    
    @staticmethod
    def get_user_by_id(cursor, id):
        query = "SELECT user_id, email, password, username, group_id FROM user WHERE user_id=%s"
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
    def update_username(cursor, user_id, username):
        cursor.execute("UPDATE user SET username = %s WHERE user_id = %s",
        (username, user_id))

    @staticmethod
    def has_user_group(cursor, id):
        query_check_user = "SELECT group_id FROM user WHERE user_id = %s"
        cursor.execute(query_check_user, (id,))
        user_data = cursor.fetchone()

        if user_data and user_data[0] is not None:
            return user_data[0]
        return 0

    @staticmethod
    def groups_info(cursor, user_id):
        query = """
            SELECT gi.group_name, ug.group_status
            FROM group_info gi
            JOIN user ug ON gi.group_id = ug.group_id
            WHERE ug.user_id = %s
        """
        cursor.execute(query, (user_id,))
        group_data = cursor.fetchone() 
        return group_data
    
    @staticmethod
    def groups_updata(cursor, group_id, group_name):
        query = "UPDATE group_info SET group_name = %s WHERE group_id = %s"
        cursor.execute(query, (group_name, group_id,))
        group_data = cursor.fetchone() 
        return group_data
    
    @staticmethod
    def is_owner(cursor, id):
        query_check_owner = "SELECT group_status FROM user WHERE user_id = %s"
        cursor.execute(query_check_owner, (id,))
        user_data = cursor.fetchone()

        if user_data and user_data[0] == 'owner':
            return True
        return False
        

    @staticmethod
    def create_group(cursor, id, group_name):
        query_create_group = "INSERT INTO group_info (group_name) VALUES (%s)"
        cursor.execute(query_create_group, (group_name,))
        group_id = cursor.lastrowid
        query_update_user = "UPDATE user SET group_id = %s, group_status = %s WHERE user_id = %s"
        cursor.execute(query_update_user, (group_id, 'owner', id))
        return group_id

    @staticmethod
    def add_member(cursor, id, member_email):
        query = """
            UPDATE user SET group_id = %s, group_status = "member"
        WHERE email = %s
        """
        group_id = User.has_user_group(cursor, member_email)
        if group_id == 0:
            cursor.execute(query, (id, member_email))
            return "User was assign to your group"
    
    @staticmethod
    def delete_member(cursor, member_email):
        query = """
        UPDATE user
        SET group_status = NULL, group_id = NULL
        WHERE email = %s
    """
        cursor.execute(query, (member_email,))
        return "Group status was removed for the user"

    @staticmethod
    def get_group_members(cursor, group_id):
        # SQL запит для отримання учасників групи
        query = "SELECT username, email, group_status FROM user WHERE group_id = %s"
        cursor.execute(query, (group_id,))
        return (cursor.fetchall())
    
    

        
      

    
        
        