from sqlalchemy import create_engine,MetaData,Table,Column,Integer,String
engine=create_engine("sqlite:///test.db",echo=True)
meta=MetaData()
students=Table(
"students",meta,
Column("id",Integer,primary_key=True),
Column("name",String),
Column("lastname",String),
)
meta.create_all(engine)
# ins=students.insert().values(name="m",lastname="k")

conn=engine.connect()
# result=conn.execute(ins)
s=students.select().where(students.c.id>1)
result=conn.execute(s)
for i in result:
    print(i[1])
# print(result.fetchone())
update=students.update().where(students.c.id==1).values(name="j")
conn.execute(update)


select=students.select()
result=conn.execute(select)
for i in result:
    print(i)



delete=students.delete().where(students.c.id==2)
conn.execute(delete)
sel=students.select()
r=conn.execute(sel)
for i in r:
    print(i)
