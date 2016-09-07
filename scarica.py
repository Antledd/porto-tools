# coding: utf-8
from porto.author import Author
import requests
import codecs
import begin



authors = [
    Author(firstname="Fulvio", lastname="Corno", id="002154"),
    Author(firstname="Dario", lastname="Bonino", id="012325"),
    Author(firstname="Luigi", lastname="De Russis", id="025734"),
    Author(firstname="Sebastian", lastname="Aced Lopez", id="027070"),
    Author(firstname="Faisal", lastname="Razzak", id="023127"),
    Author(firstname="Muhammad", lastname="Sanaullah", id="024462"),
    Author(firstname="Laura", lastname="Farinetti", id="002236"),
    Author(firstname="Teodoro", lastname="Montanaro", id="036541"),
    Author(firstname="Alberto", lastname="Monge Roffarello", id="040637"),
]

baseURL = "http://porto.polito.it/cgi/exportview/creators/"
output_basedir = "./cached_js/"


def scarica_autore(author):

    name = author.lastname + '=3A' + author.firstname + '=3A' + author.id + '=3A' + '.js'

    portoURL = baseURL + name + "/JSON/" + name
    filename = output_basedir + name

    r = requests.get(portoURL)

    try:
        porto_json = r.json()
        print "%s has %d papers" % (author.lastname, len(porto_json))

        porto_text = r.text

        f = codecs.open(filename, "w", encoding="utf-8")
        f.write(porto_text)
        f.close()
    except ValueError:
        print "ERROR in processing %s", author.lastname


@begin.start(auto_convert=True)
def run(list=False, *selected):
    """
    Scarica automaticamente pubblicazioni dal PORTO in formato JSON.

    Opzioni:
        scarica --list
            stampa l'elenco degli autori noti al programma

        scarica (default)
            scarica e salva le pubblicazioni di TUTTI gli autori noti

        scarica <id> <id> <id> ...
            scarica e salva solo le pubblicazioni degli autori citati
            <id> può essere una parte (substring) della matricola autore
            <id> può essere una parte (substring, case-insensitive) del cognome autore
            in caso di match multipli, vale solo il primo
    """

    if(list==True):
        print "Known authors:"
        for author in authors:
            print "%s: %s %s" % (author.id, author.lastname, author.firstname)
    elif len(selected)==0:
        # print all
        print "Downloading all authors"
        for author in authors:
            print author
            scarica_autore(author)
    else:
        print "Downloading matching authors", selected
        for sel in selected:
            print sel
            sel_author = [a for a in authors if (sel in a.id or sel.lower() in a.lastname.lower())]
            if(len(sel_author)==1):
                print sel_author[0]
                scarica_autore(sel_author[0])