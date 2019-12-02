from lxml import etree, html
import os

page_xpath = {
    #Capa
    'numero': '//*[@id="txtNumProcesso"]/text()',
    'orgao_julgador': '//*[@id="txtOrgaoJulgador"]/text()',
    'classe_da_acao': '//*[@id="txtClasse"]/text()',
    'data_autuacao': '//*[@id="txtAutuacao"]/text()',
    'situacao': '//*[@id="txtSituacao"]/text()',
    'juiz': '//*[@id="txtMagistrado"]/text()',
    'processos_relacionados': '//*[@id="tableRelacionado"]/tr[2]',

    #partes e representantes:
    'impetrante': '//*[@id="fldPartes"]/table/tr[2]/td[1]',
    'impetrado': '//*[@id="fldPartes"]/table/tr[2]/td[2]',
    'interessado': '//*[@id="fldPartes"]/table/tr[4]/td/text()',
    'mpf': '//*[@id="fldPartes"]/table/tr[6]/td',

    #andamento
    'andamento': '//*[@id="divInfraAreaProcesso"]/table/tr/td'
}

page_table_keys = [
    'processos_relacionados',
    'impetrante',
    'impetrado',
    'interessado',
    'mpf',
    'andamento'
]

def extrai_processos():

    pasta = 'avaliacao/extrator/data/'
    arquivos = []
    processos = []

    for r, d, f in os.walk(pasta):
        for file in f:
            if '.html' in file:
                arquivos.append(os.path.join(r, file))

    for i in arquivos:
        processos.append(extrai_info(i))

    return processos


def extrai_info(arquivo=None):

    parser = etree.HTMLParser()
    tree = etree.parse(arquivo, parser)
    doc = html.parse(arquivo)

    processo = {}
    for key in page_xpath:
        if(key in page_table_keys):
            if(key == 'andamento'):
                andamento = [td.text_content().replace(u'\xa0', u' ') for td in doc.xpath(page_xpath[key])]
                eventos = []
                for i in range(0, int(len(andamento)/5)):
                    eventos.append(
                        {
                            'evento': andamento[i*5],
                            'data_hora': andamento[i*5+1],
                            'descricao': andamento[i*5+2],
                            'usuario': andamento[i*5+3],
                            'documentos': andamento[i*5+4]
                        }
                    )

                processo[key] = eventos
            elif(key == 'interessado'):
                processo[key] = [td.replace(u'\xa0', u' ') for td in tree.xpath(page_xpath[key])]
            else:
                processo[key] = [td.text_content().replace(u'\xa0', u' ') for td in doc.xpath(page_xpath[key])]
        else:
            processo[key] = tree.xpath(page_xpath[key])[0]

    return processo