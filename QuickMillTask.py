import datetime
from unicodedata import name
import nidaqmx
from nidaqmx import constants
from nidaqmx.constants import AcquisitionType
from nidaqmx import stream_readers
import numpy as np
import pandas as pd


# Instantiate variables
sample_rate = 12800 # sample rate as specified in the task
time_req = 10 # 10 secs to record samples
samples_to_acq = sample_rate * time_req # total samples to recorded in given time 
cont_mode = AcquisitionType.FINITE
# units_g = nidaqmx.constants.AccelUnits.G

Device_name = "cDAQ1Mod1"
Ch00_name = 'A00'
Ch01_name = 'A01'
Ch02_name = 'A02'

sensitivity = 100

min_val = -5 # Min value of the expected signal
max_val = 5 # Max value of the expected signal

with nidaqmx.Task() as task:
    
    # Create accelerometer channel and configure sample clock and trigger specs
    task.ai_channels.add_ai_accel_chan(physical_channel=f"{Device_name}/ai0", name_to_assign_to_channel=Ch00_name,
                                       sensitivity=sensitivity, min_val=min_val, max_val=max_val)
    task.ai_channels.add_ai_accel_chan(physical_channel=f"{Device_name}/ai1", name_to_assign_to_channel=Ch01_name,
                                       sensitivity=sensitivity, min_val=min_val, max_val=max_val)
    task.ai_channels.add_ai_accel_chan(physical_channel=f"{Device_name}/ai2", name_to_assign_to_channel=Ch02_name,
                                       sensitivity=sensitivity, min_val=min_val, max_val=max_val)

    # setting up sample clock timing 
    task.timing.cfg_samp_clk_timing(sample_rate, sample_mode = cont_mode, samps_per_chan=samples_to_acq)

    # setting up stream reader to read multiple analog streams
    reader = stream_readers.AnalogMultiChannelReader(task.in_stream)

    # setting up np array
    buffer = np.zeros((3, samples_to_acq), dtype=np.float64)
    
    print("Collecting data : .................")
    # Start time used to generate timestamp
    start = datetime.datetime.now()
    
    # Dumping data input numpy array
    reader.read_many_sample(buffer, samples_to_acq, timeout=constants.WAIT_INFINITELY)
    
    # End Time used to generate time stamps
    end = datetime.datetime.now()
    
    # performing a transpose of the array 
    data = buffer.T.astype(np.float64)
    
    # Saving the data into a CSV file
    df = pd.DataFrame(data, index = pd.date_range(start = start,end = end, periods=samples_to_acq), columns=['X-Axis (mG)', 'Y-Axis (mG)', 'Z-Axis (mG)'])
    df.index.name = 'Timestamp'
    df.to_csv('./QuickMill_out.csv')
    # print(df.head())
