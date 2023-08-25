from ldap3 import Server, Connection, MODIFY_REPLACE, MODIFY_ADD


class ActiveDirectoryManager:
    def __init__(self, ad_server, ad_username, ad_password):
        self.ad_server = ad_server
        self.ad_username = ad_username
        self.ad_password = ad_password
        self.conn = None

    def connect(self):
        self.server = Server(self.ad_server, get_info='ALL')
        self.conn = Connection(
            self.server,
            user=self.ad_username,
            password=self.ad_password,
            auto_bind=True
        )

    def disconnect(self):
        self.conn.unbind()
        self.conn = None

    def add_new_user(self, user_attributes):
        dn = f"CN={user_attributes['Name']},CN=Users,DC=piracanjuba,DC=local"
        user_entry = {
            "objectClass": ["top", "person", "organizationalPerson", "user"],
            "cn": [user_attributes["Name"]],
            "sAMAccountName": [user_attributes["SamAccountName"]],
            "userPrincipalName": [user_attributes["UserPrincipalName"]],
            "mail": [user_attributes["EmailAddress"]],
            "givenName": [user_attributes["GivenName"]],
            "displayName": [user_attributes["DisplayName"]],
            "description": [user_attributes["Description"]],
            "postalCode": [user_attributes["PostalCode"]],
            "co": [user_attributes["Country"]],
            "company": [user_attributes["Company"]],
            "department": [user_attributes["Department"]],
            "title": [user_attributes["Title"]],
            "scriptPath": [user_attributes["scriptPath"]],
            "changePasswordAtLogon": [str(user_attributes["ChangePasswordAtLogon"]).lower()],
            "wWWHomePage": [user_attributes["HomePage"]],
            "extensionAttribute2": [user_attributes["extensionAttribute2"]],
            "extensionAttribute4": [user_attributes["extensionAttribute4"]],
            "extensionAttribute5": [user_attributes["extensionAttribute5"]],
            "extensionAttribute10": [user_attributes["extensionAttribute10"]],
            "accountPassword": [user_attributes["AccountPassword"]],
            "sn": [user_attributes["sn"]],
            "pager": [user_attributes["pager"]],
            "l": [user_attributes["l"]],
            "st": [user_attributes["st"]],
            "physicalDeliveryOfficeName": [user_attributes["physicalDeliveryOfficeName"]],
            "info": [user_attributes["info"]]
        }

        self.conn.add(dn, attributes=user_entry)
        modifications = {
            "sn": [(MODIFY_REPLACE, ["Aparecida Oliveira Xa"])],
            "pager": [(MODIFY_REPLACE, ["013986"])],
            "l": [(MODIFY_REPLACE, ["Juiz de Fora"])],
            "st": [(MODIFY_REPLACE, ["MG"])],
            "physicalDeliveryOfficeName": [(MODIFY_REPLACE, ["Juiz de Fora"])],
            "info": [(MODIFY_REPLACE, ["ID ERP: JAXAVIER"])]
        }

        self.conn.modify(dn, modifications)

        group_dn = "CN=G_SESuite_ECM,OU=Groups,DC=piracanjuba,DC=local"
        member_dn = f"CN={user_attributes['Name']},CN=Users,DC=piracanjuba,DC=local"
        group_modifications = {
            "member": [(MODIFY_ADD, [member_dn])]
        }
        self.conn.modify(group_dn, group_modifications)

if __name__ == "__main__":
    ad_manager = ActiveDirectoryManager("your_ad_server", "your_ad_username", "your_ad_password")
    ad_manager.connect()

    user_attributes = {
        "Name": "Jennifer Aparecida Oliveira Xavier",
        "SamAccountName": "jennifer.xavier",
        "UserPrincipalName": "jennifer.xavier@piracanjuba.com.br",
        "EmailAddress": "jennifer.xavier@piracanjuba.com.br",
        "GivenName": "Jennifer",
        "DisplayName": "Jennifer Aparecida Oliveira Xavier",
        "Description": "5038020601",
        "PostalCode": "36.092-000",
        "Country": "BR",
        "Company": "Laticinios Bela Vista S.A.",
        "Department": "POSTO JUIZ DE FORA - MG",
        "extensionAttribute10": "ASSISTENTE ADMINISTRATIVO",
        "Title": "ASSISTENTE ADMINISTRATIVO",
        "scriptPath": "OFCSCAN.BAT",
        "ChangePasswordAtLogon": True,
        "HomePage": "JAXAVIER",
        "extensionAttribute2": "5038020601",
        "extensionAttribute4": "013986",
        "extensionAttribute5": "JAXAVIER",
        "AccountPassword": "setpassword"
    }

    ad_manager.add_new_user(user_attributes)
    ad_manager.disconnect()

    """
    New-ADUser 
        -Name "Jennifer Aparecida Oliveira Xavier" 
        -SamAccountName "jennifer.xavier" 
        -UserPrincipalName "jennifer.xavier@piracanjuba.com.br" 
        -EmailAddress  "jennifer.xavier@piracanjuba.com.br" 
        -GivenName "Jennifer" 
        -DisplayName "Jennifer Aparecida Oliveira Xavier" 
        -Description "5038020601" -PostalCode "36.092-000" 
        -Country "BR" -Company "Laticinios Bela Vista S.A." 
        -Department "POSTO JUIZ DE FORA - MG" 
        -extensionAttribute10 "ASSISTENTE ADMINISTRATIVO" 
        -Title "ASSISTENTE ADMINISTRATIVO" 
        -scriptPath "OFCSCAN.BAT" 
        -ChangePasswordAtLogon $true 
        -wWWHomePage "JAXAVIER" 
        -extensionAttribute2 "5038020601" # FPW -> COD_centro_custo | AD atual -> u_description
        -extensionAttribute3 "xxxxxxx" # FPW -> u_cod_representante -ignorar- | AD atual -> u_facsimiletelephonenumber
        -extensionAttribute4 "013986" # FPW -> u_matricula | AD atual -> u_pager
        -extensionAttribute5 "JAXAVIER"  # FPW -> u_sap_id | AD atual -> u_wwwhomepage
        -extensionAttribute10 "ASSISTENTE ADMINISTRATIVO"   # FPW ->  e o mesmo que em Title
        -AccountPassword $setpassword 

    Move-ADObject -Identity "CN=Jennifer Aparecida Oliveira Xavier,CN=Users,DC=piracanjuba,DC=local" -TargetPath "OU=Default,OU=Unidades,DC=piracanjuba,DC=local" 
    Set-ADUser -Identity "jennifer.xavier" -Replace @{sn ="Aparecida Oliveira Xa"}
    Set-ADUser -Identity "jennifer.xavier" -Replace @{pager ="013986"}
    Set-ADUser -Identity "jennifer.xavier" -Replace @{wWWHomePage ="JAXAVIER"}
    Set-ADUser -Identity "jennifer.xavier" -Replace @{l ="Juiz de Fora"}
    Set-ADUser -Identity "jennifer.xavier" -Replace @{st ="MG"}
    Set-ADUser -Identity "jennifer.xavier" -Replace @{physicalDeliveryOfficeName ="Juiz de Fora"}
    Set-ADUser -Identity "jennifer.xavier" -Replace @{info ="ID ERP: JAXAVIER"}
    Add-ADGroupMember -Identity "G_SESuite_ECM" -Members "jennifer.xavier"
    """
