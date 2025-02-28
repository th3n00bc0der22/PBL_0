import os
import json
import copy
from abc import ABC, abstractmethod

# Variáveis globais e listas de controle
totalcompras = []
totalcarrinho = []
totallistadesejos = []
listaPrd = []       # Lista de produtos (objetos da classe Produtos)
listaUsr = []       # Lista de usuários (objetos da classe Usuarios)
logado = False
usrlogado = ""      # Usuário atualmente logado

categorias = [
    "Eletrônicos",
    "Moda e Acessórios",
    "Casa e Decoração",
    "Beleza e Saúde",
    "Alimentos e Bebidas",
    "Esportes e Lazer",
    "Livros, Papelaria e Colecionáveis",
    "Automotivo",
    "Bebês e Crianças",
    "Serviços e Assinaturas",
]

# =============================================================================
# Classes
# =============================================================================
#obs: marketplace era pra ser um singleton mas nao pude implementar
class Marketplace():
    def __init__(self):
        pass

    def menu_ini(self, logado):
        pass

    def tela_ini(self, usr):
        pass

    def consultar_desejos(self, listadesejos):
        for prd in listaPrd:
            for desejo in usrlogado.listadesejos:
                # Atenção: aqui a referência "usrlogado.listadesejo" provavelmente deveria ser "desejo"
                if desejo.nome.contains(prd.nome):
                    print(f"O {prd.nome} é semelhante ao {desejo.nome}, contido na sua lista de desejos")
        pass

    def carrinho(self):
        if usrlogado.carrinho:
            print(f"O seu carrinho contém: {usrlogado.carrinho}")
        pass

    def salvadados(self):
        dados["produtos"] = [produto.salvar() for produto in listaPrd]
        dados["usuarios"] = [usuario.salvar() for usuario in listaUsr]
        with open("D:/curso de POO em python/PBL0/dadosMkp.json", "w") as arquivo:
            json.dump(dados, arquivo, indent=4)
            print("Dados salvos.")


class Usuarios():
    def __init__(self, nome, email, senha, regiao, saldo, tipousuar, codigo, compras, carrinho, listadesejos):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.regiao = regiao
        self.saldo = saldo
        self.tipousuar = tipousuar
        self.codigo = codigo
        self.compras = compras
        self.carrinho = carrinho
        self.listadesejos = listadesejos

    def comprar(self, compras):
        pass

    def definir(self):
        pass

    def vender(self):
        pass

    def salvar(self):
        return {
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "regiao": self.regiao,
            "saldo": self.saldo,
            "tipousuar": self.tipousuar,
            "codigo": self.codigo,
            "compras": [prd.salvar() for prd in self.compras],
            "carrinho": [prd.salvar() for prd in self.carrinho],
            "listadesejos": [prd.salvar() for prd in self.listadesejos]
        }

    def cadastrarproduto(self):
        for i in range(len(categorias)):
            print(categorias[i], i+1)
            print("-" * 30)
        print(" ")
        numcategoria = input("Selecione a categoria do produto: ")
        numcategoria = int(numcategoria) - 1
        os.system("cls")
        categoria = categorias[numcategoria] if categorias[numcategoria] else print("Desculpe, não entendemos o que quis dizer")
        nome = input("Qual o nome do produto que será adicionado? ")
        estado = input("Qual o estado de conservação do produto? ")
        valor = input("Qual o valor cobrado? ")
        loja = input("Qual o nome da sua loja? ")
        qtd = input("Qual a quantidade de produtos ofertados? ")
        prd = Produtos(categoria, nome, estado, valor, loja, qtd)
        listaPrd.append(prd)
        dados["produtos"].append(prd.salvar())
        with open("D:/curso de POO em python/PBL0/dadosMkp.json", "w") as arquivo:
            json.dump(dados, arquivo, indent=4)
            print("dados salvos")


class Produtos:
    def __init__(self, categoria, nome, estado, valor, loja, qtd):
        self.categoria = categoria
        self.nome = nome
        self.estado = estado
        self.valor = valor
        self.loja = loja
        self.qtd = qtd

    def comprar(self, qtdcompra):
        copia = copy.deepcopy(self)
        copia.qtd = qtdcompra
        self.qtd -= int(qtdcompra)  # Atualiza o estoque original
        return copia

    def salvar(self):
        return {
            "categoria": self.categoria,
            "nome": self.nome,
            "estado": self.estado,
            "valor": self.valor,
            "loja": self.loja,
            "qtd": self.qtd
        }

# =============================================================================
# Carregamento dos Dados do Arquivo JSON
# =============================================================================

try:
    with open("D:/curso de POO em python/PBL0/dadosMkp.json", "r") as arquivo:
        dados = json.load(arquivo)
        # Carregar usuários e converter listas de produtos para objetos
        for usuario in dados["usuarios"]:
            compras = [Produtos(
                categoria=prd["categoria"],
                nome=prd["nome"],
                estado=prd["estado"],
                valor=prd["valor"],
                loja=prd["loja"],
                qtd=prd["qtd"]
            ) for prd in usuario["compras"]]
            carrinho = [Produtos(
                categoria=prd["categoria"],
                nome=prd["nome"],
                estado=prd["estado"],
                valor=prd["valor"],
                loja=prd["loja"],
                qtd=prd["qtd"]
            ) for prd in usuario["carrinho"]]
            listadesejos = [Produtos(
                categoria=prd["categoria"],
                nome=prd["nome"],
                estado=prd["estado"],
                valor=prd["valor"],
                loja=prd["loja"],
                qtd=prd["qtd"]
            ) for prd in usuario["listadesejos"]]
            usr = Usuarios(
                nome=usuario["nome"],
                email=usuario["email"],
                senha=usuario["senha"],
                regiao=usuario["regiao"],
                saldo=usuario["saldo"],
                tipousuar=usuario["tipousuar"],
                codigo=usuario["codigo"],
                compras=compras,
                carrinho=carrinho,
                listadesejos=listadesejos
            )
           
            listaUsr.append(usr)
        # Carregar produtos
        for produto in dados["produtos"]:
            prd = Produtos(
                categoria=produto["categoria"],
                nome=produto["nome"],
                estado=produto["estado"],
                valor=produto["valor"],
                loja=produto["loja"],
                qtd=produto["qtd"]
            )
            listaPrd.append(prd)
except:
    print("Dados não encontrados.")
    print("Não existem produtos ou usuários cadastrados.")

# =============================================================================
# Processo de Autenticação (Login/Registro)
# =============================================================================

while True:
    print("Olá usuário!")
    registro = input("Faça login ou se registre na nossa plataforma: ").strip().lower()

    if "log" in registro:
        os.system("cls")
        print("O usuário quer fazer login")
        print("Informe o seu Login:")
        email = input("Digite o seu email: ")
        for usr in listaUsr:
            if usr.email == email:
                while True:
                    senha = input(f"{usr.nome}, digite agora a sua senha: ")
                    if usr.senha == senha:
                        logado = True
                        usrlogado = usr
                        print("Login concluído!")
                        print(usrlogado.nome)
                        break
                    else:
                        print("Senha incorreta!")
        if logado:
            print("Login concluído")
            print(usrlogado.nome)
            break
        else:
            os.system("cls")
            print("=" * 50)
            print("Login não efetuado, email não encontrado.")
            print("=" * 50)

    elif "reg" in registro:
        print("O usuário quer fazer registro")
        nome = input("Informe o seu nome: ")
        email = input("Informe o seu email: ")
        senha = input("Crie uma senha: ")
        regiao = input("Informe a sua região: ")
        saldo = input("Informe o seu saldo: ")
        tipousuar = input("Você quer criar uma conta de cliente ou vendedor? ")
        codigo = input("Informe o seu CPF ") if tipousuar == "cliente" else input("Informe o seu CNPJ ")
        compras = []       # Inicialmente vazio
        carrinho = []
        listadesejos = []
        usr = Usuarios(nome, email, senha, regiao, saldo, tipousuar, codigo, compras, carrinho, listadesejos)
        listaUsr.append(usr)
        dados["usuarios"].append(usr.salvar())
        with open("D:/curso de POO em python/PBL0/dadosMkp.json", "w") as arquivo:
            json.dump(dados, arquivo, indent=4)
        os.system("cls")
    else:
        os.system("cls")
        print("Desculpe. Não entendemos o que você quis dizer... Pode por favor tentar novamente?")
        print("")

# =============================================================================
# Função Marketplace e Fluxo de Compra
# =============================================================================



buscalista = []
os.system("cls")
def marketplace():
    buscalista.clear
    if usrlogado.listadesejos:
        for desejo in usrlogado.listadesejos:
        # Atenção: aqui a referência "usrlogado.listadesejo" provavelmente deveria ser "desejo"
            if desejo.qtd>0:
                print(f"Nós temos, em nosso estoque o produto que você demonstrou interesse: {desejo.nome}, com {desejo.qtd} exemplar(es)")
            elif desejo.qtd==0:
                print(f"Nós normalmente vendemos o {desejo.nome} que você demonstrou interesse, mas no momento o estoque é de 0 unidades :(")
    print("Olá! O que deseja?")
    rota = input("Pesquisar produtos || Consultar carrinho || cadastrar produtos || ").strip().lower()
    print(rota)

    if "cad" in rota:
        print("=" * 50)
        print(" " * 15, "produtos:")
        print("=" * 50)
        usrlogado.cadastrarproduto()

    elif "produt" in rota:
        print("=" * 50)
        print(" " * 15, "Produtos:")
        print("=" * 50)
        print("")
        for i in range(len(categorias)):
            print(categorias[i], i + 1)
            print("-" * 30)
        print(" ")
        print("pressione enter para voltar")
        try:
            numcategoria = input("Selecione o número da categoria: ")
            numcategoria = int(numcategoria) - 1
            os.system("cls")
            print(f"Você buscou por produtos da categoria: {categorias[numcategoria]}")
            print("=" * 30)
            for prd in listaPrd:
                if categorias[numcategoria] == prd.categoria:
                    buscalista.append(prd)
            for i in range(len(buscalista)):
                print(buscalista[i].nome, i + 1)
            print("Envie qualquer coisa diferente das opções acima para sair.")
            try:
                prdescolhido = input("Escolha seu produto: ")
                prdescolhido = int(prdescolhido) - 1
                if buscalista[prdescolhido].nome:
                    prddesejado = buscalista[prdescolhido]
                    print(prddesejado.nome, "R$: ", prddesejado.valor, prddesejado.qtd)
                    if prddesejado.qtd == 0:
                        while True:    
                            print("Produto esgotado. Adicionar à lista de desejos?")
                            produtovazio = input("Digite 'adicionar' para incluir na lista ou 'sair': ").strip().lower()
                            if "sair" in produtovazio:
                                print("sair")
                                break
                            if "adicionar" in produtovazio:
                                print("add a lista de desejos")
                                usrlogado.listadesejos.append(prddesejado)
                                for usuario in dados["usuarios"]:
                                    if usuario["email"] == usrlogado.email:
                                        usuario["listadesejos"].append(prddesejado.salvar())
                                        break

                                with open("D:/curso de POO em python/PBL0/dadosMkp.json", "w") as arquivo:
                                    json.dump(dados, arquivo, indent=4)
                                    print("dados salvos")
                                    buscalista.clear
                                break
                            else:
                                print("Desculpe, não conseguimos entender o que voce quis dizer")
                    else:
                        opcaoproduto = input("Comprar?  Adicionar ao carrinho? ").strip().lower()

                
                if "comp" in opcaoproduto:
                    while True:
                        qtdcompra = input(f"Quantos {prddesejado.nome}? ")
                        if int(prddesejado.qtd) < int(qtdcompra):
                            print("Quantidade insuficiente.")
                        print(f"{usrlogado.nome}, {qtdcompra} undidade(s) de: {prddesejado.nome} foram comprada(s)!")
                        prddesejado = prddesejado.comprar(qtdcompra)
                        usrlogado.compras.append(prddesejado)
                        dados["produtos"] = [produto.salvar() for produto in listaPrd]
                        dados["usuarios"] = [usuario.salvar() for usuario in listaUsr]
                        with open("D:/curso de POO em python/PBL0/dadosMkp.json", "w") as arquivo:
                            json.dump(dados, arquivo, indent=4)
                            buscalista.clear
                            print("Comprado!")
                        break   
                elif "carrin" in opcaoproduto:
                    usrlogado.carrinho.append(prddesejado)
                    for usuario in dados["usuarios"]:
                        if usuario["email"] == usrlogado.email:
                            usuario["carrinho"].append(prddesejado.salvar())

                    with open("D:/curso de POO em python/PBL0/dadosMkp.json", "w") as arquivo:
                        json.dump(dados, arquivo, indent=4)
                        print("dados salvos")
                    print(usrlogado.nome, prddesejado.nome, "adicionado ao carrinho!")
                    buscalista.clear
                    return
                else:
                    print("Desculpe. Não conseguimos entender o que você quis dizer...")     
            except:
                os.system("cls")
                print("Entrada não reconhecida, voltando ao menu anterior")
                        
        except:
            os.system("cls") 
            print("voltando ao menu anterior")
                   

    elif "carr" in rota:
        if usrlogado.carrinho:
            for prd in usrlogado.carrinho:
                print(f"{prd.nome} | Preço: {prd.valor} | Quantidade: {prd.qtd}")
        else:
            print("Seu carrinho está vazio.")
        if acaocarrinho:
            print("saindo")
        acaocarrinho = input("digite enter para sair")

    elif "carrin" not in rota or "cad"not in rota or "comp" not in rota :
        os.system("cls") 
        print("Opção não reconhecida. Retornando ao menu.")

while logado:
    marketplace()
