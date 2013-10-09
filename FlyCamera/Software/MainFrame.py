# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.5 (standalone edition) on Sun Jun 17 14:16:25 2012

import wx
import sys

from RecorderPanel import *
from DatabaseList import *
from AllCamerasPanel import *
from LateralPanel import *
# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade


class MainFrame(wx.Frame):
	# Array of tracker panels, in the some order as they appear in the notebook
	__recorderPanels = []

	__camerasPanel = None
	#here only because we want to close it
	__mainApp = None

	# List of all the panels that can be displayed
	__contentList = None

	contentSizer = None
	# Panel where the main content is displayer
	#contentPanel = None


	__lateralPanel = None

	#def __init__(self, *args, **kwds):
	def __init__(self, parent, mainApp):
		# begin wxGlade: MainFrame.__init__
		#kwds["style"] = wx.DEFAULT_FRAME_STYLE
		#wx.Frame.__init__(self, *args, **kwds)
		wx.Frame.__init__(self, parent, wx.ID_ANY)
		#self.panel_1 = wx.Panel(self, -1)
		self.__lateralPanel = LateralPanel(self)

		


		self.__contentList = []
		#self.notebook = wx.Notebook(self, -1, style=0)
		


		#self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged, self.notebook)
		
		#self.notebook_1_pane_1 = RecorderPanel(self.notebook)
		#wx.Panel(self.notebook, -1)

		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow, self)
		self.SetTitle("frame_1")
		#self.__set_properties()

		#self.__do_layout()
		
		#self.contentPanel = wx.Panel(self, wx.ID_ANY)

		self.contentSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.contentSizer.Add(self.__lateralPanel, 0, wx.ALL | wx.EXPAND)
		#self.contentSizer.Add(self.__lateralPanel, 1, wx.LEFT)
		#self.contentSizer.Add((20,20),0,wx.EXPAND)


	


		#databasePanel = DatabaseListPanel(self.notebook)
		#databasePanel = DatabaseListPanel(self.contentPanel)
		databasePanel = DatabaseListPanel(self)
		recordings = GetAllRecordings()
		databasePanel.UpdateListFromDBTable(recordings)
		self.AddFrameContent(databasePanel)
		#self.AddPanel(databasePanel, "Database")
		#self.AddFrameContent()
		self.__lateralPanel.AddButton(ADMIN, databasePanel, "Database", self.DisplayFrameContent)

		
		self.camerasPanel = AllCamerasPanel(self)
		#self.camerasPanel = AllCamerasPanel(self.contentPanel)
		self.AddFrameContent(self.camerasPanel)
		#self.camerasPanel = AllCamerasPanel(self.notebook)
		#self.AddPanel(self.camerasPanel, "Cameras overview")
		self.__lateralPanel.AddButton(PROCESSES, self.camerasPanel, "Overview", self.DisplayFrameContent)





		#qrGenerator = QRGeneratorPanel(self)
		#self.AddFrameContent(qrGenerator)
		#self.__lateralPanel.AddButton(TOOLS, databasePanel, "QR code", self.DisplayFrameContent)



		self.DisplayFrameContent(databasePanel)







		
		#self.contentPanel.setSizer(self.contentSizer)


		#sizer_0 = wx.BoxSizer(wx.HORIZONTAL)
		#sizer_0.Add(self.contentPanel, 0, wx.ALL | wx.EXPAND)

		sizer_0 = self.contentSizer


		# begin wxGlade: MainFrame.__do_layout
		

		
		#self.notebook.AddPage(self.notebook_1_pane_1, "Device 1")


		#sizer_1.Add(self.notebook, 4, wx.EXPAND, border=5)
		#self.contentSizer.Add(self.contentPanel, 4, wx.EXPAND, border=5)
		#self.contentPanel 
		
		#self.SetSizer(self.contentSizer)
		#self.contentSizer.Fit(self)
		self.SetSizer(sizer_0)
		sizer_0.Fit(self)
		self.Layout()
		
		#self.SetMinSize(sizer_1.GetMinSize())
		# end wxGlade

		
		self.__mainApp = mainApp
		#self.imlist = wx.ImageList(16, 16)
		
		# end wxGlade
		



	#def __do_layout(self):
		
	
	
		
	#def AddPanel (self, panel, title):
	def AddFrameContent (self, content):
		#self.notebook.AddPage(panel, title)
		self.__contentList.append(content)

		self.contentSizer.Add(content, 3, wx.ALL | wx.EXPAND)

		#if len(self.__contentList) == 1:
		#	content.Show()
		#	self.Fit()
		#	self.Layout()
		#else:
		self.Fit()
		self.Layout()
		content.Hide()
		

		

	# Given a content panel (that was already added)
	# it shows it, hiding all the others.
	def DisplayFrameContent (self, displayContent):
		for content in self.__contentList:
			if content == displayContent:
				content.Show()
			else:
				content.Hide()
		self.Layout()
	
	def AddRecorder(self, recorder, title):
		# Creates the RecorderPanel
		index = len(self.__recorderPanels)


		# Creates a notebook for this RecorderPanel
		#notebook = wx.Notebook(self.contentPanel, -1, style=0)
		notebook = wx.Notebook(self, -1, style=0)
		


		recorderPanel = RecorderPanel(index, notebook)
		recorderPanel.SetRecorder(recorder)

		# Connects the RecorderPanel with the preview interface
		recorderPanel.AddCameraPanelForPreview(self.camerasPanel.GetCameraPanel(index))
		self.__recorderPanels.append(recorderPanel)



		notebook.AddPage(recorderPanel, title);
		notebook.AddPage(wx.Panel(notebook), "Tracker")

		# Connects the notebook to the LateralPanel
		self.__lateralPanel.AddButton(PROCESSES, notebook, "Camera " + str(index), self.DisplayFrameContent)

		# Adds this new content
		self.AddFrameContent(notebook)

		#self.Fit()
		#self.Layout()

		#trackerPanel.SetTabSelected(	len(self.__recorderPanels) == 0	)
		#self.notebook.AddPage(recorderPanel, title)
		return recorderPanel
		
	'''
	def OnPageChanged(self,event):
		old = event.GetOldSelection()
		new = event.GetSelection()
		
		# The first time, there is not an old tab selected
		if old != -1:
			self.__recorderPanels[old].SetTabSelected(False)
		self.__recorderPanels[new].SetTabSelected(True)
	'''
	def OnCloseWindow(self, event):
		# It can't postpone the closure of the window
		if not event.CanVeto():
			#print "I can't veto"
			self.__mainApp.DestroyGently()
			self.Destroy()
			return
				
		# Check if there is a panel recording
		isRecording = False
		for trackerPanel in self.__recorderPanels:
			if trackerPanel.IsRecording():
				isRecording = True
				break
			
		#print "Is recording: ", isRecording
		# Dialog window
		destroyWindow = False
		if isRecording:
			dialogue = wx.MessageDialog(None, 'You are recording from camera.\nAre you sure to quit?', 'Question',  wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
			destroyWindow = dialogue.ShowModal() == wx.ID_YES
			#print "destroyWindow: ", destroyWindow
			dialogue.Destroy()
			#print "post dialogue.DestroyGently(): "
		else:
			destroyWindow = True
		#print "destroyWindow: ", destroyWindow
		# DestroyGently or not?
		if destroyWindow:			
			#print "DestroyGently"
			# Stop recording
			self.__mainApp.DestroyGently()
			self.Destroy()
			'''
			for trackerPanel in self.__recorderPanels:
				#trackerPanel.OnStop(None)	#StopCapture()
				#trackerPanel.OnToggleRecording(None)
				#trackerPanel.OnToggleAcquire(None)
				#print "Wait for trackerPanel: ", trackerPanel
				trackerPanel.DestroyAndWait(2)
				print "Joined with trackerPanel: ", trackerPanel
			#print "All destroyed"
			self.DestroyGently()
			
			self.__queue.close()
			self.__queue.join_thread()
			
			#print "post self.DestroyGently()"
			print "Program terminated."
			'''
			#sys.exit()
			#exit(0)
			#print "post sys.exit()"
		else:
			#print "Not destroyed"
			event.Veto(True)
# end of class MainFrame