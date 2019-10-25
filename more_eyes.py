from sys import argv

from input.get_document import DataFile
from nlp.process import NLP

document = DataFile(argv[1])
nat_lang = NLP(document.content)

print(document.__dict__)
print(nat_lang.__dict__)
