import json

file_public_hearing_br_lds = './PublicHearingBR_LDS.jsonl'
file_public_hearing_br_nli = './PublicHearingBR_NLI.jsonl'

def load_jsonl(filename):
    dataset = []
    with open(filename, encoding='utf-8') as fin:
        for line in fin:
            dataset.append(json.loads(line))
    return dataset

def print_phbr_lds(n=206):
    for sample in phbr_lds[0:n]:
        id = sample['id']
        transcricao = sample['transcricao'] # long document
        materia = sample['materia'] # summary
        metadados = sample['metadados'] # structured summary
        
        print(f"\n########## ID: {id}")
        for envolvido in metadados['envolvidos']:
            cargo = envolvido['cargo']
            nome = envolvido['nome']
            opinioes = envolvido['opinioes']
            
            print(f"\n\tNome: {nome}")
            print(f"\tCargo: {cargo}")
            print("\tOpiniões:")
            for opiniao in opinioes:
                print(f"\t\t- {opiniao}")              
                
phbr_lds = load_jsonl(file_public_hearing_br_lds)
phbr_nli = load_jsonl(file_public_hearing_br_nli)

print_phbr_lds(1)

#phbr_nli[0]['metadados_extraidos']['envolvidos'][0]['opinioes'][0]['verificacao_alucinacao'].keys()