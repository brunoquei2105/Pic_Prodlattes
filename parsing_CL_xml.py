import xml.etree.ElementTree as ET
import pandas as pd
import mysql.connector
from datetime import date

connection = mysql.connector.connect(host='localhost', user='root', password='21050630', database='Pic_prodlattes', charset='utf8')
cursor = connection.cursor(dictionary=True)

"""Inicializando a árvore XML"""
tree = ET.parse('C:/Users/Bruno Queiroz/Desktop/ADS/Iniciação_cientifica/arquivo_xml/curriculo-silvio.xml')
root = tree.getroot()

#print(ET.tostring(root, encoding='utf8').decode('utf8'))


def child_tag(root):
    """Função que printa as tags filhas relacionadas com a tag raiz"""
    child_list = [(child.tag) for child in root]
    print(child_list)


child_tag(root)
child_tag(root[0])
'''
DADOS-GERAIS -> child_tag(root[0])
PRODUCAO-BIBLIOGRAFICA -> child_tag(root[1])
PRODUCAO-TECNICA -> child_tag(root[2])
OUTRA-PRODUCAO -> child_tag(root[3])
DADOS-COMPLEMENTARES -> child_tag(root[4])
'''


def child_atribute(root):
    child_atb = [(child.attrib) for child in root]
    print(child_atb)


child_atribute(root[0])

#print(lista := [elemt for elemt in root.iter()])



def get_id(root) :
    """Pega o número de Identificação do CV(chave primária) """
    for child in root.iter('CURRICULO-VITAE'):
        num_identificador = str(child.attrib['NUMERO-IDENTIFICADOR'])
        return num_identificador

print(pk := get_id(root))


def get_nome(root):
    """Função retorna o nome completo do CV analisado"""
    for child in root.iter('DADOS-GERAIS'):
        nome = str(child.attrib['NOME-COMPLETO'])
        return nome


print(nome := get_nome(root))

def get_article(root):
    soma = 0
    for artigo in root.iter("DADOS-BASICOS-DO-ARTIGO"):
        print(f"Titulo do Artigo: {artigo.attrib['TITULO-DO-ARTIGO']}, Ano: {artigo.attrib['ANO-DO-ARTIGO']}")
        soma += 1
    return f'O Professor {get_nome(root)} tem {soma} artigos publicados.'


print(get_article(root))


def get_resume_cv(root):
    for resume in root.iter("RESUMO-CV"):
        print(resume.attrib['TEXTO-RESUMO-CV-RH'])


get_resume_cv(root)


resposta = input('Você deseja salvar as informações do Curriculo Lattes no BD Pic_Prodlattes: ')
if resposta == "Sim" or resposta == 'sim':
    #Inserindo dados do XML no BD MySql Pic_prodlattes
    cursor.execute(f"INSERT INTO CV(num_id, nome, artigos) VALUES('{get_id(root)}', '{get_nome(root)}', '{get_article(root)}')")
    connection.commit()
    current_date = date.today()
    print(f'Insert realizado com sucesso: {current_date}')
    #COMANDO SELECT
    select = input('Você deseja visualizar a Tabela CV?')
    if select == 'Sim' or select == 'sim':
        sql_select = 'SELECT * FROM CV;'
        cursor.execute(sql_select)
        data_frame = pd.DataFrame(cursor)
        print(data_frame.head())
        # UPDATE
    else:
        update = input('Deseja atualizar o dado de alguma coluna da Tabela User: ')
        if update == 'Sim' or update == 'sim':
            columns = ['num_id', 'nome', 'artigos']
            for column in columns:
                print(column)
            coluna = str(input('Qual das coluna deseja alterar: '))
            valor = str(input('Digite a alteração que deseja fazer nesta coluna: '))
            sql_update = f'UPDATE USER set {coluna} = {valor}'
            cursor.execute(sql_update)
            print('Até Logo.')
else:
    print('Até Logo.')


cursor.close()
connection.commit()
connection.close()
