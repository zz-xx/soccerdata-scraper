import tkinter as tk                
from tkinter import font
import tkinter.ttk as ttk
from ctypes import windll

from cefpython3 import cefpython as cef
from PIL import ImageTk, Image

from scrape import Category, Page
from process import Plot





class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground






class HoverCanvas(tk.Canvas):
    def __init__(self, master, activebackground, **kw):
        tk.Canvas.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.activebackground = activebackground
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.config(background=self.activebackground)

    def on_leave(self, e):
        self.config(background=self.defaultBackground)






class RunApp(tk.Tk):


    
    def __init__(self, *args, **kwargs):
        
        
        tk.Tk.__init__(self, *args, **kwargs)

        w = 1024 # width for the Tk root
        h = 600 # height for the Tk root

        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # set the dimensions of the screen 
        # and where it is placed
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.themeColor = '#303030'
        self.config(background=self.themeColor)
        self.columnconfigure(0, weight=1)

        self.wm_title("Soccer Data Scraper v1.0")
        self.overrideredirect(True)
    
    
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, StartPage, AboutPage, AcknowledgementPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")



    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    

    def move_event(self, event):
        self.geometry('+{0}+{1}'.format(event.x_root, event.y_root))



    def set_appwindow(self):

        GWL_EXSTYLE=-20
        WS_EX_APPWINDOW=0x00040000
        WS_EX_TOOLWINDOW=0x00000080

        hwnd = windll.user32.GetParent(self.winfo_id())
        style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW
        style = style | WS_EX_APPWINDOW
        windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

        # re-assert the new window style
        self.wm_withdraw()
        self.after(10, lambda: self.wm_deiconify())






class HomePage(tk.Frame):



    def __init__(self, parent, controller):
        
        
        tk.Frame.__init__(self, parent, bg='#303030', width=1024, height=600, borderwidth = 0, highlightthickness = 0)
        self.controller = controller
    

        #-----title frame 
        title_frame = tk.Frame(self, width=1024, height=30, background='#212121', borderwidth = 0, highlightthickness = 0)
        title_frame.grid(row=0, column=0, sticky="ew")
        title_frame.columnconfigure(0, weight=1)
        title_frame.bind('<B1-Motion>', controller.move_event)
    
        
        #-------close button
        #make a frame to hold close button
        closeButtonFrame = tk.Frame(title_frame, width=30, height=30, borderwidth = 0, highlightthickness = 0) #their units in pixels
        closeButtonFrame.grid_propagate(False) #disables resizing of frame
        closeButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        closeButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        closeButtonFrame.grid(row=0, column=28, sticky="e") #put frame where the button should be

        #make actual button and grid it into frame
        closeButton = HoverButton(closeButtonFrame, text="X", fg='#606060', command=controller.destroy, background='#212121', relief=tk.FLAT, activebackground='red')
        closeButton.config(height=1, width=2, anchor=tk.N)
        helv36 = font.Font(family='Helvetica', size=16, weight='bold')
        closeButton['font'] = helv36
        closeButton.grid(sticky="wens") #makes the button expand


        #----minimize button
        minimizeButtonFrame = tk.Frame(title_frame, width=30, height=30, borderwidth = 0, highlightthickness = 0) #their units in pixels
        minimizeButtonFrame.grid_propagate(False) #disables resizing of frame
        minimizeButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        minimizeButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        minimizeButtonFrame.grid(row=0, column=27, sticky="e") #put frame where the button should be

        minimizeButton = HoverButton(minimizeButtonFrame, text="–", fg='#606060', command=controller.lower, background='#212121', relief=tk.FLAT, activebackground='#1a75ff')
        minimizeButton.config(height=1, width=2, anchor=tk.N)
        helv36 = font.Font(family='Helvetica', size=16, weight='bold')
        minimizeButton['font'] = helv36
        minimizeButton.grid(sticky="wens") #makes the button expand


        #------add icon to title bar
        iconFrame = tk.Frame(title_frame, width=30, height=30, borderwidth = 0, highlightthickness = 0)
        iconFrame.grid(row=0, column=0)

        iconCanvas = tk.Canvas(iconFrame, width=26, height=26, bd=0, highlightthickness=0)
        #lol this almost did not work
        #The variable img is a local variable which gets garbage collected 
        #after the class is instantiated. Save a reference to the photo
        self.img = ImageTk.PhotoImage(Image.open(".\\gui\\icons\\home.png").resize((26, 26)))
        iconCanvas.create_image(0, 0, image=self.img, anchor="nw")
        iconCanvas.grid(row=0, column=0)
        iconCanvas.bind('<B1-Motion>', controller.move_event)


        #------add application name to title bar
        appNameFrame = tk.Frame(title_frame, width=934, height=30, borderwidth = 0, highlightthickness = 0)
        appNameFrame.bind('<B1-Motion>', controller.move_event)
        appNameFrame.grid(row=0, column=1)

        #create canvas for holding app name
        imageCanvas = HoverCanvas(appNameFrame, '#23272A', bg='#212121', width=934, height=30, bd=0, highlightthickness=0)
        imageCanvas.bind('<B1-Motion>', controller.move_event)
        imageCanvas.grid(row=0, column=1)
        #add actual app name to canvas
        imageCanvas.create_text(98, 15, fill="#606060", activefill='#304ffe', font="Helvetica 12 bold", text="Soccer Data Scraper v1.0")


        #----create frame to store content of window
        contentFrame = tk.Frame(self, width=1280, height=690, background='#303030', borderwidth = 0, highlightthickness = 0)
        contentFrame.grid(row=1, column=0)

        #create canvas on which actual content would be added
        contentCanvas = HoverCanvas(contentFrame, '#303030', bg='#2C2F33', width=1024, height=570, bd=0, highlightthickness=0)
        contentCanvas.grid(row=0, column=0)

        
        #----start button
        startButtonFrame = tk.Frame(contentFrame, width=220, height=130, borderwidth = 0, highlightthickness = 0) #their units in pixels
        startButtonFrame.grid_propagate(False) #disables resizing of frame
        startButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        startButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        startButtonFrame.grid(row=0, column=0) #put frame where the button should be

        startButton = HoverButton(startButtonFrame, text='Start', background='#00e676', relief=tk.FLAT, activebackground='#18ffff', command=lambda:controller.show_frame("StartPage"))
        startButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=26, weight='bold')
        startButton['font'] = verdana
        startButton.configure(width=30, height=8)
        contentCanvas.create_window(265, 135, anchor=tk.NW, window=startButtonFrame)


        #----about button
        aboutButtonFrame = tk.Frame(contentFrame, width=220, height=130, borderwidth = 0, highlightthickness = 0) #their units in pixels
        aboutButtonFrame.grid_propagate(False) #disables resizing of frame
        aboutButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        aboutButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        aboutButtonFrame.grid(row=0, column=0) #put frame where the button should be
        
        aboutButton = HoverButton(aboutButtonFrame, text='About', background='#d50000', relief=tk.FLAT, activebackground='#ff3d00', command=lambda:controller.show_frame("AboutPage"))
        aboutButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=26, weight='bold')
        aboutButton['font'] = verdana
        aboutButton.configure(width=30, height=8)
        contentCanvas.create_window(500, 135, anchor=tk.NW, window=aboutButtonFrame)


        #-----acknowledgements button
        acknowledgementButtonFrame = tk.Frame(contentFrame, width=435, height=130, borderwidth = 0, highlightthickness = 0) #their units in pixels
        acknowledgementButtonFrame.grid_propagate(False) #disables resizing of frame
        acknowledgementButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        acknowledgementButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        acknowledgementButtonFrame.grid(row=0, column=0) #put frame where the button should be

        acknowledgementButton = HoverButton(acknowledgementButtonFrame, text='Acknowledgements', background='#FFCC33', relief=tk.FLAT, activebackground='#ffff8d', command=lambda:controller.show_frame("AcknowledgementPage"))
        acknowledgementButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=26, weight='bold')
        acknowledgementButton['font'] = verdana
        acknowledgementButton.configure(width=60, height=8)
        contentCanvas.create_window(275, 280, anchor=tk.NW, window=acknowledgementButtonFrame)






class StartPage(tk.Frame):



    def __init__(self, parent, controller):
        
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
       
        #-----title frame 
        title_frame = tk.Frame(self, width=1024, height=30, background='#212121', borderwidth = 0, highlightthickness = 0)
        title_frame.grid(row=0, column=0, sticky="ew")
        title_frame.columnconfigure(0, weight=1)
        title_frame.bind('<B1-Motion>', controller.move_event)
         
        
        #close button
        #make a frame to hold close button
        closeButtonFrame = tk.Frame(title_frame, width=30, height=30, borderwidth = 0, highlightthickness = 0) #their units in pixels
        closeButtonFrame.grid_propagate(False) #disables resizing of frame
        closeButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        closeButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        closeButtonFrame.grid(row=0, column=28, sticky="e") #put frame where the button should be

        #make actual button and grid it into frame
        closeButton = HoverButton(closeButtonFrame, text="X", fg='#00e676', command=controller.destroy, background='#212121', relief=tk.FLAT, activebackground='red')
        closeButton.config(height=1, width=2, anchor=tk.N)
        helv36 = font.Font(family='Helvetica', size=16, weight='bold')
        closeButton['font'] = helv36
        closeButton.grid(sticky="wens") #makes the button expand


        #minimize button
        minimizeButtonFrame = tk.Frame(title_frame, width=30, height=30, borderwidth = 0, highlightthickness = 0) #their units in pixels
        minimizeButtonFrame.grid_propagate(False) #disables resizing of frame
        minimizeButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        minimizeButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        minimizeButtonFrame.grid(row=0, column=27, sticky="e") #put frame where the button should be

        minimizeButton = HoverButton(minimizeButtonFrame, text="–", fg='#00e676', command=controller.lower, background='#212121', relief=tk.FLAT, activebackground='#1a75ff')
        minimizeButton.config(height=1, width=2, anchor=tk.N)
        helv36 = font.Font(family='Helvetica', size=16, weight='bold')
        minimizeButton['font'] = helv36
        minimizeButton.grid(sticky="wens") #makes the button expand


        #add icon to title bar
        iconFrame = tk.Frame(title_frame, width=30, height=30, borderwidth = 0, highlightthickness = 0)
        iconFrame.grid(row=0, column=0)

        iconCanvas = tk.Canvas(iconFrame, width=26, height=26, bd=0, highlightthickness=0)
        #lol this almost did not work
        #The variable img is a local variable which gets garbage collected 
        # after the class is instantiated. Save a reference to the photo
        self.img = ImageTk.PhotoImage(Image.open(".\\gui\\icons\\home.png").resize((26, 26)))
        iconCanvas.create_image(0, 0, image=self.img, anchor="nw")
        iconCanvas.grid(row=0, column=0)
        iconCanvas.bind('<B1-Motion>', controller.move_event)


        #add application name to title bar
        appNameFrame = tk.Frame(title_frame, width=934, height=30, borderwidth = 0, highlightthickness = 0)
        appNameFrame.bind('<B1-Motion>', controller.move_event)
        appNameFrame.grid(row=0, column=1)

        #create canvas for holding app name
        imageCanvas = HoverCanvas(appNameFrame, '#23272A', bg='#212121', width=934, height=30, bd=0, highlightthickness=0)
        imageCanvas.bind('<B1-Motion>', controller.move_event)
        imageCanvas.grid(row=0, column=1)

        #add actual app name to canvas
        imageCanvas.create_text(122, 15, fill="#00e676", activefill='#18ffff', font="Helvetica 12 bold", text="Start - Soccer Data Scraper v1.0")
        

        #----create frame to store content of window
        self.contentFrame = tk.Frame(self, width=1024, height=570, background='#303030', borderwidth = 0, highlightthickness = 0)
        self.contentFrame.grid(row=1, column=0)

        #create canvas on which actual content would be added
        self.contentCanvas = HoverCanvas(self.contentFrame, '#303030', bg='#2C2F33', width=1024, height=520, bd=0, highlightthickness=0)
        self.contentCanvas.grid(row=0, column=0)
        


        #add frame content here

        #dark icons initialization
        self.pliconDark = ImageTk.PhotoImage(Image.open(".\\gui\\icons\\pldark.png").resize((30, 30)))
        self.lliconDark = ImageTk.PhotoImage(Image.open(".\\gui\\icons\\lldark.png").resize((30, 30)))
        self.saIconDark = ImageTk.PhotoImage(Image.open(".\\gui\\icons\\sadark.png").resize((50, 25)))
        self.bliconDark = ImageTk.PhotoImage(Image.open(".\\gui\\icons\\bldark.png").resize((36, 25)))


        #create rectangle to hold tab like buttons
        self.contentCanvas.create_rectangle(0, 0, 1024, 80, fill='#363636', activefill='#2C2F33', outline='#333333')

        #premier league button
        plButtonFrame = tk.Frame(self.contentFrame, width=256, height=60, borderwidth = 0, highlightthickness = 0) #their units in pixels
        plButtonFrame.grid_propagate(False) #disables resizing of frame
        plButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        plButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        plButtonFrame.grid(row=0, column=0) #put frame where the button should be

        self.plicon = ImageTk.PhotoImage(Image.open(".\\gui\\icons\\pl1.png").resize((30, 30)))
        plButton = HoverButton(plButtonFrame, text='Premier League', fg='#606060', background='#3D1958', relief=tk.FLAT, activebackground='#304FFE', command=lambda:self.press_premier_league())
        plButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        plButton['font'] = verdana
        plButton.configure(compound=tk.LEFT, image=self.plicon, width=256, height=60)
        plButton = self.contentCanvas.create_window(0, 10, anchor=tk.NW, window=plButtonFrame)


        #la liga button
        llButtonFrame = tk.Frame(self.contentFrame, width=256, height=60, borderwidth = 0, highlightthickness = 0) #their units in pixels
        llButtonFrame.grid_propagate(False) #disables resizing of frame
        llButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        llButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        llButtonFrame.grid(row=0, column=0) #put frame where the button should be

        self.llicon = ImageTk.PhotoImage(Image.open(".\\gui\\icons\\ll1.png").resize((30, 30)))
        llButton = HoverButton(llButtonFrame, text='La Liga', background='#00AA00', relief=tk.FLAT, activebackground='#304FFE', command=lambda:self.press_la_liga())
        llButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        llButton['font'] = verdana
        llButton.configure(compound=tk.LEFT, image=self.llicon, width=256, height=60)
        llButton = self.contentCanvas.create_window(256, 10, anchor=tk.NW, window=llButtonFrame)


        #serie a button
        saButtonFrame = tk.Frame(self.contentFrame, width=256, height=60, borderwidth = 0, highlightthickness = 0) #their units in pixels
        saButtonFrame.grid_propagate(False) #disables resizing of frame
        saButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        saButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        saButtonFrame.grid(row=0, column=0) #put frame where the button should be

        self.saIcon = ImageTk.PhotoImage(Image.open(".\\gui\\icons\\sa1.png").resize((50, 25)))
        saButton = HoverButton(saButtonFrame, text='Serie A', background='#0068A8', relief=tk.FLAT, activebackground='#304FFE', command=lambda:self.press_serie_a())
        saButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        saButton['font'] = verdana
        saButton.configure(compound=tk.LEFT, image=self.saIcon, width=256, height=60)
        saButton = self.contentCanvas.create_window(512, 10, anchor=tk.NW, window=saButtonFrame)


        #bundesliga button
        blButtonFrame = tk.Frame(self.contentFrame, width=256, height=60, borderwidth = 0, highlightthickness = 0) #their units in pixels
        blButtonFrame.grid_propagate(False) #disables resizing of frame
        blButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        blButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        blButtonFrame.grid(row=0, column=0) #put frame where the button should be

        self.blicon = ImageTk.PhotoImage(Image.open(".\\gui\\icons\\bl1.png").resize((36, 25)))
        blButton = HoverButton(blButtonFrame, text='Bundesliga', background='#D3010C', relief=tk.FLAT, activebackground='#304FFE', command=lambda:self.press_bundesliga())
        blButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        blButton['font'] = verdana
        blButton.configure(compound=tk.LEFT, image=self.blicon, width=256, height=60)
        blButton = self.contentCanvas.create_window(768, 10, anchor=tk.NW, window=blButtonFrame)


        #-----create various buttons for navigating to different frames

        #create appropriate sized frame for canvas
        navigationCanvasFrame = tk.Frame(self, width=1024, height=50, background='#2C2F33', borderwidth = 0, highlightthickness = 0)
        navigationCanvasFrame.grid(row=2, column=0)

        #create canvas and put it in above frame
        navigationCanvas = HoverCanvas(navigationCanvasFrame, '#2C2F33', bg='#363636', width=1024, height=50, bd=0, highlightthickness=0)
        navigationCanvas.grid(row=0, column=0)
        
        #'navigate to' text
        navigationCanvas.create_text(80, 25, fill="#00e676", activefill='#18ffff', font="verdana 12 bold", text="Navigate to")
        
        #place button in canvas

        #home button
        homeButtonFrame = tk.Frame(navigationCanvasFrame, width=80, height=30, borderwidth = 0, highlightthickness = 0) #their units in pixels
        homeButtonFrame.grid_propagate(False) #disables resizing of frame
        homeButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        homeButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        homeButtonFrame.grid(row=0, column=0) #put frame where the button should be

        homeButton = HoverButton(homeButtonFrame, text='Home', background='#AA00FF', relief=tk.FLAT, activebackground='#304FFE', command=lambda:controller.show_frame("HomePage"))
        homeButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        homeButton['font'] = verdana
        homeButton.configure(width=30, height=8)
        navigationCanvas.create_window(155, 10, anchor=tk.NW, window=homeButtonFrame)


        #about button
        aboutButtonFrame = tk.Frame(navigationCanvasFrame, width=80, height=30, borderwidth = 0, highlightthickness = 0) #their units in pixels
        aboutButtonFrame.grid_propagate(False) #disables resizing of frame
        aboutButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        aboutButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        aboutButtonFrame.grid(row=0, column=0) #put frame where the button should be
        
        aboutButton = HoverButton(aboutButtonFrame, text='About', background='#d50000', relief=tk.FLAT, activebackground='#ff3d00', command=lambda:controller.show_frame("AboutPage"))
        aboutButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        aboutButton['font'] = verdana
        aboutButton.configure(width=30, height=8)
        navigationCanvas.create_window(265, 10, anchor=tk.NW, window=aboutButtonFrame)


        #Acknowledgements page button
        acknowledgementButtonFrame = tk.Frame(navigationCanvasFrame, width=200, height=30, borderwidth = 0, highlightthickness = 0) #their units in pixels
        acknowledgementButtonFrame.grid_propagate(False) #disables resizing of frame
        acknowledgementButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        acknowledgementButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        acknowledgementButtonFrame.grid(row=0, column=0) #put frame where the button should be

        acknowledgementButton = HoverButton(acknowledgementButtonFrame, text='Acknowledgements', background='#FFCC33', relief=tk.FLAT, activebackground='#ffff8d', command=lambda:controller.show_frame("AcknowledgementPage"))
        acknowledgementButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        acknowledgementButton['font'] = verdana
        acknowledgementButton.configure(width=60, height=8)
        navigationCanvas.create_window(375, 10, anchor=tk.NW, window=acknowledgementButtonFrame)

    


    def set_season(self, season):
        print(f'{season} selected.')
        print(f'{self.league} selected.')
        self.season = season

        pageScraper = Page.Page(self.season, self.league, self.seasons)

        print(f"Scraping data from page '{self.season}'...")
        page = pageScraper.get_data(dump=True)
        print('Scraped data successfully..!')


        plot = Plot.Plot() 

        print(f"Plotting report for '{self.season}'...")
        plot.plot_single_season_report(page, self.season, self.league, self.seasons, dump=True)
        print('Graph plotted successfully..!')

        import os
        cwd = os.getcwd()
        cef.Initialize()
        cef.CreateBrowserSync(url=f'{cwd}\\dumps\\reports\\{self.league}\\{self.season}.html', 
                            window_title='test')
        cef.MessageLoop()
        #cef.Shutdown()




    def press_premier_league(self):
        '''Action to do after premier league button is pressed
        '''

        #clear content canvas
        self.contentCanvas.delete("all")


        #redraw canvas with premier league content

        #create rectangle to hold tab like buttons
        self.contentCanvas.create_rectangle(0, 0, 1024, 80, fill='#363636', activefill='#2C2F33', outline='#333333')

        #premier league button
        plButtonFrame = tk.Frame(self.contentFrame, width=256, height=60, borderwidth = 0, highlightthickness = 0) #their units in pixels
        plButtonFrame.grid_propagate(False) #disables resizing of frame
        plButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        plButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        plButtonFrame.grid(row=0, column=0) #put frame where the button should be

        plButton = HoverButton(plButtonFrame, fg='#606060', text='Premier League', background='#3D1958',  relief=tk.SUNKEN, activebackground='#3D1958', command=lambda:self.press_premier_league())
        plButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        plButton['font'] = verdana
        plButton.configure(compound=tk.LEFT, image=self.plicon, width=256, height=60)
        plButton = self.contentCanvas.create_window(0, 10, anchor=tk.NW, window=plButtonFrame)


        #la liga button
        llButtonFrame = tk.Frame(self.contentFrame, width=256, height=60, borderwidth = 0, highlightthickness = 0) #their units in pixels
        llButtonFrame.grid_propagate(False) #disables resizing of frame
        llButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        llButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        llButtonFrame.grid(row=0, column=0) #put frame where the button should be

        llButton = HoverButton(llButtonFrame, text='La Liga', background='#2C2F33', relief=tk.FLAT, activebackground='#00aa00', command=lambda:self.press_la_liga())
        llButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        llButton['font'] = verdana
        llButton.configure(compound=tk.LEFT, image=self.lliconDark, width=256, height=60)
        llButton = self.contentCanvas.create_window(256, 10, anchor=tk.NW, window=llButtonFrame)


        #serie a button
        saButtonFrame = tk.Frame(self.contentFrame, width=256, height=60, borderwidth = 0, highlightthickness = 0) #their units in pixels
        saButtonFrame.grid_propagate(False) #disables resizing of frame
        saButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        saButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        saButtonFrame.grid(row=0, column=0) #put frame where the button should be

        saButton = HoverButton(saButtonFrame, text='Serie A', background='#2C2F33', relief=tk.FLAT, activebackground='#0068a8', command=lambda:self.press_serie_a())
        saButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        saButton['font'] = verdana
        saButton.configure(compound=tk.LEFT, image=self.saIconDark, width=256, height=60)
        saButton = self.contentCanvas.create_window(512, 10, anchor=tk.NW, window=saButtonFrame)


        #bundesliga button
        blButtonFrame = tk.Frame(self.contentFrame, width=256, height=60, borderwidth = 0, highlightthickness = 0) #their units in pixels
        blButtonFrame.grid_propagate(False) #disables resizing of frame
        blButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        blButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        blButtonFrame.grid(row=0, column=0) #put frame where the button should be

        blButton = HoverButton(blButtonFrame, text='Bundesliga', background='#2C2F33', relief=tk.FLAT, activebackground='#d3010c', command=lambda:self.press_bundesliga())
        blButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        blButton['font'] = verdana
        blButton.configure(compound=tk.LEFT, image=self.bliconDark, width=256, height=60)
        blButton = self.contentCanvas.create_window(768, 10, anchor=tk.NW, window=blButtonFrame)
        

        #action after pressing premier league button
        #draw content here
        
        optionMenuFrame = tk.Frame(self.contentFrame, width=800, height=70, bg='#303030', borderwidth = 0, highlightthickness = 0) #their units in pixels
        optionMenuFrame.grid_propagate(False) #disables resizing of frame
        optionMenuFrame.columnconfigure(0, weight=1) #enables button to fill frame
        optionMenuFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        optionMenuFrame.grid(row=0, column=0) #put frame where the button should be
        
        var = tk.StringVar()
        var.set('Select season')

        self.league = 'pl'
        categoryScraper = Category.Category()

        print('Getting available seasons..') 
        self.seasons = categoryScraper.get_league_seasons(self.league)
        print('Recieved seasons..!')

        seasonNames = list(self.seasons.keys())
        option = tk.OptionMenu(optionMenuFrame, var, *seasonNames, command=self.set_season)
        verdana = font.Font(family='verdana', size=16, weight='bold')
        option.config(width=120, height=2, fg='#606060', bg='#252525', borderwidth=0, bd=0, activebackground='#3d1958', font=verdana)
        option['highlightthickness'] = 0
        option['menu'].config(bg='#363636', fg='#606060', activebackground='#3d1958', bd=0, borderwidth=0, font=verdana)
        option.grid(row=0, column=0)

        self.contentCanvas.create_window(102, 240, anchor=tk.NW, window=optionMenuFrame)

    
    

    def press_la_liga(self):
        '''Actions after la liga button is pressed
        '''

        #clear content canvas
        self.contentCanvas.delete("all")


        #redraw canvas with premier league content

        #create rectangle to hold tab like buttons
        self.contentCanvas.create_rectangle(0, 0, 1024, 80, fill='#363636', activefill='#2C2F33', outline='#333333')

        #premier league button
        plButtonFrame = tk.Frame(self.contentFrame, width=256, height=60, borderwidth = 0, highlightthickness = 0) #their units in pixels
        plButtonFrame.grid_propagate(False) #disables resizing of frame
        plButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        plButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        plButtonFrame.grid(row=0, column=0) #put frame where the button should be

        plButton = HoverButton(plButtonFrame, text='Premier League', background='#2C2F33',  relief=tk.FLAT, activebackground='#3d1958', command=lambda:self.press_premier_league())
        plButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        plButton['font'] = verdana
        plButton.configure(compound=tk.LEFT, image=self.pliconDark, width=256, height=60)
        plButton = self.contentCanvas.create_window(0, 10, anchor=tk.NW, window=plButtonFrame)


        #la liga button
        llButtonFrame = tk.Frame(self.contentFrame, width=256, height=60, borderwidth = 0, highlightthickness = 0) #their units in pixels
        llButtonFrame.grid_propagate(False) #disables resizing of frame
        llButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        llButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        llButtonFrame.grid(row=0, column=0) #put frame where the button should be

        llButton = HoverButton(llButtonFrame, text='La Liga', background='#00aa00', relief=tk.SUNKEN, activebackground='#00aa00', command=lambda:self.press_la_liga())
        llButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        llButton['font'] = verdana
        llButton.configure(compound=tk.LEFT, image=self.llicon, width=256, height=60)
        llButton = self.contentCanvas.create_window(256, 10, anchor=tk.NW, window=llButtonFrame)


        #serie a button
        saButtonFrame = tk.Frame(self.contentFrame, width=256, height=60, borderwidth = 0, highlightthickness = 0) #their units in pixels
        saButtonFrame.grid_propagate(False) #disables resizing of frame
        saButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        saButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        saButtonFrame.grid(row=0, column=0) #put frame where the button should be

        saButton = HoverButton(saButtonFrame, text='Serie A', background='#2C2F33', relief=tk.FLAT, activebackground='#0068a8', command=lambda:self.press_serie_a())
        saButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        saButton['font'] = verdana
        saButton.configure(compound=tk.LEFT, image=self.saIconDark, width=256, height=60)
        saButton = self.contentCanvas.create_window(512, 10, anchor=tk.NW, window=saButtonFrame)


        #bundesliga button
        blButtonFrame = tk.Frame(self.contentFrame, width=256, height=60, borderwidth = 0, highlightthickness = 0) #their units in pixels
        blButtonFrame.grid_propagate(False) #disables resizing of frame
        blButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        blButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        blButtonFrame.grid(row=0, column=0) #put frame where the button should be

        blButton = HoverButton(blButtonFrame, text='Bundesliga', background='#2C2F33', relief=tk.FLAT, activebackground='#d3010c', command=lambda:self.press_bundesliga())
        blButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        blButton['font'] = verdana
        blButton.configure(compound=tk.LEFT, image=self.bliconDark, width=256, height=60)
        blButton = self.contentCanvas.create_window(768, 10, anchor=tk.NW, window=blButtonFrame)
        

        #action after pressing la liga button
        #draw content here

        optionMenuFrame = tk.Frame(self.contentFrame, width=800, height=70, bg='#303030', borderwidth = 0, highlightthickness = 0) #their units in pixels
        optionMenuFrame.grid_propagate(False) #disables resizing of frame
        optionMenuFrame.columnconfigure(0, weight=1) #enables button to fill frame
        optionMenuFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        optionMenuFrame.grid(row=0, column=0) #put frame where the button should be
        
        var = tk.StringVar()
        var.set('Select season')

        self.league = 'll'
        categoryScraper = Category.Category()

        print('Getting available seasons..') 
        self.seasons = categoryScraper.get_league_seasons(self.league)
        print('Recieved seasons..!')

        seasonNames = list(self.seasons.keys())
        option = tk.OptionMenu(optionMenuFrame, var, *seasonNames, command=self.set_season)
        verdana = font.Font(family='verdana', size=16, weight='bold')
        option.config(width=120, height=2, fg='#606060', bg='#252525', borderwidth=0, bd=0, activebackground='#00aa00', font=verdana)
        option['highlightthickness'] = 0
        option['menu'].config(bg='#363636', fg='#606060', activebackground='#00aa00', bd=0, borderwidth=0, font=verdana)
        option.grid(row=0, column=0)

        self.contentCanvas.create_window(102, 240, anchor=tk.NW, window=optionMenuFrame)




    def press_serie_a(self):
        '''Actions after Serie A button is pressed
        '''

        #clear content canvas
        self.contentCanvas.delete("all")


        #redraw canvas with premier league content

        #create rectangle to hold tab like buttons
        self.contentCanvas.create_rectangle(0, 0, 1024, 80, fill='#363636', activefill='#2C2F33', outline='#333333')

        #premier league button
        plButtonFrame = tk.Frame(self.contentFrame, width=256, height=60, borderwidth = 0, highlightthickness = 0) #their units in pixels
        plButtonFrame.grid_propagate(False) #disables resizing of frame
        plButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        plButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        plButtonFrame.grid(row=0, column=0) #put frame where the button should be

        plButton = HoverButton(plButtonFrame, text='Premier League', background='#2C2F33',  relief=tk.FLAT, activebackground='#3d1958', command=lambda:self.press_premier_league())
        plButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        plButton['font'] = verdana
        plButton.configure(compound=tk.LEFT, image=self.pliconDark, width=256, height=60)
        plButton = self.contentCanvas.create_window(0, 10, anchor=tk.NW, window=plButtonFrame)


        #la liga button
        llButtonFrame = tk.Frame(self.contentFrame, width=256, height=60, borderwidth = 0, highlightthickness = 0) #their units in pixels
        llButtonFrame.grid_propagate(False) #disables resizing of frame
        llButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        llButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        llButtonFrame.grid(row=0, column=0) #put frame where the button should be

        llButton = HoverButton(llButtonFrame, text='La Liga', background='#2C2F33', relief=tk.FLAT, activebackground='#00aa00', command=lambda:self.press_la_liga())
        llButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        llButton['font'] = verdana
        llButton.configure(compound=tk.LEFT, image=self.lliconDark, width=256, height=60)
        llButton = self.contentCanvas.create_window(256, 10, anchor=tk.NW, window=llButtonFrame)


        #serie a button
        saButtonFrame = tk.Frame(self.contentFrame, width=256, height=60, borderwidth = 0, highlightthickness = 0) #their units in pixels
        saButtonFrame.grid_propagate(False) #disables resizing of frame
        saButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        saButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        saButtonFrame.grid(row=0, column=0) #put frame where the button should be

        saButton = HoverButton(saButtonFrame, text='Serie A', background='#0068A8', relief=tk.SUNKEN, activebackground='#0068a8', command=lambda:self.press_serie_a())
        saButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        saButton['font'] = verdana
        saButton.configure(compound=tk.LEFT, image=self.saIcon, width=256, height=60)
        saButton = self.contentCanvas.create_window(512, 10, anchor=tk.NW, window=saButtonFrame)


        #bundesliga button
        blButtonFrame = tk.Frame(self.contentFrame, width=256, height=60, borderwidth = 0, highlightthickness = 0) #their units in pixels
        blButtonFrame.grid_propagate(False) #disables resizing of frame
        blButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        blButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        blButtonFrame.grid(row=0, column=0) #put frame where the button should be

        blButton = HoverButton(blButtonFrame, text='Bundesliga', background='#2C2F33', relief=tk.FLAT, activebackground='#d3010c', command=lambda:self.press_bundesliga())
        blButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        blButton['font'] = verdana
        blButton.configure(compound=tk.LEFT, image=self.bliconDark, width=256, height=60)
        blButton = self.contentCanvas.create_window(768, 10, anchor=tk.NW, window=blButtonFrame)
        

        #action after pressing serie a button
        #draw content here

        optionMenuFrame = tk.Frame(self.contentFrame, width=800, height=70, bg='#303030', borderwidth = 0, highlightthickness = 0) #their units in pixels
        optionMenuFrame.grid_propagate(False) #disables resizing of frame
        optionMenuFrame.columnconfigure(0, weight=1) #enables button to fill frame
        optionMenuFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        optionMenuFrame.grid(row=0, column=0) #put frame where the button should be


        var = tk.StringVar()
        var.set('Select season')

        self.league = 'sa'
        categoryScraper = Category.Category()

        print('Getting available seasons..') 
        self.seasons = categoryScraper.get_league_seasons(self.league)
        print('Recieved seasons..!')

        seasonNames = list(self.seasons.keys())[6:]
        option = tk.OptionMenu(optionMenuFrame, var, *seasonNames, command=self.set_season)
        verdana = font.Font(family='verdana', size=16, weight='bold')
        option.config(width=120, height=2, fg='#606060', bg='#252525', borderwidth=0, bd=0, activebackground='#0068a8', font=verdana)
        option['highlightthickness'] = 0
        option['menu'].config(bg='#363636', fg='#606060', activebackground='#0068a8', bd=0, borderwidth=0, font=verdana)
        option.grid(row=0, column=0)

        self.contentCanvas.create_window(102, 240, anchor=tk.NW, window=optionMenuFrame)




    def press_bundesliga(self):
        '''Actions after pressing Bundesliga button
        '''

        #clear content canvas
        self.contentCanvas.delete("all")


        #redraw canvas with premier league content

        #create rectangle to hold tab like buttons
        self.contentCanvas.create_rectangle(0, 0, 1024, 80, fill='#363636', activefill='#2C2F33', outline='#333333')

        #premier league button
        plButtonFrame = tk.Frame(self.contentFrame, width=256, height=60, borderwidth = 0, highlightthickness = 0) #their units in pixels
        plButtonFrame.grid_propagate(False) #disables resizing of frame
        plButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        plButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        plButtonFrame.grid(row=0, column=0) #put frame where the button should be

        plButton = HoverButton(plButtonFrame, text='Premier League', background='#2C2F33',  relief=tk.FLAT, activebackground='#3d1958', command=lambda:self.press_premier_league())
        plButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        plButton['font'] = verdana
        plButton.configure(compound=tk.LEFT, image=self.pliconDark, width=256, height=60)
        plButton = self.contentCanvas.create_window(0, 10, anchor=tk.NW, window=plButtonFrame)


        #la liga button
        llButtonFrame = tk.Frame(self.contentFrame, width=256, height=60, borderwidth = 0, highlightthickness = 0) #their units in pixels
        llButtonFrame.grid_propagate(False) #disables resizing of frame
        llButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        llButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        llButtonFrame.grid(row=0, column=0) #put frame where the button should be

        llButton = HoverButton(llButtonFrame, text='La Liga', background='#2C2F33', relief=tk.FLAT, activebackground='#00aa00', command=lambda:self.press_la_liga())
        llButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        llButton['font'] = verdana
        llButton.configure(compound=tk.LEFT, image=self.lliconDark, width=256, height=60)
        llButton = self.contentCanvas.create_window(256, 10, anchor=tk.NW, window=llButtonFrame)


        #serie a button
        saButtonFrame = tk.Frame(self.contentFrame, width=256, height=60, borderwidth = 0, highlightthickness = 0) #their units in pixels
        saButtonFrame.grid_propagate(False) #disables resizing of frame
        saButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        saButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        saButtonFrame.grid(row=0, column=0) #put frame where the button should be

        saButton = HoverButton(saButtonFrame, text='Serie A', background='#2C2F33', relief=tk.FLAT, activebackground='#0068a8', command=lambda:self.press_serie_a())
        saButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        saButton['font'] = verdana
        saButton.configure(compound=tk.LEFT, image=self.saIconDark, width=256, height=60)
        saButton = self.contentCanvas.create_window(512, 10, anchor=tk.NW, window=saButtonFrame)


        #bundesliga button
        blButtonFrame = tk.Frame(self.contentFrame, width=256, height=60, borderwidth = 0, highlightthickness = 0) #their units in pixels
        blButtonFrame.grid_propagate(False) #disables resizing of frame
        blButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        blButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        blButtonFrame.grid(row=0, column=0) #put frame where the button should be

        blButton = HoverButton(blButtonFrame, text='Bundesliga', background='#D3010C', relief=tk.SUNKEN, activebackground='#d3010c', command=lambda:self.press_bundesliga())
        blButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        blButton['font'] = verdana
        blButton.configure(compound=tk.LEFT, image=self.blicon, width=256, height=60)
        blButton = self.contentCanvas.create_window(768, 10, anchor=tk.NW, window=blButtonFrame)
        

        #action after pressing serie a button
        #draw content here

        optionMenuFrame = tk.Frame(self.contentFrame, width=800, height=70, bg='#303030', borderwidth = 0, highlightthickness = 0) #their units in pixels
        optionMenuFrame.grid_propagate(False) #disables resizing of frame
        optionMenuFrame.columnconfigure(0, weight=1) #enables button to fill frame
        optionMenuFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        optionMenuFrame.grid(row=0, column=0) #put frame where the button should be

        var = tk.StringVar()
        var.set('Select season')

        self.league = 'bl'
        categoryScraper = Category.Category()

        print('Getting available seasons..') 
        self.seasons = categoryScraper.get_league_seasons(self.league)
        print('Recieved seasons..!')

        seasonNames = list(self.seasons.keys())
        option = tk.OptionMenu(optionMenuFrame, var, *seasonNames, command=self.set_season)
        verdana = font.Font(family='verdana', size=16, weight='bold')
        option.config(width=120, height=2, fg='#606060', bg='#252525', borderwidth=0, bd=0, activebackground='#d3010c', font=verdana)
        option['highlightthickness'] = 0
        option['menu'].config(bg='#363636', fg='#606060', activebackground='#d3010c', bd=0, borderwidth=0, font=verdana)
        option.grid(row=0, column=0)

        self.contentCanvas.create_window(102, 240, anchor=tk.NW, window=optionMenuFrame)






class AboutPage(tk.Frame):



    def __init__(self, parent, controller):


        tk.Frame.__init__(self, parent)
        self.controller = controller


        #-----title frame 
        title_frame = tk.Frame(self, width=1024, height=30, background='#212121', borderwidth = 0, highlightthickness = 0)
        title_frame.grid(row=0, column=0, sticky="ew")
        title_frame.columnconfigure(0, weight=1)
        title_frame.bind('<B1-Motion>', controller.move_event)
    
        
        #close button

        #make a frame to hold close button
        closeButtonFrame = tk.Frame(title_frame, width=30, height=30, borderwidth = 0, highlightthickness = 0) #their units in pixels
        closeButtonFrame.grid_propagate(False) #disables resizing of frame
        closeButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        closeButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        closeButtonFrame.grid(row=0, column=28, sticky="e") #put frame where the button should be

        #make actual button and grid it into frame
        closeButton = HoverButton(closeButtonFrame, text="X", fg='#d50000', command=controller.destroy, background='#212121', relief=tk.FLAT, activebackground='red')
        closeButton.config(height=1, width=2, anchor=tk.N)
        helv36 = font.Font(family='Helvetica', size=16, weight='bold')
        closeButton['font'] = helv36
        closeButton.grid(sticky="wens") #makes the button expand


        #----minimize button
        minimizeButtonFrame = tk.Frame(title_frame, width=30, height=30, borderwidth = 0, highlightthickness = 0) #their units in pixels
        minimizeButtonFrame.grid_propagate(False) #disables resizing of frame
        minimizeButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        minimizeButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        minimizeButtonFrame.grid(row=0, column=27, sticky="e") #put frame where the button should be

        minimizeButton = HoverButton(minimizeButtonFrame, text="–", fg='#d50000', command=controller.lower, background='#212121', relief=tk.FLAT, activebackground='#1a75ff')
        minimizeButton.config(height=1, width=2, anchor=tk.N)
        helv36 = font.Font(family='Helvetica', size=16, weight='bold')
        minimizeButton['font'] = helv36
        minimizeButton.grid(sticky="wens") #makes the button expand


        #add icon to title bar
        iconFrame = tk.Frame(title_frame, width=30, height=30, borderwidth = 0, highlightthickness = 0)
        iconFrame.grid(row=0, column=0)

        iconCanvas = tk.Canvas(iconFrame, width=26, height=26, bd=0, highlightthickness=0)
        self.img = ImageTk.PhotoImage(Image.open(".\\gui\\icons\\home.png").resize((26, 26)))
        iconCanvas.create_image(0, 0, image=self.img, anchor="nw")
        iconCanvas.grid(row=0, column=0)
        iconCanvas.bind('<B1-Motion>', controller.move_event)


        #add application name to title bar
        appNameFrame = tk.Frame(title_frame, width=934, height=30, borderwidth = 0, highlightthickness = 0)
        appNameFrame.bind('<B1-Motion>', controller.move_event)
        appNameFrame.grid(row=0, column=1)

        #create canvas for holding app name
        imageCanvas = HoverCanvas(appNameFrame, '#23272A', bg='#212121', width=934, height=30, bd=0, highlightthickness=0)
        imageCanvas.bind('<B1-Motion>', controller.move_event)
        imageCanvas.grid(row=0, column=1)

        #add actual app name to canvas
        imageCanvas.create_text(128, 15, fill="#d50000", activefill='#ff3d00', font="Helvetica 12 bold", text="About - Soccer Data Scraper v1.0")
        

        #create frame to store content of window
        contentFrame = tk.Frame(self, width=1024, height=570, background='#303030', borderwidth = 0, highlightthickness = 0)
        contentFrame.grid(row=1, column=0)

        #create canvas on which actual content would be added
        contentCanvas = HoverCanvas(contentFrame, '#303030', bg='#2C2F33', width=1024, height=520, bd=0, highlightthickness=0)
        contentCanvas.grid(row=0, column=0)

        
        #add frame content here


        #-----create various buttons for navigating to different frames

        #create appropriate sized frame for canvas
        navigationCanvasFrame = tk.Frame(self, width=1024, height=50, background='#2C2F33', borderwidth = 0, highlightthickness = 0)
        navigationCanvasFrame.grid(row=2, column=0)

        #create canvas and put it in above frame
        navigationCanvas = HoverCanvas(navigationCanvasFrame, '#333333', bg='#2C2F33', width=1024, height=50, bd=0, highlightthickness=0)
        navigationCanvas.grid(row=0, column=0)

        #'navigate to' text
        navigationCanvas.create_text(80, 25, fill="#d50000", activefill='#ff3d00', font="verdana 12 bold", text="Navigate to")

        #place button in canvas

        #start button
        startButtonFrame = tk.Frame(navigationCanvasFrame, width=80, height=30, borderwidth = 0, highlightthickness = 0) #their units in pixels
        startButtonFrame.grid_propagate(False) #disables resizing of frame
        startButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        startButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        startButtonFrame.grid(row=0, column=0) #put frame where the button should be

        startButton = HoverButton(startButtonFrame, text='Start', background='#00e676', relief=tk.FLAT, activebackground='#18ffff', command=lambda:controller.show_frame("StartPage"))
        startButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        startButton['font'] = verdana
        startButton.configure(width=30, height=8)
        navigationCanvas.create_window(155, 10, anchor=tk.NW, window=startButtonFrame)

        #home button
        homeButtonFrame = tk.Frame(navigationCanvasFrame, width=80, height=30, borderwidth = 0, highlightthickness = 0) #their units in pixels
        homeButtonFrame.grid_propagate(False) #disables resizing of frame
        homeButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        homeButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        homeButtonFrame.grid(row=0, column=0) #put frame where the button should be

        homeButton = HoverButton(homeButtonFrame, text='Home', background='#AA00FF', relief=tk.FLAT, activebackground='#304FFE', command=lambda:controller.show_frame("HomePage"))
        homeButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        homeButton['font'] = verdana
        homeButton.configure(width=30, height=8)
        navigationCanvas.create_window(265, 10, anchor=tk.NW, window=homeButtonFrame)

        #Acknowledgements page button
        acknowledgementButtonFrame = tk.Frame(navigationCanvasFrame, width=200, height=30, borderwidth = 0, highlightthickness = 0) #their units in pixels
        acknowledgementButtonFrame.grid_propagate(False) #disables resizing of frame
        acknowledgementButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        acknowledgementButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        acknowledgementButtonFrame.grid(row=0, column=0) #put frame where the button should be

        acknowledgementButton = HoverButton(acknowledgementButtonFrame, text='Acknowledgements', background='#FFCC33', relief=tk.FLAT, activebackground='#ffff8d', command=lambda:controller.show_frame("AcknowledgementPage"))
        acknowledgementButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        acknowledgementButton['font'] = verdana
        acknowledgementButton.configure(width=60, height=8)
        navigationCanvas.create_window(375, 10, anchor=tk.NW, window=acknowledgementButtonFrame)






class AcknowledgementPage(tk.Frame):



    def __init__(self, parent, controller):


        tk.Frame.__init__(self, parent)
        self.controller = controller


        #-----title frame 
        title_frame = tk.Frame(self, width=1024, height=30, background='#212121', borderwidth = 0, highlightthickness = 0)
        title_frame.grid(row=0, column=0, sticky="ew")
        title_frame.columnconfigure(0, weight=1)
        title_frame.bind('<B1-Motion>', controller.move_event)
    
        
        #close button

        #make a frame to hold close button
        closeButtonFrame = tk.Frame(title_frame, width=30, height=30, borderwidth = 0, highlightthickness = 0) #their units in pixels
        closeButtonFrame.grid_propagate(False) #disables resizing of frame
        closeButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        closeButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        closeButtonFrame.grid(row=0, column=28, sticky="e") #put frame where the button should be

        #make actual button and grid it into frame
        closeButton = HoverButton(closeButtonFrame, text="X", fg='#FFCC33', command=controller.destroy, background='#212121', relief=tk.FLAT, activebackground='red')
        closeButton.config(height=1, width=2, anchor=tk.N)
        helv36 = font.Font(family='Helvetica', size=16, weight='bold')
        closeButton['font'] = helv36
        closeButton.grid(sticky="wens") #makes the button expand


        #minimize button
        minimizeButtonFrame = tk.Frame(title_frame, width=30, height=30, borderwidth = 0, highlightthickness = 0) #their units in pixels
        minimizeButtonFrame.grid_propagate(False) #disables resizing of frame
        minimizeButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        minimizeButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        minimizeButtonFrame.grid(row=0, column=27, sticky="e") #put frame where the button should be

        minimizeButton = HoverButton(minimizeButtonFrame, text="–", fg='#FFCC33', command=controller.lower, background='#212121', relief=tk.FLAT, activebackground='#1a75ff')
        minimizeButton.config(height=1, width=2, anchor=tk.N)
        helv36 = font.Font(family='Helvetica', size=16, weight='bold')
        minimizeButton['font'] = helv36
        minimizeButton.grid(sticky="wens") #makes the button expand


        #add icon to title bar
        iconFrame = tk.Frame(title_frame, width=30, height=30, borderwidth = 0, highlightthickness = 0)
        iconFrame.grid(row=0, column=0)

        iconCanvas = tk.Canvas(iconFrame, width=26, height=26, bd=0, highlightthickness=0)
        self.img = ImageTk.PhotoImage(Image.open(".\\gui\\icons\\home.png").resize((26, 26)))
        iconCanvas.create_image(0, 0, image=self.img, anchor="nw")
        iconCanvas.grid(row=0, column=0)
        iconCanvas.bind('<B1-Motion>', controller.move_event)


        #add application name to title bar
        appNameFrame = tk.Frame(title_frame, width=934, height=30, borderwidth = 0, highlightthickness = 0)
        appNameFrame.bind('<B1-Motion>', controller.move_event)
        appNameFrame.grid(row=0, column=1)

        #create canvas for holding app name
        imageCanvas = HoverCanvas(appNameFrame, '#23272A', bg='#212121', width=934, height=30, bd=0, highlightthickness=0)
        imageCanvas.bind('<B1-Motion>', controller.move_event)
        imageCanvas.grid(row=0, column=1)

        #add actual app name to canvas
        imageCanvas.create_text(182, 15, fill="#FFCC33", activefill='#ffff8d', font="Helvetica 12 bold", text="Acknowledgements - Soccer Data Scraper v1.0")
        

        #----create frame to store content of window
        contentFrame = tk.Frame(self, width=1024, height=570, background='#000000', borderwidth = 0, highlightthickness = 0)
        contentFrame.grid(row=1, column=0)

        #create canvas on which actual content would be added
        contentCanvas = HoverCanvas(contentFrame, '#303030', bg='#2C2F33', width=1024, height=520, bd=0, highlightthickness=0)
        contentCanvas.grid(row=0, column=0)


        #add content of frame here


        #-----create various buttons for navigating to different frames

        #create appropriate sized frame for canvas
        navigationCanvasFrame = tk.Frame(self, width=1024, height=50, background='#2C2F33', borderwidth = 0, highlightthickness = 0)
        navigationCanvasFrame.grid(row=2, column=0)

        #create canvas and put it in above frame
        navigationCanvas = HoverCanvas(navigationCanvasFrame, '#333333', bg='#2C2F33', width=1024, height=50, bd=0, highlightthickness=0)
        navigationCanvas.grid(row=0, column=0)
       
        #'navigate to' text
        navigationCanvas.create_text(80, 25, fill="#FFCC33", activefill='#ffff8d', font="verdana 12 bold", text="Navigate to ")
      
        #place button in canvas
        
        #start button
        startButtonFrame = tk.Frame(navigationCanvasFrame, width=80, height=30, borderwidth = 0, highlightthickness = 0) #their units in pixels
        startButtonFrame.grid_propagate(False) #disables resizing of frame
        startButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        startButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        startButtonFrame.grid(row=0, column=0) #put frame where the button should be

        startButton = HoverButton(startButtonFrame, text='Start', background='#00e676', relief=tk.FLAT, activebackground='#18ffff', command=lambda:controller.show_frame("StartPage"))
        startButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        startButton['font'] = verdana
        startButton.configure(width=30, height=8)
        navigationCanvas.create_window(155, 10, anchor=tk.NW, window=startButtonFrame)


        #home button
        homeButtonFrame = tk.Frame(navigationCanvasFrame, width=80, height=30, borderwidth = 0, highlightthickness = 0) #their units in pixels
        homeButtonFrame.grid_propagate(False) #disables resizing of frame
        homeButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        homeButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        homeButtonFrame.grid(row=0, column=0) #put frame where the button should be

        homeButton = HoverButton(homeButtonFrame, text='Home', background='#AA00FF', relief=tk.FLAT, activebackground='#304FFE', command=lambda:controller.show_frame("HomePage"))
        homeButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        homeButton['font'] = verdana
        homeButton.configure(width=30, height=8)
        navigationCanvas.create_window(265, 10, anchor=tk.NW, window=homeButtonFrame)


        #about button
        aboutButtonFrame = tk.Frame(navigationCanvasFrame, width=80, height=30, borderwidth = 0, highlightthickness = 0) #their units in pixels
        aboutButtonFrame.grid_propagate(False) #disables resizing of frame
        aboutButtonFrame.columnconfigure(0, weight=1) #enables button to fill frame
        aboutButtonFrame.rowconfigure(0, weight=1) #any positive number would do the trick
        aboutButtonFrame.grid(row=0, column=0) #put frame where the button should be
    
        aboutButton = HoverButton(aboutButtonFrame, text='About', background='#d50000', relief=tk.FLAT, activebackground='#ff3d00', command=lambda:controller.show_frame("AboutPage"))
        aboutButton.grid(row=0, column=0)
        verdana = font.Font(family='verdana', size=12, weight='bold')
        aboutButton['font'] = verdana
        aboutButton.configure(width=30, height=8)
        navigationCanvas.create_window(375, 10, anchor=tk.NW, window=aboutButtonFrame)






if __name__ == "__main__":
    app = RunApp()
    app.after(10, lambda: app.set_appwindow())
    app.mainloop()
