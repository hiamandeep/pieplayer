"""
Copyright (c) 2015, Aman Deep
All rights reserved.

PiePlayer:
A Basic Music Player witten in python using Gstreamer framework with Tkinter as the Gui toolkit.

"""


#!/usr/bin/env python
import pygst
pygst.require('0.10')
import gst
import gobject
import os
from Tkinter import *
from tkFileDialog import askopenfilename
from time import *

class App(object):
	
	def seek(self,val):
				
		val1=float(val)
		self.pl.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_KEY_UNIT, val1 * gst.SECOND)
		
	def poll(self):
		print 'This works'
		position, forma = self.pl.query_position(gst.FORMAT_TIME)
		position_min=(int(position)/1000000000)
		print position_min
		self.sl.set(position_min)
		self.master.after(40, self.poll)

	#def time1(self):
			
		#position, forma = self.pl.query_position(gst.FORMAT_TIME)
		#position_min=(int(position)/1000000000)
		#print position_min
		#self.sl.set(position_min)
		#duration, formar = self.pl.query_duration(gst.FORMAT_TIME)
		#dura_min=(int(duration)/1000000000)
		#print dura_min
		#Scale(master,from_=2, to=dura_min,command=self.seek,resolution=0.1,orient=HORIZONTAL).pack(fill=X)
			

	def voli(self,n):
		#self.x =float(n)
		
		if self.flagvol==True:
			fout=open('volcache.txt','w')
			fout.write(n)
		fout=open('volcache.txt','r')
		voltemp = fout.readline()
		fout.close()
		volume = voltemp.strip()
		self.y=float(volume)
		self.pl.set_property("volume",self.y)
		self.sv.set(self.y)
		self.flagvol=True
		print 'self.y', self.y


	def mute(self):
		
		if self.m_flag==True:
			self.pl.set_property('volume',0)
			self.m_flag=False
			self.mm['text']='Unmute'
		else:
			self.pl.set_property('volume',self.y)
			self.m_flag=True
			self.mm['text']='Mute'
	
	def stop(self):
		self.pl.set_state(gst.STATE_READY)
		self.flag=False
		
	def browse_play(self,master):

		self.filepath = askopenfilename() 
		if self.flagpack==True:
			self.pl.set_state(gst.STATE_READY)
			self.sl.pack_forget()
		self.pl.set_property('uri','file://'+os.path.abspath(self.filepath))
		self.pl.set_state(gst.STATE_PLAYING)
		sleep(1)
		duration,forma1= self.pl.query_duration(gst.FORMAT_TIME)
		dura_min=(int(duration)/1000000000)
		self.sl=Scale(master,from_=0, to=dura_min,command=self.seek,orient=HORIZONTAL)
		self.sl.pack(fill=X)
		self.flagpack=True
		self.poll()
		
	def pause_resume(self):
		
		if self.flag==True:
			self.pl.set_state(gst.STATE_PAUSED)
			self.flag=False
			self.pp.config(text='Resume')
			
		else:
			self.pl.set_state(gst.STATE_PLAYING)
			self.flag=True
			self.pp.config(text='Pause')
			#self.poll()


	def __init__(self,master):
		self.m_flag=True
		self.mu_flag=False
		self.f1=False
		self.flagvol=False
		self.pl = gst.element_factory_make("playbin", "player")
		master.title('Music Player')
		master.geometry('200x250')
		menubar=Menu(master)
		filemenu=Menu(menubar,tearoff=0)
		filemenu.add_command(label='open',command=lambda:self.browse_play(master))
		menubar.add_cascade(label='File',menu=filemenu)
		master.config(menu=menubar)
		#Button(master,text='File Open', command=lambda:self.browse_play(master)).pack(fill=X)
		#self.textvar='Pause'
		self.pp=Button(master,text='Pause', command=self.pause_resume)
		self.pp.pack(fill=X)
		Button(master,text='stop', command=self.stop).pack(fill=X)
		self.mm=Button(master,text='Mute', command=self.mute)
		self.mm.pack(fill=X)
		#Button(master,text='time1', command=self.time1).pack(fill=X)
		#Button(master,text='seek', command=self.seek).pack(fill=X)
		self.sv=Scale(master,from_=1, to=0,command=self.voli,resolution=0.1)
		
		self.sv.pack(fill=X)
		self.master=master
		self.flagpack=False
		self.x=0.5
		self.flag=True
				
root=Tk()
obj=App(root)

root.mainloop()
