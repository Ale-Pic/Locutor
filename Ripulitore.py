import re
import os
import json
from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple
import time
import requests
from bs4 import BeautifulSoup, Tag, NavigableString
import pickle

'''
def int_to_roman(num):
    if num > 4000:
        return str(num)
    values = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
    ]
    result = ""
    for value, symbol in values:
        while num >= value:
            result += symbol
            num -= value
    return result


# -----------------------------
# Core configuration
# -----------------------------

VOWELS = set("AEIOUYaeiouy")
LIQUIDS = set("LNRlnr")
NON_LIQUID_CONSONANTS = set("BCDFGHMPQSTVXZbcdfghmpqstvxz")  # as requested
# NOTE: after placeholdering, original 'V/v' becomes placeholder, but V is included per spec.

PLACEHOLDER_LO = "#"
PLACEHOLDER_UP = "¤"  # any char not in Latin text; must be distinct from '#'


_SERVO = {
"servo","servas","servat","servamus","servatis","servant",
"servor","servaris","servatur","servamur","servamini","servantur",

"servabam","servabas","servabat","servabamus","servabatis","servabant",
"servabar","servabaris","servabatur","servabamur","servabamini","servabantur",

"servabo","servabis","servabit","servabimus","servabitis","servabunt",
"servabor","servaberis","servabitur","servabimur","servabimini","servabuntur",

"servavi","servavisti","servavit","servavimus","servavistis","servaverunt","servavere",
"servasti","servastis","servarunt",

"servaveram","servaveras","servaverat","servaveramus","servaveratis","servaverant",
"servavero","servaveris","servaverit","servaverimus","servaveritis","servaverint",

"servem","serves","servet","servemus","servetis","servent",
"server","servetur","servemur","servemini","serventur",

"servarem","servares","servaret","servaremus","servaretis","servarent",
"servarer","servareris","servaretur","servaremur","servaremini","servarentur",

"servaverim","servavissem","servavisses","servavisset","servavissemus","servavissetis","servavissent",

"serva","servate","servato","servatote","servanto",
"servare","servari","servavisse",

# present participle
"servans","servantis","servanti","servantem","servante",
"servantes","servantium","servantibus",
"servantia",

# gerundive
"servandus","servanda","servandum","servandi","servandae","servando","servandam","servande",
"servandorum","servandarum","servandis","servandos","servandas",

# perfect participle
"servatus","servata","servatum","servati","servatae","servato","servatam","servate",
"servatorum","servatarum","servatis","servatos","servatas",

# future participle
"servaturus","servatura","servaturum","servaturi","servaturae","servaturo","servaturam","servature",
"servaturorum","servaturarum","servaturis","servaturos","servaturas"
}
_SERVIO = {
"servio","servis","servitis","serviunt",
"servior","serviris","servitur","servimur","servimini","serviuntur",

"serviebam","serviebas","serviebat","serviebamus","serviebatis","serviebant",
"serviebar","serviebaris","serviebatur","serviebamur","serviebamini","serviebantur",

"serviam","servies","serviet","serviemus","servietis","servient",
"serviar","servieris","servietur","serviemur","serviemini","servientur",

"servivi","servii","servivisti","serviisti","servivit","serviit","servivimus","serviimus",
"servivistis","serviistis","serviverunt","servivere","servierunt","serviere",

"serviveram","servieram","serviveras","servieras","serviverat","servierat",
"serviveramus","servieramus","serviveratis","servieratis","serviverant","servierant",

"servivero","serviero","serviveris","servieris","serviverit","servierit",
"serviverimus","servierimus","serviveritis","servieritis","serviverint","servierint",

"serviam","servias","serviat","serviamus","serviatis","serviant",
"serviar","serviaris","serviatur","serviamur","serviamini","serviantur",

"servirem","servires","serviret","serviremus","serviretis","servirent",
"servirer","servireris","serviretur","serviremur","serviremini","servirentur",

"serviverim","servierim",
"servivissem","serviissem","servivisses","serviisses","servivisset","serviisset",
"servivissemus","serviissemus","servivissetis","serviissetis","servivissent","serviissent",

"servite","servito","servitote","serviunto",

"servire","serviri","servivisse","serviisse",

"serviens","servientis","servienti","servientem","serviente",
"servientes","servientium","servientibus","servientia",

"serviendus","servienda","serviendum","serviendi","serviendae","serviendo","serviendam","serviende",
"serviendorum","serviendarum","serviendis","serviendos","serviendas",

"servitus","servita","servitum","serviti","servitae","servito","servitam","servite",
"servitorum","servitarum","servitis","servitos","servitas",

"serviturus","servitura","serviturum","servituri","serviturae","servituro","servituram","serviture",
"serviturorum","serviturarum","servituris","servituros","servituras"
}
_SERVUS = {
"servus","serve","servo","servum",
"servorum","servis","servos"
}
_SERVA = {
"serva","servae","servam","servarum","servis","servas"
}
_SERO = {
"seruisti","seruistis","seruerunt","seruere",
"serueram","serueras","seruerat","serueramus","serueratis","seruerant",
"seruero","seruerit","seruerimus","serueritis","seruerint",
"seruerim",
"seruissem","seruisses","seruisset","seruissemus","seruissetis","seruissent",
"seruisse"
}
_MALO = {
"malui","maluisti","maluit","maluimus","maluistis","maluerunt","maluere",
"malueram","malueras","maluerat","malueramus","malueratis","maluerant",
"maluero","malueris","maluerit","maluerimus","malueritis","maluerint",
"maluerim",
"maluissem","maluisses","maluisset","maluissemus","maluissetis","maluissent",
"maluisse"
}
_MALVA = {
"malva","malvae","malvam","malvarum","malvis","malvas"
}
_MALVACEUS = {
"malvaceus","malvacea","malvaceum",
"malvacei","malvaceae","malvaceo",
"malvaceam","malvacee",
"malvaceorum","malvacearum","malvaceis",
"malvaceos","malvaceas"
}
_VALVA = {
"valva","valvae","valvam","valvarum","valvis","valvas"
}
_VALVATUS = {
# positive
"valvatus","valvata","valvatum",
"valvati","valvatae","valvato",
"valvatam","valvate",
"valvatorum","valvatarum","valvatis",
"valvatos","valvatas",

# comparative
"valvatior","valvatius",
"valvatioris","valvatiori","valvatiorem","valvatiore",
"valvatiores","valvatiorum","valvatioribus",
"valvatiora",

# superlative
"valvatissimus","valvatissima","valvatissimum",
"valvatissimi","valvatissimae","valvatissimo",
"valvatissimam","valvatissime",
"valvatissimorum","valvatissimarum","valvatissimis",
"valvatissimos","valvatissimas"
}
_VALVOLAE = {
"valvolae","valvolarum","valvolis","valvolas"
}
_VALVOLI = {
"valvoli","valvolorum","valvolis","valvolos"
}
_VALEO = {
"valui","valuisti","valuit","valuimus","valuistis","valuerunt","valuere",
"valueram","valueras","valuerat","valueramus","valueratis","valuerant",
"valuero","valueris","valuerit","valuerimus","valueritis","valuerint",
"valuerim",
"valuissem","valuisses","valuisset","valuissemus","valuissetis","valuissent",
"valuisse"
}
_SALIO = {
"saluisti","saluit","saluimus","saluistis","saluerunt",
"salueram","salueras","saluerat","salueramus","salueratis","saluerant",
"saluero","saluerit","saluerimus","salueritis","saluerint",
"saluerim",
"saluissem","saluisses","saluisset","saluissemus","saluissetis","saluissemus","saluissetis","saluisset","saluisse","saluisset","saluissetis","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisset","saluisse","saluissent"
}
_SALVEO = {
"salveo","salves","salvet","salvemus","salvetis","salvent",
"salveor","salvetur","salvemur","salvemini","salventur",

"salvebam","salvebas","salvebat","salvebamus","salvebatis","salvebant",
"salvebar","salvebaris","salvebatur","salvebamur","salvebamini","salvebantur",

"salvebo","salvebis","salvebit","salvebimus","salvebitis","salvebunt",
"salvebor","salveberis","salvebitur","salvebimur","salvebimini","salvebuntur",

"salveam","salveas","salveat","salveamus","salveatis","salveant",
"salvear","salvearis","salveatur","salveamur","salveamini","salveantur",

"salverem","salveres","salveret","salveremus","salveretis","salverent",
"salverer","salvereris","salveretur","salveremur","salveremini","salverentur",

"salve","salvete","salveto","salvetote","salvento",
"salvere","salvemini",

"salveri"
}
_SALVO = {
# indicative present (active + passive)
"salvo","salvas","salvat","salvamus","salvatis","salvant",
"salvor","salvaris","salvatur","salvamur","salvamini","salvantur",

# indicative imperfect (active + passive)
"salvabam","salvabas","salvabat","salvabamus","salvabatis","salvabant",
"salvabar","salvabaris","salvabatur","salvabamur","salvabamini","salvabantur",

# indicative future (active + passive)
"salvabo","salvabis","salvabit","salvabimus","salvabitis","salvabunt",
"salvabor","salvaberis","salvabitur","salvabimur","salvabimini","salvabuntur",

# indicative perfect system (active only)
"salvavi","salvavisti","salvavit","salvavimus","salvavistis","salvaverunt","salvavere",
"salvaveram","salvaveras","salvaverat","salvaveramus","salvaveratis","salvaverant",
"salvavero","salvaveris","salvaverit","salvaverimus","salvaveritis","salvaverint",

# subjunctive present (active + passive)
"salvem","salves","salvet","salvemus","salvetis","salvent",
"salver","salveris","salvetur","salvemur","salvemini","salventur",

# subjunctive imperfect (active + passive)
"salvarem","salvares","salvaret","salvaremus","salvaretis","salvarent",
"salvarer","salvareris","salvaretur","salvaremur","salvaremini","salvarentur",

# subjunctive perfect & pluperfect (active)
"salvaverim",
"salvavissem","salvavisses","salvavisset","salvavissemus","salvavissetis","salvavissent",

# imperatives + infinitives
"salva","salvate","salvato","salvatote","salvanto",
"salvare","salvari",

# perfect infinitive
"salvavisse",

# present participle
"salvans","salvantis","salvanti","salvantem","salvante",
"salvantes","salvantium","salvantibus",
"salvantia",

# gerundive
"salvandus","salvanda","salvandum","salvandi","salvandae","salvando","salvandam","salvande",
"salvandorum","salvandarum","salvandis","salvandos","salvandas",

# perfect participle
"salvatus","salvata","salvatum","salvati","salvatae","salvato","salvatam","salvate",
"salvatorum","salvatarum","salvatis","salvatos","salvatas",

# future participle
"salvaturus","salvatura","salvaturum","salvaturi","salvaturae","salvaturo","salvaturam","salvature",
"salvaturorum","salvaturarum","salvaturis","salvaturos","salvaturas"
}
_SALVATOR = {"salvator", "salvatoris", "salvatori", "salvatorem", "salvatore", "salvatores", "salvatorum", "salvatoribus"}
_SALVATIO = {"salvatio", "salvationis", "salvationi", "salvationem", "salvatione", "salvationes", "salvationum", "salvationibus"}
_SALVAMENTUM = {"salvamentum", "salvamenti", "salvamento", "salvamenta", "salvamentorum", "salvamentis"}
_SALVUS = {
# positive
"salvus","salva","salvum",
"salvae","salvo",
"salvam","salve",
"salvorum","salvarum","salvis",
"salvos","salvas",

# comparative
"salvior","salvius",
"salvioris","salviori","salviorem","salviore",
"salviores","salviorum","salvioribus",
"salviora",

# superlative
"salvissimus","salvissima","salvissimum",
"salvissimi","salvissimae","salvissimo",
"salvissimam","salvissime",
"salvissimorum","salvissimarum","salvissimis",
"salvissimos","salvissimas"
}
_PARVITAS = {
"parvitas","parvitatis","parvitati","parvitatem","parvitate",
"parvitates","parvitatum","parvitatibus"
}
_PARVULUS = {
# positive
"parvulus","parvula","parvulum",
"parvuli","parvulae","parvulo",
"parvulam","parvule",
"parvulorum","parvularum","parvulis",
"parvulos","parvulas",

# comparative
"parvulior","parvulius",
"parvulioris","parvuliori","parvuliorem","parvuliore",
"parvuliores","parvuliorum","parvulioribus",
"parvuliora",

# superlative
"parvulissimus","parvulissima","parvulissimum",
"parvulissimi","parvulissimae","parvulissimo",
"parvulissimam","parvulissime",
"parvulissimorum","parvulissimarum","parvulissimis",
"parvulissimos","parvulissimas"
}
_PARVUS = {
"parvus","parva","parvum",
"parvae","parvo",
"parvam","parve",
"parvorum","parvarum","parvis",
"parvos","parvas"
}
_PAREO = {
"paruisti","paruit","paruimus","paruistis","paruerunt","paruere",
"parueram","parueras","paruerat","parueramus","parueratis","paruerant",
"paruero","parueris","paruerit","paruerimus","parueritis","paruerint",
"paruerim",
"paruissem","paruisses","paruisset","paruissemus","paruissetis","paruissent",
"paruisse"
}

_VOLVO = {
# indicative present (active + passive)
"volvo","volvis","volvitis","volvunt",
"volvor","volveris","volvitur","volvimur","volvimini","volvuntur",

# indicative imperfect (active + passive)
"volvebam","volvebas","volvebat","volvebamus","volvebatis","volvebant",
"volvebar","volvebaris","volvebatur","volvebamur","volvebamini","volvebantur",

# indicative future (active + passive)
"volvam","volves","volvet","volvemus","volvetis","volent",
"volvar","volveris","volvetur","volvemur","volvemini","volentur",

# subjunctive present (active + passive)
"volvam","volvas","volvat","volvamus","volvatis","volvant",
"volvar","volvaris","volvatur","volvamur","volvamini","volvantur",

# subjunctive imperfect (active + passive)
"volverem","volveres","volveret","volveremus","volveretis","volverent",
"volverer","volvereris","volveretur","volveremur","volveremini","volverentur",

# imperatives
"volve","volvite","volvito","volvitote","volvunto",

# infinitives
"volvere","volvi","volvisse",

# present participle
"volvens","volventis","volventi","volentem","volvente",
"volventes","volventium","volventibus","volventia",

# gerundive
"volvendus","volvenda","volvendum","volvendi","volvendae","volvendo","volvendam","volvende",
"volvendorum","volvendarum","volvendis","volvendos","volvendas",

# perfect participle
"volutus","voluta","volutum","voluti","volutae","voluto","volutam","volute",
"volutorum","volutarum","volutis","volutos","volutas",

# future participle
"voluturus","volutura","voluturum","voluturi","voluturae","voluturo","voluturam","voluture",
"voluturorum","voluturarum","voluturis","voluturos","voluturas"
}
_SOLVO = {
# indicative present (active + passive)
"solvo","solvis", "solvitis","solvunt",
"solvor","solvitur","solvimur","solvimini","solvuntur",

# indicative imperfect (active + passive)
"solvebam","solvebas","solvebat","solvebamus","solvebatis","solvebant",
"solvebar","solvebaris","solvebatur","solvebamur","solvebamini","solvebantur",

# indicative future (active + passive)
"solvam","solves","solvet","solvemus","solvetis","solvent",
"solvar","solveris","solvetur","solvemur","solvemini","solventur",

# subjunctive present (active + passive)
"solvam","solvas","solvat","solvamus","solvatis","solvant",
"solvar","solvaris","solvatur","solvamur","solvamini","solvantur",

# subjunctive imperfect (active + passive)
"solverem","solveres","solveret","solveremus","solveretis","solverent",
"solverer","solvereris","solveretur","solveremur","solveremini","solverentur",

# imperatives
"solve","solvite","solvito","solvitote","solvunto",

# infinitives
"solvere",

# present participle
"solvens","solventis","solventi","solventem","solvente",
"solventes","solventium","solventibus","solventia",

# gerundive
"solvendus","solvenda","solvendum","solvendi","solvendae","solvendo","solvendam","solvende",
"solvendorum","solvendarum","solvendis","solvendos","solvendas",

# perfect participle
"solutus","soluta","solutum","soluti","solutae","soluto","solutam","solute",
"solutorum","solutarum","solutis","solutos","solutas",

# future participle
"soluturus","solutura","soluturum","soluturi","soluturae","soluturo","soluturam","soluture",
"soluturorum","soluturarum","soluturis","soluturos","soluturas"
}
_SOLUI = {"soluisti", "soluistis", "soluerunt", "solueram", "solueras",
          "soluerat", "solueramus", "solueratis", "soluerant", "soluero",
          "soluerit", "soluerimus", "solueritis", "soluerint", "soluerim", "soluissem",
          "soluisses", "soluisset", "soluissemus", "soluissetis", "soluissent", "soluisse"}
_SILEO = {
"siluisti","siluit","siluimus","siluistis","siluerunt","siluere",
"silueram","silueras","siluerat","silueramus","silueratis","siluerant",
"siluero","silueris","siluerit","siluerimus","silueritis","siluerint",
"siluerim",
"siluissem","siluisses","siluisset","siluissemus","siluissetis","siluissent",
"siluisse"
}
_SILVA = {
"silva","silvae","silvam","silvarum","silvis","silvas"
}
_SILVANUS = {
"Silvanus","Silvane","Silvani","Silvano","Silvanum",
"Silvanorum","Silvanis","Silvanos"
}
_SILVATICUS = {
# positive
"silvaticus","silvatica","silvaticum",
"silvatici","silvaticae","silvatico",
"silvaticam","silvatice",
"silvaticorum","silvaticarum","silvaticis",
"silvaticos","silvaticas",

# comparative
"silvaticior","silvaticius",
"silvaticioris","silvaticiori","silvaticiorem","silvaticiore",
"silvaticiores","silvaticiorum","silvaticioribus",
"silvaticiora",

# superlative
"silvaticissimus","silvaticissima","silvaticissimum",
"silvaticissimi","silvaticissimae","silvaticissimo",
"silvaticissimam","silvaticissime",
"silvaticissimorum","silvaticissimarum","silvaticissimis",
"silvaticissimos","silvaticissimas"
}
_SILVESCO = {
# indicative present (active only; inchoative verb)
"silvesco","silvescis","silvescit","silvescimus","silvescitis","silvescunt",

# indicative imperfect
"silvescebam","silvescebas","silvescebat","silvescebamus","silvescebatis","silvescebant",

# indicative future
"silvescam","silvesces","silvescet","silvescemus","silvescetis","silvescent",

# subjunctive present
"silvescam","silvescas","silvescat","silvescamus","silvescatis","silvescant",

# subjunctive imperfect
"silvescerem","silvesceres","silvesceret","silvesceremus","silvesceretis","silvescerent",

# imperatives
"silvesce","silvescite","silvescito","silvescitote","silvescunto",

# infinitive
"silvescere",

# present participle
"silvescens","silvescentis","silvescenti","silvescentem","silvescente",
"silvescentes","silvescentium","silvescentibus","silvescentia"
}
_SILVESTER = {
# positive
"silvester","silvestris","silvestre",
"silvestris","silvestri","silvestrem","silvestri",
"silvestres","silvestrium","silvestribus","silvestria",

# comparative
"silvestrior","silvestrius",
"silvestrioris","silvestriori","silvestriorem","silvestriore",
"silvestriores","silvestriorum","silvestrioribus",
"silvestriora",

# superlative
"silvestrissimus","silvestrissima","silvestrissimum",
"silvestrissimi","silvestrissimae","silvestrissimo",
"silvestrissimam","silvestrissime",
"silvestrissimorum","silvestrissimarum","silvestrissimis",
"silvestrissimos","silvestrissimas"
}
_SILVIA = {
"Silvia","Silviae","Silviam","Silviarum","Silviis","Silvias"
}
_SILVICOLA = {
"silvicola","silvicolae","silvicolam","silvicolā","silvicolarum","silvicolis","silvicolas"
}
_SILVICULTRIX = {
"silvicultrix","silvicultricis","silvicultrici","silvicultricem","silvicultrice",
"silvicultrices","silvicultricium","silvicultricibus"
}
_SILVIFRAGUS = {
# positive
"silvifragus","silvifraga","silvifragum",
"silvifragi","silvifragae","silvifrago",
"silvifragam","silvifrage",
"silvifragorum","silvifragarum","silvifragis",
"silvifragos","silvifragas",

# comparative
"silvifragior","silvifragus",
"silvifragioris","silvifragiori","silvifragiorem","silvifragiori",
"silvifragiores","silvifragiorum","silvifragioribus",
"silvifragiora",

# superlative
"silvifragissimus","silvifragissima","silvifragissimum",
"silvifragissimi","silvifragissimae","silvifragissimo",
"silvifragissimam","silvifragissime",
"silvifragissimorum","silvifragissimarum","silvifragissimis",
"silvifragissimos","silvifragissimas"
}
_SILVIGER = {
# positive
"silviger","silvigera","silvigerum",
"silvigeri","silvigerae","silvigero",
"silvigeram","silvigere",
"silvigerorum","silvigerarum","silvigeris",
"silvigeros","silvigeras",

# comparative
"silvigerior","silvigerius",
"silvigerioris","silvigeriori","silvigeriorem","silvigeriore",
"silvigeriores","silvigeriorum","silvigerioribus",
"silvigeriora",

# superlative
"silvigerissimus","silvigerissima","silvigerissimum",
"silvigerissimi","silvigerissimae","silvigerissimo",
"silvigerissimam","silvigerissime",
"silvigerissimorum","silvigerissimarum","silvigerissimis",
"silvigerissimos","silvigerissimas"
}
_SILVOSUS = {
# positive
"silvosus","silvosa","silvosum",
"silvosi","silvosae","silvoso",
"silvosam","silvose",
"silvosorum","silvosarum","silvosis",
"silvosos","silvosas",

# comparative
"silvosior","silvosius",
"silvosioris","silvosiori","silvosiorem","silvosiore",
"silvosiores","silvosiorum","silvosioribus",
"silvosiora",

# superlative
"silvosissimus","silvosissima","silvosissimum",
"silvosissimi","silvosissimae","silvosissimo",
"silvosissimam","silvosissime",
"silvosissimorum","silvosissimarum","silvosissimis",
"silvosissimos","silvosissimas"
}
_SILVULA = {
"silvula","silvulae","silvulam","silvularum","silvulis","silvulas"
}
_ALVEUS = {
"alveus","alvee","alvei","alveo","alveum",
"alveorum","alveos","alveis"
}
_ALO = {
"alui","aluisti","aluit","aluimus","aluistis","aluerunt","aluere",
"alueram","alueras","aluerat","alueramus","alueratis","aluerant",
"aluero","alueris","aluerit","aluerimus","alueritis","aluerint",
"aluerim",
"aluissem","aluisses","aluisset","aluissemus","aluissetis","aluissent",
"aluisse"
}
_ASSERVO = {
# indicative present (active + passive)
"asservo","asservas","asservat","asservamus","asservatis","asservant",
"asservor","asservaris","asservatur","asservamur","asservamini","asservantur",

# indicative imperfect (active + passive)
"asservabam","asservabas","asservabat","asservabamus","asservabatis","asservabant",
"asservabar","asservabaris","asservabatur","asservabamur","asservabamini","asservabantur",

# indicative future (active + passive)
"asservabo","asservabis","asservabit","asservabimus","asservabitis","asservabunt",
"asservabor","asservaberis","asservabitur","asservabimur","asservabimini","asservabuntur",

# indicative perfect system (active)
"asservavi","asservavisti","asservavit","asservavimus","asservavistis","asservaverunt","asservavere",
"asservaveram","asservaveras","asservaverat","asservaveramus","asservaveratis","asservaverant",
"asservavero","asservaveris","asservaverit","asservaverimus","asservaveritis","asservaverint",

# subjunctive present (active + passive)
"asservem","asserves","asservet","asservemus","asservetis","asservent",
"asserver","asservetur","asservemur","asservemini","asserventur",

# subjunctive imperfect (active + passive)
"asservarem","asservares","asservaret","asservaremus","asservaretis","asservarent",
"asservarer","asservareris","asservaretur","asservaremur","asservaremini","asservarentur",

# subjunctive perfect & pluperfect
"asservaverim",
"asservavissem","asservavisses","asservavisset","asservavissemus","asservavissetis","asservavissent",

# imperatives
"asserva","asservate","asservato","asservatote","asservanto",

# infinitives
"asservare","asservari","asservavisse",

# present participle
"asservans","asservantis","asservanti","asservantem","asservante",
"asservantes","asservantium","asservantibus","asservantia",

# gerundive
"asservandus","asservanda","asservandum","asservandi","asservandae","asservando","asservandam","asservande",
"asservandorum","asservandarum","asservandis","asservandos","asservandas",

# perfect participle
"asservatus","asservata","asservatum","asservati","asservatae","asservato","asservatam","asservate",
"asservatorum","asservatarum","asservatis","asservatos","asservatas",

# future participle
"asservaturus","asservatura","asservaturum","asservaturi","asservaturae","asservaturo","asservaturam","asservature",
"asservaturorum","asservaturarum","asservaturis","asservaturos","asservaturas"
}
_CONSERVO = {
# indicative present (active + passive)
"conservo","conservas","conservat","conservamus","conservatis","conservant",
"conservor","conservaris","conservatur","conservamur","conservamini","conservantur",

# indicative imperfect (active + passive)
"conservabam","conservabas","conservabat","conservabamus","conservabatis","conservabant",
"conservabar","conservabaris","conservabatur","conservabamur","conservabamini","conservabantur",

# indicative future (active + passive)
"conservabo","conservabis","conservabit","conservabimus","conservabitis","conservabunt",
"conservabor","conservaberis","conservabitur","conservabimur","conservabimini","conservabuntur",

# indicative perfect system (active)
"conservavi","conservavisti","conservavit","conservavimus","conservavistis","conservaverunt","conservavere",
"conservaveram","conservaveras","conservaverat","conservaveramus","conservaveratis","conservaverant",
"conservavero","conservaveris","conservaverit","conservaverimus","conservaveritis","conservaverint",

# subjunctive present (active + passive)
"conservem","conserves","conservet","conservemus","conservetis","conservent",
"conserver","conservetur","conservemur","conservemini","conserventur",

# subjunctive imperfect (active + passive)
"conservarem","conservares","conservaret","conservaremus","conservaretis","conservarent",
"conservarer","conservareris","conservaretur","conservaremur","conservaremini","conservarentur",

# subjunctive perfect & pluperfect (active)
"conservaverim",
"conservavissem","conservavisses","conservavisset","conservavissemus","conservavissetis","conservavissent",

# imperatives
"conserva","conservate","conservato","conservatote","conservanto",

# infinitives
"conservare","conservari","conservavisse",

# present participle
"conservans","conservantis","conservanti","conservantem","conservante",
"conservantes","conservantium","conservantibus","conservantia",

# gerundive
"conservandus","conservanda","conservandum","conservandi","conservandae","conservando","conservandam","conservande",
"conservandorum","conservandarum","conservandis","conservandos","conservandas",

# perfect participle
"conservatus","conservata","conservatum","conservati","conservatae","conservato","conservatam","conservate",
"conservatorum","conservatarum","conservatis","conservatos","conservatas",

# future participle
"conservaturus","conservatura","conservaturum","conservaturi","conservaturae","conservaturo","conservaturam","conservature",
"conservaturorum","conservaturarum","conservaturis","conservaturos","conservaturas"
}
_INSERVO = {
# indicative present (active + passive)
"inservo","inservas","inservat","inservamus","inservatis","inservant",
"inservor","inservaris","inservatur","inservamur","inservamini","inservantur",

# indicative imperfect (active + passive)
"inservabam","inservabas","inservabat","inservabamus","inservabatis","inservabant",
"inservabar","inservabaris","inservabatur","inservabamur","inservabamini","inservabantur",

# indicative future (active + passive)
"inservabo","inservabis","inservabit","inservabimus","inservabitis","inservabunt",
"inservabor","inservaberis","inservabitur","inservabimur","inservabimini","inservabuntur",

# indicative perfect system (active)
"inservavi","inservavisti","inservavit","inservavimus","inservavistis","inservaverunt","inservavere",
"inservaveram","inservaveras","inservaverat","inservaveramus","inservaveratis","inservaverant",
"inservavero","inservaveris","inservaverit","inservaverimus","inservaveritis","inservaverint",

# subjunctive present (active + passive)
"inservem","inserves","inservet","inservemus","inservetis","inservent",
"inserver","inservetur","inservemur","inservemini","inserventur",

# subjunctive imperfect (active + passive)
"inservarem","inservares","inservaret","inservaremus","inservaretis","inservarent",
"inservarer","inservareris","inservaretur","inservaremur","inservaremini","inservarentur",

# subjunctive perfect & pluperfect
"inservaverim",
"inservavissem","inservavisses","inservavisset","inservavissemus","inservavissetis","inservavissent",

# imperatives
"inserva","inservate","inservato","inservatote","inservanto",

# infinitives
"inservare","inservari","inservavisse",

# present participle
"inservans","inservantis","inservanti","inservantem","inservante",
"inservantes","inservantium","inservantibus","inservantia",

# gerundive
"inservandus","inservanda","inservandum","inservandi","inservandae","inservando","inservandam","inservande",
"inservandorum","inservandarum","inservandis","inservandos","inservandas",

# perfect participle
"inservatus","inservata","inservatum","inservati","inservatae","inservato","inservatam","inservate",
"inservatorum","inservatarum","inservatis","inservatos","inservatas",

# future participle
"inservaturus","inservatura","inservaturum","inservaturi","inservaturae","inservaturo","inservaturam","inservature",
"inservaturorum","inservaturarum","inservaturis","inservaturos","inservaturas"
}
_OBSERVO = {
# indicative present (active + passive)
"observo","observas","observat","observamus","observatis","observant",
"observor","observaris","observatur","observamur","observamini","observantur",

# indicative imperfect (active + passive)
"observabam","observabas","observabat","observabamus","observabatis","observabant",
"observabar","observabaris","observabatur","observabamur","observabamini","observabantur",

# indicative future (active + passive)
"observabo","observabis","observabit","observabimus","observabitis","observabunt",
"observabor","observaberis","observabitur","observabimur","observabimini","observabuntur",

# indicative perfect system (active)
"observavi","observavisti","observavit","observavimus","observavistis","observaverunt","observavere",
"observaveram","observaveras","observaverat","observaveramus","observaveratis","observaverant",
"observavero","observaveris","observaverit","observaverimus","observaveritis","observaverint",

# subjunctive present (active + passive)
"observem","observes","observet","observemus","observetis","observent",
"observer","observetur","observemur","observemini","observentur",

# subjunctive imperfect (active + passive)
"observarem","observares","observaret","observaremus","observaretis","observarent",
"observarer","observareris","observaretur","observaremur","observaremini","observarentur",

# subjunctive perfect & pluperfect
"observaverim",
"observavissem","observavisses","observavisset","observavissemus","observavissetis","observavissent",

# imperatives
"observa","observate","observato","observatote","observanto",

# infinitives
"observare","observari","observavisse",

# present participle
"observans","observantis","observanti","observantem","observante",
"observantes","observantium","observantibus","observantia",

# gerundive
"observandus","observanda","observandum","observandi","observandae","observando","observandam","observande",
"observandorum","observandarum","observandis","observandos","observandas",

# perfect participle
"observatus","observata","observatum","observati","observatae","observato","observatam","observate",
"observatorum","observatarum","observatis","observatos","observatas",

# future participle
"observaturus","observatura","observaturum","observaturi","observaturae","observaturo","observaturam","observature",
"observaturorum","observaturarum","observaturis","observaturos","observaturas"
}
_PRAESERVO = {
# indicative present (active + passive)
"praeservo","praeservas","praeservat","praeservamus","praeservatis","praeservant",
"praeservor","praeservaris","praeservatur","praeservamur","praeservamini","praeservantur",

# indicative imperfect (active + passive)
"praeservabam","praeservabas","praeservabat","praeservabamus","praeservabatis","praeservabant",
"praeservabar","praeservabaris","praeservabatur","praeservabamur","praeservabamini","praeservabantur",

# indicative future (active + passive)
"praeservabo","praeservabis","praeservabit","praeservabimus","praeservabitis","praeservabunt",
"praeservabor","praeservaberis","praeservabitur","praeservabimur","praeservabimini","praeservabuntur",

# indicative perfect system (active)
"praeservavi","praeservavisti","praeservavit","praeservavimus","praeservavistis","praeservaverunt","praeservavere",
"praeservaveram","praeservaveras","praeservaverat","praeservaveramus","praeservaveratis","praeservaverant",
"praeservavero","praeservaveris","praeservaverit","praeservaverimus","praeservaveritis","praeservaverint",

# subjunctive present (active + passive)
"praeservem","praeserves","praeservet","praeservemus","praeservetis","praeservent",
"praeserver","praeserveris","praeservetur","praeservemur","praeservemini","praeserventur",

# subjunctive imperfect (active + passive)
"praeservarem","praeservares","praeservaret","praeservaremus","praeservaretis","praeservarent",
"praeservarer","praeservareris","praeservaretur","praeservaremur","praeservaremini","praeservarentur",

# subjunctive perfect & pluperfect
"praeservaverim",
"praeservavissem","praeservavisses","praeservavisset","praeservavissemus","praeservavissetis","praeservavissent",

# imperatives
"praeserva","praeservate","praeservato","praeservatote","praeservanto",

# infinitives
"praeservare","praeservari","praeservavisse",

# present participle
"praeservans","praeservantis","praeservanti","praeservantem","praeservante",
"praeservantes","praeservantium","praeservantibus","praeservantia",

# gerundive
"praeservandus","praeservanda","praeservandum","praeservandi","praeservandae","praeservando","praeservandam","praeservande",
"praeservandorum","praeservandarum","praeservandis","praeservandos","praeservandas",

# perfect participle
"praeservatus","praeservata","praeservatum","praeservati","praeservatae","praeservato","praeservatam","praeservate",
"praeservatorum","praeservatarum","praeservatis","praeservatos","praeservatas",

# future participle
"praeservaturus","praeservatura","praeservaturum","praeservaturi","praeservaturae","praeservaturo","praeservaturam","praeservature",
"praeservaturorum","praeservaturarum","praeservaturis","praeservaturos","praeservaturas"
}
_RESERVO = {
# indicative present (active + passive)
"reservo","reservas","reservat","reservamus","reservatis","reservant",
"reservor","reservaris","reservatur","reservamur","reservamini","reservantur",

# indicative imperfect (active + passive)
"reservabam","reservabas","reservabat","reservabamus","reservabatis","reservabant",
"reservabar","reservabaris","reservabatur","reservabamur","reservabamini","reservabantur",

# indicative future (active + passive)
"reservabo","reservabis","reservabit","reservabimus","reservabitis","reservabunt",
"reservabor","reservaberis","reservabitur","reservabimur","reservabimini","reservabuntur",

# indicative perfect system (active)
"reservavi","reservavisti","reservavit","reservavimus","reservavistis","reservaverunt","reservavere",
"reservaveram","reservaveras","reservaverat","reservaveramus","reservaveratis","reservaverant",
"reservavero","reservaveris","reservaverit","reservaverimus","reservaveritis","reservaverint",

# subjunctive present (active + passive)
"reservem","reserves","reservet","reservemus","reservetis","reservent",
"reserver","reservetur","reservemur","reservemini","reserventur",

# subjunctive imperfect (active + passive)
"reservarem","reservares","reservaret","reservaremus","reservaretis","reservarent",
"reservarer","reservareris","reservaretur","reservaremur","reservaremini","reservarentur",

# subjunctive perfect & pluperfect
"reservaverim",
"reservavissem","reservavisses","reservavisset","reservavissemus","reservavissetis","reservavissent",

# imperatives
"reserva","reservate","reservato","reservatote","reservanto",

# infinitives
"reservare","reservari","reservavisse",

# present participle
"reservans","reservantis","reservanti","reservantem","reservante",
"reservantes","reservantium","reservantibus","reservantia",

# gerundive
"reservandus","reservanda","reservandum","reservandi","reservandae","reservando","reservandam","reservande",
"reservandorum","reservandarum","reservandis","reservandos","reservandas",

# perfect participle
"reservatus","reservata","reservatum","reservati","reservatae","reservato","reservatam","reservate",
"reservatorum","reservatarum","reservatis","reservatos","reservatas",

# future participle
"reservaturus","reservatura","reservaturum","reservaturi","reservaturae","reservaturo","reservaturam","reservature",
"reservaturorum","reservaturarum","reservaturis","reservaturos","reservaturas"
}
_PERSERVO = {
# indicative present (active + passive)
"perservo","perservas","perservat","perservamus","perservatis","perservant",
"perservor","perservaris","perservatur","perservamur","perservamini","perservantur",

# indicative imperfect (active + passive)
"perservabam","perservabas","perservabat","perservabamus","perservabatis","perservabant",
"perservabar","perservabaris","perservabatur","perservabamur","perservabamini","perservabantur",

# indicative future (active + passive)
"perservabo","perservabis","perservabit","perservabimus","perservabitis","perservabunt",
"perservabor","perservaberis","perservabitur","perservabimur","perservabimini","perservabuntur",

# indicative perfect system (active)
"perservavi","perservavisti","perservavit","perservavimus","perservavistis","perservaverunt","perservavere",
"perservaveram","perservaveras","perservaverat","perservaveramus","perservaveratis","perservaverant",
"perservavero","perservaveris","perservaverit","perservaverimus","perservaveritis","perservaverint",

# subjunctive present (active + passive)
"perservem","perserves","perservet","perservemus","perservetis","perservent",
"perserver","perserveris","perservetur","perservemur","perservemini","perserventur",

# subjunctive imperfect (active + passive)
"perservarem","perservares","perservaret","perservaremus","perservaretis","perservarent",
"perservarer","perservareris","perservaretur","perservaremur","perservaremini","perservarentur",

# subjunctive perfect & pluperfect
"perservaverim",
"perservavissem","perservavisses","perservavisset","perservavissemus","perservavissetis","perservavissent",

# imperatives
"perserva","perservate","perservato","perservatote","perservanto",

# infinitives
"perservare","perservari","perservavisse",

# present participle
"perservans","perservantis","perservanti","perservantem","perservante",
"perservantes","perservantium","perservantibus","perservantia",

# gerundive
"perservandus","perservanda","perservandum","perservandi","perservandae","perservando","perservandam","perservande",
"perservandorum","perservandarum","perservandis","perservandos","perservandas",

# perfect participle
"perservatus","perservata","perservatum","perservati","perservatae","perservato","perservatam","perservate",
"perservatorum","perservatarum","perservatis","perservatos","perservatas",

# future participle
"perservaturus","perservatura","perservaturum","perservaturi","perservaturae","perservaturo","perservaturam","perservature",
"perservaturorum","perservaturarum","perservaturis","perservaturos","perservaturas"
}
_SERVABILIS = {
# positive
"servabilis","servabile",
"servabilis","servabili","servabilem","servabili",
"servabiles","servabilium","servabilibus","servabilia",

# comparative
"servabilior","servabilius",
"servabilioris","servabiliori","servabiliorem","servabiliore",
"servabiliores","servabiliorum","servabilioribus",
"servabiliora",

# superlative
"servabilissimus","servabilissima","servabilissimum",
"servabilissimi","servabilissimae","servabilissimo",
"servabilissimam","servabilissime",
"servabilissimorum","servabilissimarum","servabilissimis",
"servabilissimos","servabilissimas"
}
_SERVATOR = {
"servator","servatoris","servatori","servatorem","servatore",
"servatores","servatorum","servatoribus"
}
_ASSERVIO = {
# indicative present (active + passive)
"asservio","assiservis","asservitis","asserviunt",
"asservior","asserviris","asservitur","asservimur","asservimini","asserviuntur",

# indicative imperfect (active + passive)
"asserviebam","asserviebas","asserviebat","asserviebamus","asserviebatis","asserviebant",
"asserviebar","asserviebaris","asserviebatur","asserviebamur","asserviebamini","asserviebantur",

# indicative future (active + passive)
"asserviam","asservies","asserviet","asserviemus","asservietis","asservient",
"asserviar","asservieris","asservietur","asserviemur","asserviemini","asservientur",

# indicative perfect system (active; iv/i alternation)
"asservivi","asservii","asservivisti","asserviisti","asservivit","asserviit",
"asservivimus","asserviimus","asservivistis","asserviistis",
"asserviverunt","asservivere","asserviierunt","asserviiere",

"asserviveram","asserviieram","asserviveras","asserviieras","asserviverat","asserviierat",
"asserviveramus","asserviieramus","asserviveratis","asserviieratis","asserviverant","asserviierant",

"asservivero","asserviiero","asserviveris","asserviieris","asserviverit","asserviierit",
"asserviverimus","asserviierimus","asserviveritis","asserviieritis","asserviverint","asserviierint",

# subjunctive present (active + passive)
"asserviam","asservias","asserviat","asserviamus","asserviatis","asserviant",
"asserviar","asserviaris","asserviatur","asserviamur","asserviamini","asserviantur",

# subjunctive imperfect (active + passive)
"asservirem","asservires","asserviret","asserviremus","asserviretis","asservirent",
"asservirer","asservireris","asserviretur","asserviremur","asserviremini","asservirentur",

# subjunctive perfect & pluperfect
"asserviverim","asserviierim",
"asservivissem","asserviissem","asservivisses","asserviiisses","asservivisset","asserviisset",
"asservivissemus","asserviissemus","asservivissetis","asserviissetis","asservivissent","asserviissent",

# imperatives
"asservite","asservito","asservitote","asserviunto",

# infinitives
"asservire","asserviri","asservivisse","asserviisse",

# present participle
"asserviens","asservientis","asservienti","asservientem","asserviente",
"asservientes","asservientium","asservientibus","asservientia",

# gerundive
"asserviendus","asservienda","asserviendum","asserviendi","asserviendae","asserviendo","asserviendam","asserviende",
"asserviendorum","asserviendarum","asserviendis","asserviendos","asserviendas",

# perfect participle
"asservitus","asservita","asservitum","asserviti","asservitae","asservito","asservitam","asservite",
"asservitorum","asservitarum","asservitis","asservitos","asservitas",

# future participle
"asserviturus","asservitura","asserviturum","asservituri","asserviturae","asservituro","asservituram","asserviture",
"asserviturorum","asserviturarum","asservituris","asservituros","asservituras"
}
_DESERVIO = {
# indicative present (active + passive)
"deservio","deservis","deservit","deservimus","deservitis","deserviunt",
"deservior","deserviris","deservitur","deservimur","deservimini","deserviuntur",

# indicative imperfect (active + passive)
"deserviebam","deserviebas","deserviebat","deserviebamus","deserviebatis","deserviebant",
"deserviebar","deserviebaris","deserviebatur","deserviebamur","deserviebamini","deserviebantur",

# indicative future (active + passive)
"deserviam","deservies","deserviet","deserviemus","deservietis","deservient",
"deserviar","deservieris","deservietur","deserviemur","deserviemini","deservientur",

# indicative perfect system (active; iv/i alternation)
"deservivi","deservii","deservivisti","deserviisti","deservivit","deserviit",
"deservivimus","deserviimus","deservivistis","deserviistis",
"deserviverunt","deservivere","deserviierunt","deserviiere",

"deserviveram","deserviieram","deserviveras","deserviieras","deserviverat","deserviierat",
"deserviveramus","deserviieramus","deserviveratis","deserviieratis","deserviverant","deserviierant",

"deservivero","deserviiero","deserviveris","deserviieris","deserviverit","deserviierit",
"deserviverimus","deserviierimus","deserviveritis","deserviieritis","deserviverint","deserviierint",

# subjunctive present (active + passive)
"deserviam","deservias","deserviat","deserviamus","deserviatis","deserviant",
"deserviar","deserviaris","deserviatur","deserviamur","deserviamini","deserviantur",

# subjunctive imperfect (active + passive)
"deservirem","deservires","deserviret","deserviremus","deserviretis","deservirent",
"deservirer","deservireris","deserviretur","deserviremur","deserviremini","deservirentur",

# subjunctive perfect & pluperfect
"deserviverim","deserviierim",
"deservivissem","deserviissem","deservivisses","deserviiisses","deservivisset","deserviisset",
"deservivissemus","deserviissemus","deservivissetis","deserviissetis","deservivissent","deserviissent",

# imperatives
"deservi","deservite","deservito","deservitote","deserviunto",

# infinitives
"deservire","deserviri","deservivisse","deserviisse",

# present participle
"deserviens","deservientis","deservienti","deservientem","deserviente",
"deservientes","deservientium","deservientibus","deservientia",

# gerundive
"deserviendus","deservienda","deserviendum","deserviendi","deserviendae","deserviendo","deserviendam","deserviende",
"deserviendorum","deserviendarum","deserviendis","deserviendos","deserviendas",

# perfect participle
"deservitus","deservita","deservitum","deserviti","deservitae","deservito","deservitam","deservite",
"deservitorum","deservitarum","deservitis","deservitos","deservitas",

# future participle
"deserviturus","deservitura","deserviturum","deservituri","deserviturae","deservituro","deservituram","deserviture",
"deserviturorum","deserviturarum","deservituris","deservituros","deservituras"
}
_INSERVIO = {
# indicative present (active + passive)
"inservio","inservis","inservitis","inserviunt",
"inservior","inserviris","inservitur","inservimur","inservimini","inserviuntur",

# indicative imperfect (active + passive)
"inserviebam","inserviebas","inserviebat","inserviebamus","inserviebatis","inserviebant",
"inserviebar","inserviebaris","inserviebatur","inserviebamur","inserviebamini","inserviebantur",

# indicative future (active + passive)
"inserviam","inservies","inserviet","inserviemus","inservietis","inservient",
"inserviar","inservieris","inservietur","inserviemur","inserviemini","inservientur",

# indicative perfect system (active; iv/i alternation)
"inservivi","inservii","inservivisti","inserviisti","inservivit","inserviit",
"inservivimus","inserviimus","inservivistis","inserviistis",
"inserviverunt","inservivere","inserviierunt","inserviiere",

"inserviveram","inserviieram","inserviveras","inserviieras","inserviverat","inserviierat",
"inserviveramus","inserviieramus","inserviveratis","inserviieratis","inserviverant","inserviierant",

"inservivero","inserviiero","inserviveris","inserviieris","inserviverit","inserviierit",
"inserviverimus","inserviierimus","inserviveritis","inserviieritis","inserviverint","inserviierint",

# subjunctive present (active + passive)
"inserviam","inservias","inserviat","inserviamus","inserviatis","inserviant",
"inserviar","inserviaris","inserviatur","inserviamur","inserviamini","inserviantur",

# subjunctive imperfect (active + passive)
"inservirem","inservires","inserviret","inserviremus","inserviretis","inservirent",
"inservirer","inservireris","inserviretur","inserviremur","inserviremini","inservirentur",

# subjunctive perfect & pluperfect
"inserviverim","inserviierim",
"inservivissem","inserviissem","inservivisses","inserviiisses","inservivisset","inserviisset",
"inservivissemus","inserviissemus","inservivissetis","inserviissetis","inservivissent","inserviissent",

# imperatives
"inservite","inservito","inservitote","inserviunto",

# infinitives
"inservire","inserviri","inservivisse","inserviisse",

# present participle
"inserviens","inservientis","inservienti","inservientem","inserviente",
"inservientes","inservientium","inservientibus","inservientia",

# gerundive
"inserviendus","inservienda","inserviendum","inserviendi","inserviendae","inserviendo","inserviendam","inserviende",
"inserviendorum","inserviendarum","inserviendis","inserviendos","inserviendas",

# perfect participle
"inservitus","inservita","inservitum","inserviti","inservitae","inservito","inservitam","inservite",
"inservitorum","inservitarum","inservitis","inservitos","inservitas",

# future participle
"inserviturus","inservitura","inserviturum","inservituri","inserviturae","inservituro","inservituram","inserviture",
"inserviturorum","inserviturarum","inservituris","inservituros","inservituras"
}
_PRAESERVIO = {
# indicative present (active + passive)
"praeservio","praeservis","praeservit","praeservimus","praeservitis","praeserviunt",
"praeservior","praeserviris","praeservitur","praeservimur","praeservimini","praeserviuntur",

# indicative imperfect (active + passive)
"praeserviebam","praeserviebas","praeserviebat","praeserviebamus","praeserviebatis","praeserviebant",
"praeserviebar","praeserviebaris","praeserviebatur","praeserviebamur","praeserviebamini","praeserviebantur",

# indicative future (active + passive)
"praeserviam","praeservies","praeserviet","praeserviemus","praeservietis","praeservient",
"praeserviar","praeservieris","praeservietur","praeserviemur","praeserviemini","praeservientur",

# indicative perfect system (active; iv/i alternation)
"praeservivi","praeservii","praeservivisti","praeserviisti","praeservivit","praeserviit",
"praeservivimus","praeserviimus","praeservivistis","praeserviistis",
"praeserviverunt","praeservivere","praeserviierunt","praeserviiere",

"praeserviveram","praeserviieram","praeserviveras","praeserviieras","praeserviverat","praeserviierat",
"praeserviveramus","praeserviieramus","praeserviveratis","praeserviieratis","praeserviverant","praeserviierant",

"praeservivero","praeserviiero","praeserviveris","praeserviieris","praeserviverit","praeserviierit",
"praeserviverimus","praeserviierimus","praeserviveritis","praeserviieritis","praeserviverint","praeserviierint",

# subjunctive present (active + passive)
"praeserviam","praeservias","praeserviat","praeserviamus","praeserviatis","praeserviant",
"praeserviar","praeserviaris","praeserviatur","praeserviamur","praeserviamini","praeserviantur",

# subjunctive imperfect (active + passive)
"praeservirem","praeservires","praeserviret","praeserviremus","praeserviretis","praeservirent",
"praeservirer","praeservireris","praeserviretur","praeserviremur","praeserviremini","praeservirentur",

# subjunctive perfect & pluperfect
"praeserviverim","praeserviierim",
"praeservivissem","praeserviissem","praeservivisses","praeserviiisses","praeservivisset","praeserviisset",
"praeservivissemus","praeserviissemus","praeservivissetis","praeserviissetis","praeservivissent","praeserviissent",

# imperatives
"praeservi","praeservite","praeservito","praeservitote","praeserviunto",

# infinitives
"praeservire","praeserviri","praeservivisse","praeserviisse",

# present participle
"praeserviens","praeservientis","praeservienti","praeservientem","praeserviente",
"praeservientes","praeservientium","praeservientibus","praeservientia",

# gerundive
"praeserviendus","praeservienda","praeserviendum","praeserviendi","praeserviendae","praeserviendo","praeserviendam","praeserviende",
"praeserviendorum","praeserviendarum","praeserviendis","praeserviendos","praeserviendas",

# perfect participle
"praeservitus","praeservita","praeservitum","praeserviti","praeservitae","praeservito","praeservitam","praeservite",
"praeservitorum","praeservitarum","praeservitis","praeservitos","praeservitas",

# future participle
"praeserviturus","praeservitura","praeserviturum","praeservituri","praeserviturae","praeservituro","praeservituram","praeserviture",
"praeserviturorum","praeserviturarum","praeservituris","praeservituros","praeservituras"
}
_SERVILIS = {
# positive
"servilis","servile",
"servilis","servili","servilem","servili",
"serviles","servilium","servilibus","servilia",

# comparative
"servilior","servilius",
"servilioris","serviliori","serviliorem","serviliore",
"serviliores","serviliorum","servilioribus",
"serviliora",

# superlative
"servilissimus","servilissima","servilissimum",
"servilissimi","servilissimae","servilissimo",
"servilissimam","servilissime",
"servilissimorum","servilissimarum","servilissimis",
"servilissimos","servilissimas","serviliter"
}
_SERVITIUM = {
"servitium","servitii","servitio","servitium",
"servitia","servitiorum","servitiis"
}
_SERVITOR = {
"servitor","servitoris","servitori","servitorem","servitore",
"servitores","servitorum","servitoribus"
}
_SERVITRITIUS = {
"servitritius","servitritia","servitritium",
"servitritii","servitritiae","servitritio",
"servitritiam","servitritie",
"servitritiorum","servitritiarum","servitritiis",
"servitritios","servitritias"
}
_SERVITUDO = {
"servitudo","servitudinis","servitudini","servitudinem","servitudine",
"servitudines","servitudinum","servitudinibus"
}
_SERVITUS = {
# positive
"servitus","servita","servitum",
"serviti","servitae","servito",
"servitam","servite",
"servitorum","servitarum","servitis",
"servitos","servitas",

# comparative
"servitior","servitius",
"servitioris","servitiori","servitiorem","servitiore",
"servitiores","servitiorum","servitioribus",
"servitiora",

# superlative
"servitissimus","servitissima","servitissimum",
"servitissimi","servitissimae","servitissimo",
"servitissimam","servitissime",
"servitissimorum","servitissimarum","servitissimis",
"servitissimos","servitissimas"
}
_SERVULUS = {
# servulus
"servulus","servule","servuli","servulo","servulum",
"servulorum","servulis","servulos",

# servula
"servula","servulae","servulam",
"servularum","servulis","servulas"
}
_SUBSERVIO = {
# indicative present (active + passive)
"subservio","subservis","subservit","subservimus","subservitis","subserviunt",
"subservior","subserviris","subservitur","subservimur","subservimini","subserviuntur",

# indicative imperfect (active + passive)
"subserviebam","subserviebas","subserviebat","subserviebamus","subserviebatis","subserviebant",
"subserviebar","subserviebaris","subserviebatur","subserviebamur","subserviebamini","subserviebantur",

# indicative future (active + passive)
"subserviam","subservies","subserviet","subserviemus","subservietis","subservient",
"subserviar","subservieris","subservietur","subserviemur","subserviemini","subservientur",

# indicative perfect system (active; iv/i alternation)
"subservivi","subservii","subservivisti","subserviisti","subservivit","subserviit",
"subservivimus","subserviimus","subservivistis","subserviistis",
"subserviverunt","subservivere","subserviierunt","subserviiere",

"subserviveram","subserviieram","subserviveras","subserviieras","subserviverat","subserviierat",
"subserviveramus","subserviieramus","subserviveratis","subserviieratis","subserviverant","subserviierant",

"subservivero","subserviiero","subserviveris","subserviieris","subserviverit","subserviierit",
"subserviverimus","subserviierimus","subserviveritis","subserviieritis","subserviverint","subserviierint",

# subjunctive present (active + passive)
"subserviam","subservias","subserviat","subserviamus","subserviatis","subserviant",
"subserviar","subserviaris","subserviatur","subserviamur","subserviamini","subserviantur",

# subjunctive imperfect (active + passive)
"subservirem","subservires","subserviret","subserviremus","subserviretis","subservirent",
"subservirer","subservireris","subserviretur","subserviremur","subserviremini","subservirentur",

# subjunctive perfect & pluperfect
"subserviverim","subserviierim",
"subservivissem","subserviissem","subservivisses","subserviiisses","subservivisset","subserviisset",
"subservivissemus","subserviissemus","subservivissetis","subserviissetis","subservivissent","subserviissent",

# imperatives
"subservi","subservite","subservito","subservitote","subserviunto",

# infinitives
"subservire","subserviri","subservivisse","subserviisse",

# present participle
"subserviens","subservientis","subservienti","subservientem","subserviente",
"subservientes","subservientium","subservientibus","subservientia",

# gerundive
"subserviendus","subservienda","subserviendum","subserviendi","subserviendae","subserviendo","subserviendam","subserviende",
"subserviendorum","subserviendarum","subserviendis","subserviendos","subserviendas",

# perfect participle
"subservitus","subservita","subservitum","subserviti","subservitae","subservito","subservitam","subservite",
"subservitorum","subservitarum","subservitis","subservitos","subservitas",

# future participle
"subserviturus","subservitura","subserviturum","subservituri","subserviturae","subservituro","subservituram","subserviture",
"subserviturorum","subserviturarum","subservituris","subservituros","subservituras"
}
_SSERO = {
# assero
"asseruisti","asseruistis","asseruerunt","asseruere",
"asserueram","asserueras","asseruerat","asserueramus","asserueratis","asseruerant",
"asseruero","asseruerit","asseruerimus","asserueritis","asseruerint",
"asseruerim",
"asseruissem","asseruisses","asseruisset","asseruissemus","asseruissetis","asseruissent",
"asseruisse",

# desero
"deseruisti","deseruistis","deseruerunt","deseruere",
"deserueram","deserueras","deseruerat","deserueramus","deserueratis","deseruerant",
"deseruero","deseruerit","deseruerimus","deserueritis","deseruerint",
"deseruerim",
"deseruissem","deseruisses","deseruisset","deseruissemus","deseruissetis","deseruissent",
"deseruisse",

# circumsero
"circumserui","circumseruisti","circumseruit","circumseruimus","circumseruistis","circumseruerunt","circumseruere",
"circumserueram","circumserueras","circumseruerat","circumserueramus","circumserueratis","circumseruerant",
"circumseruero","circumserueris","circumseruerit","circumseruerimus","circumserueritis","circumseruerint",
"circumseruerim",
"circumseruissem","circumseruisses","circumseruisset","circumseruissemus","circumseruissetis","circumseruissent",
"circumseruisse",

# consero
"conserui","conseruisti","conseruit","conseruimus","conseruistis","conseruerunt","conseruere",
"conserueram","conserueras","conseruerat","conserueramus","conserueratis","conseruerant",
"conseruero","conseruerit","conseruerimus","conserueritis","conseruerint",
"conseruerim",
"conseruissem","conseruisses","conseruisset","conseruissemus","conseruissetis","conseruissent",
"conseruisse",

# dissero
"disserui","disseruisti","disseruit","disseruimus","disseruistis","disseruerunt","disseruere",
"disserueram","disserueras","disseruerat","disserueramus","disserueratis","disseruerant",
"disseruero","disserueris","disseruerit","disseruerimus","disserueritis","disseruerint",
"disseruerim",
"disseruissem","disseruisses","disseruisset","disseruissemus","disseruissetis","disseruissent",
"disseruisse",

# insero
"inseruisti","inseruistis","inseruerunt","inseruere",
"inserueram","inserueras","inseruerat","inserueramus","inserueratis","inseruerant",
"inseruero","inseruerit","inseruerimus","inserueritis","inseruerint",
"inseruerim",
"inseruissem","inseruisses","inseruisset","inseruissemus","inseruissetis","inseruissent",
"inseruisse",

# intersero
"interserui","interseruisti","interseruit","interseruimus","interseruistis","interseruerunt","interseruere",
"interserueram","interserueras","interseruerat","interserueramus","interserueratis","interseruerant",
"interseruero","interserueris","interseruerit","interseruerimus","interserueritis","interseruerint",
"interseruerim",
"interseruissem","interseruisses","interseruisset","interseruissemus","interseruissetis","interseruissent",
"interseruisse",

# obsero
"obserui","obseruisti","obseruit","obseruimus","obseruistis","obseruerunt","obseruere",
"obserueram","obserueras","obseruerat","obserueramus","obserueratis","obseruerant",
"obseruero","obseruerit","obseruerimus","obserueritis","obseruerint",
"obseruerim",
"obseruissem","obseruisses","obseruisset","obseruissemus","obseruissetis","obseruissent",
"obseruisse",

# prosero
"proserui","proseruisti","proseruit","proseruimus","proseruistis","proseruerunt","proseruere",
"proserueram","proserueras","proseruerat","proserueramus","proserueratis","proseruerant",
"proseruero","proserueris","proseruerit","proseruerimus","proserueritis","proseruerint",
"proseruerim",
"proseruissem","proseruisses","proseruisset","proseruissemus","proseruissetis","proseruissent",
"proseruisse",

# resero
"reserui","reseruisti","reseruit","reseruimus","reseruistis","reseruerunt","reseruere",
"reserueram","reserueras","reseruerat","reserueramus","reserueratis","reseruerant",
"reseruero","reseruerit","reseruerimus","reserueritis","reseruerint",
"reseruerim",
"reseruissem","reseruisses","reseruisset","reseruissemus","reseruissetis","reseruissent",
"reseruisse",

# subsero
"subseruisti","subseruistis","subseruerunt","subseruere",
"subserueram","subserueras","subseruerat","subserueramus","subserueratis","subseruerant",
"subseruero","subserueris","subseruerit","subseruerimus","subserueritis","subseruerint",
"subseruerim",
"subseruissem","subseruisses","subseruisset","subseruissemus","subseruissetis","subseruissent",
"subseruisse"
}
_SILVIUS = {"Silvius", "Silvii", "Silvio", "Silvium"}
_ARVUS = {"arvus", "arvo", "arvum", "arve", "arvorum", "arvis", "arvos"}
_SERVITUS = {"servitus", "servitutis", "servituti", "servitutem", "servitute", "servitutes", "servitutum", "servitutibus"}
_AREO = {"arui", "aruisti", "aruit", "aruimus", "aruistis", "aruerunt", "aruere", "arueram", "arueras", "aruerat", "arueramus", "arueratis", "aruerant", "aruero", "arueris", "aruerit", "aruerimus", "arueritis", "aruerint", "aruerim", "aruissem", "aruisses", "aruisset", "aruissemus", "aruissetis", "aruissent", "aruisse"}
_SARIO = {"sarui", "saruisti", "saruit", "saruimus", "saruistis", "saruerunt", "saruere", "sarueram", "sarueras", "saruerat", "sarueramus", "sarueratis", "saruerant", "saruero", "sarueris", "saruerit", "saruerimus", "sarueritis", "saruerint", "saruerim", "saruissem", "saruisses", "saruisset", "saruissemus", "saruissetis", "saruissent", "saruisse"}

_V = set()
for insieme in (_SERVO, _SERVIO, _SERVUS, _SERVA, _MALVA, _MALVACEUS, _VALVA, _VALVATUS, _VALVOLAE,
                _VALVOLI, _SALVEO, _SALVO, _SALVUS, _SALVATOR, _SALVATIO, _SALVAMENTUM,
                _PARVITAS, _PARVULUS, _PARVUS, _VOLVO,
                _SILVA, _SILVANUS, _SILVATICUS, _SILVESCO, _SILVESTER, _SILVIA, _SILVICOLA, _SILVICULTRIX,
                _SILVIFRAGUS, _SILVIGER, _SILVOSUS, _SILVULA, _ALVEUS, _ASSERVO, _CONSERVO, _INSERVO,
                _OBSERVO, _PRAESERVO, _RESERVO, _PERSERVO, _SERVABILIS, _SERVATOR, _ASSERVIO, _DESERVIO,
                _INSERVIO, _PRAESERVIO, _SERVILIS, _SERVITIUM, _SERVITOR, _SERVITRITIUS, _SERVITUDO, _SERVITUS,
                _SERVULUS, _SUBSERVIO, _SILVIUS, _ARVUS, _SERVITUS):
    for forma in insieme:
        if forma not in _V:
            _V.add(forma.replace("u", "#").replace("v", "#").lower())

_U = set()
for insieme in (_SERO, _MALO, _VALEO, _SALIO, _PAREO, _SILEO, _ALO, _SSERO, _AREO, _SARIO):
    for forma in insieme:
        if forma not in _U:
            _U.add(forma.replace("u", "#").replace("v", "#").lower())

#controllino:
for forma in _U:
    if forma in _V:
        raise IndexError(f"Due lemmi sono sovrapposti: {forma}")

def is_letter(ch: str) -> bool:
    # Basic Latin letters only (A-Z/a-z). Extend if you need macrons etc.
    return ("A" <= ch <= "Z") or ("a" <= ch <= "z")


def is_vowel(ch: str) -> bool:
    return ch in VOWELS


def is_whitespace(ch: str) -> bool:
    return ch.isspace()


def placeholderize(text: str) -> str:
    # Preserve case by using two placeholders.
    trans = []
    for ch in text:
        if ch == "u" or ch == "v":
            trans.append(PLACEHOLDER_LO)
        elif ch == "U" or ch == "V":
            trans.append(PLACEHOLDER_UP)
        else:
            trans.append(ch)
    return "".join(trans)


def unplaceholder_char(ph: str, want_u: bool) -> str:
    """
    ph is '#' or '¤'. want_u True => U/u, else V/v. Case depends on placeholder.
    """
    if ph == PLACEHOLDER_UP:
        return "U" if want_u else "V"
    else:
        return "u" if want_u else "v"


def find_word_bounds(text: str, idx: int) -> Tuple[int, int]:
    """
    Return (start, end) indices of the "word" containing idx, where word = consecutive letters + placeholders.
    """
    n = len(text)
    start = idx
    while start > 0 and (is_letter(text[start - 1]) or text[start - 1] in (PLACEHOLDER_LO, PLACEHOLDER_UP)):
        start -= 1
    end = idx
    while end < n and (is_letter(text[end]) or text[end] in (PLACEHOLDER_LO, PLACEHOLDER_UP)):
        end += 1
    return start, end


def normalize_stem(stem: str) -> str:
    # Store stems in lowercase, placeholders removed from stem portion.
    return stem.replace(PLACEHOLDER_UP, PLACEHOLDER_LO).lower()


# -----------------------------
# Memory model
# -----------------------------

@dataclass
class StemMemory:
    """
    Maps stem -> decision for what placeholder becomes at that position.
    For single placeholder: stem -> 'u' or 'v'
    For double placeholder: stem -> one of 'uu','uv','vu','vv'
    """
    single: Dict[str, str] = field(default_factory=dict)
    double: Dict[str, str] = field(default_factory=dict)

    def save_json(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"single": self.single, "double": self.double}, f, ensure_ascii=False, indent=2)

    @classmethod
    def load_json(cls, path: str) -> "StemMemory":
        with open(path, "r", encoding="utf-8") as f:
            obj = json.load(f)
        mem = cls()
        mem.single = dict(obj.get("single", {}))
        mem.double = dict(obj.get("double", {}))
        return mem


# -----------------------------
# Interactive chooser
# -----------------------------

def default_prompt_single(context: str, word: str, stem: str) -> Tuple[str, bool]:
    """
    Returns (choice, memorize)
    choice in {'u','v'}
    """
    print("\nAmbiguous U/V decision")
    print("Context:", context)
    print("Word   :", word)
    print("Stem   :", stem)
    while True:
        ans = input("Choose [u/v], add ! to memorize stem (e.g. u!): ").strip().lower()
        if ans in ("u", "v", "u!", "v!"):
            memorize = ans.endswith("!")
            choice = ans[0]
            return choice, memorize
        print("Invalid. Example inputs: u, v, u!, v!")


def default_prompt_double(context: str, word: str, stem: str) -> Tuple[str, bool]:
    """
    Returns (choice, memorize)
    choice in {'uu','uv','vu','vv'}
    """
    print("\nAmbiguous ## decision")
    print("Context:", context)
    print("Word   :", word)
    print("Stem   :", stem)
    while True:
        ans = input("Choose [uu/uv/vu/vv], add ! to memorize (e.g. uv!): ").strip().lower()
        if ans in ("uu", "uv", "vu", "vv", "uu!", "uv!", "vu!", "vv!"):
            memorize = ans.endswith("!")
            choice = ans[:-1] if memorize else ans
            return choice, memorize
        print("Invalid. Example inputs: uv, uu!, vv, vu!")


def get_context_snippet(text: str, idx: int, radius: int = 40) -> str:
    left = max(0, idx - radius)
    right = min(len(text), idx + radius)
    snippet = text[left:right]
    # Mark the current index approximately (best-effort).
    caret_pos = idx - left
    return snippet[:caret_pos] + "⟦" + snippet[caret_pos:caret_pos + 1] + "⟧" + snippet[caret_pos + 1:]


# -----------------------------
# Regularizer
# -----------------------------

class UVRegularizer:
    def __init__(self, memory: Optional[StemMemory] = None):
        self.memory = memory if memory is not None else StemMemory()

    def regularize(
        self,
        text: str,
        interactive: bool = True,
        memory_path: Optional[str] = None,
    ) -> str:
        """
        Main entry point:
        - placeholderize
        - scan and resolve placeholders
        - optionally load/save memory to JSON
        """
        if memory_path:
            try:
                self.memory = StemMemory.load_json(memory_path)
            except FileNotFoundError:
                pass

        t = placeholderize(text)
        out = []
        i = 0
        n = len(t)

        while i < n:
            ch = t[i]

            # Handle triple ### (or ¤¤¤ or mixed) as 3 placeholders in a row
            if self._is_placeholder(ch) and i + 2 < n and self._is_placeholder(t[i + 1]) and self._is_placeholder(t[i + 2]):
                out.append(unplaceholder_char(t[i], want_u=True))
                out.append(unplaceholder_char(t[i + 1], want_u=False))
                out.append(unplaceholder_char(t[i + 2], want_u=True))
                i += 3
                continue

            # Handle double ##
            if self._is_placeholder(ch) and i + 1 < n and self._is_placeholder(t[i + 1]):
                repl2 = self._resolve_double(t, i, interactive)
                out.append(repl2[0])
                out.append(repl2[1])
                i += 2
                continue

            # Handle single #
            if self._is_placeholder(ch):
                repl1 = self._resolve_single(t, i, interactive)
                out.append(repl1)
                i += 1
                continue

            out.append(ch)
            i += 1

        result = "".join(out)

        if memory_path:
            self.memory.save_json(memory_path)

        return result

    def _is_placeholder(self, ch: str) -> bool:
        return ch == PLACEHOLDER_LO or ch == PLACEHOLDER_UP

    def _prev_char(self, t: str, i: int) -> str:
        return t[i - 1] if i > 0 else ""

    def _next_letter_char(self, t: str, i: int) -> str:
        """
        Look at the char immediately after placeholder(s).
        We do NOT skip punctuation/spaces; the rule says "before vowel vs consonant".
        If next is not a letter, treat as consonant (i.e., not vowel).
        """
        j = i + 1
        if j >= len(t):
            return ""
        return t[j]

    def _resolve_single(self, t: str, i: int, interactive: bool) -> str:
        ph = t[i]
        prev = self._prev_char(t, i)
        nextc = self._next_letter_char(t, i)

        # Determine categories
        prev_is_space_or_start = (prev == "") or is_whitespace(prev)
        prev_is_vowel = is_vowel(prev)
        prev_is_liquid = prev in LIQUIDS
        prev_is_nonliquid_consonant = prev in NON_LIQUID_CONSONANTS

        next_is_vowel = is_vowel(nextc)
        next_is_consonant = is_letter(nextc) and not next_is_vowel

        # Word + stem for memory/interaction
        w0, w1 = find_word_bounds(t, i)
        word = t[w0:w1]
        stem_raw = t[w0:i]  # part before placeholder within word
        stem = normalize_stem(stem_raw)

        if word.lower().replace("¤", "#") in _V:
            return unplaceholder_char(ph, want_u=False)
        elif word.lower().replace("¤", "#") in _U:
            return unplaceholder_char(ph, want_u=True)
        elif len(word) > 4 and word[-3:] == "m#e" or word[-3:] == "r#e":
            return unplaceholder_char(ph, want_u=False)
        elif len(word) >= 10:
            for sequenza in {"m#a", "m#e", "m#i", "m#o"}:
                if sequenza in word:
                    return unplaceholder_char(ph, want_u=False)

        # 1) After non-liquid consonants: always U
        if prev_is_nonliquid_consonant:
            return unplaceholder_char(ph, want_u=True)

        # 2) After liquids:
        if prev_is_liquid:
            # If # is before a consonant after a liquid, it automatically becomes U instead.
            if next_is_consonant or (not is_letter(nextc)):
                return unplaceholder_char(ph, want_u=True)

            # If before a vowel after liquids: case-by-case OR memory
            if stem in self.memory.single:
                want = self.memory.single[stem]  # 'u' or 'v'
                return unplaceholder_char(ph, want_u=(want == "u"))

            if not interactive:
                # Non-interactive fallback: default to V before vowel after liquid (common in many Latin contexts),
                # but you can change this policy easily.
                return unplaceholder_char(ph, want_u=False)

            context = get_context_snippet(t, i)
            choice, memorize = default_prompt_single(context=context, word=word, stem=stem)
            if memorize:
                self.memory.single[stem] = choice
            return unplaceholder_char(ph, want_u=(choice == "u"))

        # 3) If preceded by whitespace or vowel (or start): U before consonant, V before vowel
        if prev_is_space_or_start or prev_is_vowel:
            if next_is_vowel:
                return unplaceholder_char(ph, want_u=False)  # V
            else:
                return unplaceholder_char(ph, want_u=True)   # U

        # 4) Otherwise (e.g., after other consonants not listed, or punctuation inside word):
        # Treat like: consonant context => U (safe default given your other rules).
        return unplaceholder_char(ph, want_u=True)

    def _resolve_double(self, t: str, i: int, interactive: bool) -> Tuple[str, str]:
        ph1, ph2 = t[i], t[i + 1]
        prev = self._prev_char(t, i)
        after2 = t[i + 2] if i + 2 < len(t) else ""
        after2_is_vowel = is_vowel(after2)
        after2_is_consonant = is_letter(after2) and not after2_is_vowel

        # Word + stem for memory/interaction (stem before the first #)
        w0, w1 = find_word_bounds(t, i)
        word = t[w0:w1]
        stem_raw = t[w0:i]
        stem = normalize_stem(stem_raw)

        # Rule: If two ## found:
        # - If they follow a consonant:
        #   * UU if they precede a consonant
        #   * UV if they precede a vowel
        # - If they follow a vowel: evaluate like liquids (case-by-case)
        prev_is_vowel = is_vowel(prev)
        prev_is_consonant = is_letter(prev) and not prev_is_vowel

        if prev_is_consonant:
            if after2_is_vowel:
                # U + V
                return (
                    unplaceholder_char(ph1, want_u=True),
                    unplaceholder_char(ph2, want_u=False),
                )
            else:
                # U + U (covers consonant or non-letter)
                return (
                    unplaceholder_char(ph1, want_u=True),
                    unplaceholder_char(ph2, want_u=True),
                )

        if prev_is_vowel:
            # Memory?
            if stem in self.memory.double:
                pat = self.memory.double[stem]  # 'uu','uv','vu','vv'
                return (
                    unplaceholder_char(ph1, want_u=(pat[0] == "u")),
                    unplaceholder_char(ph2, want_u=(pat[1] == "u")),
                )

            if not interactive:
                # Non-interactive fallback: common-ish pattern after vowel is 'uv' (e.g., "au" + consonant-vowel split),
                # but this is heuristic—change if you prefer.
                pat = "uv" if after2_is_vowel else "uu"
                return (
                    unplaceholder_char(ph1, want_u=(pat[0] == "u")),
                    unplaceholder_char(ph2, want_u=(pat[1] == "u")),
                )

            context = get_context_snippet(t, i)
            choice, memorize = default_prompt_double(context=context, word=word, stem=stem)
            if memorize:
                self.memory.double[stem] = choice
            return (
                unplaceholder_char(ph1, want_u=(choice[0] == "u")),
                unplaceholder_char(ph2, want_u=(choice[1] == "u")),
            )

        # If prev is neither vowel nor consonant (start/space/punct), treat as "whitespace/vowel-like":
        # decide based on what follows (after2).
        if after2_is_vowel:
            return (
                unplaceholder_char(ph1, want_u=True),
                unplaceholder_char(ph2, want_u=False),
            )
        else:
            return (
                unplaceholder_char(ph1, want_u=True),
                unplaceholder_char(ph2, want_u=True),
            )


lettere = {'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
           'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's',
           'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm'}
numeri = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}
punteggiatura = {'!', '\"', '(', ')', '?', ';', ',', ':', '.', ' ', '\n'}
greci = {'χ', 'σ', 'ϊ', 'ι', 'Ύ', 'Β', 'Ο', 'φ', 'ὶ', 'Ἳ', 'Ϝ', 'ἤ',
         'π', 'ἧ', 'ά', 'ῥ', 'ᾁ', 'Ἰ', 'ἅ', 'ἇ', 'ῷ', 'Ὕ', 'Δ', 'ὔ', 'Ω', 'ὲ', 'ἰ',
         'ᾗ', 'Ἱ', 'Ὸ', 'ᾔ', 'ῖ', 'Ί', 'Θ', 'Ἅ', 'Ἵ', 'Π', 'Τ', 'ᾳ', 'ὓ', 'Ή',
         'ᾤ', 'Ὴ', 'Ὁ', 'Κ', 'Ἓ', 'Ὦ', 'ὠ', 'Ὢ', 'ὃ', 'δ', 'ἠ', 'λ', 'ἒ',
         'ἂ', 'Η', 'ῳ', 'Έ', 'Ἃ', 'ᾰ', 'ἱ', 'υ', 'ύ', 'Ἕ', 'θ', 'Ὣ', 'ϋ',
         'κ', 'Ῥ', 'Υ', 'Ὃ', 'Ὄ', 'ὤ', 'Χ', 'ῶ', 'ὢ', 'ῴ', 'ϰ', 'Ὂ', 'ω', 'ᾄ', 'Ἧ', 'Ξ', 'ὁ', 'ἷ',
         'Α', 'ᾠ', 'τ', 'ἄ', 'ἣ', 'Μ', 'ἥ', 'ἕ', 'ώ', 'ὴ', 'ἵ', 'Ὶ', 'Ὤ', 'Ὀ', 'Ε', 'Ὥ', 'ἑ', 'ἶ',
         'ὣ', 'ᾑ', 'ᾲ', 'ί', 'ε', 'ἡ', 'ἐ', 'Ἄ', 'ἴ', 'ζ', 'ὦ', 'ᾆ', 'Ἑ', 'Ὧ', 'ῦ', 'ῤ', 'ΐ', 'Ό', 'Ἆ', 'ὖ',
         'ᾇ', 'ἓ', 'ἔ', 'ὂ', 'Ἴ', 'Ἠ', 'ρ', 'ἲ', 'ψ', 'ὧ', 'ᾖ', 'ή', 'ἁ', 'ὕ', 'ὰ', 'ὗ', 'έ', 'Ἒ',
         'ῒ', 'ο', 'Ὠ', 'ῃ', 'Φ', 'ᾶ', 'ὐ', 'Ά', 'ῇ', 'Ι', 'ῂ', 'ὑ', 'ᾐ', 'ῆ', 'Ἶ', 'ὄ', 'ἳ', 'ᾴ',
         'ς', 'ἦ', 'Ὅ', 'Ἔ', 'ὺ', 'ῄ', 'ξ', 'η', 'Ἥ', 'Ἦ', 'Ἡ', 'β', 'Ψ', 'Ἂ', 'ΐ', 'ά', 'ᾅ',
         'Λ', 'ν', 'ῲ', 'Ἤ', 'ὡ', 'ᾧ', 'Ἣ', 'ἃ', 'ὥ', 'ἀ', 'ᾂ', 'Ὑ', 'Ἢ',
         'ᾀ', 'ᾦ', 'ϕ', 'ὀ', 'ύ', 'ϛ', 'ὅ', 'ί', 'Ἐ', 'ΰ', 'Ἀ', 'ὒ', 'ἆ', 'ᾷ', 'Ζ', 'μ', 'Ώ',
         'Ἁ', 'Ν', 'α', 'Ὡ', 'ἢ'}
ebraici = {'א', 'ג', 'ץ', 'פ', 'ט', 'ח', 'ש', 'צ', 'מ', 'ה', 'ל', 'ך', 'ע', 'ת', 'ז', 'ס',
           'ם', 'ף', 'כ', 'ד', 'ק', 'ב', 'נ', 'ו', 'ר', 'י'}
matematici = {'ϑ', '÷', '≡', '˚', '∗', 'ₙ', '*', '±', 'ʃ', '∓', 'ƒ', '√', 'Ø',
              '+', '⋅', '¼', '∂', '=', '⸱', '∫', '¹', '₃', '½', '²', '%', 'ª', '¾', '⸟', '/', '\\',
              '–', '∞', '|', '³', '∑', '×', '∬', 'є', '<', '>'}

emendandi = {'χ', 'ϑ', 'â', 'И', 'σ', 'э', 'Ë', 'ǽ', '÷', 'ϊ', '\uf03e', '≡', 'Ń', 'ങ', 'ഴ', 'Я', 'е',
             'ă', '⁑', '\uf075', 'ι', 'Ύ', 'Β', 'Ο', 'æ', 'щ', 'φ', 'ὶ', 'Ἳ', 'Ϝ', 'ἤ', 'ō', 'ł', '☋', 'ѵ',
             'Õ', 'π', 'ἧ', 'û', 'ക', '˚', '¸', 'ů', 'ά', 'œ', 'ൊ', 'Ϡ', 'ു', 'ള', 'й', 'Š', 'ґ', 'î',
             'Á', 'ῥ', 'ᾁ', '≫', 'Ἰ', 'ἅ', '∗', 'ἇ', 'ß', 'ć', 'ņ', '⋮', 'ῷ', '♃', '\u202f', '—', 'ǒ',
             'Ὕ', 'ആ', '⟩', 'Δ', 'ὔ', 'ₙ', 'Ω', '῎', '3', 'א', '¡', 'ǐ', 'Ρ', '͡', 'ὲ', 'ം', 'ൎ', 'ἰ',
             'ь', '‘', 'ə', 'ട', 'þ', '¯', 'ᾗ', '˜', 'ė', 'Ἱ', 'ൽ', 'Ὸ', 'ā', 'ū', '™', 'ᾔ', '$', 'Ą',
             'Ↄ', 'ð', '>', 'ῖ', 'Ί', 'ല', 'í', 'В', '_', 'É', '☼', '\x1d', 'Θ', 'ș', 'Ϟ', 'ý', '₂', 'з',
             'ĩ', 'Ā', 'Ἅ', 'Ἵ', 'Π', 'Ş', 'ὼ', 'Τ', 'ᾳ', 'ч', 'ὓ', 'Ή', '῾', 'è', 'പ', '~', '↑', 'ř',
             'ᾤ', '\u200b', '◦', '൱', 'എ', 'ю', 'ļ', '\x81', '¤', 'ş', '€', 'ഹ', '͂', '*', 'ג', 'Ὴ',
             'М', '묩', '`', 'ˆ', 'µ', 'Ὁ', 'Κ', '\uf02f', 'Ἓ', 'Ὦ', '\xad', '§', '¢', 'സ', 'ὠ', 'Ὢ',
             'д', 'ὃ', 'п', 'ץ', 'δ', 'ạ', 'Ф', 'Ʒ', 'ἠ', 'λ', '൲', 'Û', '͞', '♎', 'ͅ', 'у', '±', 'ἒ',
             'ʃ', '0', 'ἂ', '´', 'Η', '-', 'ῳ', 'л', 'פ', '©', 'ö', '̶', 'Έ', '₧', 'ט', '\u2003', 'Ἃ', '“',
             'Â', 'ח', 'а', 'С', 'ש', '∓', 'ᾰ', '¶', 'ÿ', 'യ', '♀', 'ἱ', '¬', 'υ', 'ύ', 'Å', 'в', 'ã',
             'ϱ', 'Ἕ', '̄', '◡', 'Ö', 'θ', 'Ŏ', 'ф', 'Ὣ', 'Ñ', 'Ņ', 'ж', 'ϋ', 'Œ', 'ὸ', '@', '〉', 'к',
             '‟', 'צ', 'κ', 'מ', '•', 'Ῥ', 'Υ', 'ﬁ', 'Ὃ', 'ĕ', 'Ὄ', 'ὤ', '…', 'വ', 'Χ', 'é', 'ῶ', 'ὢ',
             '\n', 'ῴ', '᾿', 'ϰ', 'ﬂ', 'Е', 'Ὂ', 'Ú', 'ȣ', '6', 'ŀ', '̨', 'ƒ', 'ω', '\u2061', '맩', '⁘',
             'െ', 'ᾄ', '\xa0', 'Ἧ', '̵', 'г', 'Д', 'ן', 'Ξ', '῞', 'ὁ', 'ü', 'ĭ', 'ἷ', 'Ī', 'и', '’',
             'Α', 'ᾠ', 'ה', 'ל', 'ꝫ', '√', 'Ł', 'Σ', '♍', 'ך', 'м', 'ע', 'τ', 'Î', '͵', '⟨', 'ŏ', 'Ó',
             'ꝑ', 'Њ', 'ъ', 'ἄ', 'ñ', 'ഥ', 'ἣ', 'Ž', '൫', 'ò', '′', '♄', '^', 'Μ', 'ἥ', '₁', 'ı', 'ἕ',
             '⁗', 'ώ', 'å', '\u2009', 'ൃ', '♦', 'ബ', 'ὴ', 'ἵ', '൹', 'Ø', 'ʹ', 'Ὶ', '£', 'ų', 'Ὤ',
             'н', 'х', 'Ὀ', 'ϙ', 'Ε', 'А', 'Ὥ', 'ἑ', 'ό', 'Æ', '\x90', '+', 'ﬅ', 'ἶ', 'Л', '‚', 'ὣ', '⋅',
             ']', 'ᾑ', 'ᾲ', 'č', 'ί', '7', '[', 'ε', 'ഷ', 'ô', 'മ', '¼', 'Ü', 'ἡ', 'ἐ', '⋯', '®', 'Ἄ',
             'ἴ', 'ﬃ', 'З', 'Ç', '◊', '‹', 'ζ', 'ὦ', '·', 'Ã', 'ḡ', '☽', 'ᾆ', '»', 'Ē', 'Ἑ', 'Ὧ', '―',
             'ῦ', '∂', 'У', '¥', 'ç', 'ῤ', 'ΐ', 'ת', 'Ό', 'Р', '𐆖', '൭', 'ϝ', '=', 'ũ', 'Ἆ', '벣', 'ὖ',
             'ൻ', 'ᾇ', 'š', 'ἓ', 'ἔ', 'ὂ', '☜', 'Ἴ', '9', 'Ἠ', 'ז', 'õ', 'ന', 'º', 'ρ', 'Ū', 'ἲ', '⸱',
             'ψ', 'Ì', 'ὧ', 'È', 'Ý', '∫', 'ഗ', 'അ', 'ᾖ', '\uf069', '¹', 'ס', '̡', 'ή', 'Γ', 'ẽ', '●',
             'ǎ', 'ↄ', 'ĉ', '₃', 'ם', 'Ж', 'ἁ', '\u200e', 'Ō', 'ï', '{', 'ↀ', 'ף', 'ണ', '½', 'כ', 'ഞ',
             '¦', 'À', '²', '\uf070', '☊', '൰', 'ὕ', 'ൈ', '\uf03c', '˙', 'ȩ', '῀', '−', 'à', '൬',
             'ś', '♋', '2', 'ę', 'ὰ', 'ᶃ', '\ufeff', 'ш', 'ѐ', 'Ÿ', 'ὗ', 'Ä', 'Ϙ', 'έ', ';', '5', 'Ἒ',
             'ῒ', 'ο', 'Ὠ', 'ῃ', 'Φ', '‴', 'ד', '♉', 'ᾶ', 'ὐ', '✴', '%', 'Ά', 'ച', 'ῇ', '\uf073', '☞',
             'Ê', 'ì', '♈', 'Ι', '്', 'ῂ', '·', 'ä', 'Ï', 'ń', '☾', 'Ч', '᾽', 'γ', 'ª', 'Ð', 'ὑ', '〈',
             'ē', 'ц', '¾', 'ᾐ', 'ɩ', 'Х', 'Þ', 'ῆ', 'Ἶ', 'ὄ', 'р', 'ἳ', 'Ϲ', '\t', 'ᾴ', 'ǵ', '⸟', '‡',
             '※', 'ത', 'ς', '/', 'ἦ', '́', 'ț', 'ą', 'Ὅ', 'Ἔ', '\\', '«', 'ὺ', 'ῄ', 'ξ', 'η', 'Ἥ', 'Ἦ',
             '\x8d', 'ż', 'Ἡ', 'Đ', 'β', '¿', 'Ψ', '�', 'Ἂ', 'Т', '8', 'ΐ', 'П', '–', 'ק', 'ά', 'ᾅ', '∞',
             'Λ', 'ë', '#', 'ụ', '൯', 'ശ', 'Г', 'ν', 'ῲ', 'ø', '\x8f', '♂', '›', 'ב', 'Ἤ', '℞', 'ὡ',
             '☉', 'Ӿ', '♊', 'я', '}', 'ᾧ', 'Ù', 'ы', 'Н', 'Ἣ', 'נ', '4', 'ӯ', '̃', '|', 'ẻ', 'ἃ', 'ὥ',
             '̈', 'ї', '▼', 'ര', '\uf023', 'К', '̅', 'ἀ', 'ᾂ', 'Ὑ', 'с', 'ě', '̆', 'ദ', '³', '”', 'Ἢ',
             'ī', 'ᾀ', '‛', 'ᾦ', '∑', '\x1c', 'ϕ', 'റ', 'о', '″', 'Í', '1', 'ി', 'ὀ', 'ó', 'Ɔ', 'ו', 'ύ',
             '‰', 'ϛ', 'ὅ', 'ί', 'Ἐ', 'ר', '☿', 'Ϛ', '∘', 'á', '■', 'ȳ', 'ΰ', 'ž', 'б', '\uf07e', '×', 'О',
             'Ἀ', '⁹', '̍', 'ὒ', 'ἆ', 'ê', 'ù', '‑', 'י', 'ᾷ', 'Б', '°', 'Ζ', 'т', 'і', 'Ц', '\uf0f0', 'Ò',
             'μ', 'Ώ', 'Ἁ', 'ർ', '¨', 'ŭ', 'Ô', '˛', 'ọ', 'ú', 'Ν', '∬', 'є', '„', 'α', 'Ὡ', 'ſ', '†',
             'ധ', 'ἢ', 'ാ', 'ഒ', '<'}
rimuovendi = emendandi - greci - ebraici - matematici - punteggiatura - numeri - lettere
scartandi = {'®', '⁑', 'ഷ', '�', 'Я', '♦', 'Þ', 'Б', '☼', '◊', '~', '¦', 'ൊ', 'ן', '♍', 'അ', 'š',
             '〈', 'ധ', '‚', 'ബ', 'ഥ', 'ി', 'Е', 'П', ']', 'Ņ', 'ↄ', 'Ý', '☽', 'т', 'യ',
             '\uf069', 'Ↄ', '♊', '♎', 'н', '̅', 'м', '‑', '⁗', '☿', 'Ô', '☜', 'ദ', '§', 'ô', 'ї',
             'г', 'Ϙ', 'ѐ', '′', 'ത', '‡', 'Š', '᾽', 'ḡ', 'і', 'ꝑ', 'ഗ', 'എ', '♃', '†', '↑', '#',
             '̄', 'ю', 'Г', '●', '̨', 'ഹ', 'п', '͞', '©', 'ᶃ', '›', 'പ', 'വ', '₂', '൭', '―', '൯',
             '☋', 'В', 'ř', '῞', '¢', '¥', 'л', 'Ϛ', '\uf070', '@', '¯', 'ണ', 'ĩ', '̶', '̃', '≫', 'ച',
             '˛', 'ട', '-', '″', '\u2061', 'ന', '™', '⋮', '▼', 'ф', '\uf075', 'ὸ', ';', '〉', 'þ', 'к',
             '‰', '̵', 'ϝ', '∘', 'Ą', 'ș', '⋯', 'А', 'Σ', '€', 'ആ', 'Ϡ', '☉', '묩', 'ь', '῀', '‴',
             '̡', '͂', '°', '͵', 'Д', 'മ', 'ൽ', 'ъ', 'О', 'Ρ', '₁', 'µ', 'ൻ', '♈', '̆', 'ы', '벣',
             '\uf023', '\x81', '¿', 'Ɔ', '\uf03c', '¸', 'ർ', 'Û', '\u2009', 'Ÿ', '\uf03e', '൬', 'ങ',
             'ﬁ', '\x1c', 'ə', '−', 'ð', 'У', 'ě', '☞', '\u200e', '♋', 'ш', '■', 'Õ', 'З', 'у', '¡',
             'ґ', '\uf02f', '¶', 'ഒ', '¤', 'б', '᾿', '൫', '✴', '\u202f', '൲', 'ൎ', '※', 'ů', 'ശ',
             '͡', 'ͅ', '˙', 'Ž', '℞', '\x8d', 'ഞ', 'Ч', '„', 'ț', 'ѵ', 'ό', 'γ', 'Ϟ', 'ꝫ', '♄',
             '\ufeff', '⁘', '맩', 'Т', '്', 'ц', 'х', '♀', '£', 'Ж', '\x90', '\xad', 'ö', 'സ', 'М', 'ൃ',
             'з', 'Γ', 'щ', 'ŀ', 'റ', 'р', '˜', 'ž', 'Ф', '[', 'Ϲ', 'º', 'ര', 'ↀ', '\x1d', 'ч', 'Ц', 'ˆ',
             'ല', '\xa0', 'я', '῎', '́', 'ȣ', 'Ӿ', '\x8f', 'й', 'Р', '^', 'Ð', '◦', 'К', '·', '\uf073',
             'Н', 'ǵ', 'ൈ', '♂', 'ὼ', 'И', '⁹', '¬', '☾', '_', '൹', '•', 'ϱ', 'ള', 'ϙ', '̈', 'ഴ',
             '𐆖', '´', '\t', '₧', 'в', '‹', '\uf07e', '⟨', '`', '⟩', 'Њ', 'ж', '൱', 'и', '\u2003',
             '¨', 'ം', 'ʹ', 'ų', '\u200b', 'ĉ', 'Л', 'ാ', '൰', 'Ʒ', 'െ', '̍', 'ു', 'ക', '◡',
             'Х', '῾', '♉', 'д', '☊', '$', '\uf0f0', 'э'}
'''
#cartella = r"C:\Users\aless\PycharmProjects\Locutor\Puliti\Tutto"
#for documento in os.listdir(cartella):
#    print("Pulisco", documento)
#    with open(r"C:\Users\aless\PycharmProjects\Locutor\Grezzi\Tutto"+"\\"+documento, "r", encoding="utf-8") as file:
#        testo = file.read()
'''
    testo = testo.replace("ﬁ", "fi")
    testo = testo.replace("ö", "o")
    testo = testo.replace("ů", "u")
    testo = testo.replace("ě", "e")
    testo = testo.replace("Ÿ", "Y")
    testo = testo.replace("ὸ", "o")
    testo = testo.replace("Õ", "O")
    testo = testo.replace("ĩ", "i")
    testo = testo.replace("Ý", "Y")
'''
#    testo = re.sub(r"\[\d+\]", "", testo)
'''
    testo = testo.replace("Ē", "E")
    testo = testo.replace("Ō", "O")
    testo = testo.replace("Ī", "I")
    testo = testo.replace("Ā", "A")
    testo = testo.replace("«", "\"")
    testo = testo.replace("»", "\"")
    testo = testo.replace("|", ".")
    testo = testo.replace("ó", "o")
    testo = testo.replace("à", "a")
    testo = testo.replace("é", "e")
    testo = testo.replace("ï", "i")
    testo = testo.replace("·", ",")
    testo = testo.replace("Æ", "Ae")
    testo = testo.replace("œ", "oe")
    testo = testo.replace("è", "e")
    testo = testo.replace("ĕ", "e")
    testo = testo.replace("ŏ", "o")
    testo = testo.replace("ă", "a")
    testo = testo.replace("ŭ", "u")
    testo = testo.replace("î", "ii")
    testo = testo.replace("â", "a")
    testo = testo.replace("ì", "i")
    testo = testo.replace("ú", "u")
    testo = testo.replace("ò", "o")
    testo = testo.replace("á", "a")
    testo = testo.replace("Í", "I")
    testo = testo.replace("ü", "u")
    testo = testo.replace("ę", "e")
    testo = testo.replace("ş", "s")
    testo = testo.replace("ņ", "n")
    testo = testo.replace("ſ", "s")
    testo = testo.replace("ļ", "l")
    testo = testo.replace("ù", "u")
    testo = testo.replace("õ", "on")
    testo = testo.replace("ẽ", "en")
    testo = testo.replace("Œ", "OE")
    testo = testo.replace("û", "un")
    testo = testo.replace("ӯ", "y")
    testo = testo.replace("Ŏ", "O")
    testo = testo.replace("ē", "e")
    testo = testo.replace("ō", "o")
    testo = testo.replace("ī", "i")
    testo = testo.replace("ā", "a")
    testo = testo.replace("ū", "u")
    testo = testo.replace("æ", "ae")
    testo = testo.replace("—", " ")
    testo = testo.replace("“", "\"")
    testo = testo.replace("”", "\"")
    testo = testo.replace("…", "...")
    testo = testo.replace("ë", "e")
    testo = testo.replace("ȳ", "y")
    testo = testo.replace("ã", "an")
    testo = testo.replace("Ū", "U")
    testo = testo.replace("‘", "\"")
    testo = testo.replace("’", "\"")
    testo = testo.replace("ñ", "n")
    testo = testo.replace("Ñ", "N")
    testo = testo.replace("ĭ", "i")
    testo = testo.replace("ä", "a")
    testo = testo.replace("ç", "c")
'''
#    testo = re.sub(r"(?<=\s)\d+(?=\s)", lambda m: int_to_roman(int(m.group())), testo)
'''
    testo = testo.replace("í", "i")
    testo = testo.replace("С", "C")
    testo = testo.replace("ê", "e")
    testo = testo.replace("Ø", "O")
    testo = testo.replace("Ç", "C")
    testo = testo.replace("È", "E")
    testo = testo.replace("с", "c")
    testo = testo.replace("а", "a")
    testo = testo.replace("е", "e")
    testo = testo.replace("о", "o")
    testo = testo.replace("Ü", "U")
    testo = testo.replace("Ń", "N")
    testo = testo.replace("ß", "ss")
    testo = testo.replace("å", "a")
    testo = testo.replace("ø", "o")
    testo = testo.replace("Ì", "I")
    testo = testo.replace("À", "A")
    testo = testo.replace("Ö", "O")
    testo = testo.replace("‛", "\"")
    testo = testo.replace("Ó", "O")
    testo = testo.replace("Ş", "S")
    testo = testo.replace("Î", "I")
    testo = testo.replace("ũ", "um")
    testo = testo.replace("Ï", "I")
    testo = testo.replace("Ò", "O")
    testo = testo.replace("Ã", "A")
    testo = testo.replace("ụ", "u")
    testo = testo.replace("ạ", "a")
    testo = testo.replace("ą", "a")
    testo = testo.replace("ı", "i")
    testo = testo.replace("č", "c")
    testo = testo.replace("ł", "l")
    testo = testo.replace("ć", "c")
    testo = testo.replace("ý", "y")
    testo = testo.replace("Â", "A")
    testo = testo.replace("Ú", "U")
    testo = testo.replace("ė", "e")
    testo = testo.replace("Ł", "L")
    testo = testo.replace("Đ", "D")
    testo = testo.replace("‟", "\"")
    testo = testo.replace("É", "E")
    testo = testo.replace("Ê", "E")
    testo = testo.replace("ś", "s")
    testo = testo.replace("ẻ", "e")
    testo = testo.replace("ọ", "o")
    testo = testo.replace("Ë", "E")
    testo = testo.replace("ÿ", "y")
    testo = testo.replace("Ä", "A")
    testo = testo.replace("Ù", "U")
    testo = testo.replace("ż", "z")
    testo = testo.replace("ǎ", "a")
    testo = testo.replace("Á", "A")
    testo = testo.replace("ǒ", "o")
    testo = testo.replace("Å", "A")
    testo = testo.replace("ǐ", "i")
    testo = testo.replace("ń", "n")
    testo = testo.replace("ﬅ", "st")
    testo = testo.replace("ﬃ", "ffi")
    testo = testo.replace("ﬂ", "fl")
    testo = testo.replace("ȩ", "e")
    testo = testo.replace("ǽ", "ae")
    tavola = str.maketrans("", "", "".join(rimuovendi))
    result = testo.translate(tavola)
    for carattere in scartandi:
        testo = testo.replace(carattere, "")
    with open("C:\\Users\\aless\\PycharmProjects\\Locutor\\Puliti\\Tutto\\"+documento, "w", encoding="utf-8") as nuovo:
        nuovo.write(testo)

conservandi = set(str(lettere)+str(numeri)+str(matematici)+str(greci)+str(ebraici)+str(punteggiatura))
scartandi_ = set()
puliti = "C:\\Users\\aless\\PycharmProjects\\Locutor\\Puliti\\Tutto"
for documento in os.listdir(puliti):
    print("Controllo", documento)
    with open(puliti+"\\"+documento, "r", encoding="utf-8") as tavoletta:
        testo = tavoletta.read()
    for carattere in testo:
        if carattere not in conservandi and carattere not in scartandi_:
            scartandi_.add(carattere)
print(scartandi_)

cartella = r"/Users/locutorumrex/PycharmProjects/Locutor/Puliti/Tutto"
with open("documento_.txt", "r") as libromastro:
    registro = libromastro.read().split("\n")
    terminati = len([entrata for entrata in registro if entrata != ""])
print(registro)
print(terminati)
with open("documento_.txt", "w") as segnalibro:
    for entrata in registro:
        segnalibro.write(entrata+"\n")
    for documento in os.listdir(cartella):
        if documento in registro or documento.startswith(".") or "Summa_theologica" in documento:
            continue
        terminati += 1
        print(f"\033[35mPulisco {documento}, {terminati}\033[0m")
        with open(cartella+"/"+documento, "r", encoding="utf-8") as file:
            testo = file.read()
        testo = testo.replace("j", "i")
        testo = testo.replace("J", "I")
        testo = testo.replace("K", "C")
        testo = testo.replace("k", "c")
        testo = testo.replace("W", "V")
        testo = testo.replace("w", "v")
        testo = re.sub(r"([a-z])([A-Z])", r"\1. \2", testo)
        reg = UVRegularizer()
        testo = reg.regularize(testo, interactive=True, memory_path="uv_memory.json")
        with open(cartella+"/"+documento, "w", encoding="utf-8") as lavagna:
            lavagna.write(testo)
        segnalibro.write(documento+"\n")
'''
UA = {"User-Agent": "Alessandro Piccirilli/1.0 (contact: alessandro.piccirilli.2000@gmail.com"}
PROBLEMATICI = set()
def get_latin_section(soup: BeautifulSoup):
    """
    Wiktionary language sections are usually <h2><span class="mw-headline" id="Latin">Latin</span></h2>
    We return a container-like slice by walking forward until the next h2.
    """
    headline = soup.find("div", class_="mw-body-content")
    if not headline:
        print("Latin section not found")
        return None

    h2 = headline.find("h2")
    if not h2:
        print("Latin <h2> not found")
        return None

    # Collect nodes until next h2
    nodes = []
    cur = h2.next_sibling
    while cur:
        if isinstance(cur, Tag) and cur.name == "h2":
            break
        if isinstance(cur, Tag) or (isinstance(cur, NavigableString) and cur.strip()):
            nodes.append(cur)
        cur = cur.next_sibling

    wrapper = soup.new_tag("div")
    for n in nodes:
        wrapper.append(n if isinstance(n, Tag) else soup.new_string(str(n)))
    return wrapper

def extract_perfect_active_from_headword_line(headword_line: Tag) -> str | None:
    """
    Given a single <span class="headword-line"> ... </span>, find the form after 'perfect active'.
    On Wiktionary, forms are often inside <i> / <b> / <span class="form-of"> / <a> etc.
    We'll use a text-based split and then pick the first "word-like" token after the label.
    """
    text = headword_line.get_text(" ", strip=True)

    # Normalize whitespace and lowercase for searching; but keep original for extraction if needed
    m = re.search(r"\bperfect active\b", text, flags=re.IGNORECASE)
    if not m:
        return None

    after = text[m.end():].strip()

    # Often looks like: "fēcī, ...": grab first Latin-ish token up to punctuation/space
    # This is intentionally conservative. Adjust if you want multiword forms.
    m2 = re.match(r"([A-Za-zĀĒĪŌŪȲāēīōūȳĔĕŎŏĂăĬĭŬŭ]+)", after)
    if m2:
        return m2.group(1)

    # Fallback: find first <i> or <b> after the label in DOM order
    # (Useful if punctuation makes plain-text matching tricky.)
    # We'll scan descendants; once we pass a node containing "perfect active", pick next <i>/<b>/<a>.
    passed = False
    for node in headword_line.descendants:
        if isinstance(node, NavigableString):
            if re.search(r"\bperfect active\b", str(node), flags=re.IGNORECASE):
                passed = True
            continue
        if passed and isinstance(node, Tag) and node.name in {"i", "b", "a"}:
            cand = node.get_text(strip=True)
            if cand and not re.search(r"perfect|active", cand, flags=re.IGNORECASE):
                # Skip links like "perfect active" if any
                return cand

    return None

def extract_supine_from_headword_line(headword_line: Tag) -> str | None:
    """
    Given a single <span class="headword-line"> ... </span>, find the form after 'perfect active'.
    On Wiktionary, forms are often inside <i> / <b> / <span class="form-of"> / <a> etc.
    We'll use a text-based split and then pick the first "word-like" token after the label.
    """
    text = headword_line.get_text(" ", strip=True)

    # Normalize whitespace and lowercase for searching; but keep original for extraction if needed
    m = re.search(r"\bsupine\b", text, flags=re.IGNORECASE)
    if not m:
        return None

    after = text[m.end():].strip()

    # Often looks like: "fēcī, ...": grab first Latin-ish token up to punctuation/space
    # This is intentionally conservative. Adjust if you want multiword forms.
    m2 = re.match(r"([A-Za-zĀĒĪŌŪȲāēīōūȳĔĕŎŏĂăĬĭŬŭ]+)", after)
    if m2:
        return m2.group(1)

    # Fallback: find first <i> or <b> after the label in DOM order
    # (Useful if punctuation makes plain-text matching tricky.)
    # We'll scan descendants; once we pass a node containing "perfect active", pick next <i>/<b>/<a>.
    passed = False
    for node in headword_line.descendants:
        if isinstance(node, NavigableString):
            if re.search(r"\bsupine\b", str(node), flags=re.IGNORECASE):
                passed = True
            continue
        if passed and isinstance(node, Tag) and node.name in {"i", "b", "a"}:
            cand = node.get_text(strip=True)
            if cand and not re.search(r"supine", cand, flags=re.IGNORECASE):
                # Skip links like "perfect active" if any
                return cand
    return None

def scrape_latin_perfect_active(page_title: str) -> tuple[str | None, str | None] | None:
    time.sleep(0.9)
    url = f"https://en.wiktionary.org/wiki/{page_title}"
    html = requests.get(url, headers=UA, timeout=30).text
    soup = BeautifulSoup(html, "html.parser")

    # headword-line blocks can appear multiple times (different POS / etymologies).
    for hw in soup.find_all("span", class_="headword-line"):
        form = extract_perfect_active_from_headword_line(hw)
        form_ = extract_supine_from_headword_line(hw)
        if form is not None:
            form = form.translate(str.maketrans({
                "Ā": "A", "Ē": "E", "Ī": "I", "Ō": "O", "Ū": "U", "Ȳ": "Y",
                "ā": "a", "ē": "e", "ī": "i", "ō": "o", "ū": "u", "ȳ": "y",
                "Ĕ": "E", "ĕ": "e",
                "Ŏ": "O", "ŏ": "o",
                "Ă": "A", "ă": "a",
                "Ĭ": "I", "ĭ": "i",
                "Ŭ": "U", "ŭ": "u",
            }))
        if form_ is not None:
            form_ = form_.translate(str.maketrans({
                "Ā": "A", "Ē": "E", "Ī": "I", "Ō": "O", "Ū": "U", "Ȳ": "Y",
                "ā": "a", "ē": "e", "ī": "i", "ō": "o", "ū": "u", "ȳ": "y",
                "Ĕ": "E", "ĕ": "e",
                "Ŏ": "O", "ŏ": "o",
                "Ă": "A", "ă": "a",
                "Ĭ": "I", "ĭ": "i",
                "Ŭ": "U", "ŭ": "u",
            }))
        if form is None and form_ is None:
            print("Problema col verbo:", page_title)
            PROBLEMATICI.add(page_title)
        else:
            print("Forme:", form, form_)
        return form, form_
    print("Could not find 'perfect active' inside any Latin headword-line:", page_title)
    return None, None

def extract_genitive_from_headword_line(headword_line: Tag) -> str | None:
    """
    Given a single <span class="headword-line"> ... </span>, find the form after 'perfect active'.
    On Wiktionary, forms are often inside <i> / <b> / <span class="form-of"> / <a> etc.
    We'll use a text-based split and then pick the first "word-like" token after the label.
    """
    text = headword_line.get_text(" ", strip=True)

    # Normalize whitespace and lowercase for searching; but keep original for extraction if needed
    m = re.search(r"\bgenitive\b", text, flags=re.IGNORECASE)
    if not m:
        return None

    after = text[m.end():].strip()

    # Often looks like: "fēcī, ...": grab first Latin-ish token up to punctuation/space
    # This is intentionally conservative. Adjust if you want multiword forms.
    m2 = re.match(r"([A-Za-zĀĒĪŌŪȲāēīōūȳĔĕŎŏĂăĬĭŬŭ]+)", after)
    if m2:
        return m2.group(1)

    # Fallback: find first <i> or <b> after the label in DOM order
    # (Useful if punctuation makes plain-text matching tricky.)
    # We'll scan descendants; once we pass a node containing "perfect active", pick next <i>/<b>/<a>.
    passed = False
    for node in headword_line.descendants:
        if isinstance(node, NavigableString):
            if re.search(r"\bgenitive\b", str(node), flags=re.IGNORECASE):
                passed = True
            continue
        if passed and isinstance(node, Tag) and node.name in {"i", "b", "a"}:
            cand = node.get_text(strip=True)
            if cand and not re.search(r"genitive", cand, flags=re.IGNORECASE):
                # Skip links like "perfect active" if any
                return cand

    return None

def scrape_latin_genitive(page_title: str) -> str | None:
    time.sleep(0.9)
    url = f"https://en.wiktionary.org/wiki/{page_title}"
    html = requests.get(url, headers=UA, timeout=30).text
    soup = BeautifulSoup(html, "html.parser")
    # headword-line blocks can appear multiple times (different POS / etymologies).
    for hw in soup.find_all("span", class_="headword-line"):
        form = extract_genitive_from_headword_line(hw)
        if form is not None:
            form = form.translate(str.maketrans({
                "Ā": "A", "Ē": "E", "Ī": "I", "Ō": "O", "Ū": "U", "Ȳ": "Y",
                "ā": "a", "ē": "e", "ī": "i", "ō": "o", "ū": "u", "ȳ": "y",
                "Ĕ": "E", "ĕ": "e",
                "Ŏ": "O", "ŏ": "o",
                "Ă": "A", "ă": "a",
                "Ĭ": "I", "ĭ": "i",
                "Ŭ": "U", "ŭ": "u",
            }))
            print("Forma:", form)
            return form

    print("Could not find 'genitive' inside any Latin headword-line:", page_title)
    PROBLEMATICI.add(page_title)
    print("Problema col nome", page_title)
    return None


API = "https://en.wiktionary.org/w/api.php"
sessione = requests.Session()
sessione.headers.update(UA)
'''
lemmi = {"v1": set(), "v2": set(), "v3": set(), "v4": set(), "vi": set(), "n1": set(), "n2": set(), "n3": set(),
         "n4": set(), "n5": set(), "a1": set(),
         "a2": set(), "a1_": set(), "av": set(), "co": set(), "de": set(), "nu": set(), "pa": set(), "pre": set(), "pro": set()}
pagine = {"v1": "Category: Latin first conjugation verbs", "v2": "Category: Latin second conjugation verbs",
          "v3": "Category: Latin third conjugation verbs", "v4": "Category: Latin fourth conjugation verbs",
          "vi": "Category: Latin irregular verbs", "n1": "Category: Latin first declension nouns",
          "n2": "Category: Latin second declension nouns", "n3": "Category: Latin third declension nouns",
          "n4": "Category: Latin fourth declension nouns", "n5": "Category: Latin fifth declension nouns",
          "a1": "Category: Latin first and second declension adjectives",
          "a2": "Category: Latin third declension adjectives", "a1_": "Latin third declension adjectives of one termination",
          "av": "Category: Latin adverbs",
          "co": "Category: Latin conjunctions", "de": "Category: Latin determiners", "nu": "Category: Latin numerals",
          "pa": "Category: Latin particles", "pre": "Category: Latin prepositions", "pro": "Category: Latin pronouns"}
chiavi = lemmi.keys()
for chiave in chiavi:
    parametri = {"action": "query", "format": "json", "list": "categorymembers", "cmtitle": pagine[chiave],
                 "cmlimit": "500", "cmnamespace": "0"}
    continuazioni = {}
    while True:
        time.sleep(0.95)
        print("Scrapo:", pagine[chiave])
        richiesta = sessione.get(API, params={**parametri, **continuazioni}, timeout=30)
        richiesta.raise_for_status()
        scrapato = richiesta.json()
        membri = scrapato.get("query", {}).get("categorymembers", [])
        for membro in membri:
            lemmi[chiave].add(membro["title"])
        continuazioni = scrapato.get("continue")
        if not continuazioni:
            break
with open("Lemmiscrapati.pkl", "xb") as lemmatura:
    pickle.dump(lemmi, lemmatura)
print("\033[35mHo scrapato tutto\033[0m")
'''
with open("Lemmiscrapati.pkl", "rb") as lemmatura:
    lemmi = pickle.load(lemmatura)
'''
forme_flesse = set()
print("Verbi della prima coniugazione")
attive_presente = {"o", "as", "at", "amus", "atis", "ant", "abam", "abas", "abat", "abamus", "abatis", "abant",
                   "abo", "abis", "abit", "abimus", "abitis", "abunt", "em", "es", "et", "emus", "etis", "ent",
                   "arem", "ares", "aret", "aremus", "aretis", "arent", "a", "ate", "ato", "atote", "anto",
                   "are", "ans", "antis", "anti", "antem", "ante", "antes", "antium", "antibus", "antia", "andus",
                   "andi", "ando", "andum", "ande", "anda", "andae", "andam", "andorum", "andis", "andos",
                   "andarum", "andas"}
passive_presente = {"or", "aris", "atur", "amur", "amini", "antur", "abar", "abaris", "abatur", "abamur", "abamini",
                    "abantur", "abor", "aberis", "abitur", "abimur", "abimini", "abuntur", "er", "eris", "etur",
                    "emur", "emini", "entur", "arer", "areris", "aretur", "aremur", "aremini", "arentur", "ator",
                    "antor", "ari"}
attive_perfetto = {"i", "isti", "it", "imus", "istis", "erunt", "ere", "eram", "eras", "erat", "eramus", "eratis",
                   "erant", "ero", "eris", "erit", "erimus", "eritis", "erunt", "erim", "issem", "isses", "isset",
                   "issemus", "issetis", "issent"}
perfetti_sincopati = {"asti", "astis", "arunt", "aram", "aras", "arat", "aramus", "aratis", "arant", "aro", "arit",
                      "arimus", "arunt", "arim", "assem", "asses", "asset", "assemus", "assetis", "assent"}
supini = {"u", "us", "i", "o", "um", "e", "a", "ae", "am", "orum", "is", "os", "arum", "as", "urus", "uri", "uro",
          "urum", "ure", "ura", "urae", "uram", "urorum", "uris", "uros", "urarum", "uras"}
for lemma in lemmi["v1"]:
    print(lemma)
    if lemma.endswith("o"):
        radice = lemma[:-1]
        deponente = False
    elif lemma.endswith("or"):
        radice = lemma[:-2]
        deponente = True
    elif lemma.endswith("at"):
        radice = lemma[:-2]
        deponente = False
    else:
        print("Lemma inaspettato:", lemma)
        continue
    if lemma in {"adiuvo", "adjuvo", "adlavo", "iuvo", "adjuvo", "lavo", "perlavo"}:
        perfetto = lemma[:-1]
        supino = lemma[:-2]+"t"
    elif lemma in {"adlavo", "lavo", "perlavo"}:
        perfetto = lemma[:-1]
        supino = lemma[:-1]+"at"
    elif lemma in {"adsto", "antesto", "antisto", "asto", "circumsto", "consto", "disto", "insto", "intersto", "obsto",
                   "persto", "praesto", "prosto", "resto", "supersto"}:
        perfetto = lemma[:-1]+"it"
        supino = lemma[:-1]+"at"
    elif lemma.endswith(("frico", "plico", "tono", "seco", "sono", "crepo", "cubo", "domo", "mico", "neco", "vaco",
                         "veto")):
        perfetto = lemma[:-1]+"u"
        supino = lemma[:-1]+"at"
    elif lemma == "sto":
        perfetto = "stet"
        supino = lemma[:-1]+"at"
    elif lemma == "effrico" or lemma == "exfrico":
        perfetto = lemma[:-2]+"x"
        supino = lemma[:-1]+"at"
    else:
        perfetto = radice+"av"
        supino = radice+"at"
    if not deponente:
        for desinenza in attive_presente:
            forma = radice+desinenza
            try:
                forme_flesse.add(forma)
            except KeyError:
                pass
        for desinenza in attive_perfetto:
            forma = perfetto+desinenza
            try:
                forme_flesse.add(forma)
            except KeyError:
                pass
        for desinenza in perfetti_sincopati:
            forma = perfetto+desinenza
            try:
                forme_flesse.add(forma)
            except KeyError:
                pass
    for desinenza in passive_presente:
        forma = radice+desinenza
        try:
            forme_flesse.add(forma)
        except KeyError:
            pass
    for desinenza in supini:
        forma = supino+desinenza
        try:
            forme_flesse.add(forma)
        except KeyError:
            pass
print("Verbi della seconda coniugazione")
attive_presente = {"eo", "es", "et", "emus", "etis", "ent", "ebam", "ebas", "ebat", "ebamus", "ebatis", "ebant",
                   "ebo", "ebis", "ebit", "ebimus", "ebitis", "ebunt", "eam", "eas", "eat", "eamus", "eatis", "eant",
                   "erem", "eres", "eret", "eremus", "eretis", "erent", "e", "ete", "eto", "etote", "ento",
                   "ere", "ens", "entis", "enti", "entem", "ente", "entes", "entium", "entibus", "entia", "endus",
                   "endi", "endo", "endum", "ende", "enda", "endae", "endam", "endorum", "endis", "endos",
                   "endarum", "endas"}
passive_presente = {"eor", "eris", "etur", "emur", "emini", "entur", "ebar", "ebaris", "ebatur", "ebamur", "ebamini",
                    "ebantur", "ebor", "eberis", "ebitur", "ebimur", "ebimini", "ebuntur", "ear", "earis", "eatur",
                    "eamur", "eamini", "eantur", "erer", "ereris", "eretur", "eremur", "eremini", "erentur", "etor",
                    "entor", "eri"}
for lemma in lemmi["v2"]:
    print(lemma)
    if lemma.endswith("o"):
        radice = lemma[:-1]
        deponente = False
    elif lemma.endswith("or"):
        radice = lemma[:-2]
        deponente = True
    elif lemma.endswith("et"):
        radice = lemma[:-2]
        deponente = False
    else:
        print("Lemma inaspettato:", lemma)
        continue
    perfetto_, supino_ = scrape_latin_perfect_active(lemma)
    if deponente:
        perfetto, supino = None, perfetto_[:-6] if perfetto_ is not None else None
    else:
        perfetto = perfetto_[:-1] if perfetto_ is not None else None
        supino = supino_[:-2] if supino_ is not None else None
    if not deponente:
        for desinenza in attive_presente:
            forma = radice+desinenza
            try:
                forme_flesse.add(forma)
            except KeyError:
                pass
        if perfetto is not None:
            for desinenza in attive_perfetto:
                forma = perfetto+desinenza
                try:
                    forme_flesse.add(forma)
                except KeyError:
                    pass
    for desinenza in passive_presente:
        forma = radice+desinenza
        try:
            forme_flesse.add(forma)
        except KeyError:
            pass
    if supino is not None:
        for desinenza in supini:
            forma = supino+desinenza
            try:
                forme_flesse.add(forma)
            except KeyError:
                pass
with open("Seconda_coniugazione.pkl", "xb") as f:
    pickle.dump(forme_flesse, f)
print("Verbi della terza coniugazione")
attive_presente = {"o", "is", "it", "imus", "itis", "unt", "ebam", "ebas", "ebat", "ebamus", "ebatis", "ebant",
                   "am", "es", "et", "emus", "etis", "ent", "am", "as", "at", "amus", "atis", "ant",
                   "erem", "eres", "eret", "eremus", "eretis", "erent", "e", "ite", "ito", "itote", "unto",
                   "ere", "ens", "entis", "enti", "entem", "ente", "entes", "entium", "entibus", "entia", "endus",
                   "endi", "endo", "endum", "ende", "enda", "endae", "endam", "endorum", "endis", "endos",
                   "endarum", "endas"}
passive_presente = {"or", "eris", "itur", "imur", "imini", "untur", "ebar", "ebaris", "ebatur", "ebamur", "ebamini",
                    "ebantur", "ar", "eris", "etur", "emur", "emini", "entur", "ar", "aris", "atur",
                    "amur", "amini", "antur", "erer", "ereris", "eretur", "eremur", "eremini", "erentur", "itor",
                    "untor", "i"}
_eo = {"eo", "is", "it", "imus", "itis", "eunt", "ibam", "ibas", "ibat", "ibamus", "ibant", "ibo", "ibis", "ibit",
       "ibimus", "ibitis", "ibunt", "eam", "eas", "eat", "eamus", "eatis", "eant", "i", "ite", "ito", "itote", "eunto",
       "ire", "iens", "euntis", "eunti", "euntem", "eunte", "euntes", "euntium", "euntibus", "entia", "eundus",
       "eundi", "eundo", "eundum", "eunde", "eunda", "eundae", "eundam", "eundorum", "eundis", "eundos", "eundarum",
       "eundas", "itur", "ibatur", "ibitur", "eatur", "eretur", "irem", "ires", "iret", "iremus", "iretis", "irent"}
verbistrani = set()
for lemma in lemmi["v3"]: verbistrani.add(lemma)
for lemma in lemmi["vi"]: verbistrani.add(lemma)
for lemma in verbistrani:
    print(lemma)
    if lemma.endswith("o"):
        radice = lemma[:-1]
        deponente = False
    elif lemma.endswith("or"):
        radice = lemma[:-2]
        deponente = True
    elif lemma.endswith("it"):
        radice = lemma[:-2]
        deponente = False
    else:
        print("Lemma inaspettato:", lemma)
        continue
    if lemma.endswith("io"):
        _io = True
    else:
        _io = False
    if lemma.endswith("eo"):
        eo_ = True
    else:
        eo_ = False
    perfetto_, supino_ = scrape_latin_perfect_active(lemma)
    if deponente:
        perfetto, supino = None, perfetto_[:-6] if perfetto_ is not None else None
    else:
        perfetto = perfetto_[:-1] if perfetto_ is not None else None
        supino = supino_[:-2] if supino_ is not None else None
    if not deponente:
        if eo_:
            for desinenza in _eo:
                forma = radice[:-1]+desinenza
                try:
                    forme_flesse.add(forma)
                except KeyError:
                    pass
        else:
            for desinenza in attive_presente:
                if desinenza[0] == "i":
                    forma = radice+desinenza
                elif lemma.endswith("fero") and desinenza in {"is", "it", "itis", "itur", "eris", "ere"}:
                    forma = radice+desinenza[1:]
                elif lemma.endswith("facio") and desinenza == "e":
                    forma = radice[:-1]
                elif lemma.endswith(("duco", "dico")) and desinenza == "e":
                    forma = radice
                elif lemma.endswith("eo") and desinenza == "o":
                    forma = radice+"eo"
                elif lemma.endswith("eo") and desinenza == "unt":
                    forma = radice+"eunt"
                elif _io:
                    forma = radice+"i"+desinenza
                else:
                    forma = radice+desinenza
                try:
                    forme_flesse.add(forma)
                except KeyError:
                    pass
        if perfetto is not None:
            for desinenza in attive_perfetto:
                forma = perfetto+desinenza
                try:
                    forme_flesse.add(forma)
                except KeyError:
                    pass
    for desinenza in passive_presente:
        if _eo:
            break
        if desinenza[0] == "i":
            forma = radice+desinenza
        else:
            forma = radice+"i"+desinenza
        try:
            forme_flesse.add(forma)
        except KeyError:
            pass
    if supino is not None:
        for desinenza in supini:
            forma = supino+desinenza
            try:
                forme_flesse.add(forma)
            except KeyError:
                pass
with open("Terza_coniugazione.pkl", "xb") as f:
    pickle.dump(forme_flesse, f)
print("Verbi della quarta coniugazione")
attive_presente = {"io", "is", "it", "imus", "itis", "iunt", "iebam", "iebas", "iebat", "iebamus", "iebatis", "iebant",
                   "iam", "ies", "iet", "iemus", "ietis", "ient", "ias", "iat", "iamus", "iatis", "iant",
                   "irem", "ires", "iret", "iremus", "iretis", "irent", "i", "ite", "ito", "itote", "iunto",
                   "ire", "iens", "ientis", "ienti", "ientem", "iente", "ientes", "ientium", "ientibus", "ientia", "iendus",
                   "iendi", "iendo", "iendum", "iende", "ienda", "iendae", "iendam", "iendorum", "iendis", "iendos",
                   "iendarum", "iendas"}
passive_presente = {"ior", "iris", "itur", "imur", "imini", "iuntur", "iebar", "iebaris", "iebatur", "iebamur", "iebamini",
                    "iebantur", "iar", "ieris", "ietur", "iemur", "iemini", "ientur", "iaris", "iatur",
                    "iamur", "iamini", "iantur", "irer", "ireris", "iretur", "iremur", "iremini", "irentur", "itor",
                    "iuntor", "iri"}
perfetti_sincopati = {"isti", "irunt", "iram", "iras", "irat", "iramus", "iratis", "irant", "iro", "irit",
                      "irimus", "irunt", "irim"}
for lemma in lemmi["v4"]:
    print(lemma)
    if lemma.endswith("o"):
        radice = lemma[:-1]
        deponente = False
    elif lemma.endswith("or"):
        radice = lemma[:-2]
        deponente = True
    elif lemma.endswith("it"):
        radice = lemma[:-2]
        deponente = False
    else:
        print("Lemma inaspettato:", lemma)
        continue
    perfetto_, supino_ = scrape_latin_perfect_active(lemma)
    if deponente:
        perfetto, supino = None, perfetto_[:-6] if perfetto_ is not None else None
    else:
        perfetto = perfetto_[:-1] if perfetto_ is not None else None
        supino = supino_[:-2] if supino_ is not None else None
    if not deponente:
        for desinenza in attive_presente:
            forma = radice+desinenza
            try:
                forme_flesse.add(forma)
            except KeyError:
                pass
        if perfetto is not None:
            for desinenza in attive_perfetto:
                forma = perfetto+desinenza
                try:
                    forme_flesse.add(forma)
                except KeyError:
                    pass
            for desinenza in perfetti_sincopati:
                forma = perfetto+desinenza
                try:
                    forme_flesse.add(forma)
                except KeyError:
                    pass
            if perfetto.endswith("v"):
                for desinenza in attive_perfetto:
                    forma = perfetto[:-1]+desinenza
                    try:
                        forme_flesse.add(forma)
                    except KeyError:
                        pass
    for desinenza in passive_presente:
        forma = radice+desinenza
        try:
            forme_flesse.add(forma)
        except KeyError:
            pass
    if supino is not None:
        for desinenza in supini:
            forma = supino+desinenza
            try:
                forme_flesse.add(forma)
            except KeyError:
                pass
with open("Quarta_coniugazione.pkl", "xb") as f:
    pickle.dump(forme_flesse, f)
print("Nomi della prima declinazione")
desinenze = {"a", "ae", "am", "arum", "is", "as"}
for lemma in lemmi["n1"]:
    print(lemma)
    if lemma.endswith("a"):
        radice = lemma[:-1]
    elif lemma.endswith("ae"):
        radice = lemma[:-2]
    else:
        print("Lemma inaspettato:", lemma)
        continue
    for desinenza in desinenze:
        try:
            forme_flesse.add(radice+desinenza)
        except KeyError:
            pass
print("Nomi della seconda declinazione")
desinenze = {"us", "i", "o", "um", "e", "orum", "is", "os"}
for lemma in lemmi["n2"]:
    print(lemma)
    if lemma.endswith("us"):
        radice = lemma[:-2]
    elif lemma.endswith("i"):
        radice = lemma[:-1]
    else:
        print("Lemma inaspettato:", lemma)
        continue
    for desinenza in desinenze:
        try:
            forme_flesse.add(radice+desinenza)
        except KeyError:
            pass
print("Nomi della quarta declinazione")
desinenze = {"us", "ui", "um", "u", "uum", "ibus"}
for lemma in lemmi["n4"]:
    print(lemma)
    for desinenza in desinenze:
        try:
            forme_flesse.add(lemma[:-2]+desinenza)
        except KeyError:
            pass
print("Nomi della quinta declinazione")
desinenze = {"es", "ei", "em", "e", "erum", "ebus"}
for lemma in lemmi["n5"]:
    print(lemma)
    for desinenza in desinenze:
        try:
            forme_flesse.add(lemma[:-2]+desinenza)
        except KeyError:
            pass
print("Nomi della terza declinazione")
desinenze = {"is", "i", "em", "e", "es", "um", "ium", "ibus"}
for lemma in lemmi["n3"]:
    print(lemma)
    if lemma.endswith("io"):
        radice = lemma+"n"
    elif lemma.endswith("or"):
        radice = lemma
    else:
        radice = scrape_latin_genitive(lemma)
        if radice is not None:
            radice = radice[:-2]
        else:
            print("Problema col nome:", lemma)
            continue
    try:
        forme_flesse.add(lemma)
    except KeyError:
        pass
    for desinenza in desinenze:
        try:
            forme_flesse.add(radice+desinenza)
        except KeyError:
            pass
with open("Sostantivi.pkl", "xb") as f:
    pickle.dump(forme_flesse, f)
print("Aggettivi")
positivi = {"us", "i", "o", "um", "e", "a", "ae", "am", "orum", "is", "os", "arum", "as"}
comparativi = {"ior", "ioris", "iori", "iorem", "iore", "ius", "iores", "iorum", "ioribus", "iora"}
for lemma in lemmi["a1"]:
    print(lemma)
    if not lemma.endswith("us"):
        print("Lemma inaspettato:", lemma)
        continue
    else:
        radice = lemma[:-2]
    for desinenza in positivi:
        try:
            forme_flesse.add(radice+desinenza)
        except KeyError:
            pass
        try:
            forme_flesse.add(radice+"issim"+desinenza)
        except KeyError:
            pass
    for desinenza in comparativi:
        try:
            forme_flesse.add(radice+desinenza)
        except KeyError:
            pass
positivi_ = {"is", "i", "em", "es", "ium", "ibus", "ia"}
for lemma in lemmi["a2"]:
    print(lemma)
    neutrando = True
    if lemma.endswith("is"):
        radice = lemma[:-2]
    elif lemma.endswith("er"):
        radice = lemma[:-2]+"r"
    elif lemma in lemmi["a1_"]:
        neutrando = False
        radice = scrape_latin_genitive(lemma)
        if radice is not None:
            radice = radice[:-2]
        else:
            print("Problema con l'aggettivo:", lemma)
            continue
    else:
        print("Lemma inaspettato:", lemma)
        continue
    try:
        forme_flesse.add(lemma)
    except KeyError:
        pass
    for desinenza in positivi_:
        try:
            forme_flesse.add(radice+desinenza)
        except KeyError:
            pass
        try:
            forme_flesse.add(radice+"issim"+desinenza)
        except KeyError:
            pass
        if neutrando:
            try:
                forme_flesse.add(radice+"e")
            except KeyError:
                pass
    for desinenza in comparativi:
        try:
            forme_flesse.add(radice+desinenza)
        except KeyError:
            pass
print("Particelle")
for lemma_ in lemmi["av"], lemmi["co"], lemmi["pa"], lemmi["pre"], lemmi["nu"]:
    for lemma in lemma_:
        forme_flesse.add(lemma)
forme_flesse = {forma for forma in forme_flesse if " " not in forma}
forme_flesse_ = set()
for forma in forme_flesse:
    forme_flesse_.add(forma)
    forme_flesse_.add(forma+"que")
    forme_flesse_.add(forma+"ve")
    forme_flesse_.add(forma+"ne")
with open("forme_flesse.pkl", "xb") as flessura:
    pickle.dump(forme_flesse_, flessura)
print(PROBLEMATICI)
'''
