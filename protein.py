#!python

# author: Yuhong LIN
# cerate date: 18:40, Jan 3, 2024

# sth for protein process

def one2three(s):
    # s: str, 1-letter code for residue
    # return: str, 3-letter code

    one2three_dict = {'V':'VAL', 'I':'ILE', 'L':'LEU', 'E':'GLU', 'Q':'GLN', 'D':'ASP', 'N':'ASN', 'H':'HIS', 'W':'TRP', 'F':'PHE', 'Y':'TYR', 'R':'ARG', 'K':'LYS', 'S':'SER', 'T':'THR', 'M':'MET', 'A':'ALA', 'G':'GLY', 'P':'PRO', 'C':'CYS'}

    return one2three_dict[s]

def three2one(s):
    # s: str, 3-letter code for residue
    # return: str, 1-letter code

    three2one_dict = {'VAL':'V', 'ILE':'I', 'LEU':'L', 'GLU':'E', 'GLN':'Q', 'ASP':'D', 'ASN':'N', 'HIS':'H', 'TRP':'W', 'PHE':'F', 'TYR':'Y', 'ARG':'R', 'LYS':'K', 'SER':'S', 'THR':'T', 'MET':'M', 'ALA':'A', 'GLY':'G', 'PRO':'P', 'CYS':'C'}

    return three2one_dict[s]


if __name__ == '__main__':
    # testing

    print(one2three('S'))
    print(three2one('TYR'))