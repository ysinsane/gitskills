from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from . import inventory
from .forms import *
from .. import db
from .. models import Permission, Role, User, Post, Comment,Item,Record

@inventory.route('/taked',methods=['GET', 'POST'])
def taked():
    form = SearchRecordForm()
    page = request.args.get('page', 1, type=int)
    pagination=Record.query.paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
    records=pagination.items
    if form.validate_on_submit() and form.username!='':
        keyword,username=form.keyword.data,form.username.data
        pagination=db.session.query(Record).filter(Record.spec.like("%"+keyword+"%")
            ).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        items=pagination.items    
    return render_template('inventory/taked.html',form=form,
                        records=records,pagination=pagination)

@inventory.route('/index',methods=['GET', 'POST'])
def index():
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    pagination=Item.query.paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
    items=pagination.items
    if form.validate_on_submit():
        keyword=form.keyword.data
        pagination=db.session.query(Item).filter(Item.spec.like("%"+keyword+"%")).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        items=pagination.items    
    return render_template('inventory/index.html',form=form,items=items,pagination=pagination)

@inventory.route('/take_confirm/<pn>',methods=['GET','POST'])
def take_confirm(pn):
    take_confirm_form = Take_comfirmForm()
    item=Item.query.filter_by(pn=pn).first_or_404()
    if take_confirm_form.is_submitted():
        if item.stock>take_confirm_form.num.data:
            item.stock-=take_confirm_form.num.data
            r=Record(pn=item.pn,spec=item.spec,size=item.size,
            customer_name=take_confirm_form.customer_name.data,
            qty=take_confirm_form.num.data)
            db.session.add_all([item,r])
            db.session.commit()
            flash('You take the blade successfully!') 
            redirect(url_for('.index'))
    return render_template('inventory/take_confirm.html',item=item,take_confirm_form=take_confirm_form)   
