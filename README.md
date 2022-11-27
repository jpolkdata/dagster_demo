# Dagster Demo
Dagster is an orchestrator that's designed for developing and maintaining data assets, such as tables, data sets, machine learning models, and reports.

This is a demo of Dagster basic functionality to understand how it uses assets. We define an asset that is a csv of different brands of breakfast cereals along with a rating of its protein content. We build out assets and graphs off of this dataset, resulting in a more complex lineage graph where we can determine just the Nabisco cereals as well as which of those has the highest protein content.

![image](https://user-images.githubusercontent.com/40530465/204061632-9fd63ad6-8794-4c8a-8c99-f369eeee1a96.png)

![image](https://user-images.githubusercontent.com/40530465/204061140-da23973b-d677-4c22-a776-bda2048f89b6.png)

The tutorial can be found at https://docs.dagster.io/tutorial

## Setup
```
git clone https://github.com/jpolkdata/dagster_demo
cd dagster_demo/my-dagster-project/
python3 -m venv venv
. venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Materializing the Assets
Build out just the list of cereals as an asset from the csv
```
dagit -f cereal.py
```
![image](https://user-images.githubusercontent.com/40530465/204061250-6f71ddd3-03eb-41ce-a6dd-b366ac40b641.png)

Get each cereal's protein content as a fraction, determine just the Nabisco cereals, and then join that data back together to determine the highest protein Nabisco cereal
```
dagit -f serial_asset_graph.py
```
![image](https://user-images.githubusercontent.com/40530465/204061507-bbaa4545-20d4-4b15-9a8b-86bf08c8fcac.png)

In an even more complex example, we instead pull in a zip file containing a separate csv file that contains cereal ratings. We then use that data in calculating the highest protein Nabisco cereal
```
dagit -f complex_asset_graph.py
```
![image](https://user-images.githubusercontent.com/40530465/204061961-a42918c1-d1c2-4b0e-9187-48995d2c2aef.png)

A couple of unit tests have been added to that last graph, you can run them using this command
```
pytest test_complex_asset_graph.py
```

## Adding ops and jobs
ops are individual units of computation that can be wired together to form jobs

In hello.py we have craeted a single job. All this does is calculate the sizes of all the files in our current directory and logs them. You can run this using 
```
dagit -f hello.py
```
![image](https://user-images.githubusercontent.com/40530465/204115076-380eb2b7-a751-468a-8aa1-448ab8bc8818.png)

So then we created a slightly more involved example. This time we wired together a couple of ops, one to get the file sizes but also a different op to report on the combined total size of all of those files. This is run as a serial job because the "total" file sizes op relies on the op that calculates the individual file sizes. To view the job in Dagster run
```
dagit -f serial_job.py
```
![image](https://user-images.githubusercontent.com/40530465/204115066-68d0bdbe-1f6b-4117-998f-88956b4bf6a9.png)


Then we created a complex example. This builds on the previous file size ops. Now we run a job that a) gets the total size of all of the files AND b) gets the size of the largest individual file. We can visualize this in Dagster using:
```
dagit -f complex_job.py
```
![image](https://user-images.githubusercontent.com/40530465/204115096-6ff49933-b51b-451e-971d-d9c7ffa8ec22.png)

Finally, we build out a couple of unit tests for that complex job. We want to test that the op that calculates the total file sizes is doing an accurate calculation. We also want to be sure that the job runs successfully and brings back a resulting file size that is greater than zero. We can run those test using:
```
pytest test_complex_job.py
```
