import wx,wx.grid,table,data
import wx.lib.plot as plot
from fpdf import FPDF
import time
from wx.lib.embeddedimage import PyEmbeddedImage
import risk

sensorID_dict={}
maxtime=0
point=0

Risk_on_s1=''
Risk_on_s2=''
Risk_on_s3=''

#open csv file and get data
def read_csv(source = "sensor_data.csv"):
    global sensorID_dict
    with open(source) as file:
         for line in  file:
             # remove \n in each line
             line=line.split('\n' )[0]
             #split each line
             line=line.split(',' )
             #dont write in line1
             if line[0]=="Timestamp":
                 continue
             #if dont fine this sensor id in dictionary,create a new one
             if sensorID_dict.get(line[2])==None:
                 sensorID_dict[line[2]]=[data.data(line[0],line[1],line[2],line[3],line[4],line[5],line[6])]
             else:
                 sensorID_dict[line[2]].append(data.data(line[0],line[1],line[2],line[3],line[4],line[5],line[6]))
   
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
        self.linet0=None
        self.linet1=None
        self.linet2=None
        self.linep0=None
        self.linep1=None
        self.linep2=None
        self.linev0=None
        self.linev1=None
        self.linev2=None
        self.get_lines()
        self.temboxlist=[]
        self.vibrationx=[]
        self.vibrationy=[]
 
        self.draw()
 
    #draw graph and table for each page
    def draw(self):
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




        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour("white")  
        self.plotter = plot.PlotCanvas(self.panel)
        #self.plotter2 = plot.PlotCanvas(self.panel)
        #self.plotter3 = plot.PlotCanvas(self.panel)
        self.plotter.SetInitialSize(size=(500, 300))
        #self.plotter2.SetInitialSize(size=(500, 500))
        #self.plotter3.SetInitialSize(size=(500, 500))
        
        self.nmbox = wx.BoxSizer(wx.HORIZONTAL)
        self.vboxleft = wx.BoxSizer(wx.VERTICAL)
        self.vboxmid = wx.BoxSizer(wx.HORIZONTAL)
        self.vboxright = wx.BoxSizer(wx.VERTICAL)

        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        #self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        #self.hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        for i in range(0,len(sensorID_dict)):
            boxtem=wx.CheckBox(self.panel,i,"temperature sensor"+str(i),pos=(50*i,50),size=(300,15))
            #boxpre=wx.CheckBox(self.panel,i,"pressure sensor"+str(i),pos=(50*i,50),size=(150,15))
            #boxvib=wx.CheckBox(self.panel,i,"vibration sensor"+str(i),pos=(50*i,50),size=(150,15))

            boxtem.SetValue(True)
            #boxpre.SetValue(True)
            #boxvib.SetValue(True)
            self.Bind(wx.EVT_CHECKBOX,self.checkevent)
            #self.Bind(wx.EVT_CHECKBOX,self.checkevent_pre,boxpre)
            self.temboxlist.append(boxtem)
            #self.preboxlist.append(boxpre)
            #self.vibboxlist.append(boxvib)

            self.hbox.Add(boxtem,0,wx.LEFT,border=10)
            #self.hbox2.Add(boxpre,0,wx.LEFT,border=10)
            #self.hbox3.Add(boxvib,0,wx.LEFT,border=10)

        for i in range(0,len(sensorID_dict)):
            boxtem=wx.CheckBox(self.panel,i,"temperature sensor"+str(i),pos=(50*i,50),size=(300,15))

            boxtem.SetValue(True)
            self.hbox2.Add(boxtem,0,wx.LEFT,border=10)
        self.vboxleft.Add(self.hbox,0)
        self.vboxleft.Add(self.hbox2,0)
        self.vboxmid.Add(self.plotter, 0)
        #self.vboxmid.Add(self.hbox2, 0)
        #self.vboxmid.Add(self.plotter2, 0)
        #self.vboxright.Add(self.hbox3, 0)
        #self.vboxright.Add(self.plotter3, 0)


        self.temtable = table.GridTableBase()
        #self.pretable = table.GridTableBase()
        #self.vibtable = table.GridTableBase()
        self.temgrid = wx.grid.Grid(self.panel,-1,pos=(15,550),size=(500,138))
        self.temgrid.SetTable(self.temtable)
        
        #self.pregrid = wx.grid.Grid(self.panel,-1,pos=(15+500,550),size=(500,150))
        #self.pregrid.SetTable(self.pretable)
        #self.vibgrid = wx.grid.Grid(self.panel,-1,pos=(15+1000,550),size=(500,150))
        #self.vibgrid.SetTable(self.vibtable)
        cauclate(self)
        

        self.vb = wx.BoxSizer(wx.VERTICAL)
        risklist = risk.risk().risk_analyse(sensorID_dict)
        label = ""
        for i in risklist:
            label+=i.tostring()+"\n"
        if(len(risklist)>0):
            self.word = wx.StaticText(parent=self.panel, id=10, label=risklist[0].tostring())
        else:
            self.word = wx.StaticText(parent=self.panel, id=10, label="")
        

        self.vb.Add(self.temgrid, 0)
        self.vb.Add(self.word, 0)
        self.vboxmid.Add(self.vb, 0)

        
        self.bmaps=wx.Bitmap('C:/Users/MSI-NB/Desktop/2.jpg',wx.BITMAP_TYPE_ANY)
        self.image=wx.StaticBitmap(self.panel,-1,self.bmaps)
        

        self.vboxleft.Add(self.vboxmid,0)
        self.vboxleft.Add(self.image, 0)
        self.nmbox.Add(self.vboxleft, 0)
        #self.nmbox.Add(self.vboxright, 0)
 
        
        tem=[]
        #pre=[]
        #vib=[]
        count=0
        t=[self.linet0,self.linet1,self.linet2]
        #p=[self.linep0,self.linep1,self.linep2]
        #v=[self.linev0,self.linev1,self.linev2]
        for i in self.temboxlist:
            if i.GetValue():
                tem.append(t[count])
            count+=1
        count=0
        
        '''
        for i in [self.linep0,self.linep1,self.linep2]:
            if self.preboxlist[count]:
                pre.append(i)
            count+=1
        '''

        #count=0
        #for i in [self.linev0,self.linev1,self.linev2]:
        #    if self.vibboxlist[count]:
        #        vib.append(i)
        #    count+=1
        
        gc1= plot.PlotGraphics(tem, 'Tem', 'time', 'tem')
        #gc2= plot.PlotGraphics(pre, 'Pre', 'time', 'pressure')
        #gc3= plot.PlotGraphics(vib, 'Vib', 'time', 'vibration')
        self.plotter.Draw(gc1)
        #self.plotter2.Draw(gc2)
        #self.plotter3.Draw(gc3)

        self.sensor_risk_button("1",risklist)
        self.sensor_risk_button("2",risklist)
        self.sensor_risk_button("3",risklist)

        self.panel.SetSizer(self.nmbox)
        self.Show()
        toastone = wx.MessageDialog(None, "The machine is seriously out of order and may break down at any time."+"\n"+"Please check the Risk module for more details",caption="Danger risk",style = wx.ICON_WARNING)
        if(toastone.ShowModal() == wx.ID_YES): 
            toastone.Destroy() 

    #func for sensor risk information button
    def sensor_risk_button(self,sensorid,a):
        sensorcount = 0
        sensorlevel = ""
        sensorriskname="No risk"
        for i in a:
            print(i.tostring())
            print(sensorlevel)
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
            print(sensorlevel)
            print("\n")
        if(sensorid=="1"):
            rev = wx.TextCtrl(self.panel, -1, sensorriskname,(325, 725),(140,36))
        elif(sensorid=="2"):
            rev = wx.StaticText(self.panel, -1, "Badly worn in driving wheels",(360, 345))
        else:
            rev = wx.StaticText(self.panel, -1, "No risk",(680, 400))
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


    #get each line for sensor
    def get_lines(self,time = 10000):
        global maxtime
        self.s0temdata= []
        for j in sensorID_dict["1"]:
            if(j.temperature==''):
                continue
            if float(time)>=float(j.timestamp):
                self.s0temdata.append([j.timestamp,j.temperature])
        if float(j.timestamp)>maxtime:
            maxtime = float(j.timestamp)
        for i in range(len(self.s0temdata)):
            for j in range(i,len(self.s0temdata)):
                if(self.s0temdata[i][0]>self.s0temdata[j][0]):
                    a=self.s0temdata[i]
                    self.s0temdata[i]=self.s0temdata[j]
                    self.s0temdata[j]=a
        self.maopao(self.s0temdata)
        self.linet0= plot.PolyLine(self.s0temdata, colour='red', width=1)

        self.s1temdata= []
        for j in sensorID_dict["2"]:
            if(j.temperature==''):
                continue
            if float(time)>=float(j.timestamp):
                self.s1temdata.append([j.timestamp,j.temperature])
        if float(j.timestamp)>maxtime:
            maxtime = float(j.timestamp)
        self.maopao(self.s1temdata)
        self.linet1= plot.PolyLine(self.s1temdata, colour='black', width=1)

        self.s2temdata= []
        for j in sensorID_dict["3"]:
            if(j.temperature==''):
                continue
            if float(time)>=float(j.timestamp):
                self.s2temdata.append([j.timestamp,j.temperature])
        if float(j.timestamp)>maxtime:
            maxtime = float(j.timestamp)
        self.maopao(self.s2temdata)
        self.linet2= plot.PolyLine(self.s2temdata, colour='blue', width=1)

        self.s0predata= []
        for j in sensorID_dict["1"]:
            if float(time)>=float(j.timestamp):
                self.s0predata.append([j.timestamp,j.vibrationx])
        if float(j.timestamp)>maxtime:
            maxtime = float(j.timestamp)
        self.maopao(self.s0predata)
        self.linep0= plot.PolyLine(self.s0predata, colour='red', width=1)

        self.s1predata= []
        for j in sensorID_dict["2"]:
            if float(time)>=float(j.timestamp):
                self.s1predata.append([j.timestamp,j.vibrationx])
        if float(j.timestamp)>maxtime:
            maxtime = float(j.timestamp)
        self.maopao(self.s1predata)
        self.linep1= plot.PolyLine(self.s1predata, colour='black', width=1)

        self.s2predata= []
        for j in sensorID_dict["3"]:
            if float(time)>=float(j.timestamp):
                self.s2predata.append([j.timestamp,j.vibrationx])
        if float(j.timestamp)>maxtime:
            maxtime = float(j.timestamp)
        self.maopao(self.s2predata)
        self.linep2= plot.PolyLine(self.s2predata, colour='blue', width=1)

        self.s0vibdata= []
        for j in sensorID_dict["1"]:

            if float(time)>=float(j.timestamp):
                self.s0vibdata.append([j.timestamp,j.vibrationy])
        if float(j.timestamp)>maxtime:
            maxtime = float(j.timestamp)
        self.maopao(self.s0vibdata)
        self.linev0= plot.PolyLine(self.s0vibdata, colour='red', width=1)

        self.s1vibdata= []
        for j in sensorID_dict["2"]:
            if float(time)>=float(j.timestamp):
                self.s1vibdata.append([j.timestamp,j.vibrationy])
        if float(j.timestamp)>maxtime:
            maxtime = float(j.timestamp)
        self.maopao(self.s1vibdata)
        self.linev1= plot.PolyLine(self.s1vibdata, colour='black', width=1)

        self.s2vibdata= []
        for j in sensorID_dict["3"]:
            if float(time)>=float(j.timestamp):
                self.s2vibdata.append([j.timestamp,j.vibrationy])
        if float(j.timestamp)>maxtime:
            maxtime = float(j.timestamp)
        self.maopao(self.s2vibdata)
        self.linev2= plot.PolyLine(self.s2vibdata, colour='blue', width=1)

    #func for checkbox
    def checkevent(self,event):
        for i in self.temboxlist:
            print(i.GetValue())

        tem=[]
        count=0
        t=[self.linet0,self.linet1,self.linet2]
        for i in self.temboxlist:
            #print(i.GetValue())
            if i.GetValue():
                tem.append(t[count])
            count+=1

        if(tem!=[]):
            self.plotter.Clear()
            gc= plot.PlotGraphics(tem, 'Tem', 'time', 'tem')
            self.plotter.Draw(gc)
            self.panel.Update()
            self.panel.Refresh()

        pre=[]
        count=0
        p=[self.linep0,self.linep1,self.linep2]
        for i in self.vibrationx:
            #print(i.GetValue())
            if i.GetValue():
                pre.append(p[count])
            count+=1

        if(pre!=[]):
            self.plotter2.Clear()
            gc= plot.PlotGraphics(pre, 'pre', 'time', 'pre')
            self.plotter2.Draw(gc)
            self.panel.Update()
            self.panel.Refresh()

        vib=[]
        count=0
        v=[self.linev0,self.linev1,self.linev2]
        for i in self.vibrationy:
            #print(i.GetValue())
            if i.GetValue():
                vib.append(v[count])
            count+=1

        if(vib!=[]):
            self.plotter3.Clear()
            gc= plot.PlotGraphics(vib, 'vib', 'time', 'vibration')
            self.plotter3.Draw(gc)
            self.panel.Update()
            self.panel.Refresh()

        self.Show()

    #func for reply model refresh page
    def reply_refresh(self):

        tem=[]
        count=0
        t=[self.linet0,self.linet1,self.linet2]
        for i in self.temboxlist:
            #print(i.GetValue())
            if i.GetValue():
                tem.append(t[count])
            count+=1

        self.plotter.Clear()
        gc= plot.PlotGraphics(tem, 'Tem', 'time', 'tem')
        self.plotter.Draw(gc)
        self.panel.Update()
        self.panel.Refresh()

        pre=[]
        count=0
        p=[self.linep0,self.linep1,self.linep2]
        for i in self.vibrationx:
            #print(i.GetValue())
            if i.GetValue():
                pre.append(p[count])
            count+=1

        self.plotter2.Clear()
        gc= plot.PlotGraphics(pre, 'pre', 'time', 'pre')
        self.plotter2.Draw(gc)
        self.panel.Update()
        self.panel.Refresh()

        vib=[]
        count=0
        v=[self.linev0,self.linev1,self.linev2]
        for i in self.vibrationy:
            #print(i.GetValue())
            if i.GetValue():
                vib.append(v[count])
            count+=1

        self.plotter3.Clear()
        gc= plot.PlotGraphics(vib, 'vib', 'time', 'vibration')
        self.plotter3.Draw(gc)
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

#get analise table
def cauclate(s):
    Datatem=[]
    Datapre=[]
    #Datavib=[]
    for i in [s.s0temdata,s.s1temdata,s.s2temdata]:
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

    

    #px=max(float(Datapre[0][0]),float(Datapre[1][0]),float(Datapre[2][0]))
    tx=max(float(Datatem[0][0]),float(Datatem[1][0]),float(Datatem[2][0]))
    #vx=max(float(Datavib[0][0]),float(Datavib[1][0]),float(Datavib[2][0]))
    #pa=(float(Datapre[0][1])+float(Datapre[1][1])+float(Datapre[2][1]))/3
    ta=(float(Datatem[0][1])+float(Datatem[1][1])+float(Datatem[2][1]))/3
    #va=(float(Datavib[0][1])+float(Datavib[1][1])+float(Datavib[2][1]))/3
    #pn=min(float(Datapre[0][2]),float(Datapre[1][2]),float(Datapre[2][2]))
    tn=min(float(Datatem[0][2]),float(Datatem[1][2]),float(Datatem[2][2]))
    #vn=min(float(Datavib[0][2]),float(Datavib[1][2]),float(Datavib[2][2]))
    #pd=max(float(Datapre[0][4]),float(Datapre[1][4]),float(Datapre[2][4]))
    td=max(float(Datatem[0][4]),float(Datatem[1][4]),float(Datatem[2][4]))
    #vd=max(float(Datavib[0][4]),float(Datavib[1][4]),float(Datavib[2][4]))
    #Datapre.append([px,float('%.2f' % (pa)),pn,'N/A',pd])
    Datatem.append([tx,float('%.2f' % (ta)),tn,'N/A',td])
    #Datavib.append([vx,float('%.2f' % (va)),vn,'N/A',vd])
    
    #s.pretable._data=Datapre
    #s.vibtable._data=Datavib

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

def main(sourece="sensor_data.csv"):
    global sensorID_dict
    read_csv(sourece)
    #print_sensorID_dict()
    app = wx.App()
    Dashboard(None,sensorID_dict)
    app.MainLoop()
 