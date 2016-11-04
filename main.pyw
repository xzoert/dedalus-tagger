#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PySide.QtCore import *
from PySide.QtGui import *
import tagger_widget
import sys, urllib.request, urllib.parse, json
from model import *
import os, os.path, json



class AppMainWindow(QMainWindow):
	
	def __init__(self,collection,app):
		QMainWindow.__init__(self)
		self.ui=None
		self.app=app
		self.collection=collection
		self.tableModel=None
		self.geometryInitialized=0

		confDir=os.path.expanduser("~/.dedalus")
		if not os.path.exists(confDir):
			os.makedirs(confDir)
		confFile=os.path.expanduser("~/.dedalus/tagger.json")
		if not os.path.exists(confFile):
			self.prefs={}
		else:
			try:
				with open(confFile) as jsonFile:
					self.prefs = json.load(jsonFile)
			except:
				self.prefs={}
		
		


	def setUi(self,ui):


		self.ui=ui
		self.ui.splitter.setStretchFactor(0,0)
		self.ui.splitter.setStretchFactor(1,1)

		if 'splitter' in self.prefs:
			splitterSizes=self.prefs['splitter']
			self.ui.splitter.setSizes((splitterSizes[0],splitterSizes[1]))

		self.delegate = CompleterDelegate(self)	
		self.tableModel=TaggerTableModel(self.ui.tableView,self.collection)
		self.ui.tableView.setModel(self.tableModel)
		if 'tagWidth' in self.prefs:
			self.ui.tableView.setColumnWidth(self.tableModel.COL_TAG,self.prefs['tagWidth'])
		else:
			self.ui.tableView.setColumnWidth(self.tableModel.COL_TAG,140)

		count=self.collection.getResourceCount()
		if count:
			for i in range(self.collection.getResourceCount()):
				res=self.collection.getResource(i)
				self.ui.resourceList.addItem(ResourceListItem(res))
			self.ui.resourceList.setCurrentRow(0)
			self.refreshResource()
			
		self.ui.fileLabel.setText('Resources ('+str(count)+')')
			
		self.ui.resourceList.itemClicked.connect(self.resourceChanged)
		
		self.tableModel.init()
		
		self.ui.cancelButton.clicked.connect(self.cancelClicked)
		self.ui.tableView.clicked.connect(self.itemClicked)
		
		self.ui.tableView.verticalHeader().sectionClicked.connect(self.vheaderClicked)
		
		self.ui.labelEdit.textEdited.connect(self.labelChanged)
		
		if 'width' in self.prefs and 'height' in self.prefs:
			self.resize(self.prefs['width'],self.prefs['height'])
		
		
		self.restoreGeometry()

		if 'maximized' in self.prefs and self.prefs['maximized']:
			self.showMaximized()
			
		self.ui.okButton.clicked.connect(self.saveAndExit)
		self.ui.relocateButton.clicked.connect(self.relocateResource)
			

	def relocateResource(self):
		(fileName,flt) = QFileDialog.getOpenFileName(self,self.tr("Open file"), None, "Any file (*)")
		if fileName:
			self.collection.relocateResource(fileName)

	def restoreGeometry(self):
		if 'geometry' in self.prefs:
			geo=self.prefs['geometry']
			r=QRect()
			r.setCoords(geo[0],geo[1],geo[2],geo[3])
			self.setGeometry(r)
			
		
	def refreshResource(self):
		res=self.collection.getCurrentResource()
		if not res: return
		self.ui.labelEdit.setText(res.getLabel())
		url=res.getUrl()
		self.tableModel.init()
		self.ui.relocateButton.hide()
		if res.url[:7]=='file://':
			fpath=urllib.parse.unquote(res.url[7:])
			self.ui.urlCaption.setText('Path')
			if not os.path.exists(fpath):
				self.ui.urlLabel.setText('<font color="red">'+fpath+'</font>')
				#self.ui.relocateButton.show()
			else:
				self.ui.urlLabel.setText(fpath)
				
		else:
			self.ui.urlCaption.setText('URL')
			self.ui.urlLabel.setText(urllib.parse.unquote(url))
		
	def resourceChanged(self,item):
		self.collection.gotoResource(item.getResource().getIndex())
		self.ui.resourceList.setCurrentItem(item)
		self.refreshResource()
	
	
	def cancelClicked(self):
		self.saveInnerGeometry()
		self.app.quit()
		
	def saveAndExit(self):
		self.collection.save()
		self.saveInnerGeometry()
		self.app.quit()

	def labelChanged(self,s):
		res=self.collection.getCurrentResource()
		if res:
			res.setLabel(s)
			self.ui.resourceList.item(res.getIndex()).setText(s)

	def itemClicked(self,index):
		self.ui.tableView.selectionModel().select(index, QItemSelectionModel.Deselect)
		if index.column()==self.tableModel.COL_STATE:
			tagging=self.collection.getTagging(index.row())
			if not tagging:
				return
			if tagging.state==Tag.ASSIGNED:
				# UNASSIGN
				self.collection.unassign(index.row())
				self.tableModel.reinit()
			elif tagging.state==Tag.NOT_ASSIGNED or tagging.state==Tag.INHERITED:
				# ASSIGN
				self.collection.assign(index.row())
				self.tableModel.reinit()
		elif index.column()==self.tableModel.COL_TAG or index.column()==self.tableModel.COL_COMMENT:
			self.ui.tableView.edit(index)
			
	
	
	def vheaderClicked(self,idx):
		tags=self.collection.getTags()
		if idx<len(tags):
			tag=tags[idx]
			tagging=self.collection.getTagging(idx)
			if tagging.state==Tag.ASSIGNED and tag.getAssignedCount()<self.collection.getResourceCount():
				for i in range(self.collection.getResourceCount()):
					res=self.collection.getResource(i)
					tag.assign(res)
			elif tag.getAssignedCount()>0:
				for i in range(self.collection.getResourceCount()):
					res=self.collection.getResource(i)
					tag.unassign(res)
		self.tableModel.reinit()
		self.ui.tableView.selectionModel().select(QModelIndex(), QItemSelectionModel.Clear)
	

	def savePrefs(self):
		confFile=os.path.expanduser("~/.dedalus/tagger.json")
		with open(confFile, 'w') as outfile:
			json.dump(self.prefs, outfile)

	def resizeEvent(self,e):
		if self.isMaximized():
			self.prefs['maximized']=True
		else:
			self.prefs['maximized']=False
			self.prefs['width']=self.width()
			self.prefs['height']=self.height()
		self.savePrefs()
		
	def moveEvent(self,e):
		if self.geometryInitialized<2:
			self.geometryInitialized=self.geometryInitialized+1
			self.restoreGeometry()
			return
		if not self.isMaximized():
			g=self.geometry()
			self.prefs['geometry']=g.getCoords()
		self.savePrefs()

	def saveInnerGeometry(self):
		if not self.isMaximized():
			g=self.geometry()
			self.prefs['geometry']=g.getCoords()
		self.prefs['splitter']=self.ui.splitter.sizes()
		self.prefs['tagWidth']=self.ui.tableView.columnWidth(self.tableModel.COL_TAG)
		self.savePrefs()

	def closeEvent(self,e):
		self.saveInnerGeometry()
		
			

			
class ResourceListItem(QListWidgetItem):
	
	def __init__(self,res):
		self.res=res
		QListWidgetItem.__init__(self,res.getLabel())
		
	def getResource(self):
			return self.res

class CompleterDelegate(QStyledItemDelegate):
	
	
	def __init__(self, app):
		self.app=app
		self.tagIdx=None
		QStyledItemDelegate.__init__(self,app.ui.tableView)
		app.ui.tableView.setItemDelegateForColumn(TaggerTableModel.COL_TAG, self)
		app.ui.tableView.setItemDelegateForColumn(TaggerTableModel.COL_COMMENT, self)
		
	def createEditor(self, parent, option, index):
		'''
		if self.app.model._data[index.row()]['inheritedFrom']!=self.app.model._url:
			return
		'''
		editor = QLineEdit(parent)
		editor.textEdited.connect(self.textEdited)
		self.tagIdx=index.row()
		if index.column()==TaggerTableModel.COL_TAG:
			completer = QCompleter([], editor)
			completer.setCompletionColumn(0)
			completer.setMaxVisibleItems(20)
			completer.setCompletionRole(Qt.EditRole)
			completer.setCaseSensitivity(Qt.CaseInsensitive)
			completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
			editor.setCompleter(completer)
			self.currentEditor=editor
		else:
			self.currentEditor=None
		return editor
	
	def setEditorData(self, editor, index):
		QStyledItemDelegate.setEditorData(self,editor, index)
	
	def closeEditor(self, editor, hint=None):
		QStyledItemDelegate.closeEditor(self,editor, hint)
	
	def commitData(self, editor):
		QStyledItemDelegate.commitData(self,editor)
		
	def textEdited(self,s):
		if not self.currentEditor:
			return
		
		self.gotSuggestions(self.app.collection.getSuggestions(s,self.tagIdx))
		
	def gotSuggestions(self,data):
		l=[]
		for i in data:
			l.append(i[0])
		c=self.currentEditor.completer()
		model=c.model()
		model.setStringList(l)
		self.app.tableModel.setLastSuggestions(l)


class TaggerSuggestions(QAbstractListModel):

	def __init__(self,data):
		QAbstractListModel.__init__(self)
		self._data=data
		
	def rowCount(self):
		return len(self._data)
		
	def data(self, index, role):
		if not index.isValid():
			return
		return self._data[index.row()]
		

class TaggerTableModel(QAbstractTableModel):
	
	NotAssignedBrush=QBrush(QColor(160,160,160,255))
	AssignedBrush=QBrush(QColor(0,0,0,255))
	NotAssignedBrushNew=QBrush(QColor(160,160,160,180))
	AssignedBrushNew=QBrush(QColor(200,0,0,255))
	InheritedFont=QFont()
	InheritedFont.setItalic(True)
	NormalFont=QFont()
	
	COL_TAG=1
	COL_COMMENT=2
	COL_STATE=0
	
	def __init__(self,view,collection):
		QAbstractTableModel.__init__(self)
		self.headers=['','Tag','Comment']
		self.view=view
		self.collection=collection
		self.lastSuggestions=None
	
	def setLastSuggestions(self,l):
		self.lastSuggestions=l
		
		
	def init(self):
		self.layoutAboutToBeChanged.emit()
		tags=self.collection.getTags()
		startindex=self.index(0,0)
		if (len(tags)):
			endindex=self.index(len(tags),1)
		else:
			endindex=self.index(0,1)
		self.layoutChanged.emit()
		self.view.setColumnWidth(self.COL_STATE,24)
		#self.view.setColumnWidth(self.COL_TAG,300)
		self.view.horizontalHeader().setStretchLastSection(True)
		'''
		editindex=self.index(len(tags),self.COL_TAG)
		self.view.setCurrentIndex(editindex)
		self.view.edit(editindex)
		'''
		
	def reinit(self):
		self.layoutAboutToBeChanged.emit()
		self.layoutChanged.emit()

	def data(self, index, role):
		if not index.isValid():
			return 
		tags=self.collection.getTags()
		if index.row()==len(tags):
			# insert row
			return 
		col=index.column()
		tag=tags[index.row()]
		tagging=tag.getTagging(self.collection.getCurrentResource())
		if col==self.COL_TAG:
			if tagging.state==Tag.INHERITED:
				if role == Qt.ForegroundRole: 
					if tag.isNew:
						return self.AssignedBrushNew
					else:
						return self.AssignedBrush
				elif role == Qt.FontRole: 
					return self.InheritedFont
				if role==Qt.ToolTipRole:
					return 'From: '+tagging.inheritedFrom
			elif tagging.state==Tag.ASSIGNED:
				if role == Qt.ForegroundRole: 
					if tag.isNew:
						return self.AssignedBrushNew
					else:
						return self.AssignedBrush
				elif role == Qt.FontRole: 
					if tagging.inheritedFrom:
						return self.InheritedFont
					else:
						return self.NormalFont
			elif tagging.state==Tag.NOT_ASSIGNED:
				if role == Qt.ForegroundRole: 
					if tag.isNew:
						return self.NotAssignedBrushNew
					else:
						return self.NotAssignedBrush
				elif role == Qt.FontRole: 
					return self.NormalFont
			if role==Qt.DisplayRole or role==Qt.EditRole:
				return tag.name
			if role==Qt.SizeHintRole:
				return QSize(300,20)
		elif col==self.COL_COMMENT:
			if tagging.state==Tag.INHERITED:
				if role == Qt.ForegroundRole: return self.AssignedBrush
				elif role == Qt.FontRole: return self.InheritedFont
			elif tagging.state==Tag.ASSIGNED:
				if role == Qt.ForegroundRole: return self.AssignedBrush
				elif role == Qt.FontRole: return self.NormalFont
			elif tagging.state==Tag.NOT_ASSIGNED:
				if role == Qt.ForegroundRole: return self.NotAssignedBrush
				elif role == Qt.FontRole: return self.NormalFont
			if role==Qt.DisplayRole or role==Qt.EditRole:
				return tagging.comment
			if role==Qt.SizeHintRole:
				return QSize(3000,20)
		elif col==self.COL_STATE:
			if role==Qt.DecorationRole:
				if tagging.state==Tag.ASSIGNED:
					return QPixmap(":/tagger/assigned.png")
				elif tagging.state==Tag.NOT_ASSIGNED:
					return QPixmap(":/tagger/not-assigned.png")
				elif tagging.state==Tag.INHERITED:
					return QPixmap(":/tagger/inherited.png")
			elif role==Qt.TextAlignmentRole:
				return Qt.AlignCenter
			if tagging.state==Tag.INHERITED and role==Qt.ToolTipRole:
				return 'From: '+tagging.inheritedFrom

	def editLastRow(self):
		tags=self.collection.getTags()
		idx=self.index(len(tags),self.COL_TAG)
		self.view.edit(idx)
		self.view.scrollTo(idx)

	def setData(self,index,value,role):
		if role==Qt.EditRole:
			if index.column()==self.COL_TAG:
				value=value.strip()
				tags=self.collection.getTags()
				if value=='':
					return False
				if index.row()==len(tags):
					self.beginInsertRows(QModelIndex(),len(tags),len(tags))
					isNew=True
					if self.lastSuggestions and value in self.lastSuggestions:
						isNew=False
					self.collection.addTag(value,isNew)
					self.endInsertRows()
					QTimer.singleShot(200,self.editLastRow)
					#self.view.edit(self.index(len(tags),self.COL_TAG))
				else:
					self.collection.renameTag(index.row(),value)
					self.reinit()
			elif index.column()==self.COL_COMMENT:
				self.collection.setComment(index.row(),value)
			'''
				if index.column()==0:
					self._data[index.row()]['name']=value
				elif index.column()==1:
					self._data[index.row()]['comment']=value
				self.dataChanged.emit(index,index)
			'''
			return True
		return False
		
		
	def headerData(self, col, orientation, role):
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return self.headers[col]
		elif orientation == Qt.Vertical:
			if role == Qt.DisplayRole:
				tags=self.collection.getTags()
				if col>=len(tags): 
					return ''
				else: 
					tag=tags[col]
					tagging=tag.getTagging(self.collection.getCurrentResource())
					if tagging.state==Tag.ASSIGNED:
						if tag.getAssignedCount()==self.collection.getResourceCount():
							return '*'
						else:
							return 'ALL'
					else:
						if tag.getAssignedCount()==0:
							return '*'
						else:
							return 'ALL'
			elif role==Qt.TextAlignmentRole:
				return Qt.AlignCenter
		return None
		
	'''
	def appendRow(self,parent=QModelIndex()):
		return
		count=self.getRowCount()
		self.beginInsertRows(parent,count,count)
		self._data.append({'name':'','comment':'','inheritedFrom':self._url})
		self.endInsertRows()
	'''

	def rowCount(self, parent):
		return len(self.collection.getTags())+1
	
	def columnCount(self, parent):
		return 3

	
	def flags(self,idx):
		if idx.column()==self.COL_TAG:
			tagging=self.collection.getTagging(idx.row())
			if not tagging or not tagging.inheritedFrom:
				return QAbstractTableModel.flags(self,idx) | Qt.ItemIsEditable
		elif idx.column()==self.COL_COMMENT:
			tagging=self.collection.getTagging(idx.row())
			if tagging and tagging.state==Tag.ASSIGNED:
				return QAbstractTableModel.flags(self,idx) | Qt.ItemIsEditable
			
		return QAbstractTableModel.flags(self,idx)
	



class HttpPost(QThread,QObject):
	
	
	def __init__(self,addr,data,callback):
		QThread.__init__(self)
		self.data=data
		self.callback=callback
		self.addr=addr
		self.aborted=False
		
	def abort(self):
		self.aborted=True
		
	def run(self):
		try:
			body=json.dumps(self.data).encode('utf-8')
			#print( 'Sending', self.addr, body )
			conn = urllib.request.urlopen(self.addr,body,timeout=10)
			r=conn.read().decode('utf-8')
			conn.close()
			if not self.aborted:
				r=json.loads(r)
				self.callback(r)
		except:
			print('Could not send')
			raise



def main():
	app = QApplication(sys.argv)
	ui = tagger_widget.Ui_MainWindow()
	if len(sys.argv)<2:
		print( 'Error, no URL provided' )
		sys.exit()
	collection=ResourceCollection(sys.argv[1:])
	mainWindow = AppMainWindow(collection,app)
	ui.setupUi(mainWindow)
	mainWindow.setUi(ui)

		

	mainWindow.show()
	
	app.exec_()
	
	
	sys.exit()
if __name__ == "__main__":
	main()

