from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from sqlalchemy.sql.expression import and_, or_
from . import inventory
from .forms import *
from .. import db
from ..models import Permission, Role, User, Post, Comment, Item, Record
import csv
import os


@inventory.route('/taked', methods=['GET', 'POST'])
def taked():
    form = SearchRecordForm()
    page = request.args.get('page', 1, type=int)
    pagination = Record.query.paginate(
        page,
        per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    records = pagination.items
    if form.is_submitted():
        keyword, username = form.keyword.data, form.username.data
        pagination = db.session.query(Record).filter(
            and_(
                Record.spec.like("%" + keyword + "%"),
                Record.username.like('%' + username + '%'))).paginate(
                    page,
                    per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                    error_out=False)
        records = pagination.items
    return render_template(
        'inventory/taked.html',
        form=form,
        records=records,
        pagination=pagination)


@inventory.route('/management', methods=['GET', 'POST'])
def management():
    form = FileForm()
    if form.validate_on_submit():
        with open('test.csv', 'wb') as f:
            f.write(form.file.data.read())
            Item.query.delete()
        with open("test.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = [row for row in reader]
            rows.pop(0)
            for row in rows:
                print(row[1] + row[2] + row[3] + row[4])
                if row[1] != '' and row[2] != '' and row[4] != '':

                    item = Item(
                        pn=row[0],
                        spec=row[1],
                        size=row[2],
                        series=row[3],
                        stock=row[4])
                    db.session.add(item)
                    try:
                        db.session.commit()
                    except e:
                        print(e + '!!!!!!!!!!!************')
                        flash(
                            'please check the csv file you upload is right.e.g: is P/N unique?'
                        )
    return render_template('inventory/manage.html', form=form)


@inventory.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    pagination = Item.query.filter(
        or_(
            Item.spec.like("%" + search + "%"),
            Item.pn.like("%" + search + "%"),
            Item.size.like("%" + search + "%"))).paginate(
                page,
                per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                error_out=False)
    pagination.page = page
    if form.is_submitted():
        search = form.keyword.data
        pagination = Item.query.filter(
            or_(
                Item.spec.like("%" + search + "%"),
                Item.pn.like("%" + search + "%"),
                Item.size.like("%" + search + "%"))).paginate(
                    1,
                    per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                    error_out=False)
    items = pagination.items
    return render_template(
        'inventory/index.html',
        form=form,
        items=items,
        pagination=pagination,
        search=search)


@inventory.route('/take_confirm/<pn>', methods=['GET', 'POST'])
def take_confirm(pn):
    take_confirm_form = Take_comfirmForm()
    item = Item.query.filter_by(pn=pn).first_or_404()
    if take_confirm_form.is_submitted():
        if item.stock > take_confirm_form.num.data:
            item.stock -= take_confirm_form.num.data
            r = Record(
                pn=item.pn,
                spec=item.spec,
                size=item.size,
                customer_name=take_confirm_form.customer_name.data,
                qty=take_confirm_form.num.data,
                username=current_user.username)
            db.session.add_all([item, r])
            db.session.commit()
            flash('You take the blade successfully!')
            redirect(url_for('.index'))
    return render_template(
        'inventory/take_confirm.html',
        item=item,
        take_confirm_form=take_confirm_form)
