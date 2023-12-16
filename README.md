# Checagem de imóveis

:small_blue_diamond: [Sobre](#sobre)

:small_blue_diamond: [Tecnologias utilizadas](#tecnologias-utilizadas)

:small_blue_diamond: [Funcionalidades](#funcionalidades)

:small_blue_diamond: [Pré-requisitos](#pré-requisitos)

:small_blue_diamond: [Como rodar a aplicação](#como-rodar-a-aplicação-arrow_forward)

:small_blue_diamond: [Endpoints](#Endpoints)

:small_blue_diamond: [Informações do JSON](#Informações-do-JSON-floppy_disk)

:small_blue_diamond: [Desenvolvedores](#Desenvolvedores)

## Sobre
Aplicação feita para checar dados de forma automática através de tabelas (csv) de dados disponibilizadoos pela Caixa.

### Tecnologias utilizadas
<p align="center">
  <img src="http://img.shields.io/static/v1?label=Python&message=3.10.4&color=blue&style=for-the-badge&logo=PYTHON"/>
  <img src="https://img.shields.io/static/v1?label=Flask&message=framework&color=red&style=for-the-badge&logo=FLASK"/>
  <img src="https://img.shields.io/static/v1?label=Celery&message=Async queue&color=dark green&style=for-the-badge&logo=CELERY"/>
  <img src="https://img.shields.io/static/v1?label=RABBITMQ&message=Menssage broker&color=orange&style=for-the-badge&logo=RABBITMQ"/>
  <img src="https://img.shields.io/static/v1?label=Selenium&message=Web Automation&color=dark green&style=for-the-badge&logo=SELENIUM"/>
  <img src="http://img.shields.io/static/v1?label=MongoDB&message=Database&color=cool green&style=for-the-badge&logo=MONGODB"/>

- [Python docs](https://docs.python.org/3.10/)
- Flask ([docs](https://flask.palletsprojects.com/en/3.0.x/)) - Framework para Web muito poderoso para criação de microserviços
- Celery ([docs](https://docs.celeryq.dev/en/stable/)) - Celery é um sistema de filas de tarefas assíncronas, que realiza as atividades dependendo da fila e não em tempo de envio do usuário. No projeto, ele é utilizado para fazer o upload do documento e a extração dos textos, para que não seja necessário o usuário esperar a conclusão da tarefa anterior para enviar outros documentos. O celery utiliza o método de multi-threading.
- RabbitMQ ([docs](https://www.rabbitmq.com/documentation.html)) - Broker (gestor) de mensagens.
- Selenium ([docs](https://selenium-python.readthedocs.io/getting-started.html)) - biblioteca para automação de browsers afim de extrair, coletar, ou enviar informações através deles.
- MongoDB ([docs](https://www.mongodb.com/docs/)) - Banco de dados não relacional utilizado para salvar as informações.
</p>

## Funcionalidades

:heavy_check_mark: Baixar csv através do site da caixa de forma automática

:heavy_check_mark: Analizar o arquivo csv, comparando-o com o arquivo do dia anterior à fins de verificar se houve alguma mudança

:heavy_check_mark: Salvar em um banco de dados (mongodb) para que se possa visualizar quais alterações foram feitas

:heavy_check_mark: Visualizar as informações através de uma endpoint

## Pré requisitos
### Celery
- Para conseguir rodar o celery, é necessário, primeiro, instalar um broker (Um app responsável pela execução e mantimento das tarefas do celery). No projeto, foi utilizado o  broker chamado RABBITMQ ([docs](https://www.rabbitmq.com/documentation.html)).
- Para fazer a instalação do RabbitMQ, é necessário ir para [Dowload Windows](https://www.rabbitmq.com/install-windows.html) e descer até a parte chamada "Dependencies" e baixar e instalar o Erlang (uma dependencia necessária para o RabbitMQ. Caso queria instalar diretamente: [Download Erlang 25.3.2](https://www.erlang.org/patches/otp-25.3.2)). Após baixar, a instalação é feita de forma simples, basta clicar em prosseguir (next) até o final.
- Após a instalação do Erlang, faça o download do RabbitMQ na parte, logo abaixo de dependencies, chamada "Direct Downloads", e clique no link que estará na grade de "Downloads". A instalação também é feita de forma simples, basta clicar em prosseguir (next) até o final.
![Visualização da página dita nos texos acima](https://github.com/arthurhenrique02/testeProjetoPM/assets/109195033/e70b9599-94fc-4b61-90d0-71451902e90c)
- Feito a instalação do Erlang e do RabbitMQ, abra o explorador de arquivos, vá em Disco local, clique em arquivos de programas e procure uma pasta chamada RabbitMQ Server. Após localizá-la, entre na pasta, clique na pasta chama rabbitmq_server-... (após o traço averá a versão do server do RabbitMQ, por exemplo 3.11.17), entre na pasta chamada sbin, e execute como administrador o arquivo chamado 'rabbitmq-server'. Após a execução deste arquivo, o Broker para o Celery estará funcionando e você estará habilitado a utilizá-lo.
- Caminho e arquivo que será executado como administrador:
![Captura de tela 2023-07-06 170546](https://github.com/arthurhenrique02/testeProjetoPM/assets/109195033/8c3796df-7d8c-4573-af4c-fac5e5d16669)

### MongoDB
O mongodb ([donwload para versão da grátis](https://www.mongodb.com/try/download/community)) uma instalação rápida e simples, basta clicar em prosseguir até o final. Configure-o após a instalação e mantenha o mesmo em background.


# Como rodar a aplicação :arrow_forward:

Baixe o projeto na aba ![Capturar](https://github.com/arthurhenrique02/testeProjetoPM/assets/109195033/dea87f4a-14ed-4830-a650-eb86236133f9)
(clique no botao e baixe o zip do projeto, depois faça a extracao do mesmo em sua máquina
No terminal).
Ou clone o projeto: 

&nbsp; &nbsp; :small_blue_diamond: Crie uma pasta, entre na mesma e clique com o botao direito dentro da área, após isso clique em 'Git Bash here' e digite o comando:
```
  git init
```
&nbsp; &nbsp; :small_blue_diamond: Após inicializar um repositório, digite o seguinte comando para clonar: 

```
  https://github.com/arthurhenrique02/propertiesChecker.git
```
Após o download/clone do projeto, abra-o em uma ide (estaremos utilizando o [Visual Studio Code](https://code.visualstudio.com/) para os prints de demonstração).

Crie um ambiente virtual(venv) para baixar as dependências, basta digitar o seguinte código no terminal da ide: 
```
  python -m venv .venv
```
Após ter criado o ambiente virtual precisaremos ativá-lo: 

<ul>
<li><strong>No Unix ou MacOS, usando o bash shell: </strong><code>source .venv/bin/activate</code></li>
<li><strong>No Unix ou MacOS, usando o csh shell: </strong><code>source .venv/bin/activate.csh</code></li>
<li><strong>No Unix ou MacOS, usando o fish shell: </strong><code>source .venv/bin/activate.fish</code></li>
<li><strong>No Windows usando o Command Prompt:</strong> <code>.\.venv\Scripts\activate</code></li>
<li><strong>No Windows usando o PowerShell: </strong><code>.venv\Scripts\Activate.ps1</code></li>
</ul>

&nbsp; &nbsp; &nbsp; &nbsp;![demonstração de sucesso na inicialização da venv](https://github.com/arthurhenrique02/testeProjetoPM/assets/109195033/f4952ef1-9659-47dc-ab09-f4a82412609b)

&nbsp; &nbsp; &nbsp; &nbsp;Deverá aparecer o texto '(venv)' ou '(.venv)' antes do caminho da sua pasta

<br>
<br>

Depois do ambiente ser ativado baixe todas as dependências na venv pelo pip: 

```
  pip install -r requirements.txt
```
Após a instalação das dependências, o projeto poderá ser inicializado.
Então temos que inicializar a nossa aplicação do Flask. Para isso, temos que utilizar o seguinte comando:
```
  python main.py
```
Deverá aparecer o seguinte código no terminal, após a execução do comando acima:

![image](https://github.com/arthurhenrique02/propertiesChecker/assets/109195033/d86ae866-a2bf-49a8-80fe-3694e98d1592)


Então, para que o projeto possa ser utilizado após sua inicialização, precisaremos inicalizar o celery:

&nbsp; &nbsp; Abra um outro terminal clicando no + no canto superior direito do terminal atual (Segue exemplo no Vs Code: ![terminal](https://github.com/arthurhenrique02/testeProjetoPM/assets/109195033/34f0ab1b-0ed1-479e-9023-48878b31016d))

&nbsp; &nbsp; Após abertura de outro terminal, digite o seguinte código no mesmo (no caso do windows):
```
  celery -A main.celery worker -l info --pool=solo
```
&nbsp; &nbsp; Ou, no caso de linux:
```
  celery -A main.celery worker -l info
```
Deverá aparecer o seguinte código no terminal, após a execução do comando acima:

![rodar celery](https://github.com/arthurhenrique02/propertiesChecker/assets/109195033/00c9cc7f-ba40-4311-9a9e-3764f15a893f)

Após inicializar o Celery, devemos inicializar o Celery Beat (biblioteca para o celery que realiza a execução de tasks de tempos em tempos. No caso desta aplicação, 1 vez por dia). Para isso utilizamos o comando:
```
  celery -A main.celery beat -l INFO
```
Deverá aparecer o seguinte código no terminal, após a execução do comando acima:

![image](https://github.com/arthurhenrique02/propertiesChecker/assets/109195033/259ce3d6-e67e-4439-9a95-b9e4aecab522)


❗ IMPORTANTE

vale lembrar que cada um desses comando irá abrir uma aba do browser (Chrome) devido à inicialização do projeto. Não há nada demais na inicialização desses browsers. O browser inicializado irá ser controlado pelo Selenium!

## Endpoints

A API possui apenas uma endpoint (/) onde é possível ver todos os dados através de uma tabela.

![exemplo root](https://github.com/arthurhenrique02/propertiesChecker/assets/109195033/fcfd58f4-ad2a-4f18-8472-22348818e143)
