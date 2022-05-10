import wx, wx.grid

#anasise table class
class GridTableBase(wx.grid.GridTableBase):
    _cols = "sensor1 sensor2 sensor3 allsensor".split()
    _data = [
        "1 2 3 4".split(),
        "1 2 3 4".split(),
        "1 2 3 4".split(),
        "1 2 3 4".split(),
        "1 2 3 4".split(),
    ]
    _rows = ["max","avg","min","variance","max drop"]
    _highlighted = set()

    def GetColLabelValue(self, col):
        return self._cols[col]

    def GetRowLabelValue(self, row):
        return self._rows[row]

    def GetNumberRows(self):
        return len(self._data)

    def GetNumberCols(self):
        return len(self._cols)

    def GetValue(self, row, col):
        return self._data[row][col]

    def SetValue(self, row, col, val):
        self._data[row][col] = val

    def GetAttr(self, row, col, kind):
        attr = wx.grid.GridCellAttr()
        attr.SetBackgroundColour(wx.GREEN if row in self._highlighted else wx.WHITE)
        return attr

    def set_value(self, row, col, val):
        self._highlighted.add(row)
        self.SetValue(row, col, val)

# abandoned class, just for test
class Test(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None)

        self.data = GridTableBase()
        self.grid = wx.grid.Grid(self)
        self.grid.SetTable(self.data)

        '''
        btn = wx.Button(self, label="set a2 to x")
        btn.Bind(wx.EVT_BUTTON, self.OnTest)

        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self.grid, 1, wx.EXPAND)
        self.Sizer.Add(btn, 0, wx.EXPAND)
        '''

    def OnTest(self, event):
        self.data.set_value(1, 0, "x")
        self.grid.Refresh()

'''
app = wx.PySimpleApp()
app.TopWindow = Test()
app.TopWindow.Show()
app.MainLoop()
'''




