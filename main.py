import wx
import dashboard
import sender,dataset

#login window class
class Loginwindow(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, title="FristFrame", size=(400, 300))
        panel = wx.Panel(self)
        self.title = wx.StaticText(panel, label="Input the Channel_Id or Topic or just start by local", pos=(50, 20))
        self.label_user = wx.StaticText(panel, label="Channel_Id", pos=(30, 50))
        self.text_user = wx.TextCtrl(panel, size=(235, 25), pos=(100, 50), style=wx.TE_LEFT,value="'/Robot Fleet/Ball Shooter/Drive System/ISO18435:D1.2/PublicationTEST'")
        self.label_pwd = wx.StaticText(panel, label="Topic", pos=(50, 90))
        self.text_password = wx.TextCtrl(panel, size=(235, 25), pos=(100, 90),value="'OIIE:S30:V1.1/CCOM-JSON:SyncMeasurements:V1.0'")
        self.bt_confirm = wx.Button(panel, label='Start by internet', pos=(150, 130))
        self.bt_confirm.Bind(wx.EVT_BUTTON, self.OnclickDatabase)
        self.bt_cancel = wx.Button(panel, label='Quit', pos=(270, 130))
        self.bt_cancel.Bind(wx.EVT_BUTTON, self.OnclickExit)
        self.bt_registered = wx.Button(panel, label='Start by local', pos=(45, 130))
        self.bt_registered.Bind(wx.EVT_BUTTON, self.OnclickLoacl)

    #when user click start by local, just close the window and run dashboard.
    def OnclickLoacl(self, ever):
        dashboard.main()
        try:
            self.Close()
            dashboard.main()
        except:
            wx.MessageBox("Can't find local file")
            app = wx.App()
            frame = Loginwindow(parent=None, id=-1)
            frame.Show()
            app.MainLoop()
        

    #when user click start by database, get json first and run dashboard next.
    def OnclickDatabase(self, evet):
        message = ""
        Channel_Id = self.text_user.GetValue()
        Topic = self.text_password.GetValue()
        if Channel_Id == "" and Topic == "":
            message = 'You must input Channel_Id or Topic to link to database'
            wx.MessageBox(message)
        elif Channel_Id != "" and Topic != "":
            message = 'You just need fill Channel_Id OR Topic, dont fill both two'
            wx.MessageBox(message)
        elif Channel_Id != "":
            try:
                sender.main(dataset.connected_to_SQL(Channel_Id))
                self.Close()
                dashboard.main('url.csv')
            except:
                wx.MessageBox("Can't connect to database, please check your Channel_Id or internet")
        elif Topic != "":     
            try:
                sender.main(dataset.connected_to_SQLt(Topic))
                self.Close()
                dashboard.main('url.csv')
            except:
                wx.MessageBox("Can't connect to database, please check your Topic or internet")

    #when user press exit, just exit program
    def OnclickExit(self, event):
        exit(0)


if __name__ == '__main__':
    app = wx.App()
    frame = Loginwindow(parent=None, id=-1)
    frame.Show()
    app.MainLoop()