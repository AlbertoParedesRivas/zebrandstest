from models.admin import AdminModel
from common.mailgun import Mailgun


def sendNotification(type, data):
    to = getAdminsEmails()

    if type == "DELETE":
        print(f"{data['author']} just deleted a product: {data['sku']} {data['name']}")
        content = f"{data['author']} just deleted a product: {data['sku']} {data['name']}"
        Mailgun.send_email(to, "Product deleted", content, "")

    if type == "REGISTER":
        print(f"{data['author']} just registered a new product: {data['sku']} {data['name']}")
        content = f"{data['author']} just registered a new product: {data['sku']} {data['name']}"
        Mailgun.send_email(to, "Product registered", content, "")

    if type == "UPDATE":
        if data["updatedFields"]:
            print(f"{data['author']} just updated a product's data: {data['sku']} {data['name']}")
            print("Updated fields:")
            content = f"{data['author']} just updated a product's data: {data['sku']} {data['name']} Updated fields: "
            htmlContent = f"{data['author']} just updated a product's data: {data['sku']} {data['name']} <br/>Updated fields:<br/>"
            for field in data["updatedFields"]:
                content = content + f"{field} "
                htmlContent = htmlContent + f"{field}<br/>"
                print(f"{field}")
                
        Mailgun.send_email(to, "Product updated", content, htmlContent)
            

def getAdminsEmails():
    adminEmails = list()

    for admin in AdminModel.find_all():
        adminEmails.append(admin.email)

    return adminEmails