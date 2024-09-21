from flask import Flask, render_template, request, redirect, url_for, flash
import oracledb

import webbrowser

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Credenciais do banco Oracle
username = "jkss30742"
password = "[REDACTED]"
dsn = "200.131.242.43:1521/IFNMGPDB"

def get_db_connection():
    return oracledb.connect(user=username, password=password, dsn=dsn)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/empresa')
def empresa():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Empresa')
    empresas = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('empresa.html', empresas=empresas)

@app.route('/add_empresa', methods=['POST'])
def add_empresa():
    if request.method == 'POST':
        registro = request.form['registro']
        nome = request.form['nome']
        
        # Validação do comprimento do registro
        if len(registro) > 7:
            flash("O registro não pode ter mais de 7 caracteres.")
            return redirect(url_for('empresa'))  
               
        # Validação do comprimento do nome
        if len(nome) > 50:
            flash("O nome não pode ter mais de 50 caracteres.")
            return redirect(url_for('empresa'))  
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO Empresa (registro, nome) VALUES (:registro, :nome)',
                           {'registro': registro, 'nome': nome})
            conn.commit()
            flash('Empresa adicionada com sucesso!')
        except oracledb.IntegrityError:
            flash('Erro: Registro já existe!')
        except Exception as e:
            flash('Erro: Dados inválidos!')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('empresa'))

@app.route('/update_empresa', methods=['POST'])
def update_empresa():
    if request.method == 'POST':
        registro = request.form['registro']
        nome = request.form['nome']
        
        # Validação do comprimento do nome
        if len(nome) > 50:
            flash("O nome não pode ter mais de 50 caracteres.")
            return redirect(url_for('empresa'))  
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE Empresa SET nome = :nome WHERE registro = :registro',
                       {'nome': nome, 'registro': registro})
        conn.commit()
        cursor.close()
        conn.close()

        flash('Empresa atualizada com sucesso!')
        return redirect(url_for('empresa'))

@app.route('/delete_empresa/<string:registro>', methods=['POST'])
def delete_empresa(registro):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Empresa WHERE registro = :registro', {'registro': registro})
    conn.commit()
    cursor.close()
    conn.close()

    flash('Empresa excluída com sucesso!')
    return redirect(url_for('empresa'))


# Tela CRUD para a tabela Colonia 
@app.route('/colonia')
def colonia():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Colonia')
    colonias = cursor.fetchall()

    # Carregar empresas
    cursor.execute('SELECT registro, nome FROM Empresa')
    empresas = cursor.fetchall()

    # Carregar jazidas
    cursor.execute('''
        SELECT ju.latitude, ju.longitude, 
               COALESCE(ju.nomeVale, ju.nomeMontanha, ju.nomePlanicie) AS nome_jazida,
               rc.regiao
        FROM JazidaUnobtanium ju
        LEFT JOIN Regiaocontrole rc ON (
            ju.nomeVale = rc.nome OR 
            ju.nomeMontanha = rc.nome OR 
            ju.nomePlanicie = rc.nome
        )
        ORDER BY ju.latitude, ju.longitude
    ''')
    jazidas = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('colonia.html', colonias=colonias, empresas=empresas, jazidas=jazidas)

@app.route('/add_colonia', methods=['POST'])
def add_colonia():
    if request.method == 'POST':
        nome = request.form['nome']
        pressurizada = request.form.get('pressurizada', '0')  # Captura como '0' caso não seja selecionado
        apelido = request.form['apelido']
        registroEmpresa = request.form['registroEmpresa']
        
         # Validação do comprimento do nome
        if len(nome) > 50:
            flash("O nome da colônia não pode ter mais de 50 caracteres.")
            return redirect(url_for('colonia')) 
        
         # Validação do comprimento do apelido
        if len(apelido) > 46:
            flash("O apelido não pode ter mais de 46 caracteres.")
            return redirect(url_for('colonia'))  

        # Pega a jazida selecionada, que contém latitude e longitude
        jazida = request.form['jazida']
        latitude, longitude = map(float, jazida.split(','))
        # latitude, longitude = jazida.split(',')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO Colonia (nome, pressurizada, apelido, registroEmpresa, latitude, longitude) VALUES (:nome, :pressurizada, :apelido, :registroEmpresa, :latitude, :longitude)',
                {'nome': nome, 'pressurizada': pressurizada, 'apelido': apelido, 'registroEmpresa': registroEmpresa, 'latitude': latitude, 'longitude': longitude}
            )
            conn.commit()
            flash('Colônia adicionada com sucesso!')
        except oracledb.IntegrityError:
            flash('Erro: Dados inválidos ou colônia já existe!')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('colonia'))

@app.route('/update_colonia', methods=['POST'])
def update_colonia():
    if request.method == 'POST':
        nome = request.form['nome']
        pressurizada = request.form.get('pressurizada', '0')  # Default to '0' if not checked
        apelido = request.form['apelido']
        registroEmpresa = request.form['registroEmpresa']
        
        # Validação do comprimento do apelido
        if len(apelido) > 46:
            flash("O apelido não pode ter mais de 46 caracteres.")
            return redirect(url_for('colonia'))  
        
        # Obter latitude e longitude a partir da jazida selecionada
        try:
            jazida = request.form['jazida']
            latitude, longitude = map(float, jazida.split(','))
        except (ValueError, KeyError):
            flash('Latitude e Longitude devem ser números válidos.')
            return redirect(url_for('colonia'))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE Colonia SET pressurizada = :pressurizada, apelido = :apelido, registroEmpresa = :registroEmpresa, latitude = :latitude, longitude = :longitude WHERE nome = :nome',
                       {'pressurizada': pressurizada, 'apelido': apelido, 'registroEmpresa': registroEmpresa, 'latitude': latitude, 'longitude': longitude, 'nome': nome})
        conn.commit()
        cursor.close()
        conn.close()

        flash('Colônia atualizada com sucesso!')
        return redirect(url_for('colonia'))

# Excluir uma colonia
@app.route('/delete_colonia/<string:nome>', methods=['POST'])
def delete_colonia(nome):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Colonia WHERE nome = :nome', {'nome': nome})
    conn.commit()
    cursor.close()
    conn.close()

    flash('Colônia excluída com sucesso!')
    return redirect(url_for('colonia'))


# Rotas para Conteiner
@app.route('/conteiner')
def conteiner():
    return render_template('conteiner.html')

@app.route('/deposito')
def deposito():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Deposito')
    depositos = cursor.fetchall()

    # Carregar colônias
    cursor.execute('SELECT * FROM Colonia')
    colonias = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('deposito.html', depositos=depositos, colonias=colonias)

@app.route('/add_deposito', methods=['POST'])
def add_deposito():
    cursor = None  # Inicializa cursor como None
    conn = None
    try:
        # Dados do formulário
        numeroserie = int(request.form['numeroserie'])
        nome = request.form['nome']
        sigla = request.form['sigla']
        tamanho = float(request.form['tamanho'])
        tipo = request.form['tipo']
        nomecolonia = request.form['nomecolonia']
        tipoconteiner = 'Deposito'  # Define o tipo de container
        
        if tamanho < 0:
            flash("O tamanho deve ser 0 ou maior.")
            return redirect(url_for('deposito'))

        # Validação do comprimento do nome
        if len(nome) > 46:
            flash("O nome não pode ter mais de 46 caracteres.")
            return redirect(url_for('deposito'))  
        
        # Validação do comprimento da sigla
        if len(sigla) > 10:
            flash("A sigla não pode ter mais de 10 caracteres.")
            return redirect(url_for('deposito'))  
        
        # Validação do comprimento do tipo
        if len(tipo) > 46:
            flash("O tipo não pode ter mais de 46 caracteres.")
            return redirect(url_for('deposito')) 
        
        # Conexão ao banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()

        # Inserir no ConteinerControle
        cursor.execute(
            'INSERT INTO ConteinerControle (numeroserie, tipoconteiner) VALUES (:numeroserie, :tipoconteiner)', 
            {'numeroserie': numeroserie, 'tipoconteiner': tipoconteiner}
        )

        # Inserir no Deposito
        cursor.execute(
            'INSERT INTO Deposito (numeroserie, nome, sigla, tamanho, tipo, nomecolonia) VALUES (:numeroserie, :nome, :sigla, :tamanho, :tipo, :nomecolonia)',
            {
                'numeroserie': numeroserie,
                'nome': nome,
                'sigla': sigla,
                'tamanho': tamanho,
                'tipo': tipo,
                'nomecolonia': nomecolonia
            }
        )

        # Commit das transações
        conn.commit()
        flash('Depósito adicionado com sucesso!')
    except oracledb.IntegrityError:
        flash('Erro: Dados inválidos ou depósito já existe!')
    except Exception as e:
        conn.rollback()  # Rollback em caso de erro
        flash(f'Erro ao adicionar depósito: {e}')
    finally:
        if cursor is not None:  # Verifica se cursor foi criado
            cursor.close()  # Fecha o cursor
        if conn is not None:  # Verifica se conn foi criado
            conn.close()  # Fecha a conexão

    return redirect(url_for('deposito'))

@app.route('/update_deposito', methods=['POST'])
def update_deposito():
    numeroserie = int(request.form['numeroserie'])
    nome = request.form['nome']
    sigla = request.form['sigla']
    tamanho = float(request.form['tamanho'])
    tipo = request.form['tipo']
    nomecolonia = request.form['nomecolonia']
    
    if tamanho < 0:
        flash("O tamanho deve ser 0 ou maior.")
        return redirect(url_for('deposito'))

    # Validação do comprimento do nome
    if len(nome) > 46:
        flash("O nome não pode ter mais de 46 caracteres.")
        return redirect(url_for('deposito'))  
    
    # Validação do comprimento de sigla
    if len(sigla) > 10:
        flash("A sigla não pode ter mais de 10 caracteres.")
        return redirect(url_for('deposito'))  
        
    # Validação do comprimento do tipo
    if len(tipo) > 46:
        flash("O tipo não pode ter mais de 46 caracteres.")
        return redirect(url_for('deposito')) 
        
    conn = get_db_connection()
    cursor = conn.cursor()  
    cursor.execute('''
            UPDATE Deposito 
            SET nome = :nome, sigla = :sigla, tamanho = :tamanho, 
                tipo = :tipo, nomecolonia = :nomecolonia 
            WHERE numeroserie = :numeroserie
        ''', {
            'nome': nome,
            'sigla': sigla,
            'tamanho': tamanho,
            'tipo': tipo,
            'nomecolonia': nomecolonia,
            'numeroserie': numeroserie
        })
    
    conn.commit()
    cursor.close()
    conn.close()
    
    flash('Depósito atualizado com sucesso!')
    return redirect(url_for('deposito'))

@app.route('/delete_deposito/<int:numeroserie>', methods=['POST'])
def delete_deposito(numeroserie):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM Deposito WHERE numeroserie = :numeroserie', {'numeroserie': numeroserie})
        conn.commit()
        flash('Depósito excluído com sucesso!')
    except Exception as e:
        conn.rollback()  # Rollback em caso de erro
        flash(f'Erro ao excluir depósito: {e}')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('deposito'))


# Rotas para Residência
@app.route('/residencia')
def residencia():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Residencia')
    residencias = cursor.fetchall()
    
    cursor.execute('SELECT * FROM Colonia')
    colonias = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('residencia.html', residencias=residencias, colonias=colonias)

@app.route('/add_residencia', methods=['POST'])
def add_residencia():
    cursor = None  # Inicializa cursor como None
    conn = None
    try:
        # Dados do formulário
        numeroserie = int(request.form['numeroserie'])
        nome = request.form['nome']
        sigla = request.form['sigla']
        tamanho = float(request.form['tamanho'])
        qtdcama = int(request.form['qtdcama'])
        qtdbanheiro = int(request.form['qtdbanheiro'])
        nomecolonia = request.form['nomecolonia']
        tipoconteiner = 'Residencia'  # Define o tipo de container
        
        if tamanho < 0:
            flash("O tamanho deve ser 0 ou maior.")
            return redirect(url_for('Residencia'))
        
        if qtdcama < 0:
            flash("Qtdcama deve ser 0 ou maior.")
            return redirect(url_for('Residencia'))
        
        if qtdbanheiro < 0:
            flash("Qtdbanheiro deve ser 0 ou maior.")
            return redirect(url_for('Residencia'))

        # Validação do comprimento do nome
        if len(nome) > 46:
            flash("O nome não pode ter mais de 46 caracteres.")
            return redirect(url_for('residencia'))  
    
        # Validação do comprimento de sigla
        if len(sigla) > 10:
            flash("A sigla não pode ter mais de 10 caracteres.")
            return redirect(url_for('residencia'))  
        
        # Conexão ao banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()

        # Inserir no ConteinerControle
        cursor.execute(
            'INSERT INTO ConteinerControle (numeroserie, tipoconteiner) VALUES (:numeroserie, :tipoconteiner)', 
            {'numeroserie': numeroserie, 'tipoconteiner': tipoconteiner}
        )

        # Inserir na Residencia
        cursor.execute(
            'INSERT INTO Residencia (numeroserie, nome, sigla, tamanho, qtdcama, qtdbanheiro, nomecolonia) VALUES (:numeroserie, :nome, :sigla, :tamanho, :qtdcama, :qtdbanheiro, :nomecolonia)',
            {
                'numeroserie': numeroserie,
                'nome': nome,
                'sigla': sigla,
                'tamanho': tamanho,
                'qtdcama': qtdcama,
                'qtdbanheiro': qtdbanheiro,
                'nomecolonia': nomecolonia
            }
        )

        # Commit das transações
        conn.commit()
        flash('Residência adicionada com sucesso!')
    except oracledb.IntegrityError:
        flash('Erro: Dados inválidos ou residência já existe!')
    except Exception as e:
        conn.rollback()  # Rollback em caso de erro
        flash(f'Erro ao adicionar residência: {e}')
    finally:
        if cursor is not None:  # Verifica se cursor foi criado
            cursor.close()  # Fecha o cursor
        if conn is not None:  # Verifica se conn foi criado
            conn.close()  # Fecha a conexão

    return redirect(url_for('residencia'))

@app.route('/update_residencia', methods=['POST'])
def update_residencia():
    try:
        numeroserie = int(request.form['numeroserie'])
        nome = request.form['nome']
        sigla = request.form['sigla']
        tamanho = float(request.form['tamanho'])  # Converte para float
        qtdcama = int(request.form['qtdcama'])     # Converte para int
        qtdbanheiro = int(request.form['qtdbanheiro'])  # Converte para int
        nomecolonia = request.form['nomecolonia']
        
        if tamanho < 0:
            flash("O tamanho deve ser 0 ou maior.")
            return redirect(url_for('Residencia'))
        
        if qtdcama < 0:
            flash("Qtdcama deve ser 0 ou maior.")
            return redirect(url_for('Residencia'))
        
        if qtdbanheiro < 0:
            flash("Qtdbanheiro deve ser 0 ou maior.")
            return redirect(url_for('Residencia'))
        
        # Validação do comprimento do nome
        if len(nome) > 46:
            flash("O nome não pode ter mais de 46 caracteres.")
            return redirect(url_for('residencia'))  
    
        # Validação do comprimento de sigla
        if len(sigla) > 10:
            flash("A sigla não pode ter mais de 10 caracteres.")
            return redirect(url_for('residencia'))  

        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE Residencia 
            SET nome = :nome, sigla = :sigla, tamanho = :tamanho, 
                qtdcama = :qtdcama, qtdbanheiro = :qtdbanheiro, nomecolonia = :nomecolonia 
            WHERE numeroserie = :numeroserie
        ''', {
            'nome': nome,
            'sigla': sigla,
            'tamanho': tamanho,
            'qtdcama': qtdcama,
            'qtdbanheiro': qtdbanheiro,
            'nomecolonia': nomecolonia,
            'numeroserie': numeroserie
        })
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Residência atualizada com sucesso!')
        return redirect(url_for('residencia'))

    except ValueError:
        flash('Erro: um ou mais campos numéricos estão inválidos.')
        return redirect(url_for('residencia'))
    except Exception as e:
        flash(f'Ocorreu um erro: {str(e)}')
        return redirect(url_for('residencia'))

@app.route('/delete_residencia/<int:numeroserie>', methods=['POST'])
def delete_residencia(numeroserie):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM Residencia WHERE numeroserie = :numeroserie', {'numeroserie': numeroserie})
        conn.commit()
        flash('Residência excluída com sucesso!')
    except Exception as e:
        conn.rollback()  # Rollback em caso de erro
        flash(f'Erro ao excluir residência: {e}')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('residencia'))  # Redireciona para a página de residências

# Rotas para Laboratório
@app.route('/laboratorio')
def laboratorio():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Laboratorio')
    laboratorios = cursor.fetchall()
    
    cursor.execute('SELECT * FROM Colonia')
    colonias = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('laboratorio.html', laboratorios=laboratorios, colonias=colonias)

@app.route('/add_laboratorio', methods=['POST'])
def add_laboratorio():
    cursor = None  # Inicializa cursor como None
    conn = None
    try:
        # Dados do formulário
        numeroserie = int(request.form['numeroserie'])
        nome = request.form['nome']
        sigla = request.form['sigla']
        tamanho = float(request.form['tamanho'])  # Tente converter para float
        finalidade = request.form['finalidade']
        nomecolonia = request.form['nomecolonia']
        tipoconteiner = 'Laboratorio'  # Define o tipo de container
        
        if tamanho < 0:
            flash("O tamanho deve ser 0 ou maior.")
            return redirect(url_for('Laboratorio'))
        
        # Validação do comprimento do nome
        if len(nome) > 46:
            flash("O nome não pode ter mais de 46 caracteres.")
            return redirect(url_for('laboratorio'))  
    
        # Validação do comprimento de sigla
        if len(sigla) > 10:
            flash("A sigla não pode ter mais de 10 caracteres.")
            return redirect(url_for('laboratorio'))  
        
        # Validação do comprimento do tipo
        if len(finalidade) > 46:
            flash("A finalidade não pode ter mais de 46 caracteres.")
            return redirect(url_for('laboratorio')) 

        # Conexão ao banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()

        # Inserir no ConteinerControle
        cursor.execute(
            'INSERT INTO ConteinerControle (numeroserie, tipoconteiner) VALUES (:numeroserie, :tipoconteiner)', 
            {'numeroserie': numeroserie, 'tipoconteiner': tipoconteiner}
        )

        # Inserir no Laboratorio
        cursor.execute(
            'INSERT INTO Laboratorio (numeroserie, nome, sigla, tamanho, finalidade, nomecolonia) VALUES (:numeroserie, :nome, :sigla, :tamanho, :finalidade, :nomecolonia)',
            {
                'numeroserie': numeroserie,
                'nome': nome,
                'sigla': sigla,
                'tamanho': tamanho,
                'finalidade': finalidade,
                'nomecolonia': nomecolonia
            }
        )

        # Commit das transações
        conn.commit()
        flash('Laboratório adicionado com sucesso!')
    except oracledb.IntegrityError:
        flash('Erro: Dados inválidos ou laboratório já existe!')
    except Exception as e:
        conn.rollback()  # Rollback em caso de erro
        flash(f'Erro ao adicionar laboratório: {e}')
    finally:
        if cursor is not None:  # Verifica se cursor foi criado
            cursor.close()  # Fecha o cursor
        if conn is not None:  # Verifica se conn foi criado
            conn.close()  # Fecha a conexão

    return redirect(url_for('laboratorio'))

@app.route('/update_laboratorio', methods=['POST'])
def update_laboratorio():
    numeroserie = int(request.form['numeroserie'])
    nome = request.form['nome']
    sigla = request.form['sigla']
    tamanho = float(request.form['tamanho'])
    finalidade = request.form['finalidade']
    nomecolonia = request.form['nomecolonia']
    
    if tamanho < 0:
        flash("O tamanho deve ser 0 ou maior.")
        return redirect(url_for('laboratorio'))
    
    # Validação do comprimento do nome
    if len(nome) > 46:
        flash("O nome não pode ter mais de 46 caracteres.")
        return redirect(url_for('laboratorio'))  
    
    # Validação do comprimento de sigla
    if len(sigla) > 10:
        flash("A sigla não pode ter mais de 10 caracteres.")
        return redirect(url_for('laboratorio'))  
        
    # Validação do comprimento do tipo
    if len(finalidade) > 46:
        flash("A finalidade não pode ter mais de 46 caracteres.")
        return redirect(url_for('laboratorio')) 

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
            UPDATE Laboratorio 
            SET nome = :nome, sigla = :sigla, tamanho = :tamanho, 
                finalidade = :finalidade, nomecolonia = :nomecolonia 
            WHERE numeroserie = :numeroserie
        ''', {
            'nome': nome,
            'sigla': sigla,
            'tamanho': tamanho,
            'finalidade': finalidade,
            'nomecolonia': nomecolonia,
            'numeroserie': numeroserie
        })
    
    conn.commit()
    cursor.close()
    conn.close()
    
    flash('Laboratório atualizado com sucesso!')
    return redirect(url_for('laboratorio'))

@app.route('/delete_laboratorio/<int:numeroserie>', methods=['POST'])
def delete_laboratorio(numeroserie):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM Laboratorio WHERE numeroserie = :numeroserie', {'numeroserie': numeroserie})
        conn.commit()
        flash('Laboratório excluído com sucesso!')
    except Exception as e:
        conn.rollback()  # Rollback em caso de erro
        flash(f'Erro ao excluir laboratório: {e}')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('laboratorio'))  # Redireciona para a página de laboratórios


# Rotas para Relatorio Colonia
@app.route('/relatorio_colonias')#sem post porque eu sou o bixo eu sou o cara eu sou o maioral
def relatorio_colonias():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        c.nome colonia_nome,
        c.pressurizada,
        c.apelido,
        d.nome deposito_nome,
        r.nome residencia_nome,
        l.nome laboratorio_nome,
        h.nome humano_nome,

        c.latitude,
        c.longitude,
        m.nome maquinario_nome,
        m.tipoMaquina,
        m.potencia,
        m.pesoOperacional,
        
        j.reserva,
        j.nomeVale,
        j.nomeMontanha,
        j.nomePlanicie,
        
        h.mascara,
        c.pressurizada,
        
        e.nome equipamento_nome,
        e.consumoEnergetico consumo,
        e.utilidade
        FROM 
            Colonia c
        LEFT JOIN 
            Deposito d ON c.nome = d.nomecolonia
        LEFT JOIN 
            Residencia r ON c.nome = r.nomecolonia
        LEFT JOIN 
            Laboratorio l ON c.nome = l.nomecolonia
        LEFT JOIN 
            Humano h ON c.nome = h.nomecolonia
        LEFT JOIN 
            Pesquisa p ON l.numeroserie = p.numeroserielab
        LEFT JOIN 
            Equipamento e ON p.nome = e.nomePesquisa
        LEFT JOIN 
            JazidaUnobtanium j ON c.latitude = j.latitude AND c.longitude = j.longitude AND j.estado = '1'
        LEFT JOIN 
            Maquinario m ON j.latitude = m.latitudejazida AND j.longitude = m.longitudejazida   
        ORDER BY 
        c.nome, d.nome, r.nome, l.nome, h.nome, e.nome, m.nome
    """)
    # Organizando os dados em uma estrutura mais legível
    relatorio = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('relatorio_colonias.html', relatorio=relatorio)

# URL que você deseja abrir
url = 'http://127.0.0.1:5000'

# Abre a URL no navegador padrão
webbrowser.open(url)

if __name__ == '__main__':
    app.run(debug=True)
