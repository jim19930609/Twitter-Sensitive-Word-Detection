import shutil
import os
import time
import tkinter as tk
import signal
import subprocess

class Parameters:
  def __init__(self):
    self.switch = False
    self.twit_interval = 4
    self.stream_interval = 1
    self.filtword = 'trump'
    self.windsize = 1
    self.windslide = 1


def Clean_Files(data_dir, result_dir):
  shutil.rmtree(data_dir)
  os.mkdir(data_dir)
  shutil.rmtree(result_dir)
  os.mkdir(result_dir)


def Obtain_Filelist(root):
  file_list = [( os.stat(root+v).st_ctime, v ) for v in os.listdir(root)]
  file_list.sort()
  file_list = [v[1] for v in file_list]
  
  return file_list


def insert_parameters():
  params.twit_interval = E_twit_interval.get("1.0",tk.END)
  params.stream_interval = E_stream_interval.get("1.0",tk.END)
  params.filtword = E_filtword.get("1.0",tk.END)
  params.windsize = E_windsize.get("1.0",tk.END)
  params.windslide = E_windslide.get("1.0",tk.END)
  
  var_ti.set( "twit interval: " + str(E_twit_interval.get("1.0",tk.END)) )
  var_si.set( "stream interval: " + str(E_stream_interval.get("1.0",tk.END)) )
  var_fw.set( "filtword: " + str(E_filtword.get("1.0",tk.END)) )
  var_wsize.set( "windsize: " + str(E_windsize.get("1.0",tk.END)) )
  var_wslid.set( "windslide: " + str(E_windslide.get("1.0",tk.END)) )
  
  window.update()

def stop_streaming():
  params.switch = False


def start_streaming():
  params.switch = True
  Clean_Files(data_dir, result_dir)

  p_list = ['exec ', 'python3', 'twit_file.py', '--interval='+str(params.twit_interval), '--filtword='+str(params.filtword)]
  s_list = ['exec ', 'python3', 'streaming.py', '--interval='+str(params.stream_interval), '--windsize='+str(params.windsize), '--windslide='+str(params.windslide)]

  twit_p = subprocess.Popen(" ".join(p_list), shell=True)
  twit_s = subprocess.Popen(" ".join(s_list), shell=True)

  file_list_orig = Obtain_Filelist(data_dir)
  file_list_result = Obtain_Filelist(result_dir)
  
  if len(file_list_result) > 0:
    index_result = len(file_list_result) - 1
  else:
    index_result = -1
  
  if len(file_list_orig) > 0:
    index_orig = len(file_list_orig) - 1
  else:
    index_orig = -1
  
  while params.switch == True:
    time.sleep(4)
    file_list_orig = Obtain_Filelist(data_dir)
    file_list_result = Obtain_Filelist(result_dir)
    
    if len(file_list_orig) - 1 > index_orig:
      index_orig = len(file_list_orig) - 1
      content_orig = open(data_dir + file_list_orig[index_orig], "rb").readline().strip()
      
      var_orig.set(content_orig)
    
    if len(file_list_result) - 1 > index_result:
      index_result = len(file_list_result) - 1
      content_result = open(result_dir + file_list_result[index_result], "rb").readline().strip()
      
      var_result.set(content_result)
    
    window.update()
  
  # Stop Streaming
  var_orig.set("")
  var_result.set("")
  twit_p.kill()
  twit_s.kill()

if __name__ == "__main__":
  # Preprocess & Init
  params = Parameters()

  data_dir = "data/"
  result_dir = "result/"
  
  # Define Window Object
  window = tk.Tk()
  window.title('Test Window')
  window.geometry('1400x600')

  # Define Frame
  
  
  # Define Display Label Object
  var_orig = tk.StringVar()
  var_result = tk.StringVar()
  
  label_orig = tk.Label(window, textvariable = var_orig, bg='green', font=('Arial', 15), width=40, height=10, wraplength = 300).grid(row=0,rowspan=4,column=3,columnspan=3,pady=5,padx=20)
  label_result = tk.Label(window, textvariable = var_result, bg='blue', font=('Arial', 15), width=40, height=10, wraplength = 300).grid(row=0,rowspan=4,column=6,columnspan=3,pady=5,padx=20)
  

  # Define Input Box
  tk.Label(window, text='Twit\nInterval',     font=('Arial', 12),    width=10, height=2).grid(row=0,column=0,pady=5,padx=15)
  tk.Label(window, text='Stream\nInterval',   font=('Arial', 12),    width=10, height=2).grid(row=2,column=0,pady=5,padx=15)
  tk.Label(window, text='Filtword',           font=('Arial', 12),    width=10, height=2).grid(row=4,column=0,pady=5,padx=15)
  tk.Label(window, text='Window\nSize',       font=('Arial', 12),    width=10, height=2).grid(row=6,column=0,pady=5,padx=15)
  tk.Label(window, text='Window\nSlide',      font=('Arial', 12),    width=10, height=2).grid(row=8,column=0,pady=5,padx=15)

  E_twit_interval   = tk.Text(window, width=6, height=2, font=('Arial',10) )
  E_stream_interval = tk.Text(window, width=6, height=2, font=('Arial',10) )
  E_filtword        = tk.Text(window, width=6, height=2, font=('Arial',10) )
  E_windsize        = tk.Text(window, width=6, height=2, font=('Arial',10) )
  E_windslide       = tk.Text(window, width=6, height=2, font=('Arial',10) ) 
  
  E_twit_interval.grid(row=0,column=1,pady=20,padx=20)
  E_stream_interval.grid(row=2,column=1,pady=20,padx=20)
  E_filtword.grid(row=4,column=1,pady=20,padx=20)
  E_windsize.grid(row=6,column=1,pady=20,padx=20)
  E_windslide.grid(row=8,column=1,pady=20,padx=20) 
  
  var_ti = tk.StringVar()
  var_si = tk.StringVar()
  var_fw = tk.StringVar()
  var_wsize = tk.StringVar()
  var_wslid = tk.StringVar()
  
  var_ti.set("2")
  var_si.set("1")
  var_fw.set("trump")
  var_wsize.set("1")
  var_wslid.set("1")

  T_twit_interval   = tk.Label(window, textvariable = var_ti, bg='gray', font=('Arial', 10),    width=8, height=2).grid(row=0,column=2,pady=5,padx=30)
  T_stream_interval = tk.Label(window, textvariable = var_si, bg='gray', font=('Arial', 10),    width=8, height=2).grid(row=2,column=2,pady=5,padx=30)
  T_filtword        = tk.Label(window, textvariable = var_fw, bg='gray', font=('Arial', 10),    width=8, height=2).grid(row=4,column=2,pady=5,padx=30)
  T_windsize        = tk.Label(window, textvariable = var_wsize, bg='gray', font=('Arial', 10), width=8, height=2).grid(row=6,column=2,pady=5,padx=30)
  T_windslide       = tk.Label(window, textvariable = var_wslid, bg='gray', font=('Arial', 10), width=8, height=2).grid(row=8,column=2,pady=5,padx=30)
  
  # Define Button Object: Function hit_me()
  button_start = tk.Button(window, text='Start', width=40, height=10, command=start_streaming).grid(row=6,rowspan=3,column=3,columnspan=3,pady=5,padx=20)
  button_stop = tk.Button(window, text='Stop', width=40, height=10, command=stop_streaming).grid(row=6,rowspan=3,column=6,columnspan=3,pady=5,padx=20)
  button_insert = tk.Button(window, text='Confirm Setting', width=20, height=4, command=insert_parameters).grid(row=9,column=0,columnspan=3,pady=5,padx=20)
  
  # Main Loop
  window.mainloop()

