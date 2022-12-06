import pprint
import time
import os
import json
import datetime


################################################
#### This function prepends timestamps as
#### dates to the text property in slack json
################################################
def prepend_timestamps(filedata):
  jdata = json.loads(filedata)
  for arr in jdata:
    if ('ts' in arr.keys()) and ('text' in arr.keys()):
      d = datetime.datetime.fromtimestamp(float(arr["ts"]))
      timestamp = d.strftime("%c")
      arr["text"] = "[" + timestamp + "] " + arr["text"]
  return json.dumps(jdata)

################################################
#### This function prepends timestamps as
#### dates to the text property in slack json
################################################
def shift_timestamps():
  today = time.time()
  twomonthsago = today - 5298900
  threemonthsago = today - 7890900
  timeincrement = 0.00001
  ts = []

# extract all timestamps from archive
  os.system('grep -hr '"ts"' slack_archive > tsfile')

  with open("tsfile","r") as f:
    lines = f.readlines()

  ### parse timestamps, convert to float and sort

  for line in lines:
    line = line.strip()
    item = line.replace(",","").split(":")[1].strip().replace('"','')
    valu = float(item)
    ts.append(valu)

  ts = sorted(ts)
  tskeys = ['{:.6f}'.format(x) for x in ts]

  ### find index of timestamp cutoff from 2 months ago

  ts_cutoff = next((index for index, item in enumerate(ts) if item > twomonthsago),None)

  ### build dict of timestamp maps for all items from before 2 months ago

  tskeys = tskeys[:ts_cutoff]

  ts_dict = {}
  timecounter = twomonthsago
  for item in tskeys:
    ts_dict[item]= '{:.6f}'.format(timecounter)
    timecounter += timeincrement

  ### some simple reporting

  print(len(tskeys))
  print("beginning = ",tskeys[0])
  print("ending = ",tskeys[-1])
#  pprint.pprint( ts_dict )

  ### Now, iterate over all files, prepend timestamps and replace timestamps with dict

  oldroot = "slack_archive"
  newroot = "slack_archive_newer"
  if not os.path.exists(newroot):
    os.makedirs(newroot)

  for (dirpath,dirs,files) in os.walk(oldroot, topdown=True):
    for dir in dirs:
      curdir = os.path.join(newroot,dir)
      if not os.path.exists(curdir):
        os.makedirs(curdir)

    for filename in files:
      infile = os.path.join(dirpath,filename)
      outpath = dirpath.split("/")
      if len(outpath) > 1:
        outfile = os.path.join(newroot,dirpath.split("/")[1],filename)
      else:
        outfile = os.path.join(newroot,filename)
      print(outfile)
      with open(infile,"r") as f:
        filedata = f.read()

      filedata = prepend_timestamps(filedata)

      for key, val in ts_dict.items():
        filedata = filedata.replace(key,val)

      with open(outfile,"w+") as of:
        of.write(filedata)

  return ts_dict

################################################
#### Main loop
################################################

def main():
  ts_dict = shift_timestamps()


main()

#if __name__ == '__main__':
#    main()

