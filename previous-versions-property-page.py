import os
import subprocess
import sys 
import hashlib
import urllib

from gi.repository import Nautilus, Gtk, GObject

class PreviousVersionsPropertyPage(GObject.GObject, Nautilus.PropertyPageProvider):
	
	def on_tree_selection_changed(self,selection):
		model, treeiter = selection.get_selected()
		if treeiter != None:
			print("You selected", model[treeiter][0])

	def on_open_dir_clicked(self, button, selection, filepath):
		model, treeiter = selection.get_selected()
		self.dir=''.join([filepath, '/.snapshot/',model[treeiter][0]])
		subprocess.Popen(["xdg-open", self.dir])

	def on_open_file_clicked(self, button, selection, filepath):
		model, treeiter = selection.get_selected()
		print("MODEL0: " + model[treeiter][0])
		print("MODEL1: " + model[treeiter][1])
		print("Filepath: " + filepath)
		self.dir=''.join([filepath, '/.snapshot/', model[treeiter][0], '/' , model[treeiter][1]])
		subprocess.Popen(["xdg-open", self.dir])

	def on_copy_clicked(self, button):
		win = Gtk.Window()
		dialog = Gtk.FileChooserDialog("Please choose a folder", win,
			Gtk.FileChooserAction.SELECT_FOLDER,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			"Select", Gtk.ResponseType.OK))
		dialog.set_default_size(800, 400)

		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			print("Select clicked")
			print("Folder selected: " + dialog.get_filename())
		elif response == Gtk.ResponseType.CANCEL:
			print("Cancel clicked")
		dialog.destroy()

	def on_restore_clicked(self, button):
		print("TO-DO")
		
	def __init__(self):
		pass

	def get_property_pages(self, files):
		if len(files) != 1:
			return

		file = files[0]
				
		if file.get_uri_scheme() != 'file':
			return

		fileuri = urllib.unquote(file.get_uri()[7:])
		filename = urllib.unquote(file.get_name())

		if os.path.isfile(fileuri):
			self.isfolder = False
			filepath = os.path.dirname(fileuri)
		elif not os.path.isfile(fileuri):
			self.isfolder = True
			filepath = fileuri
			
		if not os.path.exists("".join([filepath,'/.snapshot'])):
			return

		self.property_label = Gtk.Label('Versiones Previas')
		self.property_label.show()

		self.box = Gtk.Box(homogeneous=True,spacing=0)
		self.box.show()

		self.vbox = Gtk.Box(Gtk.BaselinePosition.CENTER,homogeneous=False,spacing=0)
		self.vbox.set_orientation(Gtk.Orientation.VERTICAL)
		self.vbox.show()

		self.box.pack_start(self.vbox,True,True,10)
	
		self.comment = Gtk.Label()
		self.comment.set_text("Las versiones anteriores provienen"
			" de puntos de restauracion del servidor"
			" de datos de la red corporativa.")
		self.comment.set_line_wrap(True)
		self.comment.set_justify(Gtk.Justification.LEFT)
		self.vbox.pack_start(self.comment,False,False,6)
		self.comment.show()

		self.version_label= Gtk.Label()
		self.version_label.set_text("Version:")
		self.version_label.set_justify(Gtk.Justification.LEFT)
		self.version_label.show()
		self.vbox.pack_start(self.version_label,False,False,6)
		
		if self.isfolder == True:
			self.folders = Gtk.ListStore(str, str)
			for dir in os.listdir("".join([filepath,'/.snapshot'])):
				if dir.startswith('L'):
					self.stringfolderlist = dir.split("_")
					self.stringday = self.stringfolderlist[1].split(".")[1]
					self.stringhour = self.stringfolderlist[2].split(".")[0]
					self.folders.append([dir,"".join(["Copia del dia ", self.stringday, " a las: ", self.stringhour[:2], ":", self.stringhour[2:]])])
				if dir.startswith('M'):
					self.stringfolderlist = dir.split(".")
					self.stringday = self.stringfolderlist[1].split("_")[0]
					self.stringhour = self.stringfolderlist[1].split("_")[1]
					self.folders.append([dir,"".join(["Copia del dia ", self.stringday, " a las: ", self.stringhour[:2], ":", self.stringhour[2:]])])
			self.folderslist_sort = Gtk.TreeModelSort(self.folders)
			self.folderslist_sort.set_sort_column_id(1,Gtk.SortType.DESCENDING)
			self.modelslist = Gtk.TreeView(model=self.folderslist_sort)
		elif self.isfolder == False:
			self.files = Gtk.ListStore(str, str, str)
			for dir in os.listdir("".join([filepath,'/.snapshot'])):
				print("Vemos el directorio: " + dir)
				print("Ruta a buscar: " + "".join([filepath,'/.snapshot/']) + dir + '/' + filename)
				if os.path.isfile("".join([filepath,'/.snapshot/']) + dir + '/' + filename):
					if dir.startswith('L'):
						self.stringfolderlist = dir.split("_")
						self.stringday = self.stringfolderlist[1].split(".")[1]
						self.stringhour = self.stringfolderlist[2].split(".")[0]
						self.files.append([dir, filename,"".join(["Copia del dia ", self.stringday, " a las: ", self.stringhour[:2], ":", self.stringhour[2:]])])
					if dir.startswith('M'):
						self.stringfolderlist = dir.split(".")
						self.stringday = self.stringfolderlist[1].split("_")[0]
						self.stringhour = self.stringfolderlist[1].split("_")[1]
						self.files.append([dir, filename,"".join(["Copia del dia ", self.stringday, " a las: ", self.stringhour[:2], ":", self.stringhour[2:]])])
			self.fileslist_sort = Gtk.TreeModelSort(self.files)
			self.fileslist_sort.set_sort_column_id(2,Gtk.SortType.DESCENDING)
			self.modelslist = Gtk.TreeView(model=self.fileslist_sort)
		else:
			return
		
		if self.isfolder:
			self.renderer = Gtk.CellRendererText()
			self.column = Gtk.TreeViewColumn("Directorio", self.renderer, text=0)
			self.column.set_sort_column_id(0)
			self.column.set_sort_indicator(True)
			self.modelslist.append_column(self.column)
			self.renderer = Gtk.CellRendererText()
			self.column = Gtk.TreeViewColumn("Fecha", self.renderer, text=1)
			self.column.set_sort_column_id(1)
			self.column.set_sort_indicator(True)
			self.modelslist.append_column(self.column)
		else:
			self.renderer = Gtk.CellRendererText()
			self.column = Gtk.TreeViewColumn("Directorio", self.renderer, text=0)
			self.column.set_sort_column_id(0)
			self.column.set_sort_indicator(True)
			self.modelslist.append_column(self.column)
			self.renderer = Gtk.CellRendererText()
			self.column = Gtk.TreeViewColumn("Archivo", self.renderer, text=1)
			self.column.set_sort_column_id(1)
			self.column.set_sort_indicator(True)
			self.modelslist.append_column(self.column)
			self.renderer = Gtk.CellRendererText()
			self.column = Gtk.TreeViewColumn("Fecha", self.renderer, text=2)
			self.column.set_sort_column_id(2)
			self.column.set_sort_indicator(True)
			self.modelslist.append_column(self.column)
		
		
		
		self.modelslist.show()
		
		self.scrollable_treelist = Gtk.ScrolledWindow()
		self.scrollable_treelist.set_vexpand(True)
		self.scrollable_treelist.add(self.modelslist)
		self.scrollable_treelist.show()
	
		self.select = self.modelslist.get_selection()
		self.select.connect("changed", self.on_tree_selection_changed)
	
		self.hbox = Gtk.Box(Gtk.BaselinePosition.CENTER,homogeneous=True,spacing=0)
		self.hbox.set_orientation(Gtk.Orientation.HORIZONTAL)
		self.hbox.show()

		self.vbox.pack_start(self.scrollable_treelist,True,True,0)
		self.vbox.pack_start(self.hbox,False,False,10)
	
		#self.button = Gtk.Button(label='Restaurar...')
		#self.button.connect("clicked", self.on_restore_clicked)
		#self.hbox.pack_end(self.button, False, False, 0)
		#self.button.show()
	
		#self.button = Gtk.Button(label='Copiar...')
		#self.button.connect("clicked", self.on_copy_clicked)
		#self.hbox.pack_end(self.button, False, False, 0)
		#self.button.show()
		
		if self.isfolder:
			self.button = Gtk.Button(label='Abrir directorio')
			self.button.connect("clicked", self.on_open_dir_clicked, self.select, filepath) 
			self.hbox.pack_end(self.button, False, False, 0)
			self.button.show()
		else:
			self.button = Gtk.Button(label='Abrir directorio del archivo')
			self.button.connect("clicked", self.on_open_dir_clicked, self.select, filepath) 
			self.hbox.pack_end(self.button, False, False, 0)
			self.button.show()
			self.button = Gtk.Button(label='Abrir archivo')
			self.button.connect("clicked", self.on_open_file_clicked, self.select, filepath) 
			self.hbox.pack_end(self.button, False, False, 0)
			self.button.show()
	
	
		return Nautilus.PropertyPage(name="NautilusPython::previous_versions",
			label=self.property_label, 
			page=self.box),
