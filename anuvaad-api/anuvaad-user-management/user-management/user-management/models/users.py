from utilities import MODULE_CONTEXT
from db import get_db
from utilities import hash_password, encrypt_password, generate_user_id
from anuvaad_auditor.loghandler import log_info, log_exception
import bcrypt


class UserManagementModel(object):

    @staticmethod
    def create_users(user):
        hashed = hash_password(user["password"].encode('utf-8'))
        # encripted     = encrypt_password(hashed)
        userID = generate_user_id()

        user_roles = []
        for role in user["roles"]:
            role_info = {}
            role_info["roleCode"] = role["roleCode"]
            role_info["roleDesc"] = role["roleDesc"]
            user_roles.append(role_info)

        try:
            collections = get_db()['sample']
            user = collections.insert({'userID': userID, 'name': user["name"], 'userName': user['userName'], 'password': hashed,
                                       'email': user["email"], 'phoneNo': user["phoneNo"], 'roles': user_roles})
            return user
        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return None

    @staticmethod
    def update_users_by_uid(user):
        try:
            collections = get_db()['sample']
            user_id = user["userID"]

            record = collections.find({"userID": user_id})

            if record == None:
                return("No record for the given user Id")
            else:

                user_roles = []
                for role in user["roles"]:
                    role_info = {}
                    role_info["roleCode"] = role["roleCode"]
                    role_info["roleDesc"] = role["roleDesc"]
                    user_roles.append(role_info)

                hashed = hash_password(user["password"].encode('utf-8'))

                results = collections.update({"userID": user_id}, {'$set': {'name': user["name"], 'userName': user['userName'], 'password': hashed,
                                                                            'email': user["email"], 'phoneNo': user["phoneNo"], 'roles': user_roles}})

                if 'writeError' in list(results.keys()):
                    return False
                return True

        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return None

    @staticmethod
    def get_user_by_keys(userIDs,userNames,roleCodes):

        try:
            collections = get_db()['sample']

            for id in userIDs:
                results = collections.find({"userID": id}, {"password":0})
                return results

            for name in userNames:
                results = collections.find({"userName": name}, {"password":0})
                return results

            for code in roleCodes:
                results = collections.find({"roles":{'roleCode':code}}, {"password":0})
                return results
        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return None

        

      