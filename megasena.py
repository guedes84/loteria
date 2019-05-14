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
numero=['']
numeros=[[''],['']]

''' Página que iremos acessar '''
driver.get("http://loterias.caixa.gov.br/wps/portal/loterias/landing/megasena")

def ultimo_resultado():
    print("Try 1 - acessar a página e verificar o último resultado")

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
    finally:
        print("ultimo_resultado executado.")
        # fechar_driver()

def resultados_anteriores():
    print("Try 2 - acessar a página e verificar os resultados anteriores.")

    try:
        ultimo_sorteio = ['']
        ''' Recebe STRING com a data do resultado e uma LISTA com as dezenas '''
        ultimo_sorteio = ultimo_resultado()

        ############################ DEBUG ##############################
        print("1º ", ultimo_sorteio[0].text, "\n2º ", ultimo_sorteio[1])
        #################################################################

        regex = re.compile(r'\s\d\d\d\d\s')
        sorteio = regex.findall(ultimo_sorteio[0].text)

        for x in range(1,int(sorteio[0])):

            ######## DEBUG ########
            print("FOR: Concurso ",x)

            ''' Explicit Waits '''
            page = WebDriverWait(driver, 5).until(
                expected_cond.presence_of_element_located((By.ID, "buscaConcurso"))
            )

            # driver.executeScript("document.getElementById('buscaConcurso').setAttribute('value', '"+x+"')")
            # driver.execute_script("document.getElementById('buscaConcurso').value='"+str(x)+"'")
            enviaconcurso = driver.find_element_by_id("buscaConcurso")
            enviaconcurso.send_keys(x)
            enviaconcurso.send_keys(Keys.RETURN)

            time.sleep(1)

            enviaconcurso.clear()
            ''' Encontra o campo com as dezenas'''
            lista_campo_dezenas = driver.find_element_by_id("ulDezenas")
            ''' percorre os campos html "li" com os valores de cada dezena'''
            lista_numeros = lista_campo_dezenas.find_elements_by_tag_name("li")
            ''' Pega o valor textual do caralho h2 que escreve "Resultado Concurso" '''
            lista_texto_concurso = driver.find_element_by_xpath("//h2[contains(text(), 'Resultado')]/span[contains(text(), 'Concurso')]")

            for x, i in enumerate(lista_numeros, 0):
                print(type(lista_numeros))
                numeros.insert(x,lista_texto_concurso.text+"-"+lista_numeros)
                ################## DEBUG ################
                # print(lista_texto_concurso.text, " - ", numero[:])
                #########################################
                print(numeros[x])

    except NoSuchElementException as erro:
        print("ERRO: Busca pelos campos html.\nCAUSA: Elementos não encontrados.")
        print(erro)
    finally:
        print("resultados_anteriores executado.")
        # fechar_driver()

def fechar_driver():
    driver.quit()

if __name__ == '__main__':
    resultados_anteriores()
    fechar_driver()