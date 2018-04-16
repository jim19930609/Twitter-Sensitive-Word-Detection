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


def Read_Convert_List():
  convert_dic = {}
  with open("topics/topic_levels.txt", "rb") as f:
    for lines in f:
      lines = lines.strip()
      lines = lines.decode('ascii')
      sp = lines.split(" ")
      convert_dic[int(sp[0])] = sp[1]
  return convert_dic


def Clean_Tweet(tweet):
  char_list = [tweet[j] for j in range(len(tweet)) if ord(tweet[j]) in range(65536)]
  tweet=''
  for j in char_list:
      tweet=tweet+j
  return tweet


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
  params.twit_interval = E_twit_interval.get("1.0",tk.END).strip()
  params.stream_interval = E_stream_interval.get("1.0",tk.END).strip()
  params.filtword = E_filtword.get("1.0",tk.END).strip()
  params.windsize = E_windsize.get("1.0",tk.END).strip()
  params.windslide = E_windslide.get("1.0",tk.END).strip()
  
  var_ti.set   ( str(E_twit_interval.get("1.0",tk.END)).strip() )
  var_si.set   ( str(E_stream_interval.get("1.0",tk.END)).strip() )
  var_fw.set   ( str(E_filtword.get("1.0",tk.END)).strip() )
  var_wsize.set( str(E_windsize.get("1.0",tk.END)).strip() )
  var_wslid.set( str(E_windslide.get("1.0",tk.END)).strip() )
  
  window.update()


def stop_streaming():
  params.switch = False


def start_streaming():
  params.switch = True
  Clean_Files(data_dir, result_dir)
  convert_dic = Read_Convert_List()

  command_p = " ".join( ['exec ', 'python3', 'twit_file.py', '--interval='+str(params.twit_interval), '--filtword='+str(params.filtword)] )
  command_s = " ".join( ['exec ', 'python3', 'streaming.py', '--interval='+str(params.stream_interval), '--windsize='+str(params.windsize), '--windslide='+str(params.windslide)] )

  twit_p = subprocess.Popen(command_p, shell=True)
  twit_s = subprocess.Popen(command_s, shell=True)

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
      content_orig = content_orig.decode('utf-8')
      content_orig = Clean_Tweet(content_orig)

      var_orig.set(content_orig)
    
    if len(file_list_result) - 1 > index_result:
      index_result = len(file_list_result) - 1
      content_result = open(result_dir + file_list_result[index_result], "rb").readline().strip()
      content_result = content_result.decode('utf-8')
      content_result = Clean_Tweet(content_result)
      
      sp = content_result.split("|||")
      content = sp[0]
      LDA_level = int(sp[1])
      Keywords = sp[2:]
      
      #var_tp.set("LDA Topic Number: " + str(LDA_level))
      var_kw.set(" ".join(Keywords))
      
      tp_color = convert_dic[LDA_level]

      T_TP.configure(background=tp_color)
      var_result.set(content)
    
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

  # Define Display Label Object
  var_orig = tk.StringVar()
  var_result = tk.StringVar()
  
  label_orig = tk.Label(window, textvariable = var_orig, bg='green', font=('Arial', 15), width=40, height=10, wraplength = 300).grid(row=1,rowspan=4,column=3,columnspan=3,pady=5,padx=20)
  label_result = tk.Label(window, textvariable = var_result, bg='blue', font=('Arial', 15), width=40, height=10, wraplength = 300).grid(row=1,rowspan=4,column=6,columnspan=3,pady=5,padx=20)
  

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
  
  
  var_tp = tk.StringVar()
  var_kw = tk.StringVar()
  var_tp.set("LDA Topic Level")
  var_kw.set("Keywords")
  
  T_TP   = tk.Label(window, textvariable = var_tp, bg='gray', font=('Arial', 10), width=20, height=2)
  T_KW   = tk.Label(window, textvariable = var_kw, bg='gray', font=('Arial', 10), width=30, height=2)
  T_TP.grid(row=0,column=6,pady=5,padx=20,sticky='w')
  T_KW.grid(row=0,column=7,pady=5,padx=20,sticky='w')
  
  # Define Button Object: Function hit_me()
  button_start = tk.Button(window, text='Start', width=40, height=10, command=start_streaming).grid(row=6,rowspan=3,column=3,columnspan=3,pady=5,padx=20)
  button_stop = tk.Button(window, text='Stop', width=40, height=10, command=stop_streaming).grid(row=6,rowspan=3,column=6,columnspan=3,pady=5,padx=20)
  button_insert = tk.Button(window, text='Confirm Setting', width=20, height=4, command=insert_parameters).grid(row=9,column=0,columnspan=3,pady=5,padx=20)
  
  # Main Loop
  window.mainloop()

