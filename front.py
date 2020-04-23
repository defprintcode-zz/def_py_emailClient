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


# creacion de la primera barrra lateral
def Menu():
    global ser, labelimgVar, label
    # BACK

    # Información de la cuenta de google
    userInfoVar = ser.users().getProfile(userId='me').execute()
    # Obtenemos las carpetas
    threads = ser.users().labels().list(userId='me').execute()
    labels = threads.get('labels', [])

    # FRONT
    # Variables de color

    # --Background--
    menuBg = "#6f916f"
    elementBg = "#b7c8b7"
    subEleBg = "#dbe3db"
    # --Font Color--
    elementoFg = "#555"

    # FontFamily
    elementFgFamily = "Tahoma"
    elementFgSize = 16
    subEleFgSize = 10

    # Bloque padre
    menu = Frame()
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
    showLabel = True
    # Recorremos las carpetas
    for labelled in labels:
        # Obtenemos la información de la carpeta
        labinfo = ser.users().labels().get(userId="me", id=labelled['id']).execute()
        print(labinfo)
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
        elif labelled['name'] == "SPAM":
            labelimgVar = spam
            labelName = "Spam"
        elif labelled['name'] == "SENT":
            labelimgVar = sent
            labelName = "Enviados"
        elif labelled['name'] == "CHAT":
            labelimgVar = chat
            labelName = "Chat"
        elif labelled['name'] == "IMPORTANT":
            labelimgVar = important
            labelName = "Importantes"
        elif labelled['name'] == "STARRED":
            labelimgVar = starred
            labelName = "Destacados"
        elif labelled['name'] == "TRASH":
            labelimgVar = trash
            labelName = "Papelera"
        elif labelled['name'] == "DRAFT":
            labelimgVar = draft
            labelName = "Borrador"
        elif labelled['name'] == "UNREAD":
            showLabel = False
        elif labelled['name'].find("CATEGORY") != -1:
            print(labelled['name'].find("CATEGORY"))
            print(labelled['name'])
            showLabel = False
        # Icono general
        else:
            labelimgVar = label
            labelName = labelled['name']
            showLabel = True

        if showLabel:
            inboxImg = Label(threadsFrame, text=labelName, image=labelimgVar, compound="left")
            inboxImg.config(padx=10, pady=3, bg=elementBg, font=(elementFgFamily, subEleFgSize), anchor=W)
            inboxImg.grid(row=i + 1, column=0, sticky=W)

            inboxUnLabel = Label(threadsFrame, text=labUnread)
            inboxUnLabel.config(pady=3, bg=elementBg, font=(elementFgFamily, subEleFgSize))
            inboxUnLabel.grid(row=i + 1, column=1, sticky=W)

            i += 1


def menuLateral():
    barra = Frame()
    barra.config(bg="#93ac93", width=361)
    barra.pack(side=LEFT, fill="y")


Menu()
menuLateral()
root.mainloop()
