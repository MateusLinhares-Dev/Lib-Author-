from flask import Flask, flash, redirect, request, url_for, render_template, get_flashed_messages
import pandas as pd 
import sqlite3


# 1- construir aplicação flask em que aceita upload de arquivo csv
app = Flask(__name__)
app.secret_key = 'lib_to_archive'
#aqui configuramos a persistência da mensagem em que retorno
app.permanent_session_lifetime = 1

@app.route('/')
def index():
    mensagens_flash = get_flashed_messages()
    return render_template('index.html', mensagens_flash=mensagens_flash)

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    #verifica se o arquivo não foi enviado
    if 'csv_file' not in request.files:
        flash('No file')
        return redirect(request.url)

    try:
        csv_file = request.files['csv_file']
    except:
        print("Error 404")

    #Verifica se foi selecionado o campo
    if csv_file.filename =='':
        flash('Nenhum arquivo Selecionado')
        return redirect(request.url)

    if csv_file:
        df = pd.read_csv(csv_file)
        if 'names' not in df.columns and 'nomes' not in df.columns:
            flash('O campo Nome ou Name, não foi encontrado no arquivo')
            return redirect(request.url)
        names = df['nomes'] if 'nomes' in df.columns else df['names']

        #salvar os nomes do banco de dados
        save_to_database(names)

        flash('Processamento concluido com sucesso.')
        return redirect(url_for('index'))
    
def save_to_database(names):
    connector = sqlite3.connect('lib.db')
    cursor = connector.cursor()

    for name in names:
        cursor.execute('SELECT NAME FROM author WHERE NAME = ?', (name,))
        nomes = cursor.fetchall()

        if nomes:
            flash(f'O nome {name} Já foi registrado')
            
        else:
                cursor.execute('insert into author (NAME) VALUES (?)', (name,))
    
    connector.commit()
    connector.close()




if __name__  == '__main__':
    app.run(debug=True)
    