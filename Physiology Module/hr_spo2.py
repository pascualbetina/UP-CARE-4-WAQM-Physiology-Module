# Write your code here :-)
from ulab import numpy as np
import math


def peak_detector(data_stream, threshold, min_distance):

  peak_val = []
  peak_loc = []
  peaks_to_remove = []

  #print("peak detection")

  for i in range(1, len(data_stream)):
    if data_stream[i-1] > threshold and data_stream[i-1] > data_stream[i]:
      peak_val.append(data_stream[i-1])
      peak_loc.append(i-1)
  #print(peak_loc)
  for j in range(1, len(peak_loc)):
    if peak_loc[j] - peak_loc[j-1] <= min_distance:
      peaks_to_remove.append(j)
      #peaks_to_remove.append(j-1)
  #print(peaks_to_remove)
  #fin_peak_val = np.delete(np.array(peak_val), peaks_to_remove)
  #fin_peak_loc = np.delete(np.array(peak_loc), peaks_to_remove)
  peaks_to_remove.sort(reverse=True)
  for index in peaks_to_remove:
      del peak_loc[index]
      del peak_val[index]

  #peak_val.clear()
  #peak_loc.clear()
  peaks_to_remove.clear()
  #print(peak_loc, peak_val)

  return  peak_loc, peak_val


def movave_filter (data_stream, movave_size):
    #print("filter")
    data_filtered = data_stream[0:len(data_stream)-movave_size]
    try:
        for j in range (len(data_stream) - movave_size):
            data_val = data_stream[j] + data_stream[j+1] + data_stream[j+2] + data_stream[j+3]
            data_filtered[j] = data_val/4
    except:
        print("error filter")

    return data_filtered

def norm (data_stream, to_norm, data_mean):
  #print("peak detection")

  if to_norm:
    #data_mean = np.mean(data_stream)
    data_norm = np.array(data_stream) - data_mean
  else:
    data_norm = data_stream
  return data_norm


def compute_hr(movave_size, data_stream, min_distance, data_mean):
    #print("computing hr")

    data_norm = norm(data_stream, True, data_mean)
    data_filtered = movave_filter(data_norm, movave_size)

    data_thres = np.mean(data_filtered)

    data_peak_val, data_peak_loc = peak_detector(data_filtered, data_thres, min_distance)
    #inv_data_peak_val, inv_data_peak_loc, inv_data_orig_peak_val = peak_detector((data_filtered*-1), data_thres, min_distance)
    try:
        data_peak_interval = []
        bpm_list = []

        if len(data_peak_loc) > 1:
            for m in range(1, len(data_peak_loc)):
                peak_interval = data_peak_loc[m] - data_peak_loc[m-1]
                #print(data_peak_loc[m], data_peak_loc[m-1])
                data_peak_interval.append(peak_interval)
                bpm_curr = 25*60/peak_interval
                if bpm_curr > 0 and bpm_curr < 300:
                    bpm_list.append(bpm_curr)

    #print("HR: " + str(bpm_list))
    except:
        print("error hr")

    data_peak_interval.clear()

    return data_peak_loc, data_peak_val, bpm_list

def genRatio (data_stream, peak_locs):
  data_sect = []
  partial_ratio = []

  try:
    #print("try")
    if len(peak_locs) > 0:
        for i in range (1, len(peak_locs)):
            a = int(peak_locs[i-1])
            b = int(peak_locs[i])

            data_sect = data_stream[a:b+1]
            #print("data")
            #print(data_sect)
            #sleep(2)
            top = np.max(data_sect)
            bot = np.min(data_sect)
            ac = (top-bot)/(math.sqrt(2))
            dc = (np.mean(data_sect))/(math.sqrt(2))
            partial_ratio.append(ac/dc)
            #print(top, bot)
    else:
        top = np.max(data_stream)
        bot = np.min(data_stream)
        ac = (top-bot)/(math.sqrt(2))
        dc = (np.mean(data_stream))/(math.sqrt(2))
        partial_ratio.append(ac/dc)
        #print(top, bot)
  except:
      #print("except")
      #'''
      top = np.max(data_stream)
      bot = np.min(data_stream)
      ac = (top-bot)/(math.sqrt(2))
      dc = (np.mean(data_stream))/(math.sqrt(2))
      partial_ratio.append(ac/dc)
      '''
      dc = (np.mean(data_stream))/(math.sqrt(2))
      bot = np.min(data_stream)
      data_stream = np.array(data_stream) - bot
      ac = (np.mean(data_stream))/(math.sqrt(2))
      partial_ratio.append(ac/dc)
      '''
  #data_sect.clear()
  #print(partial_ratio)

  return partial_ratio

def compute_spo2 (data_stream1, data_stream2, movave_size, data_peak_loc1, data_peak_loc2, data_mean1, data_mean2):

  #ir - 1, red - 2
  data_norm1 = norm(data_stream1, False, data_mean1)
  data_filtered1 = movave_filter(data_norm1, movave_size)
  data_partial_ratio_list1 = genRatio (data_filtered1, data_peak_loc1)
  #print("ir spo2")

  data_norm2 = norm(data_stream2, False, data_mean2)
  data_filtered2 = movave_filter(data_norm2, movave_size)
  data_partial_ratio_list2 = genRatio (data_filtered2, data_peak_loc2)
  #print("red spo2")

  ratio_list = []
  spo2_list = []
  spo2_lis2 = []
  z = 0
  #print(data_partial_ratio_list1)

  if len(data_partial_ratio_list1) <= len(data_partial_ratio_list2):
    z = len(data_partial_ratio_list1)
  else:
    z = len(data_partial_ratio_list2)
  #print(z)
  try:
    if z > 0:
      for k in range(z):
      #red/ir
        #print(data_partial_ratio_list1[k])
        ratio = data_partial_ratio_list2[k]/data_partial_ratio_list1[k]
        ratio_list.append(ratio)
        #spo2 = 104 - (17*ratio)
        spo2_2 = -45.060 * (ratio**2) / 10000 + 30.054 * ratio / 100 + 94.845
        spo2_lis2.append(spo2_2)
        #spo2 = 1.5958422 * (ratio**2) - 34.65966277 * ratio + 112.6898759
        spo2 = 1.596 * (ratio**2) - 34.659 * ratio + 112.690
        #print(spo2)
        if spo2 > 80 and spo2 < 105:
            spo2_list.append(spo2)
            #print("valid spo2")
        else:
            print("invalid spo2")
  except:
    print("error spo2")


  #print("SpO2: " + str(spo2_list))
  ratio_list.clear()

  return spo2_list, spo2_lis2

def run_sensor(ir, red, green, gmean, rmean, imean):
  movave_size = 4
  min_distance = 5

  data_peak_loc1, data_peak_val, par_ir_bpm = compute_hr(movave_size, ir, min_distance, imean)
  data_peak_loc2, data_peak_val, red_bpm = compute_hr(movave_size, red, min_distance, rmean)
  data_peak_loc3, data_peak_val, par_green_bpm = compute_hr(movave_size, green, min_distance, gmean)
  #print("HR: " + str(par_green_bpm))
  #print(data_peak_loc3)
  print("computing spo2")
  spo2_list, spo2_lis2 = compute_spo2(ir, red, movave_size, data_peak_loc1, data_peak_loc2, imean, rmean)


  return par_green_bpm, spo2_list

