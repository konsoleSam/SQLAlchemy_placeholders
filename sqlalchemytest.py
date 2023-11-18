import sqlalchemy

def format_placeholders(text:str,parameters:dict):
    assert type(parameters)==dict,"parmaters must be type 'dict'"
    assert type(text)==str,"text must be type 'str'"

    new_parameters={}
    for key in parameters.keys():
        if type(parameters[key])==list or type(parameters[key])==tuple:
            c=text.find(":"+key)
            assert c!=-1,"parameter '"+key+"'does not exist in text."
            reps=[]
            for i in range(len(parameters[key])):
                new_parameters[key+"_format_placeholder_"+str(i+1)]=parameters[key][i]
                reps.append(":"+key+"_format_placeholder_"+str(i+1))
            text=text[:c]+",".join(reps)+text[c+len(key)+1:]
        else:
            new_parameters[key]=parameters[key]

    return [sqlalchemy.text(text),new_parameters]



db=sqlalchemy.create_engine("sqlite:///sqlite.db")
con=db.connect()
v=format_placeholders("SELECT 1,2,3,4,5,6,:sad,'bad',:mad",parameters={"sad":[1,2,3,4,5],"mad":1})
print(v)
x=con.execute(*v)
print(list(x)[0])