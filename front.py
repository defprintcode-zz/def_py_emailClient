from tkinter import *
from PIL import ImageTk, Image
from service import service
from google.auth.transport.requests import Request
from tkinter import filedialog
import time

# Iniciamos Tkinter
root = Tk()

# Caracteristicas iniciales
root.title("Email Client by DefPrintCode():")
root.config(bg="#f9f9f9")
# HD
root.geometry("1080x720")

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


def clearFrame():
    global secondMenu, barra

    if secondMenu:
        for widget in barra.winfo_children():
            widget.destroy()

        barra.pack_forget()
        barra = Frame(root)
        barra.config(bg=elementBg)
        barra.pack(side=LEFT, fill="y")


def ListaMensajes(id):
    global ser, secondMenu
    remVar = ""
    dateVar = ""
    subVar = ""
    impVar = ""
    staVar = ""
    bgVar = ""
    fgVar = ""
    clearFrame()
    secondMenu = False

    threads = ser.users().messages().list(userId='me', labelIds=[id]).execute()
    messages = threads.get('messages', [])

    if messages:
        i = 0
        for message in messages[:9]:

            msg = ser.users().messages().get(userId='me', id=message["id"]).execute()

            for head in msg['payload']['headers']:

                if "Date" in head['name']:
                    dateVar = head['value']
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

            messSupFrame = Frame(barra)
            messSupFrame.pack(pady=10, padx=20)

            messFrame = Frame(messSupFrame)
            messFrame.config(padx=8, pady=8, bg=bgVar)
            messFrame.grid(row=i, sticky=W + E)

            impImg = Label(messFrame, image=impVar)
            impImg.config(bg=bgVar, fg=fgVar, font=(elementFgFamily, subEleFgSize))
            impImg.grid(row=0, column=0)

            rem = Label(messFrame, text=remVar)
            rem.config(bg=bgVar, fg=fgVar, font=(elementFgFamily, subEleFgSize), anchor=W)
            rem.grid(row=0, column=1, sticky=W)

            date = Label(messFrame, text=dateVar)
            date.config(pady=3, bg=bgVar, fg=fgVar, font=(elementFgFamily, subEleFgSize), anchor=E)
            date.grid(row=0, column=2, sticky=E, columnspan=1)

            staImg = Label(messFrame, image=staVar)
            staImg.config(bg=bgVar, fg=fgVar, font=(elementFgFamily, subEleFgSize))
            staImg.grid(row=1, column=0)

            bodyLabel = Label(messFrame, text=subVar)
            bodyLabel.config(bg=bgVar, fg=fgVar, font=(elementFgFamily, subEleFgSize), width=50, anchor=W)
            bodyLabel.grid(row=1, column=1, sticky=W + E, columnspan=2, )
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
        buttonReg.config(bg=subEleBg,fg=elementoFg)

    else:
        buttonReg.config(bg=subEleBg,fg=elementoFg)

    """print(event.widget)
    event.widget.config(bg="red")"""


Menu()
barra = Frame(root)
barra.config(bg=elementBg)
barra.pack(side=LEFT, fill="y")

root.mainloop()
