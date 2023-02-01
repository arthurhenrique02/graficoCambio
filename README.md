# Gráfico de Cambio

## Sobre o projeto
### Descrição:
##### Um projeto feito por hobby para treinar as skills em JavaScript, CSS, HTML e Python.
##### O projeto busca mostrar informações diárias, semanais ou mensais sobre câmbios de moedas dentro de um gráfico, a partir de uma RestAPI.

### Tecnologias utilizadas:
##### JavaScript (vanilla e ApexChart para o gráfico)
##### CSS e HTML
##### Python (Flask, Flask restful, para criação do Web app e da API)
##### SQLite (para salvar as informações)

### Informações:

#### Front-end:
##### criado um layout com HTML e css onde mostra dois cartões, um para o valor do câmbio do dia e o outro para mostrar o gráfico semanal/mensal do câmbio daquela moeda para euro.
##### Foi criado um gráfico com a biblioteca ApexChart (nome do gráfico: exchangeChart), após isso, foi criado uma função assíncrona para alterar os dados do gráfico de acordo com o desejo do usuário, podendo ser mudado a moeda atual que o gráfico mostra, os dias (para 7 ou 30 dias), e que retornará no gráfico os novos valores
##### O outro card mostra apenas o valor do câmbio da moeda que está sendo mostrada no gráfico para euro, conta com alguns elementos mostrando qual a moeda o usuário está visualizando (exemplo: EUR to USD)
##### Foi utilizado o jinja presente no Flask para fazer um loop que criasse todas as opções de moedas selecionáveis.

#### Back-end:
##### Foi criado uma APIRest (TakeExchangeInfo), com flask/flask restful, que coleta informações de uma outra API (https://api.frankfurter.app/) e salva em um banco de dados SQLite e retorna as informações, em JSON, desse banco de dados através de uma URL (/exchanges/(nome da moeda)/(quantidade de dias que deseja) para o front-end
##### Quando a API é iniciada, ela checa se no banco de dados há uma table chamada "latests" e verifica se nessa table há de 30 dias ou mais de todas as moedas que a FrankFurter API fornece. Caso não haja essas informações, a API coleta os dados de 30 dias e salva dentro do banco de dados
##### O método HTTP GET e POST retornam a mesma coisa da API, apenas suas informações.
##### Após a criação da API e da rota para os dados da mesma, foi criado um rota padrão ("/") para mostrar o gráfico


#### Dicas de como utilizar:
##### Há um arquivo txt chamado "requirements.txt", nele estão todas as bibliotecas necessárias para o funcionamento do programa, após instalar essas bibliotecas vá ao terminal de comando e digite "flask run" enquanto estiver com o arquivo "api.py" aberto, ele executará esse aquivo e criará uma rota local para acessar
