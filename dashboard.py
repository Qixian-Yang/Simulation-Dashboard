import wx,wx.grid,table,data
import wx.lib.plot as plot
from fpdf import FPDF
import time
from wx.lib.embeddedimage import PyEmbeddedImage
import risk

sensorID_dict={'1':[],'2':[],'3':[]}
maxtime=0
point=0

Risk_on_s1=''
Risk_on_s2=''
Risk_on_s3=''

#open csv file and get data
def read_csv(source = "abc.csv"):
    global sensorID_dict
    with open(source) as file:
         for line in  file:
             # remove \n in each line
             line=line.split('\n' )[0]
             #split each line
             line=line.split(',' )
             #dont write in line1
             if line[0]=="Entity Count":
                 continue
             #if dont fine this sensor id in dictionary,create a new one
             print(line)
             sensorID_dict['1'].append(data.data(line[0],line[1],'1',line[3],line[4],line[5],line[6]))
             sensorID_dict['2'].append(data.data(line[0],line[1],'2',line[7],line[8],line[9],line[10]))
             sensorID_dict['3'].append(data.data(line[0],line[1],'3',line[11],line[12],line[13],line[14]))
                 
#this func is for test
def print_sensorID_dict():
    global sensorID_dict
    for i in sensorID_dict:
        for j in sensorID_dict[i]:
            print(j)
        print("")


#main dashboard class
class Dashboard(wx.Frame):
    def __init__(self,parent,dic):
        super(Dashboard, self).__init__(parent, title='text',size=(950, 840))
        self.dic = dic   
        self.linet1=None
        self.linet2=None
        self.linet3=None
        self.linevx1=None
        self.linevx2=None
        self.linevx3=None
        self.linevy0=None
        self.linevy1=None
        self.linevy2=None
        self.get_lines()
        self.singleboxlist=[]
        self.checkboxlist=[]
        self.vibrationx=[]
        self.vibrationy=[]
        self.set_menu()
        self.panel = wx.Panel(self)
        self.draw()

 
    #draw graph and table for each page
    def draw(self):

        self.panel.SetBackgroundColour((184,240,250))  
        self.plotter = plot.PlotCanvas(self.panel,pos=(0,35))
        self.plotter.SetInitialSize(size=(500, 300))
        

        #select box
        boxtem=wx.RadioButton(self.panel,0,"temperature sensor",pos=(15,0),size=(150,20))
        boxtem.SetValue(True)
        self.singleboxlist.append(boxtem)
        boxtem.Bind(wx.EVT_RADIOBUTTON, self.checkevent)

        boxvx=wx.RadioButton(self.panel,1,"Vibration X",pos=(165,0),size=(110,20))
        self.singleboxlist.append(boxvx)
        boxvx.Bind(wx.EVT_RADIOBUTTON, self.checkevent)

        boxvy=wx.RadioButton(self.panel,2,"Vibration Y",pos=(285,0),size=(110,20))
        self.singleboxlist.append(boxvy)
        boxvy.Bind(wx.EVT_RADIOBUTTON, self.checkevent)

        boxvz=wx.RadioButton(self.panel,3,"Vibration Z",pos=(395,0),size=(110,20))
        self.singleboxlist.append(boxvz)
        boxvz.Bind(wx.EVT_RADIOBUTTON, self.checkevent)

            
        #table part
        self.data_overview = wx.StaticText(parent=self.panel,pos=(650,5), label="Data overview")
        Font = self.data_overview.GetFont()
        Font.PointSize=15
        self.data_overview.SetFont(Font)
        for i in range(0,len(sensorID_dict)):
            boxtem=wx.CheckBox(self.panel,i,"",pos=(15+175*i,20),size=(175,15))
            if(i==0):
                boxtem.SetLabel("sensor1(redline)")
            elif(i==1):
                boxtem.SetLabel("sensor2(blackline)")
            elif(i==2):
                boxtem.SetLabel("sensor3(blueline)")

            boxtem.SetValue(True)
            self.Bind(wx.EVT_CHECKBOX,self.checkevent)
            self.checkboxlist.append(boxtem)
        self.temtable = table.GridTableBase()
        self.temgrid = wx.grid.Grid(self.panel,-1,pos=(500,40),size=(500,138))
        self.temgrid.SetTable(self.temtable) 
        cauclate(self)
        
        #risk_result
        self.vb = wx.BoxSizer(wx.VERTICAL)
        risklist = risk.risk().risk_analyse(sensorID_dict)
        label = ""
        if(risklist!=None):
            for i in risklist:
                label+=i.tostring()+"\n"
        if(len(risklist)>0):
            self.risk_result = wx.TextCtrl(self.panel, -1, risklist[0].tostring(),pos=(510,190),size = (410,140),style=wx.TE_MULTILINE|wx.TE_READONLY)
        else:
            self.word = wx.StaticText(parent=self.panel,pos=(500,200), label="")
        
        #risk part
        self.bmaps=wx.Bitmap('C:/Users/MSI-NB/Desktop/2.png',wx.BITMAP_TYPE_ANY)
        self.image=wx.StaticBitmap(self.panel,-1,self.bmaps,pos=(0,340))
        self.s1button = wx.Button(self.image, label='S1',pos=(280, 385),size=(35,35))
        self.s1button.Bind(wx.EVT_BUTTON, self.on_click_s1)
        self.s2button = wx.Button(self.image, label='S2',pos=(315, 5),size=(35,35))
        self.s2button.Bind(wx.EVT_BUTTON, self.on_click_s2)
        self.s3button = wx.Button(self.image, label='S3',pos=(635, 60),size=(35,35))
        self.s3button.Bind(wx.EVT_BUTTON, self.on_click_s3)

        
        tem=[]
        count=0
        t=[self.linet1,self.linet2,self.linet3]
        for i in self.checkboxlist:
            if i.GetValue():
                tem.append(t[count])
            count+=1
        count=0

        gc1= plot.PlotGraphics(tem, 'Temperature by time line', 'time', 'tem')
        self.plotter.Draw(gc1)


        self.sensor_risk_button("1",risklist)
        self.sensor_risk_button("2",risklist)
        self.sensor_risk_button("3",risklist)

        self.Show()
        toastone = wx.MessageDialog(None, "The machine is seriously out of order and may break down at any time."+"\n"+"Please check the Risk module for more details",caption="Danger risk",style = wx.ICON_WARNING)
        if(toastone.ShowModal() == wx.ID_YES):
            toastone.Destroy()

        self.panel.Update()
        self.panel.Refresh()


    def getback(self, event):
        self.panel.DestroyChildren()
        self.singleboxlist=[]
        self.checkboxlist=[]
        self.vibrationx=[]
        self.vibrationy=[]
        self.draw()



    #func for sensor risk information button
    def sensor_risk_button(self,sensorid,a):
        sensorcount = 0
        sensorlevel = ""
        sensorriskname="No risk"
        for i in a:
            if i.place!=sensorid:
                continue
            elif i.risklevel=="red":
                sensorlevel="red"
                sensorcount+=1
                sensorriskname = i.riskname
            elif i.risklevel=="yellow" and sensorlevel!="red":
                sensorlevel="yellow"
                sensorcount+=1
                sensorriskname = i.riskname
            elif sensorlevel=="":
                sensorlevel="blue"
                sensorcount+=1
                sensorriskname = i.riskname
        if(sensorid=="1"):
            print("edit on 1")
            rev = wx.StaticText(self.panel, -1, sensorriskname,(325, 725))
        elif(sensorid=="2"):
            print("edit on 2")
            rev = wx.StaticText(self.panel, -1, sensorriskname,(360, 345))
        elif(sensorid=="3"):
            print("edit on 3")
            rev = wx.StaticText(self.panel, -1, sensorriskname,(680, 400))
        Font = rev.GetFont()
        Font.PointSize=20
        rev.SetFont(Font)
        if(sensorlevel=="red"):
            rev.SetForegroundColour('white')
            rev.SetBackgroundColour('red')
        elif(sensorlevel=="yellow"):
            rev.SetForegroundColour('black')
            rev.SetBackgroundColour('yellow')
        elif(sensorlevel=="blue"):
            rev.SetForegroundColour('white')
            rev.SetBackgroundColour('blue')
        else:
            rev.SetForegroundColour('black')
            rev.SetBackgroundColour('white')
        #rev.SetModified(True)
        print("\n")

    def on_click_s1(self,event):
        self.on_click_s("1")
    def on_click_s2(self,event):
        self.on_click_s("2")
    def on_click_s3(self,event):
        self.on_click_s("3")

       
    def on_click_s(self,snum):
        self.panel.DestroyChildren()

        self.plotter = plot.PlotCanvas(self.panel)
        self.plotter.SetInitialSize(size=(495, 300))
        

        tem=[self.linet1]
        count=0
        t=[self.linet1,self.linet2,self.linet3]
        
        gc1= plot.PlotGraphics(tem, 'Tem in risk', 'time', 'tem')
        self.plotter.Draw(gc1)
        
        self.risk_title = wx.StaticText(self.panel, -1, "Risk list of sensor"+snum,(570, 20))
        font1 = wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')
        self.risk_title.SetFont(font1)
        self.listbox = wx.ListBox(self.panel, pos=(500,70), size=(430,580), name="listBox",style=wx.LB_ALWAYS_SB)
        

        risklist = risk.risk().risk_analyse(sensorID_dict)
        font1 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')
        self.listbox.SetFont(font1)
        for i in risklist:
            if(i.place==snum):
                self.listbox.AppendItems('''Risklevel:'''+i.risklevel+'''  Riskname:'''+i.riskname)

        self.mechine_information_title = wx.StaticText(self.panel, -1, "Mechine information",(10, 310))
        self.mechine_information = wx.TextCtrl(self.panel, -1, "",(10, 330),(470,125),wx.TE_MULTILINE|wx.TE_READONLY)
        self.risk_information_title = wx.StaticText(self.panel, -1, "Risk information",(10, 460))
        self.risk_information = wx.TextCtrl(self.panel, -1, "",(10, 480),(470,145),wx.TE_MULTILINE|wx.TE_READONLY)
        self.risk_history_title = wx.StaticText(self.panel, -1, "Risk history",(10, 630))
        self.risk_history = wx.TextCtrl(self.panel, -1, "",(10, 650),(470,105),wx.TE_MULTILINE|wx.TE_READONLY)
        self.listbox.Bind(wx.EVT_LISTBOX, self.on_click_listbox)

        self.backbutton = wx.Button(self.panel, label='Back to the main page',pos=(500, 660),size=(430,80))
        self.backbutton.Bind(wx.EVT_BUTTON, self.getback)

        
    def on_click_listbox(self,event):
        risklist = risk.risk().risk_analyse(sensorID_dict)
        select = self.listbox.GetSelection()

        print(risklist[select].sensortype)

        if(risklist[select].sensortype==0):
            tem=[]
            count=0
            t=[self.linet1,self.linet2,self.linet3]
            tem.append(t[int(risklist[select].place)-1])
            count+=1

            self.plotter.Clear()
            gc= plot.PlotGraphics(tem, 'Temperature by time line', 'time', 'tem')
            self.plotter.Draw(gc)
            self.panel.Update()
            self.panel.Refresh()
        elif(risklist[select].sensortype==1):
            vibration=[]
            count=0
            p=[self.linevx1,self.linevx2,self.linevx3]
            vibration.append(p[int(risklist[select].place)-1])
            count+=1

            print(vibration)
            self.plotter.Clear()
            gc= plot.PlotGraphics(vibration, 'Vibration by time line', 'time', 'vibration')
            self.plotter.Draw(gc)
            self.panel.Update()
            self.panel.Refresh()



        self.mechine_information.Value = '''Running time: 5 hours
Sensor id: 1
'''
        self.risk_information.Value = risklist[select].tostring()
        count=-1
        for i in risklist:
            if i.riskname==risklist[select].riskname:
                count+=1
        self.risk_history.Label="This risk has been happened " +str(count)+" times"



    #get each line for sensor
    def get_lines(self,time = 10000):
        global maxtime
        self.s1temdata= []
        for j in sensorID_dict["1"]:
            if(j.temperature==''):
                continue
            if float(time)>=float(j.timestamp):
                self.s1temdata.append([j.timestamp,j.temperature])
        if float(j.timestamp)>maxtime:
            maxtime = float(j.timestamp)
        for i in range(len(self.s1temdata)):
            for j in range(i,len(self.s1temdata)):
                if(self.s1temdata[i][0]>self.s1temdata[j][0]):
                    a=self.s1temdata[i]
                    self.s1temdata[i]=self.s1temdata[j]
                    self.s1temdata[j]=a
        self.maopao(self.s1temdata)
        self.linet1= plot.PolyLine(self.s1temdata, colour='red', width=1)

        self.s2temdata= []
        for j in sensorID_dict["2"]:
            if(j.temperature==''):
                continue
            if float(time)>=float(j.timestamp):
                self.s2temdata.append([j.timestamp,j.temperature])
        if float(j.timestamp)>maxtime:
            maxtime = float(j.timestamp)
        self.maopao(self.s2temdata)
        self.linet2= plot.PolyLine(self.s2temdata, colour='black', width=1)

        self.s3temdata= []
        for j in sensorID_dict["3"]:
            if(j.temperature==''):
                continue
            if float(time)>=float(j.timestamp):
                self.s3temdata.append([j.timestamp,j.temperature])
        if float(j.timestamp)>maxtime:
            maxtime = float(j.timestamp)
        self.maopao(self.s3temdata)
        self.linet3= plot.PolyLine(self.s3temdata, colour='blue', width=1)

        self.s1vibx= []
        for j in sensorID_dict["1"]:
            if float(time)>=float(j.timestamp):
                self.s1vibx.append([j.timestamp,j.vibrationx])
        if float(j.timestamp)>maxtime:
            maxtime = float(j.timestamp)
        self.maopao(self.s1vibx)
        self.linevx1= plot.PolyLine(self.s1vibx, colour='red', width=1)

        self.s2vibx= []
        for j in sensorID_dict["2"]:
            if float(time)>=float(j.timestamp):
                self.s2vibx.append([j.timestamp,j.vibrationx])
        if float(j.timestamp)>maxtime:
            maxtime = float(j.timestamp)
        self.maopao(self.s2vibx)
        self.linevx2= plot.PolyLine(self.s2vibx, colour='black', width=1)

        self.s3vibx= []
        for j in sensorID_dict["3"]:
            if float(time)>=float(j.timestamp):
                self.s3vibx.append([j.timestamp,j.vibrationx])
        if float(j.timestamp)>maxtime:
            maxtime = float(j.timestamp)
        self.maopao(self.s3vibx)
        self.linevx3= plot.PolyLine(self.s3vibx, colour='blue', width=1)

        self.s1viby= []
        for j in sensorID_dict["1"]:

            if float(time)>=float(j.timestamp):
                self.s1viby.append([j.timestamp,j.vibrationy])
        if float(j.timestamp)>maxtime:
            maxtime = float(j.timestamp)
        self.maopao(self.s1viby)
        self.linevy0= plot.PolyLine(self.s1viby, colour='red', width=1)

        self.s2viby= []
        for j in sensorID_dict["2"]:
            if float(time)>=float(j.timestamp):
                self.s2viby.append([j.timestamp,j.vibrationy])
        if float(j.timestamp)>maxtime:
            maxtime = float(j.timestamp)
        self.maopao(self.s2viby)
        self.linevy1= plot.PolyLine(self.s2viby, colour='black', width=1)

        self.s3viby= []
        for j in sensorID_dict["3"]:
            if float(time)>=float(j.timestamp):
                self.s3viby.append([j.timestamp,j.vibrationy])
        if float(j.timestamp)>maxtime:
            maxtime = float(j.timestamp)
        self.maopao(self.s3viby)
        self.linevy2= plot.PolyLine(self.s3viby, colour='blue', width=1)

        self.s1vibz= []
        for j in sensorID_dict["1"]:

            if float(time)>=float(j.timestamp):
                self.s1vibz.append([j.timestamp,j.vibrationz])
        if float(j.timestamp)>maxtime:
            maxtime = float(j.timestamp)
        self.maopao(self.s1vibz)
        self.linevz0= plot.PolyLine(self.s1vibz, colour='red', width=1)

        self.s2vibz= []
        for j in sensorID_dict["2"]:
            if float(time)>=float(j.timestamp):
                self.s2vibz.append([j.timestamp,j.vibrationz])
        if float(j.timestamp)>maxtime:
            maxtime = float(j.timestamp)
        self.maopao(self.s2vibz)
        self.linevz1= plot.PolyLine(self.s2vibz, colour='black', width=1)

        self.s3vibz= []
        for j in sensorID_dict["3"]:
            if float(time)>=float(j.timestamp):
                self.s3vibz.append([j.timestamp,j.vibrationz])
        if float(j.timestamp)>maxtime:
            maxtime = float(j.timestamp)
        self.maopao(self.s3vibz)
        self.linevz2= plot.PolyLine(self.s3vibz, colour='blue', width=1)

    #func for checkbox
    def checkevent(self,event):
        id=-1
        for i in self.singleboxlist:
            if i.GetValue():
                id=i.GetId()
                break
        if (id == 0):
            tem=[]
            count=0
            t=[self.linet1,self.linet2,self.linet3]
            for i in self.checkboxlist:
                #print(i.GetValue())
                if i.GetValue():
                    tem.append(t[count])
                count+=1

            if(tem!=[]):
                self.plotter.Clear()
                gc= plot.PlotGraphics(tem, 'Temperature by time line', 'time', 'tem')
                self.plotter.Draw(gc)
                self.panel.Update()
                self.panel.Refresh()
        elif (id ==1):
            vibx=[]
            count=0
            p=[self.linevx1,self.linevx2,self.linevx3]
            for i in self.checkboxlist:
                #print(i.GetValue())
                if i.GetValue():
                    vibx.append(p[count])
                count+=1

            if(vibx!=[]):
                self.plotter.Clear()
                gc= plot.PlotGraphics(vibx, 'Vibrationx by time line', 'time', 'vibrationx')
                self.plotter.Draw(gc)
                self.panel.Update()
                self.panel.Refresh()
        elif(id==2):
            viby=[]
            count=0
            v=[self.linevy0,self.linevy1,self.linevy2]
            for i in self.checkboxlist:
                #print(i.GetValue())
                if i.GetValue():
                    viby.append(v[count])
                count+=1

            if(viby!=[]):
                self.plotter.Clear()
                gc= plot.PlotGraphics(viby, 'Vibrationy by time line', 'time', 'vibrationy')
                self.plotter.Draw(gc)
                self.panel.Update()
                self.panel.Refresh()

        elif(id==3):
            vibz=[]
            count=0
            v=[self.linevz0,self.linevz1,self.linevz2]
            for i in self.checkboxlist:
                #print(i.GetValue())
                if i.GetValue():
                    vibz.append(v[count])
                count+=1

            if(vibz!=[]):
                self.plotter.Clear()
                gc= plot.PlotGraphics(vibz, 'Vibrationz by time line', 'time', 'vibrationz')
                self.plotter.Draw(gc)
                self.panel.Update()
                self.panel.Refresh()

        self.Show()

    #func for reply model refresh page
    def reply_refresh(self):
        id=-1
        for i in self.singleboxlist:
            if i.GetValue():
                id=i.GetId()
                break
        if (id == 0):
            box=[self.linet1,self.linet2,self.linet3]
        elif (id == 1):
            box=[self.linevx1,self.linevx2,self.linevx3]
        elif (id == 2):
            box=[self.linevy0,self.linevy1,self.linevy2]
        elif (id == 3):
            box=[self.linevz0,self.linevz1,self.linevz2]

        boxlist=[]
        count=0
        
        for i in self.checkboxlist:
            #print(i.GetValue())
            if i.GetValue():
                boxlist.append(box[count])
            count+=1
        self.plotter.Clear()
        if (id == 0):
            gc= plot.PlotGraphics(boxlist, 'Tem', 'time', 'tem')
        elif (id == 1):
            gc= plot.PlotGraphics(boxlist, 'Vibrationx by time line', 'time', 'Vibx')
        elif (id == 2):
            gc= plot.PlotGraphics(boxlist, 'Vibrationy by time line', 'time', 'Viby')
        elif (id == 3):
            gc= plot.PlotGraphics(boxlist, 'Vibrationz by time line', 'time', 'Vibz')
        self.plotter.Draw(gc)
        self.panel.Update()
        self.panel.Refresh()

        self.Show()

    #menu click func
    def menuHandler(self, event):
        id = event.GetId()
        if id == 121:
            print("jpg")
            time.sleep(0.5)
            screen = wx.ScreenDC()
            bmp = wx.EmptyBitmap(1600,800)
            mem = wx.MemoryDC(bmp)
            mem.Blit(0,0,1600,800,screen,self.GetPosition()[0],self.GetPosition()[1])

            bmp.SaveFile('0.jpg',wx.BITMAP_TYPE_JPEG)
        if id == 122:
            print("png")
            time.sleep(0.5)
            screen = wx.ScreenDC()
            bmp = wx.EmptyBitmap(1600,800)
            mem = wx.MemoryDC(bmp)
            mem.Blit(0,0,1600,800,screen,self.GetPosition()[0],self.GetPosition()[1])

            bmp.SaveFile('0.png',wx.BITMAP_TYPE_PNG)
        if id==22:
            print('pdf')
            pdf = FPDF()
            pdf.add_page()
            pdf.set_xy(0, 0)
            pdf.set_font('arial', 'B', 13.0)
            pdfl=0
            with open("sensor_data.csv") as file:
                pdf.ln()
                for i in file:
                    pdfl+=1
                    pdf.cell(h=10.0, align='L', w=0, txt=i, border=0)
                    pdf.ln()
            pdf.output('test.pdf', 'F')
        if id == wx.ID_EXIT:
            exit(0)
        if id == 13:
            print('static')
        if id == 14:
            print('reply')
            self.reply_mode()

    #func for reply model
    def reply_mode(self):
        global maxtime
        time = 0
        while(time<=maxtime):
            time+=0.1
            self.get_lines(time)
            self.reply_refresh()

    #abandoned func
    def maopao(self,ll):
        for i in range(len(ll)):
            for j in range(i,len(ll)):
                if(float(ll[i][0])>float(ll[j][0])):
                    a=ll[i]
                    ll[i]=ll[j]
                    ll[j]=a
    def set_menu(self):
        menuBar = wx.MenuBar()
        
        menumenu = wx.Menu()
        
        exportimage = wx.Menu()
        exportmenu=wx.Menu()
        
        expng = wx.MenuItem(exportimage, id = 122, text = "png file", kind = wx.ITEM_NORMAL)
        exjpg = wx.MenuItem(exportimage, id = 121, text = "jpg file", kind = wx.ITEM_NORMAL)
        exportpdf = wx.MenuItem(menumenu, id = 22, text = "pdf file", kind = wx.ITEM_NORMAL)
        exportimage.AppendItem(exjpg)
        exportimage.AppendItem(expng)
        
        exportmenu.AppendMenu(wx.ID_ANY, "Image", exportimage)
        exportmenu.AppendItem(exportpdf)
        
        radio1 = wx.MenuItem(menumenu, id = 13, text = "static", kind = wx.ITEM_RADIO)
        radio2 = wx.MenuItem(menumenu, id = 14, text = "reply", kind = wx.ITEM_RADIO)
        menumenu.AppendItem(radio1)
        menumenu.AppendItem(radio2)
        
        menumenu.AppendSeparator()
        
        quit = wx.MenuItem(menumenu, id = wx.ID_EXIT, text = "Quit\tCtrl+Q", kind = wx.ITEM_NORMAL)
        menumenu.AppendItem(quit)
        
        menuBar.Append(menumenu, title = 'Menu')
        menuBar.Append(exportmenu, title = 'Export')
        
        self.SetMenuBar(menuBar)
        
        self.Bind(wx.EVT_MENU, self.menuHandler)

#get analise table
def cauclate(s):
    Datatem=[]
    Datapre=[]
    #Datavib=[]
    for i in [s.s1temdata,s.s2temdata,s.s3temdata]:
        mmax=0
        mmin=100
        sum=0
        variance=0
        maxdrop = 0
        last = i[0][1]
        for j in i:
            sum+=float(j[1])
            if float(j[1])>float(mmax):
                mmax=j[1]
            elif float(j[1])<float(mmin):
                mmin=j[1]
            if abs(float(j[1])-float(last))>maxdrop:
                maxdrop = abs(float(j[1])-float(last))
            last = j[1]
        avg=sum/len(i)
        variance=get_variance(i,avg)
        Datatem.append([mmax,float('%.2f' % (avg)),mmin,float('%.2f' % (variance)),float('%.2f' % (maxdrop))])

    

    tx=max(float(Datatem[0][0]),float(Datatem[1][0]),float(Datatem[2][0]))
    ta=(float(Datatem[0][1])+float(Datatem[1][1])+float(Datatem[2][1]))/3
    tn=min(float(Datatem[0][2]),float(Datatem[1][2]),float(Datatem[2][2]))
    td=max(float(Datatem[0][4]),float(Datatem[1][4]),float(Datatem[2][4]))
    Datatem.append([tx,float('%.2f' % (ta)),tn,'N/A',td])

    Datatemzhuan=[]
    print(Datatem)
    for i in Datatem[0]:
        print(i)
    for i in range (0,len(Datatem[0])):
        li=[]
        for j in range (0,len(Datatem)):
            print(j,i)
            li.append(Datatem[j][i])
        Datatemzhuan.append(li)
        print(Datatemzhuan)
    print(Datatemzhuan)
    s.temtable._data=Datatemzhuan

def get_variance(list,avg):
    sumdif=0
    for k in list:
        sumdif+=(float(k[1])-avg)*(float(k[1])-avg)
    if(avg!=0):
        return sumdif/avg
    else:
        return 0

def main(sourece="abc.csv"):
    global sensorID_dict
    read_csv(sourece)
    app = wx.App()
    Dashboard(None,sensorID_dict)
    app.MainLoop()
 