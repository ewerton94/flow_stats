# Flow: módulo de estudo em análise de frequência

Este é um aplicativo criado para facilitar estudos em hidrologia e estatístiva, criado pelo time de desenvolvimento Flow, do Centro de Tecnologia da Universidade Federal de Alagoas (CTEC/UFAL).

### 1. Getting started

* Pré-requisitos:

```powershell

django
django-modeltranslation
pandas
scipy
bs4
psycopg2
furl
plotly
xlrd
xlwt
lmoments3


```

* Procedimentos de instalação:

1. Instale e configure o postgresql (crie um banco de dados com nome: flow_stats;
2. Obtenha este diretório em seu computador (clone);
3. Instale os pré-requisitos necessários;
* Você pode instalar executando o arquivo install_requeriments.bat no windows ou executando no terminal do linux o seguinte comando:

```terminal
python -m pip install -r requirements.txt
```
4. No arquivo flow_stats/urls.py, comente a linha 26:
```python
urlpatterns += i18n_patterns(
    url(r'^admin/', admin.site.urls),
    #url(r'^stats/', include('stats.urls')),
)
```
5. Abra a linha de comando ou terminal na pasta do projeto no seu computador e execute o comando migrate (obs.: lembre-se de instalar o postgresql e criar um banco de dados com o nome flow_stats):
```powershell
python manage.py migrate

```
6. Descomente as linhas comentadas no ítem 4.
7. Se tudo ocorrer bem, já é possível executar o projeto:
```powershell
python manage.py runserver
```

8. Acesse http://localhost:8000/en-us/stats/study/