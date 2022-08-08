import datetime
from msilib import Table
from tokenize import Double
from unicodedata import name
from xmlrpc.client import DateTime
import mysql.connector
import nidaqmx
from nidaqmx import constants
from nidaqmx.constants import AcquisitionType
from nidaqmx import stream_readers
import numpy as np
import pandas as pd
import sqlalchemy


def collect_data(Device_name = "cDAQ1Mod1", sensitivity = 100, min_val = -5, max_val = 5, Ch00_name = 'A00', Ch01_name = 'A01', Ch02_name = 'A02', sample_rate = 12800, time_req = 10, cont_mode = AcquisitionType.FINITE):
    
    # Setting up database connection
    
    #         host="localhost",
    #         user="yourusername",
    #         password="yourpassword",
    #         database="mydatabase"

    
    database_connection = sqlalchemy.create_engine('mysql+pymysql://root:@localhost:3306/accelerometer')

    samples_to_acq = sample_rate * time_req
    
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
        metadata_obj = sqlalchemy.MetaData()
        mytable = sqlalchemy.Table(f'{Device_name}', metadata_obj,
                sqlalchemy.Column('Timestamp', sqlalchemy.DateTime, primary_key=True),
                sqlalchemy.Column('X-Axis (mG)', sqlalchemy.Float),
                sqlalchemy.Column('Y-Axis (mG)',sqlalchemy.Float),
                sqlalchemy.Column('Z-Axis (mG)', sqlalchemy.Float)
           )
        metadata_obj.create_all(database_connection)
        # Saving the data into a CSV file
        df = pd.DataFrame(data, index = pd.date_range(start = start,end = end, periods=samples_to_acq), columns=['X-Axis (mG)', 'Y-Axis (mG)', 'Z-Axis (mG)'])
        df.index.name = 'Timestamp'
        # df.to_csv('./QuickMill_out.csv')
        # Write data in sql database
        df.to_sql(con=database_connection, name=f'{Device_name}', if_exists='append')
