<h1 align="center"> Finance </h1>

<p align="center">
  O projeto "Finance" é uma aplicação desenvolvida utilizando o framework Django, que tem como objetivo fornecer uma solução para gestão financeira pessoal. O sistema permite que os usuários gerenciem suas finanças, controlando despesas, receitas e orçamentos.
</p>

<p align="center">
  <a href="#-tecnologias">Tecnologias</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-projeto">Projeto</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-layout">Layout</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-instalação">Instalação</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#memo-licença">Licença</a>
</p>

<p align="center">
  <img alt="License" src="https://img.shields.io/static/v1?label=license&message=MIT&color=49AA26&labelColor=000000">
</p>

<br>

## Página inicial
<p>
  Controle de orçamentos: O sistema permite que os usuários estabeleçam orçamentos mensais ou semanais para categorias específicas de despesas, auxiliando-os a manter um controle mais efetivo dos gastos e a identificar onde podem economizar.
</p>
<p align="center">
  <img alt="Página inicial" src="./media/home.png" width="100%">
</p>

## Contas
<p>
  Registro de despesas e receitas: Os usuários podem adicionar, editar e excluir despesas e receitas em categorias definidas, como alimentação, moradia, transporte, salário, entre outras. Cada registro pode conter informações como valor, dados, descrição e categoria.
</p>
<p align="center">
  <img alt="Página de cadastro e exibição das contas bancárias cadastradas" src="./media/contas.png" width="100%">
</p>

## Relatórios
<p>
  Relatórios e gráficos: O projeto oferece recursos de geração de relatórios e gráficos para visualizar as despesas e receitas ao longo do tempo. Essas visualizações podem ajudar os usuários a analisar seus hábitos financeiros e identificar padrões de gastos.
</p>
<p align="center">
  <img alt="Página de exibição das contas" src="./media/relatorios.png" width="100%">
</p>

## 🚀 Tecnologias

Esse projeto foi desenvolvido com as seguintes tecnologias:

- HTML, CSS
- Python, Django, Pytest
- Git, figma

## 💻 Projeto
O projeto "Finance" foi desenvolvido com foco na simplicidade, usabilidade e segurança. Ele oferece uma solução prática para que os usuários possam acompanhar suas finanças de forma organizada e eficiente. 

## 🔖 Layout

Você pode visualizar o layout do projeto através [DESSE LINK](https://www.figma.com/file/ymc6wEkOQQtyd4eRBa7ZJ6/psw-7.0-(Copy)?type=design&node-id=0-1&mode=design&t=4LcxuA9SDSoi3RTa-0). É necessário ter conta no [Figma](https://figma.com) para acessá-lo.

## ⬇️ Instalação
1. Clone o projeto
    ```bash
    git clone https://github.com/Alan-Gomes1/Finance.git
    ```

2. Crie um ambiente virtual
    ```bash
    python -m venv venv
    ```

3. Agora ative o ambiente
    ```bash
    source/venv/bin/activate
    ```

4. Instale as dependências
    ```bash
    pip install -r requirements.txt
    ```

5. Se você estiver utilizando linux ou wsl é necessário instalar a dependência `wkhtmltopdf` para a geração de relatórios em pdf
    ```bash
    sudo apt-get install wkhtmltopdf
    ```

6. Gere as migracões
    ```bash
    python manage.py migrate
    ```

7. Finalmente rode o projeto
    ```bash
    python manage.py runserver
    ```

## :memo: Licença

Esse projeto está sob a licença MIT.