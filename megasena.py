import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected_cond
from selenium.common.exceptions import NoSuchElementException
driver = webdriver.Chrome(executable_path="C:\selenium\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
numero=[]
numeros=[]
dezenas=[]

''' Página que iremos acessar '''
driver.get("http://loterias.caixa.gov.br/wps/portal/loterias/landing/megasena")

def ultimo_resultado():
    try:
        ''' Explicit Waits '''
        page = WebDriverWait(driver, 5).until(
            expected_cond.presence_of_element_located((By.XPATH, "//ul[@class='numbers megasena'][@id='ulDezenas']"))
        )

        driver.get(driver.current_url)
        time.sleep(1)

        lista_campo_dezenas = driver.find_element_by_id("ulDezenas")
        lista_numeros = lista_campo_dezenas.find_elements_by_tag_name("li")
        lista_ano = driver.find_element_by_xpath("//h2[contains(text(), 'Resultado')]/span[contains(text(), 'Concurso')]")
        for x,i in enumerate(lista_numeros,0):
            numero.insert(x,i.text)
        ################## DEBUG ################
        # print(lista_ano.text, " - ", numero[:])
        #########################################
        ''' Retorna a descrição do ano e a lista das dezenas '''
        return lista_ano, numero[:]

    except NoSuchElementException as erro:
        print("ERRO: Busca pelos campos html.\nCAUSA: Elementos não encontrados.")
        print(erro)

def resultados_anteriores():
    try:
        ultimo_sorteio = ['']
        ''' Recebe STRING com a data do resultado e uma LISTA com as dezenas '''
        ultimo_sorteio = ultimo_resultado()

        ############################ DEBUG ##############################
        # print("1º ", ultimo_sorteio[0].text, "\n2º ", ultimo_sorteio[1])
        #################################################################

        regex = re.compile(r'\s\d\d\d\d\s')
        sorteio = regex.findall(ultimo_sorteio[0].text)

        for num_sorteios in range(1, int(sorteio[0])):

            ''' Explicit Waits '''
            page = WebDriverWait(driver, 5).until(
                expected_cond.presence_of_element_located((By.ID, "buscaConcurso"))
            )

            # driver.executeScript("document.getElementById('buscaConcurso').setAttribute('value', '"+x+"')")
            # driver.execute_script("document.getElementById('buscaConcurso').value='"+str(x)+"'")
            enviaconcurso = driver.find_element_by_id("buscaConcurso")
            enviaconcurso.send_keys(num_sorteios)
            enviaconcurso.send_keys(Keys.RETURN)

            time.sleep(1)

            enviaconcurso.clear()
            ''' Encontra o campo com as dezenas'''
            lista_campo_dezenas = driver.find_element_by_id("ulDezenas")
            ''' percorre os campos html "li" com os valores de cada dezena'''
            lista_numeros = lista_campo_dezenas.find_elements_by_tag_name("li")
            ''' Pega o valor textual do campo h2 que escreve "Resultado Concurso" '''
            lista_texto_concurso = driver.find_element_by_xpath("//h2[contains(text(), 'Resultado')]/span[contains(text(), 'Concurso')]")

            ''' Preenche a lista DEZENAS com cada str DEZENA encontrada LISTA_NUMERO '''
            for indice, dezena in enumerate(lista_numeros):
                dezenas.insert(indice, dezena.text)
                ################## DEBUG ################
                # print(lista_texto_concurso.text, " - ", numero[:])
                #########################################

            ''' Format: Concurso - data - dezenas '''
            # print(lista_texto_concurso.text + " {0}-{1}-{2}-{3}-{4}-{5}".format(*dezenas))

            regex = re.compile(r'\s\d+\s')
            concurso = regex.findall(lista_texto_concurso.text)

            ''' Format: Concurso dezenas '''
            # print("{0}".format(*concurso) + " {0}-{1}-{2}-{3}-{4}-{5}".format(*dezenas))

            ''' Escreve as dezenas no arquivo dezenas-mega.txt '''
            f = open("D:\\megasena\\todossorteios.txt", "a")
            f.write("{0}".format(*concurso) + " {0} {1} {2} {3} {4} {5}\n".format(*dezenas))
            f.close()

            # f = open("D:\\megasena\\todossorteios.txt", "r")
            # print(f.read())

            del dezenas[:]

    except NoSuchElementException as erro:
        print("ERRO: Busca pelos campos html.\nCAUSA: Elementos não encontrados.")
        print(erro)

def fechar_driver():
    driver.quit()

if __name__ == '__main__':
    resultados_anteriores()
    fechar_driver()