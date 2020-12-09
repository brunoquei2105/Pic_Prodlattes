"""Code done by Bruno Queiroz student of first year of graduation in System Analysis and Development(IT)
date: 09/12/2020
"""
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
    """Função que printa as tags filhas relacionadas com a tag raiz
    DADOS-GERAIS -> child_tag(root[0])
    PRODUCAO-BIBLIOGRAFICA -> child_tag(root[1])
    PRODUCAO-TECNICA -> child_tag(root[2])
    OUTRA-PRODUCAO -> child_tag(root[3])
    DADOS-COMPLEMENTARES -> child_tag(root[4])
    """
    child_list = [(child.tag) for child in root]
    print(child_list)



def child_atribute(root):
    child_atb = [(child.attrib) for child in root]
    print(child_atb)



def get_id(root) :
    """Pega o número de Identificação do CV(chave primária) """
    for child in root.iter('CURRICULO-VITAE'):
        num_identificador = str(child.attrib['NUMERO-IDENTIFICADOR'])
        return num_identificador



def get_nome(root):
    """Função retorna o nome completo do CV analisado"""
    for child in root.iter('DADOS-GERAIS'):
        nome = str(child.attrib['NOME-COMPLETO'])
        return nome


def get_article(root):
    soma = 0
    for artigo in root.iter("DADOS-BASICOS-DO-ARTIGO"):
        print(f"Titulo do Artigo: {artigo.attrib['TITULO-DO-ARTIGO']}, Ano: {artigo.attrib['ANO-DO-ARTIGO']}")
        soma += 1
    return f'O Professor {get_nome(root)} tem {soma} artigos publicados.'


def get_resume_cv(root):
    for resume in root.iter("RESUMO-CV"):
        print(resume.attrib['TEXTO-RESUMO-CV-RH'])

"""USUÁRIO"""
print('====Curriculum Lattes====')
print('[1] Dados Gerais \n[2] Produção Bibliográfica \n[3] Produção Técnica \n[4] Outras Produções '
      '\n[5] Dados Complementares')
print('Qual campo deseja navegar: ')
response = int(input())

if response == 1:
    # Faz o pasing pela tag 'DADOS-GERAIS'
    print('[1]RESUMO-CV,  \n[2]FORMACAO-ACADEMICA-TITULACAO, \n[3]ATUACOES-PROFISSIONAIS, '
          '\n[4]AREAS-DE-ATUACAO, '
          '\n[5]IDIOMAS, \n[6]PREMIOS-TITULOS')
    print('Qual desses campos deseja visualizar:')
    campo = int(input())
    if campo == 1:
        #Resumo
        with open('resumo_cv.txt') as resumo:
            resumo.read()
    if campo == 2:
        #Formação academica
        print(f'***ID Curriculum: {get_id(root)}***')
        for grd in root.iter('GRADUACAO'):
            print(f'GRADUAÇÃO: {grd.attrib["NOME-CURSO"]} INSTITUIÇÃO: {grd.attrib["NOME-INSTITUICAO"]}')
        print()
        for grd in root.iter('MESTRADO'):
            print(f'MESTRADO: {grd.attrib["NOME-CURSO"]}. TÍTULO DISSERTAÇÃO: {grd.attrib["TITULO-DA-DISSERTACAO-TESE"]}'
                  f'\nAN0 INÍCIO: {grd.attrib["ANO-DE-INICIO"]} \nANO CONCLUSÃO: {grd.attrib["ANO-DE-CONCLUSAO"]} '
                  f'\nINSTITUIÇÃO: {grd.attrib["NOME-INSTITUICAO"]}')
        print()
        for grd in root.iter('DOUTORADO'):
            print(f'DOUTORADO: {grd.attrib["NOME-CURSO"]}. TÍTULO DISSERTAÇÃO: {grd.attrib["TITULO-DA-DISSERTACAO-TESE"]}'
                  f'\nANO INÍCIO: {grd.attrib["ANO-DE-INICIO"]} \nANO CONCLUSÃO: {grd.attrib["ANO-DE-CONCLUSAO"]}'
                  f'\nINSTITUIÇÃO: {grd.attrib["NOME-INSTITUICAO"]}')
    if campo == 3:
        # Atuação Profissional1
        for atuacion in root.iter('ATUACAO-PROFISSIONAL'):
            print('Atua ou atuou em diversas instituições como: ')
            print(atuacion.attrib["NOME-INSTITUICAO"])
    if campo == 4:
        print(f'***ID Curriculum: {get_id(root)}***')
        for area in root.iter('AREA-DE-ATUACAO'):
            if area.attrib["NOME-DA-ESPECIALIDADE"] == "":
                print(f'Área de Atuação: {area.attrib["NOME-DA-SUB-AREA-DO-CONHECIMENTO"]}')
            else:
                print(f'Área de Atuação: {area.attrib["NOME-DA-ESPECIALIDADE"]}')
    if campo == 5:
        print(f'***ID Curriculum: {get_id(root)}***')
        for idm in root.iter("IDIOMA"):
            print(f'IDIOMA: {idm.attrib["DESCRICAO-DO-IDIOMA"]}')
            print(f'PROFICIÊNCIA: {idm.attrib["PROFICIENCIA-DE-COMPREENSAO"]}')
    if campo == 6:
        print(f'***ID Curriculum: {get_id(root)}***')
        for prm in root.iter("PREMIO-TITULO"):
            print(f'Nome do Prêmio: {prm.attrib["NOME-DO-PREMIO-OU-TITULO"]}')
            print(f'Nome da Entidade Promotora: {prm.attrib["NOME-DA-ENTIDADE-PROMOTORA"]}')
            print(f' Ano do Prêmio: {prm.attrib["ANO-DA-PREMIACAO"]}')
            print()

if response == 2:
    #Faz o parsing por produçoes bibliográficas
    print('[1]TRABALHOS-EM-EVENTOS', '\n[2]ARTIGOS-PUBLICADOS', '\n[3]LIVROS-E-CAPITULOS',
           '\n[4]DEMAIS-TIPOS-DE-PRODUCAO-BIBLIOGRAFICA', '\n[5]ARTIGOS-ACEITOS-PARA-PUBLICACAO')



"""BANCO DE DADOS"""
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
