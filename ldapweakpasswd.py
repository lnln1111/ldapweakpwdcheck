import ldap3
import pandas
import datetime

servername = "ldap://1.1.1.1:389"
username = "11111"
password = "11111"
domainname = "123.local"

try:
    server = ldap3.Server(servername, get_info=ldap3.ALL)
    conn = ldap3.Connection(server, user="{}@{}".format(username,domainname),password=password,auto_bind=True)
    conn.bind()
    print("登录成功")
except Exception as e:
    if "invalidCredentials" in str(e):
        print("认证失败")
    elif "invalid server address" in str(e):
        print("服务器地址错误")
    else:
        print(e)
    
# search_filter = "(sAMAccountName={})".format(username)
# base_dn = "DC=111,DC=local"
# search_scope = ldap3.SUBTREE
# attributes = ['cn', 'givenName', 'mail', 'sAMAccountName']
# conn.search(base_dn, search_filter)

# user_dn = conn.entries[0].entry_dn
# print(conn.entries)

# conn.search(search_base = 'DC=111,DC=local',
#          search_filter = '(userPrincipalName=*)',
#          search_scope = ldap3.SUBTREE,
#          attributes = ['cn', 'userPrincipalName','sAMAccountName','displayName'],
#          paged_size = 1000
#          # paged_size = 2
#            )
# user = []
# userdomain = []
# for i in conn.response:
#     try :
#         user.append(i['attributes']['sAMAccountName'])
#         userdomain.append(i['attributes']['userPrincipalName'])
#     except:
#         pass
# print(user)
# print(userdomain)
# print("共有"+str(len(user))+"个域账号。")

def check_ldap_weak_password(username, password):
    servername = "ldap://1.1.1.1:389"
    domainname = "111.local"
    try:
        server = ldap3.Server(servername, get_info=ldap3.ALL)
        conn = ldap3.Connection(server, user="{}@{}".format(username,domainname),password=password,auto_bind=True)
        conn.bind()
        # print("登录成功")
        return True
    except Exception as e:
        if "invalidCredentials" in str(e):
            # print("认证失败")
            return False
        elif "invalid server address" in str(e):
            # print("服务器地址错误")
            return False
        else:
            print(e)
            return False

# weakpswuser = []
# for i in user:
#     if check_ldap_weak_password(username=i,password="888888"):
#         print(i+",is weak password")
#         weakpswuser.append(i)
# print(str(len(weakpswuser))+"个域账号使用默认口令。")

conn.search(search_base = 'DC=111,DC=local',
         search_filter = '(userPrincipalName=*)',
         search_scope = ldap3.SUBTREE,
         attributes = ['cn', 'userPrincipalName','sAMAccountName','displayName'],
         paged_size = 1000
         # paged_size = 2
           )
user = []
for i in conn.response:
    dict_tmp = []
    try :
        user.append([i['attributes']['displayName'],i['dn'],i['attributes']['sAMAccountName'],i['attributes']['userPrincipalName']])
    except:
        pass
print(user)
print("共有"+str(len(user))+"个域账号。")

weakpswuser = []
for i in user:
    if check_ldap_weak_password(username=i[2],password="888888"):
        print(i[0]+",is weak password")
        i.append("888888")
        weakpswuser.append(i)
    elif check_ldap_weak_password(username=i[2],password="123456"):
        print(i[0]+",is weak password")
        i.append("123456")
        weakpswuser.append(i)
    else:
        pass
print(str(len(weakpswuser))+"个域账号使用默认口令")

datatimenow = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
df = pandas.DataFrame(weakpswuser,columns =["姓名", "组织", "用户名", "域用户","弱口令"])
df.to_excel('域账号薄弱口令{}.xlsx'.format(datatimenow), index=False, sheet_name='Sheet1')
