from tkinter import *
#from PIL import ImageTk,Image
import sqlite3
import matplotlib.pyplot  as plt
import numpy as np 



root = Tk()
root.title(' Weather App')
#root.iconbitmap('c:/gui/codemy.ico')
root.geometry('400x500')
root.configure(bg='gray')


conn = sqlite3.connect('weatherdata.db')
c = conn.cursor()

c.execute(""" CREATE TABLE data(
        City text,
        AQI integer,
        Temp float,
        Humidity float,
        State text,
        Zipcode integer
)""")





def graph():
    
       
    id = delete_box.get()
    #print(id)
    conn = sqlite3.connect('weatherdata.db')
    c = conn.cursor()
    c.execute("SELECT AQI,Temp,Humidity FROM data WHERE oid = :oid ", {'oid' : id})
    for row in c.fetchall():
            
        aqis = row[0],
        temps = row[1],
        humidity = row[2]
        
     
    c.execute("SELECT City FROM data WHERE  oid = :oid ", {'oid' : id} ) 
    city = c.fetchall()
    
      
    data1 = { 
             
             'AQI'     : aqis,
             'Temp'     : temps,
             'Humidity' : humidity,

            }
      
       
    group_data=list(data1.values())
    group_names=list(data1.keys())
    
    #plt.barh(group_names, group_data)
    
    plt.barh(group_names, group_data)
    plt.title(city)
    plt.show()

    conn.commit()  

    conn.close()


#create save function
def update():
    conn = sqlite3.connect('weatherdata.db')
    c = conn.cursor()
    
        
        
    record_id = delete_box.get()
    
    c.execute("""UPDATE data SET
        City    =:city,
        AQI     =:aqi,
        Temp    =:temp,
        Humidity=:humid, 
        State   =:state,
        Zipcode =:zipcode
        

        WHERE oid = :oid """,
        
    {  'city' : city_editor.get(),
       'aqi'  : aqi_editor.get(),
       'temp' : temp_editor.get(),
       'humid' : humid_editor.get(),
       'state': state_editor.get(),
       'zipcode' : zipcode_editor.get(),
       'oid'   : record_id
    })
    
    
    conn.commit()  

    conn.close()
    
#Create edit function
def edit():
    editor = Tk()
    editor.title('Update A Record')

    editor.geometry('400x400')

    conn = sqlite3.connect('weatherdata.db')
    c = conn.cursor()

    record_id = delete_box.get()
    c.execute("SELECT * FROM data WHERE oid = " + record_id)
    records = c.fetchall()
    
    global city_editor
    global aqi_editor
    global temp_editor
    global humid_editor
    global state_editor
    global zipcode_editor

    city_editor = Entry(editor, width = 30)
    city_editor.grid(row=0, column=1, padx=20,pady=(30,0))

    aqi_editor = Entry(editor, width = 30)
    aqi_editor.grid(row=1, column=1)

    temp_editor = Entry(editor, width = 30)
    temp_editor.grid(row=2, column=1)

    humid_editor = Entry(editor, width = 30)
    humid_editor.grid(row=3, column=1)

    state_editor = Entry(editor, width = 30)
    state_editor.grid(row=4, column=1)

    zipcode_editor = Entry(editor, width = 30)
    zipcode_editor.grid(row=5, column=1)

  
#create label
    city_label_editor = Label(editor, text="City")
    city_label_editor.grid(row=0, column=0,pady=(30,0))

    aqi_label_editor = Label(editor, text="AQI")
    aqi_label_editor.grid(row=1, column=0)

    temp_label_editor = Label(editor, text="Temp")
    temp_label_editor.grid(row=2, column=0)

    humid_label_editor = Label(editor, text="Humidity")
    humid_label_editor.grid(row=3, column=0)

    state_label_editor = Label(editor, text="State")
    state_label_editor.grid(row=4, column=0)

    zipcode_label_editor = Label(editor, text="Zipcode")
    zipcode_label_editor.grid(row=5, column=0)

    for record in records:
        city_editor.insert(0, record[0])
        aqi_editor.insert(0, record[1])
        temp_editor.insert(0, record[2])
        humid_editor.insert(0, record[3])
        state_editor.insert(0, record[4])
        zipcode_editor.insert(0, record[5])        
        

    save_button = Button(editor,text = "Save Record",command =update)
    save_button.grid(row=6, column=0, columnspan=5, padx=10, pady=10, ipadx=145)

#Create function for delete
def delete():
    conn = sqlite3.connect('weatherdata.db')
    c = conn.cursor()

    c.execute("DELETE from data WHERE oid = "+ delete_box.get() )
    conn.commit() 

    conn.close()


#Create Submit Function
def submit():

    conn = sqlite3.connect('weatherdata.db')
    c = conn.cursor()
    # Insert into table
    c.execute("INSERT INTO  data VALUES  (:city, :aqi, :temp, :humidity, :state, :zipcode)",
    {
      'city'    : city.get(),
      'aqi'     : aqi.get(),
      'temp'    : temp.get(),
      'humidity': humidity.get(),
      'state'   : state.get(),
      'zipcode' : zipcode.get()
    })

    conn.commit()

    conn.close()

  

        
    # Clear textbox
    city.delete(0,END)
    aqi.delete(0,END)
    temp.delete(0,END)
    humidity.delete(0,END)
    state.delete(0,END)
    zipcode.delete(0,END)

#create query function
def query():
    conn = sqlite3.connect('weatherdata.db')
    c = conn.cursor()

    c.execute("SELECT *,oid FROM data")
    records = c.fetchall()
    print(records)

    #Loop thru result
    print_records = ''
    for record in records:
        print_records += str(record[0]) +" " + str(record[1])+" " + str(record[2]) + " " + str(record[3])+" " +str(record[4]) +" " +str(record[5])+"\n"

    query_label = Label(root, text=print_records)
    query_label.grid(row=14, column=0, columnspan=2)
    conn.commit()

    conn.close()

city = Entry(root, width = 30)
city.grid(row=0, column=1, padx=20,pady=(30,0))

aqi = Entry(root, width = 30)
aqi.grid(row=1, column=1)

temp = Entry(root, width = 30)
temp.grid(row=2, column=1)

humidity = Entry(root, width = 30)
humidity.grid(row=3, column=1)

state = Entry(root, width = 30)
state.grid(row=4, column=1)

zipcode = Entry(root, width = 30)
zipcode.grid(row=5, column=1)

delete_box = Entry(root, width=30)
delete_box.grid(row=9, column=1, pady=5)
#create label
city_label = Label(root, text="City")
city_label.grid(row=0, column=0,pady=(30,0))

aqi_label = Label(root, text="AQI")
aqi_label.grid(row=1, column=0)

temp_label = Label(root, text="Tempture")
temp_label.grid(row=2, column=0)

humidity_label = Label(root, text="Humidity")
humidity_label.grid(row=3, column=0)

state_label = Label(root, text="State")
state_label.grid(row=4, column=0)

zipcode_label = Label(root, text="Zipcode")
zipcode_label.grid(row=5, column=0)

delete_box_label = Label(root, text='SELECT ID')
delete_box_label.grid(row=9 , column=0, pady=5)
#create submit button

submit_button = Button(root, text='Add Record to Database',command= submit)
submit_button.grid(row=6,column=0,columnspan=2,padx=10,pady=10,ipadx=110)

#Create query Button
query_btn = Button(root, text="Show Records", command=query)
query_btn.grid(row=7, column=0, columnspan=2,padx=10,pady=10,ipadx=136)

#Create delete button
del_button = Button(root, text ='Delete Records ',command = delete)
del_button.grid(row=10, column=0, columnspan=2, padx=10, pady=10, ipadx=134)

#create update button
edit_button = Button(root, text ='Edit Records ',command = edit)
edit_button.grid(row=11, column=0, columnspan=2, padx=10, pady=10, ipadx=140)

graph_button = Button(root,text="Graph it !",command=graph)
graph_button.grid(row=12,column=0,columnspan=2,padx=10,pady=10,ipadx=90)
conn.commit()

conn.close()
#commit changes

root.mainloop()


