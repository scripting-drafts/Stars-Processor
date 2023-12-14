import re

def list_constellation_entries():
    const_list = []
    with open(r'..\data\bsc5.dat', 'r') as fi:
        for line in fi.readlines():
            if not re.match('\\d+', line[11:14]) and not ' ' in line[11:14]:
                const_abr = line[11:14]
                const_list.append(const_abr)
    const_set = set(const_list)
    return const_set

def help_module():
    print('Constellations are:\n')
    const_set = list_constellation_entries()
    print(const_set)
    print(len(const_set))

def get_available_consts():
    const_list = []
    with open(r'..\data\bsc5.dat', 'r') as fi:
        for line in fi.readlines():
            if not re.match('\\d+', line[11:14]) and not ' ' in line[11:14]:
                const_abr = line[11:14]
                const_list.append(const_abr)
    const_set = set(const_list)
    consts = list(const_set)
    # consts = [each.lower() for each in consts]
    consts.sort()

    return consts

constellations = [
    "andromeda", "antlia", "apus", "aquarius", "aquila", "ara", "aries", "auriga", 
    "bootes", "caelum", "camelopardalis", "cancer", "canes venatici", "canis major", 
    "canis minor", "capricornus", "carina", "cassiopeia", "centaurus", "cepheus", 
    "cetus", "chamaeleon", "circinus", "columba", "coma berenices", "corona australis", 
    "corona borealis", "corvus", "crater", "crux", "cygnus", "delphinus", "dorado", 
    "draco", "equuleus", "eridanus", "fornax", "gemini", "grus", "hercules", "horologium", 
    "hydra", "hydrus", "indus", "lacerta", "leo", "leo minor", "lepus", "libra", "lupus", 
    "lynx", "lyra", "mensa", "microscopium", "monoceros", "musca", "norma", "octans", 
    "ophiuchus", "orion", "pavo", "pegasus", "perseus", "phoenix", "pictor", "pisces", 
    "piscis austrinus", "puppis", "pyxis", "reticulum", "sagitta", "sagittarius", "scorpius", 
    "sculptor", "scutum", "serpens", "sextans", "taurus", "telescopium", "triangulum", 
    "triangulum australe", "tucana", "ursa major", "ursa minor", "vela", "virgo", "volans", 
    "vulpecula"
]