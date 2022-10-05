using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using NationalInstruments.DAQmx;
using Task = NationalInstruments.DAQmx.Task;

namespace quikMill
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();



        }

        private void timer1_Tick(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            int rate = 10;
            int _samplesPerChannel = 12;
            int bufferSize = rate * _samplesPerChannel;

            NationalInstruments.DAQmx.Task acelerometerTask1 = new Task();
            NationalInstruments.DAQmx.Task acelerometerTask2 = new Task();
            NationalInstruments.DAQmx.Task acelerometerTask3  = new Task();
            acelerometerTask1.AIChannels.CreateAccelerometerChannel("cDAQ1Mod1/ai0", "A00", AITerminalConfiguration.Pseudodifferential, -5, 5, 100, AIAccelerometerSensitivityUnits.MillivoltsPerG, AIExcitationSource.None, 0, AIAccelerationUnits.G);
            acelerometerTask2.AIChannels.CreateAccelerometerChannel("cDAQ1Mod1/ai1", "A01", AITerminalConfiguration.Pseudodifferential, -5, 5, 100, AIAccelerometerSensitivityUnits.MillivoltsPerG, AIExcitationSource.None, 0, AIAccelerationUnits.G);
            acelerometerTask3.AIChannels.CreateAccelerometerChannel("cDAQ1Mod1/ai2", "A02", AITerminalConfiguration.Pseudodifferential, -5, 5, 100, AIAccelerometerSensitivityUnits.MillivoltsPerG, AIExcitationSource.None, 0, AIAccelerationUnits.G);

            acelerometerTask1.Timing.ConfigureSampleClock("", rate, SampleClockActiveEdge.Rising, SampleQuantityMode.FiniteSamples, _samplesPerChannel);
            acelerometerTask2.Timing.ConfigureSampleClock("", rate, SampleClockActiveEdge.Rising, SampleQuantityMode.FiniteSamples, _samplesPerChannel);
            acelerometerTask3.Timing.ConfigureSampleClock("", rate, SampleClockActiveEdge.Rising, SampleQuantityMode.FiniteSamples, _samplesPerChannel);

            // Verify the task
            acelerometerTask1.Control(TaskAction.Verify);
            acelerometerTask2.Control(TaskAction.Verify);
            acelerometerTask3.Control(TaskAction.Verify);

            DataTable dt = new DataTable();

            //acelerometerTask.Start();
            // Prepare the table for data
            //InitializeDataTable(acelerometerTask.AIChannels, ref dt);
            //acquisitionDataGrid.DataSource = dt;

            // Read the data
            AnalogMultiChannelReader reader1 = new AnalogMultiChannelReader(acelerometerTask1.Stream);
            AnalogMultiChannelReader reader2 = new AnalogMultiChannelReader(acelerometerTask2.Stream);
            AnalogMultiChannelReader reader3 = new AnalogMultiChannelReader(acelerometerTask3.Stream);

            

            foreach (double row  in reader1.ReadMultiSample(_samplesPerChannel))
            {
                Console.WriteLine(row);
            };
            Console.WriteLine("Done1");
            foreach (Double row in reader2.ReadMultiSample(_samplesPerChannel))
            {
                Console.WriteLine(row);
            };
            Console.WriteLine("Done2");
            foreach (Double row in reader3.ReadMultiSample(_samplesPerChannel))
            {
                Console.WriteLine(row);
            };
            // clear task
            acelerometerTask1.Dispose();
            acelerometerTask2.Dispose();
            acelerometerTask3.Dispose();

            //AnalogMultiChannelReader reader = new AnalogMultiChannelReader(acelerometerTask.Stream);


            Console.WriteLine("Done");
                
        }
    }
}
