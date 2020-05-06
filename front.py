from tkinter import *
from PIL import ImageTk, Image
from service import service
import tkinterhtml
import datetime
import pytz
import base64
from emailbody import clear_email_body
from bs4 import BeautifulSoup

# Iniciamos Tkinter
root = Tk()

# Caracteristicas iniciales
root.title("Email Client by DefPrintCode():")
root.config(bg="#f9f9f9")
# HD
root.geometry("1510x768")

# variales de imagen

add = ImageTk.PhotoImage(Image.open("images/add.png"))
person = ImageTk.PhotoImage(Image.open("images/person.png"))
google = ImageTk.PhotoImage(Image.open("images/google.png"))
# Iconos de carpetas
chat = ImageTk.PhotoImage(Image.open("images/chat.png"))
sent = ImageTk.PhotoImage(Image.open("images/sent.png"))
inbox = ImageTk.PhotoImage(Image.open("images/inbox.png"))
important = ImageTk.PhotoImage(Image.open("images/important.png"))
starred = ImageTk.PhotoImage(Image.open("images/starred.png"))
trash = ImageTk.PhotoImage(Image.open("images/trash.png"))
draft = ImageTk.PhotoImage(Image.open("images/draft.png"))
spam = ImageTk.PhotoImage(Image.open("images/spam.png"))
label = ImageTk.PhotoImage(Image.open("images/label.png"))

# variables generales
inboxUn = 18
spamUn = 138

# root.iconbitmap('icon.ico')
# root.resizable(False, False)
ser = service()
labelimgVar = ""

# FRONT
# Variables de color
# --Background--
menuBg = "#6f916f"
elementBg = "#93ac93"
subEleBg = "#b7c8b7"
# --Font Color--
elementoFg = "#5d6c53"
# FontFamily
elementFgFamily = "Tahoma"
elementFgSize = 16
subEleFgSize = 10
buttonReg = ""

secondMenu = False
showMessage = False


def clearBarra():
    global secondMenu, barra

    if secondMenu:
        for widget in barra.winfo_children():
            widget.destroy()

        barra.pack_forget()
        barra = Frame(root)
        barra.config(bg=elementBg, width=0)
        barra.pack(side=LEFT, fill="y")

        clearMessage()


def clearMessage():
    global showMessage, emailFrame

    if showMessage:
        for widget in emailFrame.winfo_children():
            widget.destroy()

        emailFrame.pack_forget()
        emailFrame = Frame(root)
        emailFrame.config(width=0)
        emailFrame.pack(side=LEFT, fill="y")


def muestraEmail(event, messageId):
    global emailFrame, showMessage
    clearMessage()
    showMessage = False
    msg = ser.users().messages().get(userId='me', id=messageId).execute()
    emailDeliveVar = ""
    for head in msg['payload']['headers']:
        if head['name'] == "Subject":
            subVar = head['value']
        elif "From" in head['name']:
            fromVar = head['value']

        elif "Date" in head['name']:
            msgDateVar = head['value']
            msgSpl = msgDateVar.split("(")
            dateTimVar = datetime.datetime.strptime(msgSpl[0].strip(), '%a, %d %b %Y %H:%M:%S %z')
            dateVar = dateTimVar.astimezone(pytz.timezone("Europe/Madrid")).strftime('%d/%m/%Y  %H:%M')
        elif "Delivered-To" in head['name']:
            emailDeliveVar = head['value']

        if emailDeliveVar == "":
            emailDeliveVar = ""

    content = msg['payload']['body']['size']
    if content != 0:

        emailBodySecure = msg['payload']['body']['data']
        emailBody64 = base64.urlsafe_b64decode(emailBodySecure.encode('ISO-8859-1'))
        emailBody = emailBody64
        soup = BeautifulSoup(emailBody, 'html.parser')
        soup.find_all('body')
        emailBody = clear_email_body(soup.find_all('body')[0])

    else:
        parts = msg['payload']['parts']

        if len(parts) <= 1:
            emailBodySecure = msg['payload']['parts'][0]['body']['data']

        else:

            emailBodySecure = msg['payload']['parts'][1]['body']['data']

        emailBody64 = base64.urlsafe_b64decode(emailBodySecure.encode('ISO-8859-1'))

        soup = BeautifulSoup(emailBody64, 'html.parser')

        emailBodypre = soup.find('body')

        try:
            for tag in emailBodypre.findAll(True):
                if tag.name == "style":
                    tag.replaceWith("")
        except:
            emailBody = clear_email_body(emailBodypre)
        emailBody = clear_email_body(emailBodypre)

    emailFrame = Frame(root)
    emailFrame.config()
    emailFrame.pack(side=LEFT, fill="y")

    headFrame = Frame(emailFrame)
    headFrame.config(padx=18, pady=18)
    headFrame.grid(row=0, sticky=W)

    emailSubjectLabel = Label(headFrame, text=subVar)
    emailSubjectLabel.config(font=(elementFgFamily, elementFgSize), padx=8)
    emailSubjectLabel.grid(row=0, sticky=W)

    emailFromLabel = Label(headFrame, text="De: " + fromVar)
    emailFromLabel.config(font=(elementFgFamily, subEleFgSize), padx=18)
    emailFromLabel.grid(row=1, sticky=W)

    emailDateLabel = Label(headFrame, text=dateVar)
    emailDateLabel.config(font=(elementFgFamily, subEleFgSize), padx=18)
    emailDateLabel.grid(row=2, sticky=W)

    emailDeliveLabel = Label(headFrame, text="Para: " + emailDeliveVar)
    emailDeliveLabel.config(font=(elementFgFamily, 8), padx=8)
    emailDeliveLabel.grid(row=3, sticky=W)

    htmlFrame = tkinterhtml.HtmlFrame(emailFrame, horizontal_scrollbar="auto")
    htmlFrame.set_content(emailBody)
    htmlFrame.grid(row=1, sticky=S)

    showMessage = True


def ListaMensajes(id):
    global ser, secondMenu, messageId
    remVar = ""
    dateVar = ""
    subVar = ""
    impVar = ""
    staVar = ""
    clearBarra()
    secondMenu = False

    threads = ser.users().messages().list(userId='me', labelIds=[id]).execute()
    messages = threads.get('messages', [])

    if messages:
        i = 0
        for message in messages[:8]:

            msg = ser.users().messages().get(userId='me', id=message["id"]).execute()

            for head in msg['payload']['headers']:

                if "Date" in head['name']:
                    msgDateVar = head['value']
                    msgSpl = msgDateVar.split("(")
                    dateTimVar = datetime.datetime.strptime(msgSpl[0].strip(), '%a, %d %b %Y %H:%M:%S %z')
                    dateVar = dateTimVar.astimezone(pytz.timezone("Europe/Madrid")).strftime('%d/%m  %H:%M')

                elif "From" in head['name']:
                    fromDate = head['value']
                    fromDate = fromDate.split("<")
                    remVar = fromDate[0]

                elif head['name'] == "Subject":
                    subVar = head['value']
                    i += 1

            if 'IMPORTANT' in msg['labelIds']:
                impVar = important

            elif 'STARRED' in msg['labelIds']:
                staVar = starred

            if 'UNREAD' in msg['labelIds']:
                bgVar = menuBg
                fgVar = "black"
            else:
                bgVar = subEleBg
                fgVar = elementoFg

            messageId = msg['id']

            messSupFrame = Frame(barra)
            messSupFrame.pack(pady=10, padx=20)

            messFrame = Frame(messSupFrame)
            messFrame.config(padx=8, pady=8, bg=bgVar)
            messFrame.grid(row=i, sticky=W + E)
            messFrame.bind("<Button-1>", lambda event, messageId=messageId: muestraEmail(event, messageId))

            impImg = Label(messFrame, image=impVar)
            impImg.config(bg=bgVar, fg=fgVar, font=(elementFgFamily, subEleFgSize))
            impImg.grid(row=0, column=0)
            impImg.bind("<Button-1>", lambda event, messageId=messageId: muestraEmail(event, messageId))

            rem = Label(messFrame, text=remVar)
            rem.config(bg=bgVar, fg=fgVar, font=(elementFgFamily, subEleFgSize), anchor=W)
            rem.grid(row=0, column=1, sticky=W)
            rem.bind("<Button-1>", lambda event, messageId=messageId: muestraEmail(event, messageId))

            date = Label(messFrame, text=dateVar)
            date.config(pady=3, bg=bgVar, fg=fgVar, font=(elementFgFamily, subEleFgSize), anchor=E)
            date.grid(row=0, column=2, sticky=E, columnspan=1)
            date.bind("<Button-1>", lambda event, messageId=messageId: muestraEmail(event, messageId))

            staImg = Label(messFrame, image=staVar)
            staImg.config(bg=bgVar, fg=fgVar, font=(elementFgFamily, subEleFgSize))
            staImg.grid(row=1, column=0)
            staImg.bind("<Button-1>", lambda event, messageId=messageId: muestraEmail(event, messageId))

            bodyLabel = Label(messFrame, text=subVar)
            bodyLabel.config(bg=bgVar, fg=fgVar, font=(elementFgFamily, subEleFgSize), width=50, anchor=W)
            bodyLabel.grid(row=1, column=1, sticky=W + E, columnspan=2, )
            bodyLabel.bind("<Button-1>", lambda event, messageId=messageId: muestraEmail(event, messageId))

        secondMenu = True


# creacion de la primera barrra lateral
def Menu():
    global ser, labelimgVar, label, labelName, labelId
    # BACK

    # Información de la cuenta de google
    userInfoVar = ser.users().getProfile(userId='me').execute()
    # Obtenemos las carpetas
    threads = ser.users().labels().list(userId='me').execute()
    labels = threads.get('labels', [])

    # Bloque padre
    menu = Frame(root)
    menu.config(bg=menuBg, width=270, padx=18, pady=18)
    menu.pack(side=LEFT, fill="y")

    # -- Bloque Info de usuario--

    infoFrame = Frame(menu)
    infoFrame.config(padx=10, pady=10, bg=elementBg)
    infoFrame.grid(row=0, column=0, sticky=W + E)

    cuentaImg = Label(infoFrame, text="Cuenta de Google ", compound="left")
    cuentaImg.config(padx=10, pady=5, bg=elementBg, anchor=W, font=(elementFgFamily, elementFgSize))
    cuentaImg.grid(row=0, column=0, sticky=W + E)

    # Mostramos la dirección
    userInfoLabel = Label(infoFrame, text=userInfoVar['emailAddress'])
    userInfoLabel.config(padx=10, bg=elementBg, anchor=W, font=(elementFgFamily, subEleFgSize))
    userInfoLabel.grid(row=1, column=0, sticky=E)

    # -- Bloque intermedio --

    spaceFrame = Frame(menu)
    spaceFrame.config(padx=10, pady=45, bg=menuBg, height=25)
    spaceFrame.grid(row=2, column=0, sticky=W + E)

    # -- Bloque carpetas --

    threadsFrame = Frame(menu)
    threadsFrame.config(padx=10, pady=10, bg=elementBg)
    threadsFrame.grid(row=3, column=0, sticky=W + E)
    # Cabezera
    threadsLabel = Label(threadsFrame, text="Carpetas")
    threadsLabel.config(padx=10, pady=10, anchor=W, bg=elementBg, font=(elementFgFamily, elementFgSize))
    threadsLabel.grid(row=0, column=0, sticky=W + E)

    # Representamos la posición en el grid
    i = 1
    showIndex = 0
    showLabel = True

    # Recorremos las carpetas
    for labelled in labels:
        # Obtenemos la información de la carpeta
        labinfo = ser.users().labels().get(userId="me", id=labelled['id']).execute()

        # Si no hay mensajes sin leer no lo muestres!
        labUnread = labinfo['messagesUnread']
        if labUnread == 0:
            labUnread = ""

        # Asignamos iconos
        # eliminamos algunas bandejas
        # Traducimos los nombres

        if labelled['name'] == "INBOX":
            labelimgVar = inbox
            labelName = "Recibidos"
            showLabel = True
        elif labelled['name'] == "SPAM":
            labelimgVar = spam
            labelName = "Spam"
            showLabel = True
        elif labelled['name'] == "SENT":
            labelimgVar = sent
            labelName = "Enviados"
            showLabel = True
        elif labelled['name'] == "CHAT":
            labelimgVar = chat
            labelName = "Chat"
            showLabel = False
        elif labelled['name'] == "IMPORTANT":
            labelimgVar = important
            labelName = "Importantes"
            showLabel = True
        elif labelled['name'] == "STARRED":
            labelimgVar = starred
            labelName = "Destacados"
            showLabel = True
        elif labelled['name'] == "TRASH":
            labelimgVar = trash
            labelName = "Papelera"
            showLabel = True
        elif labelled['name'] == "DRAFT":
            labelimgVar = draft
            labelName = "Borrador"
            showLabel = True
        elif labelled['name'] == "UNREAD":
            showLabel = False
        elif labelled['name'].find("CATEGORY") != -1:

            showLabel = False
        # Icono general
        else:
            labelimgVar = label
            labelName = labelled['name']

            showLabel = True
        labelId = labelled['id']
        if showLabel:
            inboxImg = Button(threadsFrame, text=labelName, image=labelimgVar, compound="left",
                              command=lambda labelId=labelId: ListaMensajes(labelId))
            inboxImg.config(padx=10, pady=8, bg=elementBg, font=(elementFgFamily, subEleFgSize), anchor=W, bd=0,
                            activeforeground=elementoFg, activebackground=subEleBg)
            inboxImg.bind("<Button-1>", callback)
            inboxImg.grid(row=i + 1, column=0, sticky=W)

            inboxUnLabel = Label(threadsFrame, text=labUnread)
            inboxUnLabel.config(pady=3, bg=elementBg, font=(elementFgFamily, subEleFgSize))
            inboxUnLabel.grid(row=i + 1, column=1, sticky=W)
            i += 1


def callback(event):
    global buttonReg
    if buttonReg == "":
        buttonReg = event.widget
        buttonReg.config(bg=subEleBg, fg=elementoFg)
    else:
        buttonReg.config(bg=elementBg, fg="black")
        event.widget.config(bg=subEleBg, fg=elementoFg)
        buttonReg = event.widget


Menu()

barra = Frame(root)
barra.config(bg=elementBg, width=0)
barra.pack(side=LEFT, fill="y")

emailFrame = Frame(root)
emailFrame.config(width=0)
emailFrame.pack(side=LEFT, fill="y")

root.mainloop()
