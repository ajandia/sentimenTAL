#! /usr/bin/python
# -*- coding: utf-8 -*-

import spacy
import random
import operator
import pickle
from spacy.training import Example
from flask import Markup

def load_model():
    model = pickle.load(open('model_pkl', 'rb'))
    return model

def labelling(text, model):
    # We apply the model on the text
    doc = model(text)
    # We return the text with annotation predictions
    for ent in reversed(doc.ents):
        replacement = "<{}_label>{}</{}_label>".format((ent.label_.lower()),ent.text, (ent.label_.lower()))
        position = ent.start_char
        length_of_replaced = ent.end_char - ent.start_char
        text = text[:position] + replacement + text[position+length_of_replaced:]
    return text

def occurrences(text_label):
    compte_occ = []
    Sentiment = {}
    Sentiment["Colère"] = text_label.count('</col_label>')
    Sentiment["Dégoût"] = text_label.count('</deg_label>')
    Sentiment["Joie"] = text_label.count('</joie_label>')
    Sentiment["Moquerie"] = text_label.count('</moq_label>')
    Sentiment["Peur"] = text_label.count('</peur_label>')
    Sentiment["Surprise"] = text_label.count('</sur_label>')
    Sentiment["Tristesse"] = text_label.count('</tri_label>')
    for k,v in Sentiment.items():
        if v > 0:
            compte_occ.append(Markup(f'Le sentiment <strong>{(k.lower())}</strong> apparaît <strong>{v}</strong> fois dans le texte.'))
    return compte_occ

def principal(text_label):
    Sentiment = {}
    Sentiment["Colère"] = text_label.count('</col_label>')
    Sentiment["Dégoût"] = text_label.count('</deg_label>')
    Sentiment["Joie"] = text_label.count('</joie_label>')
    Sentiment["Moquerie"] = text_label.count('</moq_label>')
    Sentiment["Peur"] = text_label.count('</peur_label>')
    Sentiment["Surprise"] = text_label.count('</sur_label>')
    Sentiment["Tristesse"] = text_label.count('</tri_label>')
    for k,v in Sentiment.items():
        max_key = max(Sentiment.items(), key=operator.itemgetter(1))[0]
        if max_key != 'Dégoût':
            max_occ = Markup(f'La <strong>{(max_key.lower())}</strong> est le sentiment principal dans le texte.')
        else :
            max_occ = Markup(f'Le <strong>{(max_key.lower())}</strong> est le sentiment principal dans le texte.')
    return max_occ

