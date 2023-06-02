
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import os, datetime
from flask_sqlalchemy import SQLAlchemy

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_frete(frete_id):
    conn = get_db_connection()
    frete = conn.execute('SELECT * FROM fretes WHERE id = ?',
                        (frete_id,)).fetchone()
    conn.close()
    if frete is None:
        abort(404)
    return frete

def get_expense(expense_id):
    conn = get_db_connection()
    expense = conn.execute('SELECT * FROM despesas WHERE id = ?',
                        (expense_id,)).fetchone()
    conn.close()
    if expense is None:
        abort(404)
    return expense

app = Flask('__name__')
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    conn = get_db_connection()
    fretes = conn.execute('SELECT * FROM fretes').fetchall()
    conn.close()
    return render_template('index.html', fretes=fretes)

@app.route('/expenses')
def expenses():
    conn = get_db_connection()
    expenses = conn.execute('SELECT * FROM despesas').fetchall()
    conn.close()
    return render_template('expenses.html', expenses=expenses)

@app.route('/report')
def report():
    d = datetime.date.today()
    month = f"{d:%m}"
    print(month)
    conn = get_db_connection()
    expenses = conn.execute('SELECT * FROM despesas where execution_date LIKE "_____'+month+'%"').fetchall()
    soma = conn.execute('SELECT SUM(value) FROM despesas where execution_date LIKE "_____'+month+'%"').fetchall()
    fretes = conn.execute('SELECT * FROM fretes where execution_date LIKE "_____'+month+'%"').fetchall()
    somafrete = conn.execute('SELECT SUM(value) FROM fretes where execution_date LIKE "_____'+month+'%"').fetchall()
    conn.close()
    return render_template('report.html', expenses=expenses, soma=soma, fretes=fretes, somafrete=somafrete)

@app.route('/<int:frete_id>')
def frete(frete_id):
    frete = get_frete(frete_id)
    return render_template('frete.html', frete=frete)

@app.route('/expense/<int:expense_id>')
def expense(expense_id):
    expense = get_expense(expense_id)
    return render_template('expense.html', expense=expense)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        client= request.form['client']
        destination = request.form['destination']
        value= request.form['value']
        execution_date = request.form['execution_date']

        if not client:
            flash('Favor preencher o nome do cliente!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO fretes (client, destination, value, execution_date) VALUES (?, ?, ?, ?)',
                         (client, destination, value, execution_date))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/runReport', methods=('GET', 'POST'))
def runReport():
    if request.method == 'POST':
        client= request.form['client']
        destination = request.form['destination']
        value= request.form['value']
        execution_date = request.form['execution_date']

        if not client:
            flash('Favor preencher o nome do cliente!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO fretes (client, destination, value, execution_date) VALUES (?, ?, ?, ?)',
                         (client, destination, value, execution_date))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('report.html')

@app.route('/expenseCreate', methods=('GET', 'POST'))
def expenseCreate():
    if request.method == 'POST':
        client= request.form['client']
        category = request.form['category']
        value= request.form['value']
        execution_date = request.form['execution_date']

        if not client:
            flash('Favor preencher o nome do cliente!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO despesas (client, category, value, execution_date) VALUES (?, ?, ?, ?)',
                         (client, category, value, execution_date))
            conn.commit()
            conn.close()
            return redirect(url_for('expenses'))

    return render_template('expenseCreate.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    frete = get_frete(id)

    if request.method == 'POST':
        client= request.form['client']
        destination = request.form['destination']
        value= request.form['value']
        execution_date = request.form['execution_date']

        if not client:
            flash('Favor preencher o nome do cliente!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE fretes SET client = ?, destination = ?, value = ?, execution_date = ?'
                         ' WHERE id = ?',
                         (client, destination, value, execution_date, id) )
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', frete=frete)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    frete = get_frete(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM fretes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" foi removido com sucesso!'.format(frete['client']))
    return redirect(url_for('index'))

@app.route('/expense/<int:id>/delete', methods=('POST',))
def deleteExpense(id):
    expense = get_expense(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM despesas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" de "{}" foi removido com sucesso!'.format(expense['category'],expense['client']))
    return redirect(url_for('expenses'))

@app.route('/expense/<int:id>/edit', methods=('GET', 'POST'))
def expenseEdit(id):
    expense = get_expense(id)

    if request.method == 'POST':
        client= request.form['client']
        category = request.form['category']
        value= request.form['value']
        execution_date = request.form['execution_date']

        if not client:
            flash('Favor preencher o nome do cliente!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE despesas SET client = ?, category = ?, value = ?, execution_date = ?'
                         ' WHERE id = ?',
                         (client, category, value, execution_date, id) )
            conn.commit()
            conn.close()
            return redirect(url_for('expenses'))

    return render_template('expenseEdit.html', expense=expense)
