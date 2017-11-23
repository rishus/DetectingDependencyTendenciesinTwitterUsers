
import sqlalchemy
from sqlalchemy.orm import class_mapper, defer
from sqlalchemy import func
from sqlalchemy import Column, Integer, String, Table
#from dogpile.cache.api import NO_VALUE
from  sqlalchemy.sql.expression import func, select

import time


def getAttrList(object, cols):
    all_attrs = []
    for col in cols:
        all_attrs.append(getattr(object.c, col))
    return all_attrs



def getAllAttrList_but(object, cols):
    all_attrs = []
    for col in object.c.keys():
        if(not col in cols):
            all_attrs.append(col)
    return all_attrs
                         

def scan(session, object):
    return session.query(object).all()

def pick_at_random(session, object):
    return session.query(object).order_by(func.random()).first()



def limit(session, object, num_recs):
    return session.query(object).limit(num_recs).subquery()

def set_diff(session, from_set, without_set):
    stmt = session.query(from_set).except_(session.query(without_set)).subquery()
    return stmt

def select(session, object):
    stmt=session.query(object).subquery()
    return stmt


def proj(session, object, attrlist):
    robject = object
    if(type(object) == sqlalchemy.ext.declarative.DeclarativeMeta):
        robject = select(session, object)
    stmt=session.query(*getAttrList(robject,attrlist)).subquery()
    return stmt

def getColNames(session, object):
    robject = object
    if(type(object) == sqlalchemy.ext.declarative.DeclarativeMeta):
        robject = select(session, object)
    return robject.columns.keys()

def distinct(session, object, attrlist):
    robject = object
    if(type(object) == sqlalchemy.ext.declarative.DeclarativeMeta):
        robject = select(session, object)
    stmt=session.query(robject).distinct(*getAttrList(robject,attrlist)).subquery()
    return stmt

def drop(session, object, dropattrlist):
    robject = object
    if(type(object) == sqlalchemy.ext.declarative.DeclarativeMeta):
        robject = select(session, object)
    selectedAttrList =  getAllAttrList_but(robject, dropattrlist)
    stmt=session.query(*getAttrList(robject,selectedAttrList)).subquery()
    return stmt
    
def buildstmt(session, object):
    if(type(object) == sqlalchemy.ext.declarative.DeclarativeMeta):
        return select(session, object)
    return object

#some bug with respect to 
def aliasTwoAttr(session, robject, attr1, alias1, attr2, alias2):
    object = buildstmt(session,robject)
    stmt = session.query(getattr(object.c, attr1).label(alias1), getattr(object.c, attr2).label(alias2))
    return stmt

#some bug with respect to 
def proj_and_aliasThreeAttr(session, robject, attr1, alias1, attr2, ali):
    object = buildstmt(session,robject)
    renamed_cols = []
    for col in object.c.keys():
        if(col == attr):
            renamed_cols.append(getattr(object.c, col).label(alias))
        else:
            renamed_cols.append(getattr(object.c, col).label(col))
    stmt= session.query(*renamed_cols).subquery()
    return stmt



    
def filterGT(session, robject, attr, value):
    object = buildstmt(session,robject)
    stmt=session.query(object).filter(getattr(object.c, attr)>value).subquery()
    return stmt

def filterLT(session, robject, attr, value):
    object = buildstmt(session, robject)
    stmt=session.query(object).filter(getattr(object.c, attr)<value).subquery()
    return stmt

#both ends inclusive
def filterRange(session, robject, attr, lval, rval):
    stmt = filterGT(session, robject, attr, lval-1)
    stmt = filterLT(session, stmt, attr, rval + 1)
    return stmt

def filterEQ(session, robject, attr, value):
    object = buildstmt(session, robject)
    stmt=session.query(object).filter(getattr(object.c, attr)==value).subquery()
    return stmt

def filterEQ_B(session, robject, attr1, attr2):
    object = buildstmt(session, robject)
    stmt=session.query(object).filter(getattr(object.c, attr1)== getattr(object.c, attr2)).subquery()
    return stmt

def filterNEQ(session, robject, attr, value):
    object = buildstmt(session, robject)
    stmt=session.query(object).filter(getattr(object.c, attr)!=value).subquery()
    return stmt

def filter_attr_NEQ_attr(session, robject, attr1, attr2):
    object = buildstmt(session, robject)
    stmt=session.query(object).filter(getattr(object.c, attr1)!= getattr(object.c, attr2)).subquery()
    return stmt

def ascending(session, robject, attr):
    object = buildstmt(session, robject)
    stmt=session.query(object).order_by(getattr(object.c, attr)).subquery()
    return stmt
# def filter(session, object, attr, value):
#     return filterEQ(session, object, attr, value)


def fuse(session, roobject, riobject, attr, rattr):
    oobject = buildstmt(session, roobject)
    iobject = buildstmt(session, riobject)
    if(attr == rattr):
        print "join attributes must have different names"
    else:
        stmt=session.query(oobject, iobject, getattr(oobject.c, attr), getattr(iobject.c, rattr)).filter(getattr(oobject.c, attr)==getattr(iobject.c, rattr)).subquery()
        return stmt

def aliasAndFuse(session, roobject, riobject, attr, alias,  rattr, ralias):
    oobject = buildstmt(session, roobject)
    iobject = buildstmt(session, riobject)
    if(attr == rattr):
        print "join attributes must have different names"
    else:
        stmt=session.query(oobject, iobject, getattr(oobject.c, attr).label(alias), getattr(iobject.c, rattr).label(ralias)).filter(getattr(oobject.c, attr)==getattr(iobject.c, rattr)).subquery()
        return stmt


def aggregate(session, robject, aggAttr, aggLabel='count'):
    object = buildstmt(session, robject)
    stmt = session.query(func.count(getattr(object.c, aggAttr)).label(aggLabel), getattr(object.c, aggAttr).label(aggAttr)).group_by(getattr(object.c, aggAttr)).subquery()
    return stmt

def aggregate_list(session, robject, aggAttrs, aggLabel='count'):
    object = buildstmt(session, robject)
    stmt = session.query(func.count().label(aggLabel),
                         *getAttrList(object, aggAttrs)).group_by(*getAttrList(object, aggAttrs)).subquery()
    return stmt

def ascending_list(session, robject, attrlist):
    object = buildstmt(session, robject)
    stmt=session.query(object).order_by(*getAttrList(object, attrlist)).subquery()
    return stmt


def cardinality_distribution(session, robject, attr):
    object = buildstmt(session, robject)
    counts = aggregate(session, object, attr, 'count')
    freq_of_counts = ascending(session, aggregate(session, counts, 'count', 'freq'), 'count')
    return freq_of_counts

def cardinality_distribution_list(session, robject, attrlist):
    object = buildstmt(session, robject)
    counts = aggregate_list(session, object, attrlist, 'count')
    freq_of_counts = ascending(session, aggregate(session, counts, 'count', 'freq'), 'count')
    return freq_of_counts
    

def union(session, stmt1, stmt2):
    return (session.query(stmt1).union(session.query(stmt2))).subquery()

def getSocnetNeighbors(session, Person, pid):
	neighbors = []
	for p in session.query(Person).filter(Person.pid.in_([pid])).all():
		for e in p.neighbors:
			neighbors.append(e.id)
	return neighbors
 

def cardinality(session, stmt):
    return session.query(stmt).count()


def cardinality_in_range(session, robject, rangeAttr, range_floor, range_ceil):
	stmt = filterGT(session, robject, rangeAttr, range_floor-1)
	stmt = filterLT(session, stmt, rangeAttr, range_ceil+1)
        return cardinality(session, stmt)

    
def max(session, model, attr):
    stmt = buildstmt(session, model)
    qry = session.query(func.max(getattr(stmt.c, attr)).label("max_val"))
    res = qry.one()
    max_val= res.max_val
    return max_val

def min(session, model, attr):
    stmt = buildstmt(session, model)
    qry = session.query(func.min(getattr(stmt.c, attr)).label("min_val"))
    res = qry.one()
    min_val= res.min_val
    return min_val

def domain(session, model, attr):
    return [min(session, model, attr), max(session, model, attr)]

def cross_join(session, model1, model2):
    stmt1 = buildstmt(session, model1)
    stmt2 = buildstmt(session, model2)
    stmt = session.query(model1, model2).subquery()
    return stmt
